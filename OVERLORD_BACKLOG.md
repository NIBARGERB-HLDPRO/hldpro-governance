# Overlord Backlog

> Cross-repo governance improvements tracked here. Per-repo work goes in each repo's docs/PROGRESS.md.

## Planned

| Item | Priority | Est. Hours | Notes |
|------|----------|-----------|-------|
| Operationalize Codex ingestion review flow | HIGH | 2-3 | Finish weekly sweep worktree-safe review generation, session-start backlog surfacing, and HITL promotion workflow. |
| Create `hldpro-governance` GitHub repo | MED | 3-4 | After 8-gap plan is validated (1-2 weeks). Contains: agents/, standards/, templates/, metrics/. Local ~/.claude/ symlinks from repo. Weekly sweep runs as GitHub Action cron. |
| Schedule overlord-sweep as recurring agent | LOW | 1 | Use `claude schedule` or cron. Depends on governance repo existing. |
| Effectiveness engine baseline metrics | LOW | 4-6 | Collect bug rate, revert rate, CI pass rate per repo per week. Store in metrics/. Requires governance repo. |
| Feature registry rollout + enforcement | HIGH | 4-6 | Make `docs/FEATURE_REGISTRY.md` mandatory for all code repos, scaffold missing registries with repo-specific capability inventories, and update reusable governance/hook standards to require co-staging when source changes land. |

## In Progress

| Item | Priority | Notes |
|------|----------|-------|

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
