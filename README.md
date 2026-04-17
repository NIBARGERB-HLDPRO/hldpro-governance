# hldpro-governance

Cross-repo governance-as-code platform for the NIBARGERB-HLDPRO organization. Defines, enforces, and audits shared standards across all HLD Pro repositories.

## Overview

This repository is the central standards and audit hub for the HLD Pro ecosystem. It contains:

- A **shared standards manifest** that all code repos must satisfy
- **Claude agents** that automate governance checks (session-start, weekly sweeps, completion verification)
- **Reusable CI workflows** called by every repo's PR pipeline
- **Codex integration** for AI-powered second-opinion code reviews
- **Cross-repo dependency tracking** for shared infrastructure
- **Structured plan schema** for machine-validatable execution planning

No application code lives here — only governance policies, enforcement tooling, and audit automation.

GitHub Issues are the execution backlog/system of record for governance work. `OVERLORD_BACKLOG.md` is the governance roadmap/status mirror, not a shadow local execution backlog.

## Governed Repositories

| Repo | Type | Governance Tier | Security Tier |
|------|------|-----------------|---------------|
| ai-integration-services | SaaS platform (Supabase + Deno + Vite) | Full (hooks + CI + agents) | Full + PentAGI |
| HealthcarePlatform | Monorepo (backend + frontend), HIPAA | Full + HIPAA (zero-fail) | Full + PentAGI + HIPAA |
| local-ai-machine | AI/ML infrastructure | Full (lane-based + session locks) | Baseline |
| knocktracker | Field operations app | Standard (rules + CI) | Baseline |
| ASC-Evaluator | Knowledge repo (minimal graphify pointer/hook only) | Exempt + graphify pointer pattern | Exempt |

## Repository Structure

```
hldpro-governance/
├── STANDARDS.md                        # Shared governance contract for all repos
├── OVERLORD_BACKLOG.md                 # Cross-repo governance work tracking
├── DEPENDENCIES.md                     # Shared Supabase projects & cross-repo dependencies
├── GITHUB_ENTERPRISE_ADOPTION_PLAN.md  # Canonical enterprise rollout/closeout plan
├── GITHUB_ENTERPRISE_*.md              # Required-check baseline, ruleset pack, exception register, Sprint 1 record
├── graphify-out/                       # Governance-hosted graph outputs (canonical)
├── metrics/                            # Stored effectiveness baselines and weekly snapshots
├── wiki/                               # Governance-hosted wiki/articles derived from graphify + sweep write-back
├── raw/                                # Append-only raw feeds (issues, closeouts, operator context)
├── agents/
│   ├── overlord.md                     # Session-start standards checker
│   ├── overlord-sweep.md              # Weekly cross-repo audit agent
│   ├── overlord-audit.md              # Deep pattern analysis agent
│   └── verify-completion.md           # Hard-gate completion verification agent
├── hooks/
│   └── branch-switch-guard.sh         # Global PreToolUse hook (prevents branch conflicts)
│   └── closeout-hook.sh               # Stage 6 closeout helper for Living Knowledge Base write-back
├── scripts/overlord/
│   ├── codex_ingestion.py             # Codex review orchestration & backlog generation
│   ├── check_overlord_backlog_github_alignment.py # Ensures governance backlog stays issue-backed
│   ├── check_progress_github_issue_staleness.py   # Ensures repo PROGRESS backlog stays aligned with backlog-labeled GH issues
│   ├── validate_structured_agent_cycle_plan.py # Validates structured planning artifacts
│   └── README.md                      # Codex ingestion usage docs
├── docs/
│   ├── FAIL_FAST_LOG.md              # Error patterns and resolutions
│   ├── FEATURE_REGISTRY.md           # Governance repo feature inventory
│   ├── graphify_targets.json         # Executable manifest for graph refresh targets
│   ├── schemas/                      # Governance-owned JSON schemas
│   └── plans/                        # Governance plans, including Living Knowledge Base phases
└── .github/workflows/
    ├── graphify-governance-contract.yml # Repo-local graphify manifest/index contract enforcement
    ├── governance-check.yml           # Reusable PR gate (called by all repo CIs)
    ├── overlord-sweep.yml             # Weekly Monday 9 AM CT cron job
    └── overlord-nightly-cleanup.yml   # Artifact cleanup & stale branch reporting
```

## Core Components

### Standards Manifest

[`STANDARDS.md`](STANDARDS.md) is the master governance contract. The overlord agents check every repo against it. It defines:

