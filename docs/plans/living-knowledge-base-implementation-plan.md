# Living Knowledge Base — Implementation Plan
## HLD Pro Governance + Knowledge System
**Version 1.0 · April 2026 · CONFIDENTIAL**

---

| Attribute | Value |
|---|---|
| Document | Living Knowledge Base — Implementation Plan |
| Version | 1.0 |
| Date | April 2026 |
| Primary Repo | hldpro-governance |
| Secondary Repo | ai-integration-services (HLD Pro) |
| Total Phases | 8 tracked phases; phases 1-5 complete |
| Total Estimated Effort | 12–18 hrs for the initial 3-phase core, plus follow-on expansion phases |
| Three Tools | graphify · Karpathy Loop · MBIF Crew (dispatcher pattern only) |
| Classification | CONFIDENTIAL — Internal Use Only |

---

## 1. Executive Summary

This plan wires three open-source tools into the existing hldpro-governance + ai-integration-services stack to create a compounding knowledge system. The goal is not to install more tooling for its own sake — it is to close the three missing connections identified in the fail-fast loop assessment: watcher to live logs, pattern write-back to `operator_context`, and PR gate failures to the morning briefing.

The three tools serve distinct roles in the architecture:

| Tool | Install Strategy | Role in Stack | Time |
|---|---|---|---|
| graphify | Install as-is (pip + CLI) | Knowledge graph of all governed repos — feeds Stage 1 Research in the six-stage cycle | 2–3 hrs |
| Karpathy Loop | Build our own (no repo to install) | Stage 6 Closeout writes back to `raw/` and `wiki/` — the compounding loop | 4–5 hrs |
| MBIF Crew | Take pieces only (dispatcher pattern) | governance `CLAUDE.md` becomes a pure router — no new agents added | 1–2 hrs |

> **ARCHITECTURE PRINCIPLE:** The knowledge stack does not run parallel to the six-stage development cycle. It IS the memory layer that feeds Stage 1 (Research) and receives Stage 6 (Audit/Closeout) outputs. graphify provides the map. The Karpathy Loop keeps the map current. The dispatcher routes to the right agent without re-deriving context every session.

Everything installs into `hldpro-governance`, not into individual product repos. `ai-integration-services` gets a PreToolUse hook and `CLAUDE.md` pointer only — no structural changes to the HLD Pro codebase.

> **OPERATOR RULE:** graphify outputs are governance-hosted only. Product repos keep pointers/hooks, not tracked `graphify-out/` artifacts. When you want architecture memory, dependency shape, or repo topology, start with governance `wiki/` and `graphify-out/` instead of ad hoc RAG-style repo search.
>
> **VIEWER RULE:** Obsidian or similar tools may be used as optional local readers over governance `wiki/`, but they are not the source of truth. Git-tracked governance docs and graph artifacts remain canonical.

---

## 2. Architecture

### 2.1 Target Directory Structure

All knowledge infrastructure lives in `hldpro-governance`. Product repos get read-only pointers.

```text
hldpro-governance/
├── agents/                    ← existing: overlord, sweep, audit, verify
├── agents/overlord-sweep.md   ← MODIFIED: extend to write wiki/ findings
├── CLAUDE.md                  ← MODIFIED: pure dispatcher (MBIF Crew pattern)
├── raw/                       ← NEW: feed sources (conversations, issues, closeouts)
│   ├── conversations/
│   ├── github-issues/
│   ├── closeouts/
│   └── operator-context/
├── wiki/                      ← NEW: Karpathy Loop output
│   ├── index.md               ← entry point for all agents
│   ├── hldpro/
│   ├── decisions/
│   └── patterns/
├── graphify-out/              ← NEW: graphify graph output
│   ├── GRAPH_REPORT.md        ← read by all agents pre-session
│   ├── graph.json
│   └── graph.html
├── hooks/                     ← existing
├── STANDARDS.md               ← existing
└── DEPENDENCIES.md            ← existing

ai-integration-services/
├── CLAUDE.md                  ← MODIFIED: pointer to governance wiki/index.md
└── .claude/settings.json      ← MODIFIED: graphify PreToolUse hook added
```

