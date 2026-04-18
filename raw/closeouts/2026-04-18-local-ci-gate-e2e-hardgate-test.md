# Local CI Gate E2E Hardgate Test

**Date:** 2026-04-18
**Issue:** #282
**Branch:** `test/issue-282-local-ci-hardgate-e2e`

## Purpose

This artifact records a real end-to-end test that the governance repo Local CI Gate wiring catches governance-surface edits from the first PR run.

## Negative Control

The first commit intentionally added this governance-surface artifact without an issue-specific execution scope. Expected result: the required `local-ci-gate` check fails at planner-boundary enforcement before the PR can merge.

Observed result:

- PR: #283
- Branch: `test/issue-282-local-ci-hardgate-e2e`
- Run: `24610471671`
- Job: `71963837213`
- Required check: `local-ci-gate`
- Result: failed
- Failing checks inside Local CI Gate:
  - `governance-surface-planning`
  - `planner-boundary`
- Summary: `profile=hldpro-governance changed_files=1 source=git mode=live scope=subset total_checks=6 blockers=2 advisories=0 skipped=1 planned=0 verdict=blocker`

This proves the hardgate caught the governance-surface edit before the issue-specific plan and execution scope existed.

## Positive Control

The follow-up commit adds:

- `docs/plans/issue-282-structured-agent-cycle-plan.json`
- `raw/execution-scopes/2026-04-18-issue-282-local-ci-gate-e2e-implementation.json`

Expected result: the same PR's required `local-ci-gate` check turns green after the missing governance artifacts are present.

Observed result:

- PR: #283
- Branch: `test/issue-282-local-ci-hardgate-e2e`
- Run: `24610520596`
- Job: `71963963736`
- Required check: `local-ci-gate`
- Result: passed
- Other checks in the same PR run also passed:
  - `commit-scope`
  - `contract`
  - `Analyze (actions)`
  - `Analyze (python)`
  - `CodeQL`

This proves the required Local CI Gate check catches an unscoped governance-surface edit, then allows the same PR after the required issue-specific plan and execution scope are present.

## Ruleset Verification

Repo ruleset `15241047` (`Require Local CI Gate on main`) remains active and requires status context `local-ci-gate` on `refs/heads/main` with strict required status checks enabled.
