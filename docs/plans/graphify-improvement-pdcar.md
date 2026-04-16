# Graphify Improvement PDCA/R Plan (Final)

Date: 2026-04-09
Owner: Governance
Scope: Improve graphify knowledge-graph quality, reduce noise, and drive operator adoption
Reviewed by: Codex gpt-5.4 specialist (2 review rounds)
Issue: TBD (to be created after plan approval)

---

## Context

### What graphify does today

graphify v0.3.17 is a Python package that builds code knowledge graphs from repository source. The governance repo wraps it via `scripts/knowledge_base/build_graph.py` (277 lines). The pipeline:

1. `detect(source)` -- walks the repo tree, classifies files (code/doc/image), respects `.graphifyignore`
2. `collect_files()` + `extract(paths)` -- AST extraction per file (supports .ts, .tsx, .py, .go, .rs, .java, etc.), produces nodes + edges
3. `build_from_json(result)` -- constructs a NetworkX graph from extraction output
4. `cluster(G)` -- Leiden community detection, auto-splits communities >25% of graph size
5. `score_all(G, communities)` -- computes cohesion per community
6. Post-processing in `build_graph.py`: label inference, report generation, wiki article generation

### What the A/B test revealed

Ran graphify on AIS (1883 nodes, 2533 edges, 111 communities) and HealthcarePlatform (1549 nodes, 2396 edges, 176 communities):

| Problem | Evidence | Root Cause |
|---------|----------|------------|
| Junk-drawer mega-community | Community 0: 166 nodes, 0.01 cohesion | Cluster split threshold too generous (25% = 470 nodes for AIS) + noise files inflating node count |
| Trivial singleton communities | 27 communities with 0-2 nodes, 1.0 cohesion | Config files, type decls, standalone scripts each become isolated communities |
| False connections | 20% of edges INFERRED at avg confidence 0.5 | Shared env var references and name collisions treated as calls |
| Generic labels | Many communities still "Community N" | Labeling heuristics can't extract meaning from generic path tokens |
| Duplicate god nodes | HealthcarePlatform shows duplicate `main()`, `fail()` | Node IDs are bare function names without file context |
| Zero adoption | No operator has changed behavior based on output | Output lives in `graphify-out/` files nobody opens; no integration into daily workflow |

### graphify v0.3.17 API reality (verified from source)

| Capability | Status | Implication for plan |
|------------|--------|---------------------|
| `.graphifyignore` file support | **Native** -- `detect()` loads it automatically | No `--exclude` flag needed; just create the file |
| Cluster split for oversized communities | **Native** -- splits at >25% of nodes, min 10 | Threshold is too generous; need to reduce `_MAX_COMMUNITY_FRACTION` or post-filter |
| `cluster()` resolution parameter | **Not supported** -- signature is `(G)` only | Cannot tune clustering tightness without upstream change |
| Edge confidence in `graph.json` | **Native** -- `to_json()` adds `confidence_score` per edge | Data exists for filtering; filtering must happen before `cluster()` |
| Custom edge metadata in `to_json()` | **Not supported** -- fixed schema | Cannot add `clustering_excluded: true`; must use separate file |
| `extract()` file filtering | **Not supported** -- takes `list[Path]` directly | Filter between `collect_files()` and `extract()` in wrapper |
| Node ID format | **Bare function/class name** from extraction | Normalization must happen on extraction dict before `build_from_json()` |

---

## Plan

### Sprint 1: Trust the Graph
**Goal:** Remove noise from input and false connections from edges so the graph reflects real architecture.
**Duration:** 1 week
**Justification:** Operators won't use a tool they don't trust. Every downstream improvement (labeling, insights, PR comments) depends on the graph being accurate first. This sprint addresses the two largest quality problems: noise files inflating communities and low-confidence edges blurring boundaries.

#### 1.1 Create `.graphifyignore` files for governed repos

**Use case:** A developer looks at the graph report and sees `tailwind.config.js` as its own community and `postcss.config.js` as another. They dismiss the entire report as noise. By excluding files that never participate in meaningful call graphs, we eliminate trivial communities at the source.

**Implementation:** graphify v0.3.17 natively supports `.graphifyignore` with gitignore semantics via `detect()`. No code changes to `build_graph.py` needed -- just create the files.