Operational rules:
- `graphify-out/` is tracked only in `hldpro-governance`
- Product repos may generate local graphify artifacts transiently during rebuilds, but those are not the source of truth
- If you need `graph.html`, open it from the governance checkout/worktree, not from a product repo
- graphify/wiki replaces repo-level architecture-memory search; use product-repo RAG/search only for product features that intentionally implement customer-facing retrieval
- Community labels should be post-processed into operator-readable domain names; raw `Community N` labels are acceptable only as an intermediate artifact

### 2.2 Data Flow

The architecture creates a single compounding loop:

| Stage | What Happens | Output Location |
|---|---|---|
| Stage 1 — Research | Agents read `GRAPH_REPORT.md` and `wiki/index.md` before starting work | Context in agent session |
| Stage 2 — Plan | Locked JSON spec produced with graph-informed context | `docs/plans/` |
| Stage 3–4 — Review | overlord agents check plan against `STANDARDS.md` | `agent output/` |
| Stage 5 — Execute | Work happens in product repos | Product repo |
| Stage 6 — Closeout | Findings written to `raw/closeouts/` + `operator_context` row | `raw/` + Supabase |
| Weekly Sweep | overlord-sweep runs `graphify --update`, writes findings to `wiki/` | `wiki/` + `graphify-out/` |
| Karpathy Loop | wiki grows richer each cycle. `GRAPH_REPORT.md` updates automatically | Compounding |

---

## 3. Phase 1 — graphify Install + Initial Graph Build

**Target: ~2–3 hrs · Do this first, it is independent**

### Decision: Install as-is

graphify is a pure tool with no HLD Pro-specific logic. It installs via pip, copies a `SKILL.md` into `~/.claude/skills/`, and writes a PreToolUse hook into `settings.json`. Nothing to build. The only decision is what to point it at and where to store the output.

> **SCOPE DECISION:** Run graphify on `ai-integration-services` first. 131 edge functions + 45 migrations + all plan docs. HealthcarePlatform gets special treatment in Phase 2 (HIPAA — verify doc extraction privacy boundary before running). Other governed repos in Phase 3.

### Phase 1 Tasks

| # | Task | Repo / Location | Hrs | Priority | Notes |
|---|---|---|---|---|---|
| 1.1 | `pip install graphifyy && graphify install` | Local machine | 0.25 | HIGH | Installs CLI + skill into `~/.claude/skills/graphify/` |
| 1.2 | Run: `graphify claude install` in ai-integration-services root | ai-integration-services | 0.25 | HIGH | Writes PreToolUse hook to `.claude/settings.json` + `CLAUDE.md` section |
| 1.3 | Run initial graph build: `/graphify .` from ai-integration-services | ai-integration-services | 1.0 | HIGH | First run extracts all 131 edge functions + migrations + plan docs. Takes 20–40 min. |
| 1.4 | Move `graphify-out/` to `hldpro-governance/graphify-out/` | hldpro-governance | 0.25 | HIGH | Centralizes all graph output in governance repo. Update `.gitignore`: exclude `graph.html` (large), keep `GRAPH_REPORT.md` + `graph.json` |
| 1.5 | Install graphify git hook in ai-integration-services | ai-integration-services | 0.25 | HIGH | `graphify hook install` — rebuilds graph on every commit automatically |
| 1.6 | Add `GRAPH_REPORT.md` pointer to ai-integration-services `CLAUDE.md` | ai-integration-services | 0.25 | HIGH | One line: "Read `hldpro-governance/graphify-out/GRAPH_REPORT.md` before answering architecture questions" |
| 1.7 | Verify graph quality: review `GRAPH_REPORT.md` god nodes + communities | hldpro-governance | 0.5 | HIGH | Sanity check: are CRMConnector, edge-fn auth pattern, billing flow surfaced as god nodes? |
| 1.8 | Run: `graphify ./raw --wiki` to generate initial wiki/ stub | hldpro-governance | 0.25 | HIGH | Creates `wiki/index.md` + community articles. Seed for Phase 2 Karpathy Loop. |

