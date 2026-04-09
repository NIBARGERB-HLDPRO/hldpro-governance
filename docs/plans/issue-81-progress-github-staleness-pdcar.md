# Issue 81 — PROGRESS ↔ GitHub Issue Staleness PDCA/R

Date: 2026-04-09
Issue: [#81](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/81)
Owner: Governance
Status: Complete

## Plan

Keep the slice on detection and reporting.

Accepted scope:
- add a shared validator that compares active `docs/PROGRESS.md` backlog sections with backlog-labeled GitHub issues
- wire it into reusable governance CI for governed product repos
- surface the same drift status in the weekly overlord sweep

Explicitly out of scope:
- auto-editing product repo backlog mirrors
- changing the backlog model away from GitHub issues + PROGRESS mirror sections
- broader project-management workflow redesign

## Do

Implemented:
- added the canonical plan artifact at [issue-81-structured-agent-cycle-plan.json](issue-81-structured-agent-cycle-plan.json)
- created [check_progress_github_issue_staleness.py](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-81/scripts/overlord/check_progress_github_issue_staleness.py)
- wired the validator into [governance-check.yml](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-81/.github/workflows/governance-check.yml) for governed product repos
- added a backlog drift section to [overlord-sweep.yml](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-81/.github/workflows/overlord-sweep.yml)
- added parser coverage in [test_progress_github_issue_staleness.py](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-81/tests/test_progress_github_issue_staleness.py)
- updated governance docs:
  - [README.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-81/README.md)
  - [STANDARDS.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-81/STANDARDS.md)
  - [FEATURE_REGISTRY.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-81/docs/FEATURE_REGISTRY.md)
  - [FAIL_FAST_LOG.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-81/docs/FAIL_FAST_LOG.md)
  - [OVERLORD_BACKLOG.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-81/OVERLORD_BACKLOG.md)

Validator behavior:
- open backlog-labeled GitHub issues must appear in active backlog sections of `docs/PROGRESS.md`
- closed backlog-labeled GitHub issues must not remain listed in active backlog sections
- governance itself is intentionally skipped because its execution backlog lives in `OVERLORD_BACKLOG.md`, not `docs/PROGRESS.md`

## Check

Validation run:
- `python3 -m unittest tests/test_progress_github_issue_staleness.py`
- `python3 scripts/overlord/check_progress_github_issue_staleness.py --repo NIBARGERB-HLDPRO/ai-integration-services --progress-path /Users/bennibarger/Developer/HLDPRO/ai-integration-services/docs/PROGRESS.md`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --require-if-issue-branch --branch-name issue-81-progress-github-staleness`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `git diff --check`

Live proof against the issue evidence:
- the AIS probe failed exactly as intended
- missing open backlog issues surfaced: `#872, #874, #876, #877, #878, #879, #880, #881, #882, #883, #884, #887, #888`
- stale closed backlog issues surfaced: `#834, #835, #837, #839, #840, #841, #842, #843, #844, #845`

## Do / Check Comparison

What worked:
- the checker matched the live ai-integration-services drift instead of only synthetic fixtures
- the same validator can now be reused in repo CI and the weekly sweep without duplicating logic

What needed hardening during execution:
- the weekly sweep integration initially used piped JSON with inline Python heredocs, which would have consumed stdin incorrectly
- fixed in-slice by switching to environment-backed one-liners for JSON extraction instead of leaving a brittle report path in CI

## Adjust

Adjustment made in-slice:
- added explicit `GH_TOKEN: ${{ github.token }}` to the reusable governance-check step that calls the new `gh`-backed validator
- documented the staleness gate as part of the governance contract instead of leaving it implicit in workflow code only

No new follow-up issue was required.

## Review

Decision:
- `#81` is complete

Validated governance rule:
- governed product repos must keep active `docs/PROGRESS.md` backlog sections aligned with backlog-labeled GitHub issues
- the reusable governance gate now blocks drift and the weekly sweep reports it fleet-wide