**Acceptance Criteria:**
- [ ] `.graphifyignore` created in AIS repo root with patterns: `*.config.js`, `*.config.ts`, `**/vite-env.d.ts`, `**/postcss.config.*`, `**/tailwind.config.*`, `**/seed-*.ts`, `**/seed-*.js`, `**/seed-*.mjs`
- [ ] `.graphifyignore` created in HealthcarePlatform repo root with equivalent patterns plus `**/smoke-test.js` (duplicate `main()` source)
- [ ] `.graphifyignore` created in knocktracker repo root with equivalent patterns
- [ ] Baseline graph metrics captured before: node count, edge count, community count, singleton count, Community 0 size
- [ ] Re-run on AIS with `.graphifyignore`: baseline vs new metrics compared and delta documented in `graphify-out/ai-integration-services/.graphify_delta.json`
- [ ] Singleton community count (communities with <=2 nodes) decreases measurably from baseline
- [ ] No false negatives: spot-check that no excluded file was a real call-graph participant (review 5 random excluded files)

#### 1.2 Filter inferred edges below confidence 0.7 before clustering

**Use case:** The graph currently shows `sendReminderSMS() --calls--> TWILIO_ACCOUNT_SID()` as a real connection because both files reference the same env var name. This pollutes Community 0 by pulling unrelated functions into the same cluster. By filtering low-confidence edges before Leiden runs, communities form around real structural relationships.

**Implementation:** In `build_graph.py`, after `build_from_json(result)` returns the NetworkX graph and before `cluster(G)` is called, remove edges where `confidence_score < threshold`. Filtering also happens on the extracted edge payload for deterministic `excluded_edges.json` output. Filtered edges are saved separately.

**Acceptance Criteria:**
- [ ] `build_graph.py` accepts `--min-confidence` float flag (default: 0.7)
- [ ] Filtering happens in two places: (a) on the extracted edge payload for deterministic excluded-edge serialization, and (b) on the in-memory NetworkX graph `G` before `cluster()` is called
- [ ] Removed edges are written to `{output}/excluded_edges.json` with keys: `source`, `target`, `confidence_score`, `relation`, `source_file` -- sorted by source then target for stable diffing
- [ ] `excluded_edges.json` includes `schema_version: 1` field
- [ ] `GRAPH_REPORT.md` summary line updated to show: `Clustering: N edges used, M low-confidence excluded`
- [ ] `.graphify_summary.json` includes new field: `edges_excluded` (integer count)
- [ ] Existing `.graphify_summary.json` consumers are not broken (additive field only)
- [ ] Re-run on AIS: Community 0 node count and total INFERRED edge count decrease from baseline (delta documented)

#### 1.3 Normalize node IDs to include file context

**Use case:** HealthcarePlatform's god nodes show `main()` twice and `fail()` twice. An operator can't tell which `main()` is the important one. By prefixing node IDs with the file stem, every node is uniquely identifiable and god node rankings become meaningful.

**Implementation:** After `extract()` returns the extraction dict and before `build_from_json()` consumes it, transform node IDs and edge source/target references to include file context.

**Acceptance Criteria:**
- [ ] In `build_graph.py`, after `extract()` and before `build_from_json()`: node IDs are transformed from `main()` to `smoke-test/main()` using extraction/output file metadata when available, falling back to graph node `source_file` after `build_from_json()` if needed
- [ ] Edge `source` and `target` fields are updated to match the new node IDs
- [ ] Original bare ID is preserved in a separate `original_id` field on each node so report consumers and future migrations can correlate renamed nodes
- [ ] Transformation only applies to nodes whose bare name appears more than once across different files (non-ambiguous names like `TwentyCRMConnector` are left as-is)
- [ ] God nodes list in `GRAPH_REPORT.md` shows disambiguated names (no duplicate entries)
- [ ] Re-run on HealthcarePlatform: no duplicate god node names in top 10

#### 1.4 Add graph quality regression tests

**Use case:** After Sprint 1 changes improve graph quality, we need to prevent regressions. A future `.graphifyignore` change or graphify version upgrade could silently degrade the graph.

**Implementation:** Python test file using committed graph.json fixtures with quality assertions.