### Phase 1 Completion Gate

| Gate | Pass Condition |
|---|---|
| graphify installed | `graphify --version` returns without error |
| Graph built | `hldpro-governance/graphify-out/GRAPH_REPORT.md` exists and has god nodes + communities |
| PreToolUse hook live | `.claude/settings.json` in ai-integration-services has graphify hook entry |
| Wiki stub exists | `hldpro-governance/wiki/index.md` exists with at least one community article |
| Git hook installed | `graphify hook status` returns 'installed' in ai-integration-services |

---

## 4. Phase 2 — Dispatcher CLAUDE.md + Wiki Write-Back

**Target: ~4–5 hrs · Requires Phase 1 complete**

### Decision: Take pieces from MBIF Crew, do not install

My Brain Is Full Crew has two valuable components: the pure-router `CLAUDE.md` pattern (dispatcher that never answers directly, only delegates) and the vault folder schema. The personal health/nutrition/wellness agents are irrelevant. We steal the pattern, not the repo.

> **WHAT WE TAKE FROM MBIF CREW:** (1) `CLAUDE.md` as pure dispatcher — "NEVER RESPOND DIRECTLY. You are the dispatcher. Delegate to the right agent. Period." (2) The agent routing table pattern. (3) The vault folder schema adapted to HLD Pro's information architecture. We do NOT add new agents — the scribe/sorter/connector/librarian behaviors fold into the extended overlord-sweep.

### Phase 2 Tasks

| # | Task | Repo / Location | Hrs | Priority | Notes |
|---|---|---|---|---|---|
| 2.1 | Rewrite `hldpro-governance/CLAUDE.md` as pure dispatcher | hldpro-governance | 1.0 | HIGH | Model: MBIF Crew CLAUDE.md pattern. Route to overlord, sweep, audit, verify. Never answer directly. Include routing table. |
| 2.2 | Create `hldpro-governance/raw/` directory structure | hldpro-governance | 0.25 | HIGH | `mkdir raw/conversations raw/github-issues raw/closeouts raw/operator-context` |
| 2.3 | Create `hldpro-governance/wiki/` directory structure | hldpro-governance | 0.25 | HIGH | `mkdir wiki/hldpro wiki/decisions wiki/patterns`. Move Phase 1 wiki stub output here. |
| 2.4 | Extend `overlord-sweep.md`: add wiki write-back step | hldpro-governance | 1.5 | HIGH | After weekly audit, sweep writes findings to `wiki/patterns/` and `wiki/decisions/`. Add Karpathy 4-line prompt as final step. |
| 2.5 | Create `wiki/index.md` template | hldpro-governance | 0.5 | HIGH | Master entry point. All agents read this before starting. |
| 2.6 | Seed `raw/conversations/` with key decision excerpts | hldpro-governance | 0.5 | MEDIUM | Extract 5–10 key architectural decisions from recent Claude.ai sessions. |
| 2.7 | Add `wiki/index.md` pointer to all four overlord agent files | hldpro-governance | 0.5 | HIGH | One line added to each agent: "Read `wiki/index.md` and `graphify-out/GRAPH_REPORT.md` before starting." |
| 2.8 | Run overlord-sweep manually to verify wiki write-back works | hldpro-governance | 0.5 | HIGH | Smoke test: does sweep produce `wiki/` output? Are findings filed correctly? |

### Phase 2 Completion Gate

| Gate | Pass Condition |
|---|---|
| Dispatcher live | `hldpro-governance/CLAUDE.md` contains routing table and NEVER RESPOND DIRECTLY rule |
| wiki/ populated | `wiki/index.md` exists with linked articles. At least 3 decision pages in `wiki/decisions/` |
| Sweep extended | `overlord-sweep.md` has explicit wiki write-back step as final action |
| Agents updated | All 4 overlord agents read `wiki/index.md` at session start |
| raw/ seeded | `raw/conversations/` has at least 5 decision excerpts |

