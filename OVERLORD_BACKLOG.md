# Overlord Backlog

> Cross-repo governance improvements tracked here. Per-repo work goes in each repo's docs/PROGRESS.md.
> GitHub Issues are the execution backlog/system of record for governance work. This file is the local roadmap/status mirror for cross-repo planning, active issue-backed work, and completed-history entries that still need governance-level visibility.

## Planned

| Item | Priority | Est. Hours | Notes |
|------|----------|-----------|-------|
| Nightly cleanup timezone policy | LOW | 1 | Current cron is `04:00 UTC`, which is 11:00 PM America/Chicago during DST and 10:00 PM during standard time. If year-round 11:00 PM Central is required, replace with a timezone-aware guard strategy. Tracking issue: [#14](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/14). |
| Effectiveness engine baseline metrics | LOW | 4-6 | Issue [#43](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/43). Collect bug rate, revert rate, CI pass rate per repo per week. Store in metrics/. Requires governance repo. |
| Staged ruleset recommendation pack rollout | HIGH | 2-3 | Issue [#40](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/40). Convert the draft ruleset recommendation pack into an actionable org admin rollout sequence. |
| GitHub governance exception register rollout | MEDIUM | 1-2 | Issue [#42](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/42). Finalize approvers, review cadence, and operational adoption of `GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md`. |
| Sprint 1 repo `CODEOWNERS` rollout | HIGH | 8-12 | Issue [#41](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/41). Live default-branch recheck shows `ai-integration-services` is already covered, while `HealthcarePlatform`, `knocktracker`, and `local-ai-machine` still need `.github/CODEOWNERS` merged. |
| Living Knowledge Base — Phase 6: remaining governed repos | LOW | 2-3 | Issue [#47](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/47). Add local-ai-machine and knocktracker to graphify scope. Gate: graph quality remains useful after AIS, HealthcarePlatform, and ASC-Evaluator adoption. |
| Living Knowledge Base — Phase 7: Neo4j graph push | LOW | 4-6 | Issue [#48](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/48). `graphify --neo4j push` to local Neo4j instance. Graphiti migration. `operator_context` schema fields map to graph nodes. Gate: v2.0 local LLM milestone reached. |
| Living Knowledge Base — Phase 8: Qwen3-32B fine-tune on wiki data | LOW | TBD | Issue [#49](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/49). Fine-tune Qwen3-32B on wiki data (Karpathy "Train a Custom Model on Wiki Data" step). Gate: wiki must have 6+ months of compounding data minimum. |

## In Progress

| Item | Priority | Notes |
|------|----------|-------|
| Governance doc consistency rollout — Sprint 1 | HIGH | Issue [#45](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/45). Shared standards + reusable governance checker. Define minimum contracts, enforce section presence, and codify AIS/HP exceptions before repo-local rewrites. |

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
| Operationalize Codex ingestion review flow | 2026-04-09 | Shared helper, auth probe, canary gate, bounded timeout, and stdin/schema review path were already live; a fresh governed-repo validation against `knocktracker` completed successfully and wrote `review-2026-04-09.json`, `qualified-2026-04-09.json`, and `backlog-2026-04-09.md` under a bounded temporary ingestion root. |
| Living Knowledge Base — Phase 1 bootstrap | 2026-04-09 | graphify installed via Python 3.11, CLAUDE/settings pointers added in AIS, git hooks installed in the main AIS checkout, initial AIS code graph built (1883 nodes / 2533 edges / 111 communities), and graph artifacts synced into governance `graphify-out/` + `wiki/hldpro/`. |
| Living Knowledge Base — Phase 2 dispatcher + wiki write-back | 2026-04-09 | `CLAUDE.md` now dispatches instead of answering directly, `wiki/index.md` is the pre-session entrypoint, and overlord agents/sweep are wired for governance-hosted graph/wiki reads and write-back. |
| Living Knowledge Base — Phase 3 Karpathy Loop + closeout hook | 2026-04-09 | `raw/`, `wiki/`, closeout template, `closeout-hook.sh`, raw-feed sync, and weekly graph refresh/write-back are now implemented in governance. |
| Living Knowledge Base — Phase 4 slice (HealthcarePlatform) | 2026-04-09 | Full-repo HealthcarePlatform graph built on isolated worktree via repo-local builder (1549 nodes / 2396 edges / 176 communities), synced into governance `graphify-out/healthcareplatform/` + `wiki/healthcareplatform/`, and Phase 4 governance plan updated to reflect explicit full-repo approval. |
| Living Knowledge Base — Phase 5 slice (ASC-Evaluator) | 2026-04-09 | ASC-Evaluator adopted the governance pointer/hook pattern, and governance now hosts `graphify-out/asc-evaluator/` plus `wiki/asc-evaluator/`. |
| Required-check baseline verification | 2026-04-09 | Issue [#39](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/39). Live PR/workflow review resolved the three open policy questions: knocktracker `governance-check` skip is intentional, local-ai-machine specialized checks stay repo-specific/conditional, HealthcarePlatform `build` is baseline-safe while `playwright-gate` remains conditional. |