**Acceptance Criteria:**
- [ ] `tests/test_graph_quality.py` exists with assertions:
  - Singleton rate (communities with <=2 nodes / total) < 25%
  - Mega-community rate (communities with >50 nodes / total) < 5%
  - Mean cohesion of non-singleton communities > 0.05
  - No duplicate node IDs in graph
- [ ] Tests run against fixture `graph.json` files in `tests/fixtures/` (AIS and HealthcarePlatform post-Sprint-1 snapshots)
- [ ] Fixture schema assertions: exported `graph.json` must include `source_file`, `community`, and `confidence_score` fields (later sprints depend on all three)
- [ ] CI job in governance repo triggers on changes to `scripts/knowledge_base/**` or `tests/**`
- [ ] Fixture refresh process documented in `scripts/knowledge_base/README.md` (created if it doesn't exist)
- [ ] All tests pass on Sprint 1 output

---

### Sprint 2: Readable Output
**Goal:** Make graph output understandable without manual interpretation so operators can scan it in 2 minutes.
**Duration:** 1 week
**Justification:** Even with accurate data, generic labels like "Community 0" and 480-line reports are not actionable. Operators need meaningful names and a short summary to decide whether to dig deeper.

#### 2.1 Fix community labeling with 3-layer precedence

**Use case:** An operator opens `GRAPH_REPORT.md` and sees "Community 0 - Edge Function Handlers" (current label for 166 nodes). After Sprint 1 filtering, the community is smaller but the label may still be generic. With proper precedence -- checked-in overrides first, then directory namespace, then dominant symbol -- labels like "Compliance Gates" or "Plaid Integration" emerge naturally.

**Implementation:** Modify `_community_label()` in `build_graph.py` to check override file first, then apply existing path/token heuristics.

**Acceptance Criteria:**
- [ ] Label selection precedence: `override file` -> `dominant path namespace` -> `dominant symbol/type name`
- [ ] Override file: `--label-overrides <path>` flag, defaults to `{output}/community-overrides.json` if present
- [ ] Override file format: `{"<community_id>": "Custom Label"}` -- only overrides specified entries
- [ ] `community-labels.json` includes `type` field per community: `singleton` (<=2 nodes), `standard`, `mega` (>50 nodes)
- [ ] `community-labels.json` includes `schema_version: 1` field
- [ ] Labels are deterministic: identical input + identical overrides = identical labels across runs; tie-break rule defined (equal-frequency candidates sorted lexicographically before selection)
- [ ] No community in `GRAPH_REPORT.md` is labeled "Community N" -- all have meaningful names or explicit `type: singleton` classification
- [ ] Re-run on AIS: manual spot-check confirms non-singleton labels are meaningful (review 10 communities, document findings)

#### 2.2 Generate Top-N insights summary

**Use case:** The full `GRAPH_REPORT.md` for AIS is 550+ lines. No operator reads that. `GRAPH_INSIGHTS.md` is a <=50 line file with the top 10 most interesting findings, ranked by what an operator would actually act on: new hotspots, boundary-crossing edges, rising god nodes.

**Implementation:** New function in `build_graph.py` that filters communities and generates a ranked summary. If a prior graph exists, includes diff-based insights.

**Acceptance Criteria:**
- [ ] `build_graph.py` generates `GRAPH_INSIGHTS.md` in output directory on every run
- [ ] Insights filtered to communities with cohesion 0.05-0.8 and >3 nodes
- [ ] Singleton/pair communities excluded
- [ ] Prior-run handling is atomic: new graph is written to a temp path first, then existing `graph.json` is rotated to `graph.json.prior`, then temp is moved into place (no data loss on failed runs)
- [ ] If `.prior` exists: diff-based insights are included (new/changed/removed communities, node count deltas, new god nodes)
- [ ] If no prior graph exists: only current-run insights shown (no error, no empty diff section)
- [ ] Insights ranked by: (1) changed communities from prior run, (2) boundary-crossing edges, (3) rising god nodes, (4) new low-cohesion hotspots
- [ ] Output is <=50 lines
- [ ] Each insight is one sentence with community name, metric, and why it matters

#### 2.3 Classify and hide noise communities in the report

**Use case:** Instead of merging trivial communities (which can bury legitimate singletons like adapter classes), classify them and collapse them in the report. An operator sees "27 singleton communities (collapsed)" instead of 27 separate sections.

**Implementation:** Post-processing in report generation: group singleton/pair communities into a collapsed summary section.

**Acceptance Criteria:**
- [ ] `GRAPH_REPORT.md` groups communities with <=2 nodes into a "Singletons & Pairs" summary section at the bottom
- [ ] Summary shows: count, list of names (one-liner each), and a note that these are isolated components
- [ ] Standard and mega communities are listed in full detail as before
- [ ] `community-labels.json` retains all communities (including singletons) -- only the report collapses them
- [ ] Re-run on AIS: main report body is at least 40% shorter than current output

---

### Sprint 3: Operator Adoption — Integration
**Goal:** Put graph output where operators already work so they encounter it without seeking it out.
**Duration:** 1 week
**Justification:** The best graph in the world is useless if nobody reads it. Integration into the weekly sweep report and scoped graphs for focused analysis are the minimum viable adoption path.

#### 3.1 Subsystem-scoped graphs

**Use case:** An operator working on AIS Supabase functions doesn't care about the marketing portal graph. A scoped graph of just `backend/supabase/functions/` produces tighter, more relevant communities. The whole-repo graph remains for boundary analysis.

**Implementation:** Add `--scope` flag to `build_graph.py` that filters `collect_files()` output to paths within the scope.

**Acceptance Criteria:**
- [ ] `build_graph.py` accepts `--scope <subdirectory>` (repeatable for multiple scopes)
- [ ] Scoped graph only includes files under the specified paths
- [ ] Whole-repo graph remains the default when no `--scope` is provided
- [ ] Scoped output goes to `graphify-out/{repo}/{scope-slug}/` where scope-slug is derived from path: lowercase, slashes to hyphens, no trailing hyphen (e.g., `backend-supabase-functions`)
- [ ] Scope slug normalization is documented and consistent
- [ ] Output layout migration: existing flat `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` moved into `graphify-out/ai-integration-services/` (one-time cleanup, documented in commit message)
- [ ] `overlord-sweep.yml` updated to generate whole-repo + 2 scoped graphs per repo:
  - AIS: `backend/supabase/functions`, `apps/portal/src`
  - HealthcarePlatform: `backend/supabase/functions`, `frontend/src`

#### 3.2 Graph health section in sweep report

**Use case:** The weekly sweep report is the one artifact every operator sees. Adding a "Graph Health" section surfaces graph quality without requiring operators to open graph files.

**Implementation:** `overlord-sweep.yml` reads graph artifacts and appends a summary section to `OVERLORD_REPORT.md`.

**Acceptance Criteria:**
- [ ] Sweep report body artifact (currently written to `/tmp/sweep-report.md` by `overlord-sweep.yml`) includes `## Graph Health` section with per-repo metrics: community count, singleton rate, mega-community count, mean cohesion
- [ ] Section includes top 3 insights from each repo's `GRAPH_INSIGHTS.md` (if it exists)
- [ ] If graph artifacts don't exist for a repo: row shows "Not graphified" (no error)
- [ ] Section renders correctly in the existing report format (markdown table)

#### 3.3 Baseline graph quality score

**Use case:** Without a number to track, we can't tell if improvements are working. The quality score gives a single comparable metric per repo per week.

**Implementation:** Compute score from graph metrics and persist alongside effectiveness-baseline.

**Acceptance Criteria:**
- [ ] `graph_quality_score` computed per repo: `1 - (singleton_rate * 0.4 + mega_rate * 0.3 + low_cohesion_rate * 0.3)` where `low_cohesion_rate` = fraction of non-singleton communities with cohesion < 0.05
- [ ] Score persisted in `.graphify_summary.json` as `quality_score` field
- [ ] Sweep report `## Graph Health` table includes quality score column
- [ ] Baseline score captured for AIS, HealthcarePlatform, knocktracker, local-ai-machine before Sprint 1 changes; post-Sprint-1 score compared

---

### Sprint 4: PR Integration + Adoption Metrics
**Goal:** Bring graph awareness into the PR review workflow and measure whether operators use it.
**Duration:** 1 week
**Justification:** The PR workflow is where architectural decisions are made. If graph data appears there, operators encounter it at decision time. Adoption metrics tell us whether to invest further.

#### 4.1 PR comment with affected communities

**Use case:** A developer opens a PR that touches `backend/supabase/functions/compliance-gates/`. The governance workflow looks up the changed files in `graph.json`, finds they belong to the "Compliance Gates Sync" community (cohesion 0.42, 9 nodes), and posts a one-line comment: "This PR touches the Compliance Gates Sync community (9 nodes, cohesion 0.42)." The reviewer now has architectural context without opening the graph.

**Implementation:** Add a step to `governance-check.yml` that loads `graph.json` for the repo, maps changed files to communities, and posts a comment via `gh api`.

**Acceptance Criteria:**
- [ ] `governance-check.yml` includes a step that loads `graphify-out/{repo}/graph.json` (if it exists)
- [ ] Changed files from the PR diff are matched against node `source_file` attributes
- [ ] Matching communities above cohesion threshold (default: 0.1) are identified and de-duplicated by community ID (one PR touching many files in the same community produces one community mention, not many)
- [ ] At most one graph comment per PR (idempotent: updates existing comment on re-run via `gh api` with comment ID tracking)
- [ ] Comment format: "**Graph Context:** This PR touches {N} communities: {name} ({nodes} nodes, cohesion {score}), ..."
- [ ] Comment skips silently when: no `graph.json` exists, no community overlap found, or all matching communities below threshold
- [ ] No comment spam: repeated workflow runs update the same comment

#### 4.2 Adoption success metrics

**Use case:** After 4 sprints of investment, we need to know: did operators actually use this? The metrics tell us whether Sprint 5 is worth pursuing.

**Implementation:** Track graph quality and PR comment engagement in `metrics/graph-adoption/`.

**Acceptance Criteria:**
- [ ] `metrics/graph-adoption/` directory exists with dated + latest JSON snapshots
- [ ] Each snapshot includes per-repo: `graph_quality_score`, `community_count`, `singleton_rate`, `mega_rate`
- [ ] Each snapshot includes cross-repo: `pr_comment_hit_rate` (PRs where graph comment was posted / total PRs in sweep window)
- [ ] Weekly sweep persists graph adoption metrics alongside effectiveness-baseline
- [ ] Sweep report includes `## Graph Adoption` section with score trends (current vs prior week)
- [ ] If `pr_comment_hit_rate == 0` and `graph_quality_score < 0.5` after 2 weeks: sweep report flags "Graph adoption stalled — review investment"

---

### Sprint 5: Advanced (Gated)
**Goal:** Only pursue if Sprint 4 metrics show adoption.
**Gate:** `pr_comment_hit_rate > 0` AND `graph_quality_score > 0.6` for at least 2 repos sustained for 2 consecutive weeks.
**Justification:** These items add complexity and cost. Without proven demand, they are premature optimization.

#### 5.1 Semantic extraction on targeted subgraphs
- Use `--semantic` only on subgraphs where AST-only clustering cohesion < 0.03
- Budget: max 50k Claude tokens per repo per run
- Justification: semantic edges may reveal real relationships that AST can't detect, but only in areas where AST is clearly failing

#### 5.2 Recursive sub-clustering (upstream-dependent)
- Requires `graphify.cluster()` to accept a resolution parameter or sub-clustering hook
- If upstream supports it: implement with cohesion-improvement stop condition
- If not: file upstream feature request and track in OVERLORD_BACKLOG.md
- Justification: even after edge filtering, some communities may remain too large; recursive splitting is the clean solution

#### 5.3 Local CLI query interface
- `python3 scripts/knowledge_base/query_graph.py "what calls emitAuditLog?"`
- Fixed commands: `calls <function>`, `callers <function>`, `community <name>`, `changed-since <date>`
- Queries over local `graph.json` using NetworkX traversal
- Justification: operators who find graph data useful in PR comments will want to query it ad-hoc

#### 5.4 Edge provenance weighting
- Weight edges by type during clustering: AST import/call (1.0), doc reference (0.7), semantic similarity (0.5)
- Configurable via `edge-weights.json` in output directory
- Justification: not all edges are equal; weighting improves community quality beyond hard cutoffs

#### 5.5 Neo4j graph push
- `python3 scripts/knowledge_base/push_graph_to_neo4j.py` (script already exists as stub)
- Gate: Phase 7 of Living Knowledge Base (issue #48) + CLI query proving demand
- Justification: graph DB is only worth running if people are querying the graph

---

## Check

After each sprint, verify:
- [ ] Quality regression tests pass (`tests/test_graph_quality.py`)
- [ ] `graph_quality_score` improves or holds vs baseline
- [ ] No new `FAIL_FAST_LOG` entries from graph tooling
- [ ] Output schema changes are backwards-compatible (additive only)
- [ ] `.graphify_summary.json` consumers still work (sweep, wiki, closeout hook)
- [ ] Operator feedback collected (minimum: ask one question about graph output in sweep issue)

## Adjust

| Trigger | Response |
|---------|----------|
| Singleton rate doesn't drop after Sprint 1 | Expand `.graphifyignore` patterns; review whether `graphify.detect._is_noise_dir()` is missing common dirs |
| Labels remain generic after Sprint 2 | Add LLM-assisted labeling: one Claude API call per mega-community with top-10 node names as context |
| Community 0 stays >100 nodes after edge filtering | Lower `_MAX_COMMUNITY_FRACTION` locally by patching `graphify.cluster` constants before calling `cluster()` |
| PR comment noise is high after Sprint 4 | Raise cohesion threshold from 0.1 to 0.3; add community-size minimum |
| Adoption metrics stay at zero after Sprint 4 | Pause Sprint 5; conduct 3 operator interviews to understand why output isn't useful |
| `graphify` upstream release breaks API | Pin to v0.3.17 in requirements; file upstream compat issue |
| Fixture graphs drift from live repos | Add quarterly fixture refresh to sweep automation |

## Review

- graphify remains a governance-internal tool, not customer-facing
- `rg`/local code reads remain the implementation truth; graphify is the topology map
- All graph artifacts stay in `hldpro-governance`; product repos keep only `.graphifyignore` + pointer/hook pattern
- Sprint 5 is explicitly gated on Sprint 4 adoption signal — no premature optimization
- No upstream `graphify` package modifications in Sprints 1-4; all changes are wrapper/post-processing
- The plan leverages native graphify capabilities (`.graphifyignore`, `confidence_score`, auto-split) rather than reimplementing them

---

## Codex Specialist Review Log

### Round 1 (gpt-5.4, 2026-04-09)
- Verdict: **NEEDS REVISION**
- Key feedback: split Sprint 3 into two sprints; defer recursive sub-clustering; fix label precedence; add PR comment idempotency; replace hard-coded targets with baseline-and-measure

### Round 2 (gpt-5.4, 2026-04-09)
- Reviewed plan against actual `build_graph.py` source and graphify v0.3.17 API
- Key feedback: plan was confirmed sound after incorporating upstream API constraints
- Priority order confirmed: noise exclusion -> edge filtering -> labeling -> insights -> integration

### API Verification (Claude, 2026-04-09)
- Inspected graphify v0.3.17 source: `detect()`, `extract()`, `build_from_json()`, `cluster()`, `score_all()`, `to_json()`, `to_wiki()`
- Confirmed: `.graphifyignore` native support, `cluster()` no resolution param, `to_json()` no custom edge metadata, node IDs are bare names
- Plan updated to use native capabilities and correct fallback paths

### Round 3 — Final Sign-Off (gpt-5.4, 2026-04-09)
- Verdict: **APPROVED WITH CHANGES** (10 specific AC tweaks)
- All 10 changes incorporated:
  1. 1.2: filtering on both edge payload and in-memory graph; `excluded_edges.json` schema versioned with stable sort order
  2. 1.3: node ID normalization uses extraction metadata with `build_from_json()` fallback; `original_id` preserved
  3. 1.4: fixture schema assertions for `source_file`, `community`, `confidence_score`
  4. 2.1: tie-break rule for deterministic labels (lexicographic); removed hard 80% threshold, kept as manual spot-check
  5. 2.2: atomic prior-run handling (temp write -> rotate -> move)
  6. 3.2: targets sweep body artifact path, not `OVERLORD_REPORT.md` directly
  7. 4.1: community de-duplication by ID before commenting
- Codex confirmed sprint order and adoption gates are sound
- Codex validated graph.json schema from live artifacts (confirmed no duplicate node IDs in AIS, confidence_score present on all edges)