---

## 5. Phase 3 — Karpathy Loop + Closeout Hook

**Target: ~6–8 hrs · Requires Phase 2 complete**

### Decision: Build the Karpathy Loop, there is no repo to install

The Karpathy Loop is a pattern, not a package. The implementation is: a closeout hook that fires at Stage 6, writes structured findings to `raw/closeouts/`, creates an `operator_context` row in Supabase, and triggers `graphify --update`. The loop closes itself — no manual intervention required after setup.

> **THE LOOP IN ONE SENTENCE:** Every piece of work that completes writes back to the knowledge base. The knowledge base feeds the next piece of work. The knowledge base gets richer with every cycle. This is the compounding asset.

### Phase 3 Tasks

| # | Task | Repo / Location | Hrs | Priority | Notes |
|---|---|---|---|---|---|
| 3.1 | Create Stage 6 closeout template: `raw/closeouts/TEMPLATE.md` | hldpro-governance | 0.5 | HIGH | Fields: date, repo, task_id, decision_made, pattern_identified, contradicts_existing, links_to_wiki_pages, operator_context_written |
| 3.2 | Add closeout step to six-stage cycle `CLAUDE.md` | hldpro-governance | 0.5 | HIGH | Stage 6 now has explicit closeout sub-steps: fill template, write to `raw/closeouts/`, create `operator_context` row, run `graphify --update` |
| 3.3 | Write `closeout-hook.sh` in `hldpro-governance/hooks/` | hldpro-governance | 1.5 | HIGH | Script: (1) validate closeout template filled, (2) copy to `raw/closeouts/YYYY-MM-DD-{task}.md`, (3) run `graphify --update`, (4) prompt for `operator_context` row creation |
| 3.4 | Create GitHub Actions raw feed job | hldpro-governance | 1.5 | HIGH | Nightly: fetch new GitHub issues + PR comments from all governed repos, format as markdown, append to `raw/github-issues/` |
| 3.5 | Wire `operator_context` table to `raw/operator-context/` | ai-integration-services | 1.0 | HIGH | Edge function: on new `operator_context` row INSERT, write markdown summary to `hldpro-governance/raw/operator-context/` via GitHub API |
| 3.6 | Add weekly `graphify --update` to `overlord-sweep.yml` cron | hldpro-governance | 0.5 | HIGH | Sweep already runs Monday 9 AM CT. Add: checkout ai-integration-services, run `graphify --update`, commit updated `graphify-out/` |
| 3.7 | Add wiki health check to `overlord-sweep.md` | hldpro-governance | 0.5 | HIGH | Karpathy "Lint + Heal" step: broken wikilinks, orphan pages, stale pages (30+ days), suggest new connections |
| 3.8 | Validate full loop end-to-end | hldpro-governance | 1.0 | HIGH | Complete one real task using full six-stage cycle. Verify Stage 6 closeout -> graphify update -> wiki entry traceable end-to-end. |

### Phase 3 Completion Gate

| Gate | Pass Condition |
|---|---|
| Closeout hook works | `closeout-hook.sh` runs without error on a test closeout file |
| Loop observable | After one full six-stage cycle, `raw/closeouts/` has a new file AND `GRAPH_REPORT.md` reflects the change |
| GitHub feed live | `raw/github-issues/` has files generated by the nightly Actions job |
| operator_context bridge | A new `operator_context` INSERT in Supabase produces a file in `raw/operator-context/` |
| Wiki health check runs | overlord-sweep produces a wiki health report with at least one suggested link |

---

## 6. Future Phases (Post v1.5)

