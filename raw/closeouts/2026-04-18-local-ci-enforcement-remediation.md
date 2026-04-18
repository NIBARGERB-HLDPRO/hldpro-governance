# Closeout: Issue #275 Local CI Gate Enforcement Remediation

Date: 2026-04-18
Issue: #275
Branch: `feature/issue-275-local-ci-enforcement-remediation`

## Result

Implemented the approved remediation scope for Local CI Gate enforcement wiring:

- Generated managed shims now resolve the live shim path and target repo root at runtime instead of embedding consumer worktree paths.
- Managed shims still preserve `HLDPRO_GOVERNANCE_ROOT` as the operator override for the governance checkout.
- The deployer tests prove copied-shim portability and non-zero exit propagation through the shim, including a live blocker failure through the real runner.
- Runner JSON reports now include invocation metadata: governance root, governance ref, shim path, argv, cwd, and runner path.
- Changed-file resolution now includes unstaged tracked edits even when a profile defines `base_ref`, preventing local dry-runs from under-planning checks on dirty worktrees.
- The governance profile no longer references the stale issue #253 execution scope. It resolves the active issue execution scope from the current branch and passes that to `assert_execution_scope.py`.
- The runbook now distinguishes profile availability, shim installation, manual live gates, pre-push hook gates, and CI-required gates.
- A retrospective audit records the session deviations that caused issue #275.

## Validation

Passed:

- `python3 -m py_compile scripts/overlord/deploy_local_ci_gate.py scripts/overlord/test_deploy_local_ci_gate.py tools/local-ci-gate/local_ci_gate.py tools/local-ci-gate/tests/test_local_ci_gate.py tools/local-ci-gate/bin/hldpro-local-ci`
- `python3 scripts/overlord/test_deploy_local_ci_gate.py` (`10` tests)
- `python3 tools/local-ci-gate/tests/test_local_ci_gate.py` (`16` tests)
- `python3 -m pytest tools/local-ci-gate/tests/test_local_ci_gate.py scripts/overlord/test_deploy_local_ci_gate.py -q` (`26` tests)
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --dry-run --json`
- `python3 -m json.tool raw/execution-scopes/2026-04-18-issue-275-local-ci-enforcement-remediation-implementation.json >/dev/null`
- `git diff --check`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name feature/issue-275-local-ci-enforcement-remediation`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name feature/issue-275-local-ci-enforcement-remediation --changed-files-file /tmp/issue-275-implementation-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`

Locally blocked, not pass-equivalent:

- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-18-issue-275-local-ci-enforcement-remediation-implementation.json --changed-files-file /tmp/issue-275-implementation-changed-files.txt`

The assertion now clears the #275 branch/scope/handoff requirements, but it fails because declared forbidden roots outside this isolated worktree are dirty:

- `/Users/bennibarger/Developer/HLDPRO/hldpro-governance`
- `/Users/bennibarger/Developer/HLDPRO/knocktracker`
- `/Users/bennibarger/Developer/HLDPRO/local-ai-machine`
- `/Users/bennibarger/Developer/HLDPRO/ai-integration-services`

Those roots were not modified by this implementation branch.

## Remaining Boundary

This PR does not claim CI-required or hook-required enforcement. The approved issue #275 write scope did not include `.github/workflows/**` or `hooks/**`, so repository-level hardgate wiring is tracked separately in issue #277.

CI remains authoritative. Dry-runs are mapping evidence only.
