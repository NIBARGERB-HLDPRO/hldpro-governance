# Overlord Backlog

> Cross-repo governance improvements tracked here. Per-repo work goes in each repo's docs/PROGRESS.md.

## Planned

| Item | Priority | Est. Hours | Notes |
|------|----------|-----------|-------|
| Shared dependency symlink helper for clean worktrees | MEDIUM | 1-2 | Issue [#72](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/72). Standardize a helper/runbook command for parity checks, safe linking, and cleanup after the manual pattern in issue #70 was approved. |
| Effectiveness engine baseline metrics | LOW | 4-6 | Collect bug rate, revert rate, CI pass rate per repo per week. Store in metrics/. Requires governance repo. |

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
| Shared dependency symlink standard for clean worktrees | 2026-04-09 | Issue [#70](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/70). Governance now explicitly allows borrowing installed dependencies from the same repo's root checkout into isolated worktrees via symlinks, but only for dependency install artifacts with same-repo + lockfile verification, post-link command proof, and local-only cleanup. Helper standardization is tracked separately in issue [#72](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/72). |
