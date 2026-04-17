# hldpro-governance -- Repo Compendium

> Generated: 2026-04-09
> Repo: `hldpro-governance` (NIBARGERB-HLDPRO organization)

---

## Part 1: Product Narrative & Gap Analysis

### What Is This Repo?

**hldpro-governance** is a governance-as-code platform -- the central standards, enforcement, and audit hub for the entire HLD Pro organization. It contains zero application code. Instead, it defines, enforces, and audits shared engineering standards across all HLD Pro repositories.

The repo serves five functions:

1. **Standards definition** -- A single `STANDARDS.md` manifest that every code repo must satisfy.
2. **Automated enforcement** -- Claude agents that check standards compliance at session start, weekly sweeps, and completion gates.
3. **Reusable CI** -- GitHub Actions workflows called by every repo's PR pipeline to enforce doc co-staging, placeholder scanning, and governance checks.
4. **Cross-model code review** -- OpenAI Codex CLI integration for second-opinion code reviews across all repos.
5. **Living Knowledge Base** -- A compounding knowledge system (graphify knowledge graphs + wiki + raw feeds + Karpathy Loop write-back) that grows with every session.

### The Final-State System (End-to-End)

Below is the intended governance loop in its final state with current status and gaps.

---

#### 1. Standards Manifest

`STANDARDS.md` is the master contract. It defines:
- **Required files** for all code repos (CLAUDE.md, PROGRESS.md, FEATURE_REGISTRY.md, FAIL_FAST_LOG.md, DATA_DICTIONARY.md, SERVICE_REGISTRY.md, .gitignore)
- **Required hooks** (governance-check.sh, backlog-check.sh, check-errors.sh)
- **Doc co-staging rules** (source changes must co-stage governance docs)
- **Security tiers** (Exempt -> Baseline -> Full + PentAGI -> Full + PentAGI + HIPAA)
- **Branch isolation** (global hook blocks `git checkout <branch>`)
- **Conventional commits**, never-push-to-main, never-force-push
- **Completion verification protocol** (8-step artifact verification before marking "done")

- **Status:** DONE. Comprehensive, actively enforced.
- **Gap:** None at the standards-definition level.

#### 2. Governed Repository Portfolio

| Repo | Type | Governance Tier | Security Tier |
|------|------|-----------------|---------------|
| ai-integration-services | SaaS platform (Supabase + Deno + Vite) | Full (hooks + CI + agents) | Full + PentAGI |
| HealthcarePlatform | Monorepo (backend + frontend), HIPAA | Full + HIPAA (zero-fail) | Full + PentAGI + HIPAA |
| local-ai-machine | AI/ML infrastructure | Full (lane-based + session locks) | Baseline |
| knocktracker | Field operations app | Standard (rules + CI) | Baseline |
| ASC-Evaluator | Knowledge repo | Exempt + graphify pointer | Exempt |

- **Status:** DONE. All 5 repos registered, tiers assigned, governance bootstrapped.
- **Gap:** knocktracker and local-ai-machine still have placeholder DATA_DICTIONARY.md and SERVICE_REGISTRY.md (violates the new doc-quality contract).

#### 3. Claude Agent System

Four agents automate governance checks:

| Agent | Model | Trigger | Purpose |
|-------|-------|---------|---------|
| `overlord` | Haiku | Session start | Quick standards drift check (5 lines max). Read-only. |
| `overlord-sweep` | Sonnet | Weekly cron (Mon 9 AM CT) | Full audit: pull all 5 repos, check standards, collect metrics, generate cross-repo report + index + HTML dashboard. |
| `overlord-audit` | Sonnet | On-demand | Deep cross-repo pattern analysis, PR-ready recommendations. |
| `verify-completion` | Haiku | Before marking "done" | Hard gate: verifies artifacts exist via `git show HEAD:<path>` in isolated worktrees. |

The `CLAUDE.md` at repo root acts as a **dispatcher** -- it never answers questions directly, only routes to the correct agent.