- **Required files** — `CLAUDE.md`, `docs/PROGRESS.md`, `docs/FEATURE_REGISTRY.md`, `docs/FAIL_FAST_LOG.md`, `docs/DATA_DICTIONARY.md`, `docs/SERVICE_REGISTRY.md`, `.gitignore`
- **Required hooks** — `governance-check.sh` (doc co-staging), `backlog-check.sh` (backlog-first workflow), `check-errors.sh` (fail-fast error gate)
- **Doc co-staging rules** — Source changes must co-stage related governance docs
- **Security tiers** — From baseline (gitleaks) up to Full + PentAGI + HIPAA
- **Governance doc contracts** — Minimum structural requirements for each doc type
- **Completion verification protocol** — Artifact verification before marking work "done"

### GitHub Enterprise Governance Pack

The canonical org-governance planning pack lives at the repo root:

- [`GITHUB_ENTERPRISE_ADOPTION_PLAN.md`](GITHUB_ENTERPRISE_ADOPTION_PLAN.md)
- [`GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md`](GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md)
- [`GITHUB_ENTERPRISE_RULESET_RECOMMENDATIONS.md`](GITHUB_ENTERPRISE_RULESET_RECOMMENDATIONS.md)
- [`GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md`](GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md)
- [`GITHUB_ENTERPRISE_SPRINT1_TASKS.md`](GITHUB_ENTERPRISE_SPRINT1_TASKS.md)

Use these files instead of reconstructing org-ruleset state from old PRs or ad hoc notes.

### Structured Plan Schema

Org-wide structured execution planning now uses:

- [`docs/schemas/structured-agent-cycle-plan.schema.json`](docs/schemas/structured-agent-cycle-plan.schema.json)
- [`scripts/overlord/validate_structured_agent_cycle_plan.py`](scripts/overlord/validate_structured_agent_cycle_plan.py)

Rules:
- JSON is the canonical plan artifact
- Markdown is optional companion context
- `specialist_reviews` and `alternate_model_review` are mandatory structured fields
- reusable governance CI validates `*structured-agent-cycle-plan.json` on issue/riskfix execution branches
- Tier 1 planner writes are restricted to planning/review/handoff artifacts via execution-scope `allowed_write_paths`
- Non-planning diffs require accepted pinned-agent handoff evidence; same-model/family implementers need an active exception reference with expiry
- CI is authoritative for this planner boundary; local hook warnings are early signal only

### Claude Agents

Four agents in [`agents/`](agents/) automate governance:

| Agent | Model | Trigger | Purpose |
|-------|-------|---------|---------|
| **overlord** | Haiku | Session start | Quick standards drift check (5 lines max) |
| **overlord-sweep** | Sonnet | Weekly cron (Mon 9 AM CT) | Full audit: metrics, security, Codex reviews across all repos |
| **overlord-audit** | Sonnet | On-demand | Deep cross-repo pattern analysis, PR-ready recommendations |
| **verify-completion** | Haiku | Before marking work "done" | Hard gate — verifies artifacts exist in git tree via isolated worktrees |

All agents are **read-only** — they report findings but do not modify repositories.

### CI Workflows

Three workflows in [`.github/workflows/`](.github/workflows/):

- **`graphify-governance-contract.yml`** — Repo-local graphify contract gate. Validates the manifest-driven graph target contract, checks helper scripts compile, and fails when `wiki/index.md` is out of sync with the tracked graph summaries.
- **`governance-check.yml`** — Reusable workflow called by all repo CIs on PRs. Validates required docs exist with correct structure, enforces doc co-staging, scans for `PENDING_` placeholders, and checks `.gitignore` coverage.
- **`overlord-sweep.yml`** — Weekly scheduled audit. Checks out all 5 repos, collects metrics (bug rate, revert rate, CI pass %), validates security tiers, runs Codex second-opinion reviews, and generates compliance reports.
- **`metrics/effectiveness-baseline/`** — Reproducible weekly metrics snapshots generated by the sweep and tracked in governance.
- **`metrics/graphify-evals/`** — Repeatable graphify-vs-baseline retrieval comparisons and summaries.
- **`metrics/graphify-usage/`** — Append-only graphify usage-event logs and schema-backed logging path, including optional prompt/query/candidate telemetry for live A/B traces.
- **`overlord-nightly-cleanup.yml`** — Daily artifact cleanup and stale merged branch reporting.

### Graphify Local Validation

Use [`scripts/knowledge_base/prepare_local_graphify_repos.sh`](scripts/knowledge_base/prepare_local_graphify_repos.sh) to create helper-managed `repos/` symlinks from sibling HLDPRO checkouts when validating the manifest-driven graph refresh path from an isolated governance worktree.

### Graphify Artifact Contract

