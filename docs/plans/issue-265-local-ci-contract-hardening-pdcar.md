# PDCAR: Issue #265 Local CI Gate Contract Hardening

## Problem

The Local CI Gate toolkit now has multiple consumer profiles, but two contracts are still too implicit for broad rollout: profile validity is convention-heavy, and managed shims embed absolute governance checkout paths with no operator override.

## Plan

Land a planning/scope PR before implementation:

- Add a canonical structured agent cycle plan for issue #265.
- Add planning and implementation execution scopes.
- Add this PDCA/R and the planning cross-review artifact.
- Update governance mirrors so #264 is complete and #265 is active.

Then implement on `feat/issue-265-local-ci-contract-hardening`:

- Add profile validation for duplicate check IDs and optional metadata shape.
- Extend bundled-profile tests.
- Add `HLDPRO_GOVERNANCE_ROOT` managed-shim override while preserving embedded fallback.
- Add deployer tests for override and fallback behavior.
- Add runbook profile catalog and consumer prerequisites.

## Do

Planning artifacts are added in the planning branch only. No runner, deployer, profile, or downstream product changes occur in this PR.

## Check

Planning validation:

- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-265-local-ci-contract-hardening-plan`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-265-local-ci-contract-hardening-plan --changed-files-file /tmp/issue-265-planning-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-18-issue-265-local-ci-contract-hardening-planning.json --changed-files-file /tmp/issue-265-planning-changed-files.txt`
- `bash scripts/cross-review/require-dual-signature.sh raw/cross-review/2026-04-18-issue-265-local-ci-contract-hardening-plan.md`
- `git diff --check`

Implementation validation will additionally include:

- `python3 -m pytest tools/local-ci-gate/tests/test_local_ci_gate.py scripts/overlord/test_deploy_local_ci_gate.py -q`
- profile dry-run checks for `hldpro-governance`, `knocktracker`, and `ai-integration-services`
- managed shim generation tests for env override and fallback

## Adjust

If optional profile metadata adds churn without clear enforcement value, keep it optional and focus this slice on duplicate IDs, required fields, runbook catalog, and shim root override.

## Review

This is contract hardening for an already approved toolkit. CI remains authoritative; Local CI Gate output must continue to identify local checks as an upstream filter rather than a full CI replay.