- **Status:** DONE. All 4 agents defined and operational. Dispatcher pattern enforced.
- **Gap:** Agents are read-only; no auto-remediation capability. The sweep produces reports and recommendations but doesn't create PRs or fix issues.

#### 4. CI Enforcement

Three GitHub Actions workflows:

- **`governance-check.yml`** -- Reusable workflow called by all repo CIs on PRs. Validates required docs exist, enforces doc co-staging, scans for PENDING_ placeholders, checks .gitignore coverage.
- **`overlord-sweep.yml`** -- Weekly Monday 9 AM CT cron. Checks out all 5 repos via worktrees, runs full audit, generates report/index/dashboard. Includes Codex second-opinion reviews, security tier checks, PentAGI freshness validation, and wiki write-back.
- **`overlord-nightly-cleanup.yml`** -- Daily artifact cleanup and stale merged branch reporting.
- **`raw-feed-sync.yml`** -- Daily GitHub issue feed sync (fetches open issues from all governed repos to `raw/github-issues/`).

- **Status:** DONE. All workflows operational.
- **Gap:** Codex CLI authentication in CI is fragile (documented extensively in FAIL_FAST_LOG). The `CODEX_AUTH_JSON` path works but requires manual token management.

#### 5. Global Hooks

Two hooks enforced across all repos:

- **`branch-switch-guard.sh`** -- Global PreToolUse hook. Blocks `git checkout <branch>` and `git switch <branch>` to prevent multi-session branch corruption. Allows file restores. Forces worktree-based branch work.
- **`closeout-hook.sh`** -- Stage 6 closeout helper. Validates closeout template fields, triggers graphify knowledge-graph update, reminds about operator_context row creation, and auto-commits the closeout file.

- **Status:** DONE.
- **Gap:** None.

#### 6. Codex Integration (Cross-Model Review)

`scripts/overlord/codex_ingestion.py` orchestrates OpenAI Codex CLI for second-opinion code reviews:

- `generate` -- Runs Codex review for a repo, outputs `review-{date}.json`
- `qualify` -- Deduplicates, validates, and severity-classifies findings; generates `backlog-{date}.md`
- `status` -- Lists pending backlog files for session-start surfacing
- `promote` -- Previews or applies approved findings into repo docs

Findings are tagged `CODEX-FLAGGED` for traceability. Entries land in `~/Developer/hldpro/.codex-ingestion/{repo}/` and require human-in-the-loop review before promotion to actual repo docs.

- **Status:** DONE. Full pipeline validated against knocktracker. Auth probe, canary gate, bounded timeout, stdin/schema review path all implemented.
- **Gap:** Codex CLI auth in CI is still fragile. The production sweep uses `CODEX_AUTH_JSON` but this requires manual refresh. Codex CLI itself is a moving target (version compatibility issues documented in FAIL_FAST_LOG).

#### 7. Living Knowledge Base (Karpathy Loop)

A three-tool compounding knowledge system:

1. **Graphify** -- Builds knowledge graphs from repo codebases. Python 3.11 + graphifyy package. Produces node/edge/community analysis.
2. **Wiki** -- 619 markdown articles across 5 repo scopes + decisions + patterns. Auto-generated from graphify community analysis, manually curated for decisions and recurring patterns.
3. **Raw Feeds** -- Append-only stores for conversations, GitHub issues, closeouts, and operator context. These are the "training data" that compound over time.

The Karpathy Loop cycle:
1. **Raw capture** -- conversations, issues, closeouts, operator context
2. **Graph build** -- graphify rebuilds from repo code
3. **Wiki write-back** -- overlord-sweep updates wiki articles from graph + raw feeds
4. **Decision capture** -- Stage 6 closeouts record decisions with template validation

Current graph coverage:
- ai-integration-services: 1883 nodes / 2533 edges / 111 communities
- HealthcarePlatform: 1549 nodes / 2396 edges / 176 communities
- ASC-Evaluator: graphified (pointer/hook pattern)
- knocktracker: NOT YET GRAPHIFIED
- local-ai-machine: NOT YET GRAPHIFIED