| Phase | Description | Gate Condition |
|---|---|---|
| Phase 4 | Add HealthcarePlatform to graphify scope | Completed 2026-04-09. Governance hosts the full-repo graph outputs and wiki articles. |
| Phase 5 | Add ASC-Evaluator to graphify scope | Completed 2026-04-09 using the same governance-hosted pointer/hook pattern as HealthcarePlatform. |
| Phase 6 | Add remaining governed repos (local-ai-machine, knocktracker) | Completed 2026-04-09. Both repos now use the governance-hosted pointer/hook pattern and have graph/wiki outputs tracked in governance. |
| Phase 7 | `graphify --neo4j push` to local Neo4j instance | Completed 2026-04-09. Governance now has a Docker-backed Neo4j runtime bootstrap and a validated local push path with scoped graph ids. Future work should focus on enrichment/Graphiti choices rather than runtime uncertainty. |
| Phase 8 | Fine-tune Qwen3-32B on wiki data | Karpathy "Train a Custom Model on Wiki Data" step. Wiki must have 6 months of compounding data minimum. |

---

## 7. Decision Log

| Decision | Choice | Rationale |
|---|---|---|
| graphify install strategy | Install as-is | Pure tool, no HLD Pro logic. 2-command install. No customization needed. |
| graphify scope (Phase 1) | ai-integration-services only | Highest complexity, highest daily cognitive load. HealthcarePlatform was deferred initially, then explicitly approved on 2026-04-09 for full-repo Phase 4 adoption. ASC-Evaluator followed the same governance-hosted pattern on 2026-04-09 as Phase 5. |
| MBIF Crew strategy | Take dispatcher pattern only, no install | Personal health agents irrelevant. Scribe/sorter/connector/librarian behavior folds into extended overlord-sweep. No new agents = no new orchestration complexity for solo operator. |
| Karpathy Loop strategy | Build our own | No single repo IS the loop. Pattern implementation takes about the same time as adapting someone else's repo. We own the logic. |
| Raw feed sources (Phase 1) | Conversations + GitHub issues only | High signal, structured, already available. VAPI transcripts + support tickets deferred: high volume, low density, need filter layer first. |
| Knowledge base location | hldpro-governance only | Single source of truth. Product repos get read-only pointers. No knowledge scattered across 5 repos. |
| New agents added | None | Existing 4 overlord agents extended. Adding agents increases orchestration complexity with no benefit for solo operator. |
| overlord write access | Read-only maintained | Overlord agents remain read-only. Wiki write-back happens in overlord-sweep (already has controlled write scope to governance repo docs). |

---

## 8. Effort Summary

| Phase | Description | Estimate | Priority |
|---|---|---|---|
| Phase 1 | graphify install + initial graph build | 2–3 hrs | HIGH — immediate ROI |
| Phase 2 | Dispatcher CLAUDE.md + wiki write-back | 4–5 hrs | HIGH — closes watcher gap |
| Phase 3 | Karpathy Loop + closeout hook + raw/ automation | 6–8 hrs | HIGH — closes the loop |
| **Total** | | **12–18 hrs** | 3 weeks at 4–6 hrs/week |

> **SEQUENCING NOTE:** Phase 1 is independent and can ship immediately. Phase 2 depends on Phase 1 wiki stub. Phase 3 depends on Phase 2 dispatcher and `raw/` structure. The three phases are strictly sequential but each is independently valuable — stopping after Phase 1 or 2 still delivers real ROI.

---

## 9. Hard Rules

1. **Never modify `STANDARDS.md`** without explicit instruction
2. **Never add new agents** — the four overlord agents are sufficient; extend them, don't multiply them
3. **Never change product code** in ai-integration-services — only `CLAUDE.md` and `.claude/settings.json`
4. **HealthcarePlatform and ASC-Evaluator graphify scope must follow the approved governance plan** — as of 2026-04-09, both are approved for governance-hosted graph outputs under the documented pointer/hook pattern
5. **graphify output lives in hldpro-governance** — never commit `graphify-out/` to a product repo
6. **`raw/` feeds are append-only** — never delete or overwrite files in `raw/`
7. **`wiki/` is generated/maintained by agents** — never manually edit `wiki/` files (except `wiki/index.md` structure)
8. **The overlord agents remain read-only** — wiki write-back happens in overlord-sweep only, with controlled scope

---

*HLD Pro Living Knowledge Base Implementation Plan v1.0 — April 2026*
*Three tools. Three strategies. One compounding knowledge system.*
