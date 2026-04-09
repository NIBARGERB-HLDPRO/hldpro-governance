# hldpro-governance

Cross-repo governance-as-code platform for the NIBARGERB-HLDPRO organization. Defines, enforces, and audits shared standards across all HLD Pro repositories.

## Overview

This repository is the central standards and audit hub for the HLD Pro ecosystem. It contains:

- A **shared standards manifest** that all code repos must satisfy
- **Claude agents** that automate governance checks (session-start, weekly sweeps, completion verification)
- **Reusable CI workflows** called by every repo's PR pipeline
- **Codex integration** for AI-powered second-opinion code reviews
- **Cross-repo dependency tracking** for shared infrastructure

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
│   └── README.md                      # Codex ingestion usage docs
├── docs/
│   ├── FAIL_FAST_LOG.md              # Error patterns and resolutions
│   ├── FEATURE_REGISTRY.md           # Governance repo feature inventory
│   └── plans/                        # Governance plans, including Living Knowledge Base phases
└── .github/workflows/
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

- **`governance-check.yml`** — Reusable workflow called by all repo CIs on PRs. Validates required docs exist with correct structure, enforces doc co-staging, scans for `PENDING_` placeholders, and checks `.gitignore` coverage.
- **`overlord-sweep.yml`** — Weekly scheduled audit. Checks out all 5 repos, collects metrics (bug rate, revert rate, CI pass %), validates security tiers, runs Codex second-opinion reviews, and generates compliance reports.
- **`metrics/effectiveness-baseline/`** — Reproducible weekly metrics snapshots generated by the sweep and tracked in governance.
- **`overlord-nightly-cleanup.yml`** — Daily artifact cleanup and stale merged branch reporting.

### Hooks

[`hooks/branch-switch-guard.sh`](hooks/branch-switch-guard.sh) is a global PreToolUse hook installed in `~/.claude/settings.json`. It blocks `git checkout <branch>` and `git switch <branch>` to prevent multi-session branch conflicts. Worktrees (`git worktree add`) are the safe alternative.

### Codex Integration

[`scripts/overlord/codex_ingestion.py`](scripts/overlord/codex_ingestion.py) orchestrates OpenAI Codex CLI for second-opinion code reviews:

- **`generate`** — Runs Codex review for a repo, outputs `review-{date}.json`
- **`qualify`** — Deduplicates and validates findings, generates `backlog-{date}.md`
- **`status`** — Lists pending backlog files for session-start surfacing
- **`promote`** — Previews or applies approved findings into repo docs

Findings are tagged `CODEX-FLAGGED` for traceability. See [`scripts/overlord/README.md`](scripts/overlord/README.md) for usage examples.

## Key Governance Mechanisms

- **Backlog-first workflow** — Hard gate blocks branch creation unless a `PLANNED` or `IN_PROGRESS` entry exists in `docs/PROGRESS.md`
- **Issue-backed governance backlog** — GitHub Issues are the execution backlog for this repo; `OVERLORD_BACKLOG.md` is the roadmap/status mirror and CI blocks actionable rows without issue references
- **Doc co-staging** — Source code changes must co-stage related governance docs (PROGRESS, FEATURE_REGISTRY, FAIL_FAST_LOG, etc.)
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
