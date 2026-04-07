# Overlord Backlog

> Cross-repo governance improvements tracked here. Per-repo work goes in each repo's docs/PROGRESS.md.

## Planned

| Item | Priority | Est. Hours | Notes |
|------|----------|-----------|-------|
| Operationalize Codex ingestion review flow | HIGH | 2-3 | Finish weekly sweep worktree-safe review generation, session-start backlog surfacing, and HITL promotion workflow. |
| Nightly cleanup timezone policy | LOW | 1 | Current cron is `04:00 UTC`, which is 11:00 PM America/Chicago during DST and 10:00 PM during standard time. If year-round 11:00 PM Central is required, replace with a timezone-aware guard strategy. Tracking issue: [#14](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/14). |
| Effectiveness engine baseline metrics | LOW | 4-6 | Collect bug rate, revert rate, CI pass rate per repo per week. Store in metrics/. Requires governance repo. |
| Governance doc consistency rollout | HIGH | 4-6 | Standardize the minimum governance-doc contract across `docs/PROGRESS.md`, `docs/FEATURE_REGISTRY.md`, `docs/DATA_DICTIONARY.md`, and `docs/SERVICE_REGISTRY.md` without flattening valid repo-specific structures. Includes explicit exceptions for AIS and HealthcarePlatform. |

## In Progress

| Item | Priority | Notes |
|------|----------|-------|
| Operationalize Codex ingestion review flow | HIGH | Shared helper now exists on `feat/codex-ingestion-flow`; remaining work is validation, merge, and production sweep adoption. |
| Governance doc consistency rollout — Sprint 1 | HIGH | Shared standards + reusable governance checker. Define minimum contracts, enforce section presence, and codify AIS/HP exceptions before repo-local rewrites. |

### Sprint Breakdown — Governance Doc Consistency Rollout

#### Sprint 1 — Shared Contract + Enforcement
- Scope: update `STANDARDS.md` and reusable `governance-check.yml` so governance docs are validated by minimum contract, not just file existence.
- AC: `docs/PROGRESS.md` contract is defined in standards with explicit allowance for AIS's existing backlog model.
- AC: `docs/FEATURE_REGISTRY.md` contract requires metadata + summary table, while allowing repo-specific extra columns and appendices.
- AC: `docs/DATA_DICTIONARY.md` contract allows either canonical root content or an explicit pointer to the canonical workspace-level copy.
- AC: `docs/SERVICE_REGISTRY.md` contract requires a title and registry table without forcing one repo-wide schema.
- AC: reusable governance CI fails when required governance-doc sections/metadata are missing.
- AC: HealthcarePlatform monorepo pointer behavior and AIS long-form progress layout are formalized as allowed exceptions in standards.

#### Sprint 2 — Low-Risk Repo Scaffolding
- Scope: add missing `FEATURE_REGISTRY.md` files and tighten stub metadata where governance docs are present but weak.
- AC: [local-ai-machine/docs/FEATURE_REGISTRY.md](/Users/bennibarger/Developer/hldpro/local-ai-machine/docs) exists with required summary table and metadata.
- AC: [knocktracker/docs/FEATURE_REGISTRY.md](/Users/bennibarger/Developer/hldpro/knocktracker/docs) exists with required summary table and metadata.
- AC: [local-ai-machine/docs/DATA_DICTIONARY.md](/Users/bennibarger/Developer/hldpro/local-ai-machine/docs/DATA_DICTIONARY.md) and [knocktracker/docs/DATA_DICTIONARY.md](/Users/bennibarger/Developer/hldpro/knocktracker/docs/DATA_DICTIONARY.md) include source-of-truth metadata, not just placeholder rows.
- AC: repo-local PRs pass updated governance CI.

#### Sprint 3 — Outlier Alignment
- Scope: normalize backlog/control semantics in AIS and tighten HealthcarePlatform root-pointer docs without breaking their current information architecture.
- AC: [ai-integration-services/docs/PROGRESS.md](/Users/bennibarger/Developer/hldpro/ai-integration-services/docs/PROGRESS.md) explicitly satisfies the shared backlog/control contract without flattening the full operating document.
- AC: [HealthcarePlatform/docs/DATA_DICTIONARY.md](/Users/bennibarger/Developer/hldpro/HealthcarePlatform/docs/DATA_DICTIONARY.md) clearly identifies [HealthcarePlatform/backend/DATA_DICTIONARY.md](/Users/bennibarger/Developer/hldpro/HealthcarePlatform/backend/DATA_DICTIONARY.md) as the canonical schema source in a way the checker can validate.
- AC: no repo loses deeper repo-specific registry/dictionary content just to match a shared template.

#### Sprint 4 — Optional Deeper Normalization
- Scope: align status taxonomies and richer doc conventions only after all repos satisfy the minimum contract.
- AC: status taxonomy proposal documented before rollout.
- AC: any additional normalization remains additive and does not invalidate AIS or HP exceptions.

## Done

| Item | Date | Notes |
|------|------|-------|
| 8-gap governance closure (P0-P6) | 2026-04-01 | All merged. P0: FAIL_FAST_LOG hard gate + schema guard. P1: single source of truth. P2: backlog-first hook. P3: content quality CI. P4: cross-repo deps. P5: rollback runbooks. P6: deploy pipeline. |
| 6 feature PRs merged (v1.5-v1.8) | 2026-04-01 | #233-244: corpus infra, CoS admin, proactive monitoring, reactive conversation, booking pipeline, corpus health + LLM router |
| Cross-repo governance bootstrap (all 4 repos) | 2026-04-01 | CLAUDE.md, PROGRESS.md, FAIL_FAST_LOG.md, hooks, CI workflows |
| verify-completion agent created | 2026-04-01 | Post-incident: false completion report |
| Overlord agents created (overlord, sweep, audit) | 2026-04-01 | ~/.claude/agents/ |
| STANDARDS.md created | 2026-04-01 | ~/.claude/STANDARDS.md |
| Create `hldpro-governance` GitHub repo | 2026-04-05 | Repo live, agents + standards + deps + backlog. Branch merged with fail-fast loop closure standards. |
| Fail-fast loop closure standards | 2026-04-05 | Added to STANDARDS.md — 3 requirements for repos with test/heal cycles |
| Fail-fast loop closure implementation | 2026-04-05 | 3 items: gate surfacing (verified), logs-watcher (cron every 15min), failure-pattern-writeback. memory-writer dedup bug fixed. |
| Overlord-sweep cron | 2026-04-05 | Weekly Monday 9am CT via GitHub Actions. Checks all 5 repos against STANDARDS.md, posts issue report. |
| GitHub Enterprise security | 2026-04-05 | Secret scanning, push protection, dependabot, dependency graph, org rulesets (protect main + develop). |
| Schedule overlord-sweep as recurring agent | 2026-04-05 | Live via GitHub Actions weekly cron in `hldpro-governance`. |
| Branch-safe overlord sweep + session-start Codex backlog surfacing | 2026-04-06 | Merged in PR #9. Added branch-switch guard, worktree-safe sweep execution, and Codex backlog surfacing. Validation issue: [#10](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/10). |
| Overlord sweep production hardening | 2026-04-07 | Merged in PRs #11 and #12. Fixed count normalization crash and aligned ASC-Evaluator handling with exempt status in STANDARDS.md. |
| Harden overlord metrics quality | 2026-04-07 | Merged in PR #16. Full-history checkouts + cross-repo CI token usage now produce real commit and CI metrics in issue [#10](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/10). |
| Nightly overlord cleanup workflow | 2026-04-07 | Merged in PRs #13 and #15. Added nightly artifact cleanup + stale merged branch reporting. Validation issue: [#14](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/14). |
| Codex subagent/persona routing baseline | 2026-04-07 | Updated shared standards and overlord docs so repo-required specialists can be satisfied with spawned Codex subagents/personas mapped from repo-local definitions. |
| GitHub Actions Node 20 deprecation cleanup | 2026-04-07 | Merged in PR #18. Upgraded governance workflows from `actions/checkout@v4` to `actions/checkout@v6`; production sweep run `24059154210` completed without the prior Node 20 deprecation annotation. |