- `docs/graphify_targets.json` is the source of truth for canonical output directories under `graphify-out/<repo>/`.
- Canonical per-repo artifacts are `GRAPH_REPORT.md`, `graph.json`, `community-labels.json`, `.graphify_summary.json`, `.graphify_detect.json`, and `.graphify_ast.json`.
- Nested `graphify-out/<repo>/graph.html` files are optional and not required by the governance contract.
- Local-only exceptions remain ignored: root `graphify-out/cache/`, `graphify-out/.DS_Store`, `graphify-out/.graphify_tmp.json`, `graphify-out/graph.html`, and repo-wide nested `cache/` or `.DS_Store` noise.

### Hooks

[`hooks/branch-switch-guard.sh`](hooks/branch-switch-guard.sh) is a global PreToolUse hook installed in `~/.claude/settings.json`. It blocks `git checkout <branch>` and `git switch <branch>` to prevent multi-session branch conflicts. Worktrees (`git worktree add`) are the safe alternative.

### Codex Integration

[`scripts/overlord/codex_ingestion.py`](scripts/overlord/codex_ingestion.py) orchestrates OpenAI Codex CLI for second-opinion code reviews:

- **`generate`** — Runs Codex review for a repo, outputs `review-{date}.json`
- **`qualify`** — Deduplicates and validates findings, generates `backlog-{date}.md`
- **`status`** — Lists pending backlog files for session-start surfacing
- **`promote`** — Previews or applies approved findings into repo docs

Findings are tagged `CODEX-FLAGGED` for traceability. See [`scripts/overlord/README.md`](scripts/overlord/README.md) for usage examples.

### Graphify Measurement

- [`scripts/knowledge_base/measure_graphify_usage.py`](scripts/knowledge_base/measure_graphify_usage.py) runs deterministic graphify-vs-baseline retrieval comparisons over tracked scenario files.
- [`scripts/knowledge_base/log_graphify_usage.py`](scripts/knowledge_base/log_graphify_usage.py) appends schema-shaped usage events to `metrics/graphify-usage/events/`, including optional live prompt/query/candidate traces.
- The first scenario corpus uses the real fail-fast issues so graphify quality and token-footprint estimates are measured on live governance work, not synthetic prompts.
- The measurement output now includes per-scenario query traces so graphify-vs-baseline A/B runs are inspectable at the prompt and candidate-file level, not only via summary hit counts.
- The measurement harness now emits append-only usage events by default for each graphify and baseline scenario run, so 5-10 case A/B batches automatically produce inspectable query-trace telemetry.

## Key Governance Mechanisms

- **Backlog-first workflow** — Hard gate blocks branch creation unless a `PLANNED` or `IN_PROGRESS` entry exists in `docs/PROGRESS.md`
- **Issue-backed governance backlog** — GitHub Issues are the execution backlog for this repo; `OVERLORD_BACKLOG.md` is the roadmap/status mirror and CI blocks actionable rows without issue references
- **PROGRESS ↔ GitHub staleness gate** — governed product repos must keep active `docs/PROGRESS.md` backlog sections aligned with backlog-labeled GitHub issues; reusable governance CI and weekly sweep now surface drift
- **Doc co-staging** — Source code changes must co-stage related governance docs (PROGRESS, FEATURE_REGISTRY, FAIL_FAST_LOG, etc.)
- **Planner write-boundary** — Tier 1 planners may write planning/review/handoff artifacts only; non-planning changes require accepted pinned-agent handoff evidence and active exceptions for same-model/family implementers
- **Security tiers** — Tiered requirements from baseline gitleaks up to HIPAA-compliant PHI redaction agents, break-glass gates, and audit retention
- **Fail-fast loop closure** — Repos with test/heal cycles must auto-persist failure patterns and surface gate failures
- **Completion verification** — Creates isolated worktrees and runs `git show HEAD:<path>` to verify artifacts exist before allowing "done" status
- **PDCA/R closeout discipline** — Adjust/Review must either absorb newly discovered required work into the current slice or record it as explicit issue-backed follow-up before closure
- **Branch isolation** — Global hook prevents branch switching; worktrees required for concurrent sessions
- **Conventional commits** — All repos use `feat/fix/docs/chore` with scope

## Documentation

| File | Description |
|------|-------------|
| [`STANDARDS.md`](STANDARDS.md) | Master governance contract — what the overlord enforces |
| [`OVERLORD_BACKLOG.md`](OVERLORD_BACKLOG.md) | Cross-repo governance roadmap/status mirror; actionable work must be GitHub-issue-backed |
| [`DEPENDENCIES.md`](DEPENDENCIES.md) | Shared Supabase projects and cross-repo edge function dependencies |
| [`docs/FAIL_FAST_LOG.md`](docs/FAIL_FAST_LOG.md) | Error patterns and resolutions from this repo |
| [`docs/FEATURE_REGISTRY.md`](docs/FEATURE_REGISTRY.md) | Feature inventory for the governance repo itself |
