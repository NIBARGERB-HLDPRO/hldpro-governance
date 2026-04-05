# Overlord Backlog

> Cross-repo governance improvements tracked here. Per-repo work goes in each repo's docs/PROGRESS.md.

## Planned

| Item | Priority | Est. Hours | Notes |
|------|----------|-----------|-------|
| Create `hldpro-governance` GitHub repo | MED | 3-4 | After 8-gap plan is validated (1-2 weeks). Contains: agents/, standards/, templates/, metrics/. Local ~/.claude/ symlinks from repo. Weekly sweep runs as GitHub Action cron. |
| Schedule overlord-sweep as recurring agent | LOW | 1 | Use `claude schedule` or cron. Depends on governance repo existing. |
| Effectiveness engine baseline metrics | LOW | 4-6 | Collect bug rate, revert rate, CI pass rate per repo per week. Store in metrics/. Requires governance repo. |
| Fail-fast loop closure: live logs + pattern write-back + PR gate event | HIGH | 5 | Three connections to close the loop from ~60% to ~100%. (1) Wire hldpro-watcher.md to Supabase Management API `/logs/explorer` for live error logs — eliminates manual log cross-referencing (2h, AIS repo). (2) Auto-write failure patterns to operator_context via memory-writer after confirmed fix — so heal.py has the pattern on next run (2h, AIS repo). (3) governance-check.yml writes `context_type: system_event` row on gate failure so morning briefing surfaces it (1h, this repo). Depends on memory-writer edge function. Pair with prompt caching on v1.5 priority list. |

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