- **Status:** Phases 1-5 DONE. Infrastructure in place, three repos graphified, weekly sweep wired for read/write-back.
- **Gap:**
  - **knocktracker and local-ai-machine not graphified** (Phase 6, planned, issue #47)
  - **Neo4j graph push not implemented** (Phase 7, planned, issue #48)
  - **Qwen3-32B fine-tune not started** (Phase 8, planned, issue #49, needs 6+ months of wiki data)
  - First weekly write-back run still pending (bootstrap was done manually)

#### 8. GitHub Enterprise Configuration

Org-level security and branch protection applied:
- Secret scanning + push protection enabled
- Dependabot alerts + security updates enabled
- Dependency graph enabled
- Org rulesets protecting main and develop branches
- Web commit signoff required

A detailed 4-sprint enterprise adoption plan exists covering:
- Sprint 1: Branch governance baseline (CODEOWNERS, required checks, exception process)
- Sprint 2: Advanced security rollout (GHAS, CodeQL, dependency review)
- Sprint 3: Actions hardening (SHA pinning, approved sources, break-glass)
- Sprint 4: Audit, metadata, and operating rhythm

- **Status:** Sprint 1 largely DONE (CODEOWNERS rolled out to first-wave repos, required-check baseline verified, exception register seeded). Sprints 2-4 PLANNED.
- **Gap:**
  - CodeQL code scanning not yet enabled
  - Actions inventory not yet built
  - Audit log streaming not configured
  - Custom repository properties not applied
  - Monthly governance review cadence not established
  - 2FA org requirement not yet enabled
  - Verified domains not yet added

#### 9. Effectiveness Metrics

Weekly metrics snapshots persisted to `metrics/effectiveness-baseline/`:

| Repo | Commits (7d) | Bug Rate | Revert Rate | CI Pass Rate |
|------|---:|---:|---:|---:|
| ai-integration-services | 333 | 37.5% | 0.6% | 65.0% |
| HealthcarePlatform | 295 | 33.6% | 0.3% | 80.0% |
| local-ai-machine | 23 | 13.0% | 0.0% | 90.0% |
| knocktracker | 17 | 11.8% | 0.0% | 85.0% |
| ASC-Evaluator | 2 | 0.0% | 0.0% | N/A |

- **Status:** DONE. Reproducible dated + latest snapshots, automated via sweep.
- **Gap:** No trend analysis or historical comparison UI. Snapshots are flat files only.

---

### Summary of Major Gaps (Priority Order)

| # | Gap | Impact | Complexity |
|---|-----|--------|-----------|
| 1 | **knocktracker + local-ai-machine not graphified** | Knowledge base incomplete; 2/5 repos have no graph coverage | Low (Phase 6, issue #47) |
| 2 | **Codex CLI CI auth fragility** | Weekly sweep Codex reviews may skip silently; manual token refresh needed | Medium |
| 3 | **GitHub Enterprise Sprints 2-4 not started** | CodeQL, actions hardening, audit streaming, and operating rhythm all pending | High (multi-sprint) |
| 4 | **knocktracker/local-ai-machine placeholder docs** | DATA_DICTIONARY.md and SERVICE_REGISTRY.md are empty stubs | Low |
| 5 | **No auto-remediation in agents** | Agents report but don't fix; all remediation is manual | Medium |
| 6 | **Neo4j graph push (Phase 7)** | Knowledge graph lives in flat files only; no queryable graph DB | Medium (issue #48) |
| 7 | **Nightly cleanup timezone policy** | Cron is UTC-fixed; doesn't adjust for DST (issue #14) | Low |
| 8 | **No metrics trend analysis** | Weekly snapshots exist but no historical comparison or dashboard | Low |
| 9 | **Qwen3-32B fine-tune (Phase 8)** | Needs 6+ months of wiki data accumulation first | High (issue #49) |

---

## Part 2: Repo File Compendium

Every file in the repository (excluding `.git/` and `graphify-out/` generated artifacts) with a one-line description.

### Root Files

| File | Description |
|------|-------------|
| `README.md` | Repo overview: purpose, structure, components, agents, CI, hooks, Codex integration |
| `CLAUDE.md` | Agent dispatcher: routes to overlord agents, never answers directly. Pre-session context reads. Stage 6 closeout protocol. |
| `STANDARDS.md` | Master governance contract: required files, hooks, security tiers, doc co-staging, completion verification |
| `OVERLORD_BACKLOG.md` | Cross-repo governance roadmap/status mirror. GitHub Issues are the execution backlog. |
| `DEPENDENCIES.md` | Shared Supabase projects and cross-repo edge function dependencies |
| `.gitignore` | Git ignore rules |

### GitHub Enterprise Documents

| File | Description |
|------|-------------|
| `GITHUB_ENTERPRISE_ADOPTION_PLAN.md` | 4-sprint enterprise rollout plan: branch governance, security, actions hardening, audit |
| `GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md` | Required-check matrix by repo tier |
| `GITHUB_ENTERPRISE_RULESET_RECOMMENDATIONS.md` | Staged ruleset recommendation pack with rollout sequence |
| `GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md` | Exception register with approval authority, review cadence, seeded deviations |
| `GITHUB_ENTERPRISE_SPRINT1_TASKS.md` | Sprint 1 task breakdown |

### Agents (`agents/`)

| File | Description |
|------|-------------|
| `agents/overlord.md` | Session-start standards checker (Haiku). 5-line drift report. Read-only. |
| `agents/overlord-sweep.md` | Weekly cross-repo audit (Sonnet). Full metrics, security, Codex reviews, wiki write-back. |
| `agents/overlord-audit.md` | Deep cross-repo pattern analysis (Sonnet). PR-ready recommendations. |
| `agents/verify-completion.md` | Hard-gate completion verification (Haiku). Artifact verification via isolated worktrees. |

### Hooks (`hooks/`)

| File | Description |
|------|-------------|
| `hooks/branch-switch-guard.sh` | Global PreToolUse hook: blocks git checkout/switch branch, allows file restores |
| `hooks/closeout-hook.sh` | Stage 6 closeout helper: validates template, triggers graph update, commits closeout |

### CI Workflows (`.github/workflows/`)

| File | Description |
|------|-------------|
| `.github/workflows/governance-check.yml` | Reusable PR gate: doc existence, co-staging, placeholder scan, gitignore |
| `.github/workflows/overlord-sweep.yml` | Weekly Monday 9 AM CT cron: full cross-repo audit |
| `.github/workflows/overlord-nightly-cleanup.yml` | Daily artifact cleanup and stale branch reporting |
| `.github/workflows/raw-feed-sync.yml` | Daily GitHub issue feed sync to raw/github-issues/ |

### Scripts (`scripts/`)

| File | Description |
|------|-------------|
| `scripts/codex-review-template.sh` | Canonical template for per-repo Codex review scripts |
| `scripts/overlord/codex_ingestion.py` | Codex review orchestration: generate, qualify, status, promote |
| `scripts/overlord/build_effectiveness_metrics.py` | Weekly effectiveness metrics builder (bug rate, revert rate, CI pass rate) |
| `scripts/overlord/check_overlord_backlog_github_alignment.py` | Validates governance backlog stays GitHub-issue-backed |
| `scripts/overlord/README.md` | Codex ingestion usage documentation |
| `scripts/knowledge_base/build_graph.py` | Repo-local knowledge graph builder (calls graphify modules directly) |

### Metrics (`metrics/`)

| File | Description |
|------|-------------|
| `metrics/effectiveness-baseline/README.md` | Metrics format documentation |
| `metrics/effectiveness-baseline/2026-04-09.json` | Dated metrics snapshot (JSON) |
| `metrics/effectiveness-baseline/2026-04-09.md` | Dated metrics snapshot (markdown) |
| `metrics/effectiveness-baseline/latest.json` | Latest metrics snapshot (JSON) |
| `metrics/effectiveness-baseline/latest.md` | Latest metrics snapshot (markdown) |

### Documentation (`docs/`)

| File | Description |
|------|-------------|
| `docs/FAIL_FAST_LOG.md` | Error patterns and resolutions (15 entries, heavily Codex/CI related) |
| `docs/FEATURE_REGISTRY.md` | Feature inventory: 13 governance features with status and readiness |

### Plans (`docs/plans/`)

| File | Description |
|------|-------------|
| `docs/plans/graphify-methodology-pdcar.md` | Graphify methodology PDCA/R plan |
| `docs/plans/living-knowledge-base-implementation-plan.md` | Living Knowledge Base implementation plan (Phases 1-8) |
| `docs/plans/living-knowledge-base-claude-cli-instructions.md` | Claude CLI instructions for knowledge base |
| `docs/plans/phase4-healthcareplatform-graphify-pdcar.md` | Phase 4: HealthcarePlatform graphify plan |
| `docs/plans/phase5-asc-evaluator-graphify-pdcar.md` | Phase 5: ASC-Evaluator graphify plan |
| `docs/plans/issue-39-required-check-baseline-pdcar.md` | Required-check baseline plan |
| `docs/plans/issue-40-42-ruleset-exception-rollout-pdcar.md` | Ruleset + exception register rollout plan |
| `docs/plans/issue-41-codeowners-rollout-pdcar.md` | CODEOWNERS rollout plan |
| `docs/plans/issue-43-effectiveness-baseline-pdcar.md` | Effectiveness metrics baseline plan |
| `docs/plans/issue-45-governance-doc-consistency-pdcar.md` | Governance doc consistency plan |
| `docs/plans/issue-46-codex-ingestion-pdcar.md` | Codex ingestion operationalization plan |

### Raw Feeds (`raw/`)

| File | Description |
|------|-------------|
| `raw/closeouts/TEMPLATE.md` | Stage 6 closeout template |
| `raw/closeouts/2026-04-09-living-knowledge-base-bootstrap.md` | Knowledge base bootstrap closeout |
| `raw/conversations/2026-04-09-dispatcher-pattern.md` | Dispatcher pattern conversation capture |
| `raw/conversations/2026-04-09-graphify-ais-first.md` | Graphify AIS-first conversation |
| `raw/conversations/2026-04-09-knowledge-home.md` | Knowledge home conversation |
| `raw/conversations/2026-04-09-overlord-write-scope.md` | Overlord write scope conversation |
| `raw/conversations/2026-04-09-stage6-closeout.md` | Stage 6 closeout conversation |
| `raw/github-issues/2026-04-09-ai-integration-services.md` | AIS open issues snapshot |
| `raw/github-issues/2026-04-09-HealthcarePlatform.md` | HealthcarePlatform open issues snapshot |
| `raw/github-issues/2026-04-09-knocktracker.md` | knocktracker open issues snapshot |
| `raw/github-issues/2026-04-09-local-ai-machine.md` | local-ai-machine open issues snapshot |
| `raw/operator-context/2026-04-09-knowledge-base-bootstrap.md` | Operator context for KB bootstrap |

### Wiki (`wiki/`)

The wiki contains 619 markdown articles across 7 directories. Articles are auto-generated from graphify community analysis and manually curated for decisions and patterns.

| Directory | Article Count | Description |
|-----------|---:|-------------|
| `wiki/ai-integration-services/` | ~120 | AIS code graph community articles (connectors, supabase functions, UI, etc.) |
| `wiki/healthcareplatform/` | ~330 | HealthcarePlatform code graph articles (chart audit, CI checks, compliance, etc.) |
| `wiki/asc-evaluator/` | ~10 | ASC-Evaluator graph articles (annotation, processing) |
| `wiki/hldpro/` | ~100 | HLD Pro org-level graph articles (connectors, community clusters) |
| `wiki/decisions/` | 5 | Architectural decision records |
| `wiki/patterns/` | 1 | Recurring failure patterns |
| `wiki/index.md` | 1 | Knowledge base index and navigation |

#### Notable Wiki Articles

| File | Description |
|------|-------------|
| `wiki/index.md` | Knowledge base root: platform status, recent decisions, graph summary, navigation |
| `wiki/decisions/2026-04-09-governance-is-knowledge-home.md` | Decision: governance repo is the knowledge home |
| `wiki/decisions/2026-04-09-dispatcher-never-answers-directly.md` | Decision: CLAUDE.md dispatches, never answers |
| `wiki/decisions/2026-04-09-graphify-on-ais-first.md` | Decision: graphify AIS first |
| `wiki/decisions/2026-04-09-stage6-closeout-is-required.md` | Decision: closeout is mandatory |
| `wiki/decisions/2026-04-09-overlord-write-scope-is-bounded.md` | Decision: overlord write scope is bounded |
| `wiki/patterns/graphify-runtime-drift.md` | Pattern: graphify CLI vs module API runtime drift |

### graphify-out/ (Generated Artifacts)

| Directory | Description |
|-----------|-------------|
| `graphify-out/` | Canonical scoped outputs live under `graphify-out/<repo>/` (`GRAPH_REPORT.md`, `graph.json`, `community-labels.json`, `.graphify_summary.json`, `.graphify_detect.json`, `.graphify_ast.json`); local cache, `.DS_Store`, root `.graphify_tmp.json`, and root `graph.html` noise remain ignored. |
| `graphify-out/healthcareplatform/` | HealthcarePlatform graph artifacts |
| `graphify-out/asc-evaluator/` | ASC-Evaluator graph artifacts |

---

## Part 3: Architecture Summary

| Layer | Component | Notes |
|-------|-----------|-------|
| **Standards** | `STANDARDS.md` | Single source of truth for all repo governance |
| **Agents** | 4 Claude agents (Haiku + Sonnet) | Session-start, weekly sweep, deep audit, completion gate |
| **Dispatcher** | `CLAUDE.md` | Routes to agents; never answers directly |
| **CI** | GitHub Actions (4 workflows) | PR gates, weekly audit, nightly cleanup, raw feed sync |
| **Hooks** | 2 shell scripts | Branch-switch guard (global), closeout hook (governance) |
| **Codex** | `codex_ingestion.py` | Cross-model review: generate, qualify, promote |
| **Knowledge** | graphify + wiki + raw feeds | Karpathy Loop compounding knowledge system |
| **Metrics** | `build_effectiveness_metrics.py` | Weekly bug rate, revert rate, CI pass rate snapshots |
| **Enterprise** | GitHub Enterprise config | Secret scanning, push protection, dependabot, org rulesets |
| **Language** | Shell (hooks), Python (scripts), Markdown (agents, docs, wiki) | No application code |

---

## Part 4: Current Backlog

### Planned (from OVERLORD_BACKLOG.md)

| Item | Priority | Issue | Est. Hours |
|------|----------|-------|-----------|
| Nightly cleanup timezone policy | LOW | [#14](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/14) | 1 |
| Living Knowledge Base Phase 6 (knocktracker + local-ai-machine) | LOW | [#47](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/47) | 2-3 |
| Living Knowledge Base Phase 7 (Neo4j graph push) | LOW | [#48](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/48) | 4-6 |
| Living Knowledge Base Phase 8 (Qwen3-32B fine-tune) | LOW | [#49](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/49) | TBD |

### In Progress

None currently. Active governance execution lives in GitHub Issues.

### Done (Selected Highlights)

- 8-gap governance closure (P0-P6) -- 2026-04-01
- Cross-repo governance bootstrap (all 4 repos) -- 2026-04-01
- hldpro-governance GitHub repo creation -- 2026-04-05
- GitHub Enterprise security baseline -- 2026-04-05
- Living Knowledge Base Phases 1-5 -- 2026-04-09
- GitHub Enterprise Sprint 1 (CODEOWNERS, required checks, exceptions) -- 2026-04-09
- Effectiveness metrics baseline -- 2026-04-09
- Codex ingestion operationalization -- 2026-04-09
