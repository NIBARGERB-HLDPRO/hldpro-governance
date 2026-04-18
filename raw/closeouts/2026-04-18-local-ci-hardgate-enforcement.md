# Local CI Gate Hardgate Enforcement Closeout

**Date:** 2026-04-18
**Issue:** #277
**Branch:** `feature/issue-277-local-ci-hardgate-enforcement`

## Result

This implementation adds a CI-visible Local CI Gate workflow for `hldpro-governance` and an independent contract test that prevents the workflow from silently degrading into mapping-only evidence.

It does not close the protected-branch enforcement loop. GitHub API inspection on 2026-04-18 showed no classic branch protection for `hldpro-governance/main` and no required-status-check rule in org ruleset `14715976`. Issue #277 remains open until the Local CI Gate workflow/job is required by branch protection or ruleset evidence.

## Changes

- Added `.github/workflows/local-ci-gate.yml`.
- Added `scripts/overlord/check_local_ci_gate_workflow_contract.py`.
- Added `scripts/overlord/test_local_ci_gate_workflow_contract.py`.
- Wired the contract test into `.github/workflows/graphify-governance-contract.yml` as independent CI-visible verification.
- Updated the Local CI Gate toolkit runbook, external services runbook, progress tracker, and backlog mirror with the CI-visible-vs-required-gate boundary.

## Workflow Contract

The `local-ci-gate` workflow:

- runs on `pull_request` to `main`, `push` to `main`, and `workflow_dispatch`;
- checks out full history with `fetch-depth: 0`;
- fetches `origin main` for changed-file resolution;
- disables Python bytecode writes so import-time `__pycache__` files do not contaminate changed-file detection;
- normalizes pull request checkouts to the PR branch name before running the gate, allowing issue-scoped execution-scope discovery;
- runs `python3 scripts/overlord/test_local_ci_gate_workflow_contract.py`;
- runs `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --report-dir cache/local-ci-gate/reports --json`;
- uploads `cache/local-ci-gate/reports/` as the `local-ci-gate-reports` artifact;
- does not use `--dry-run`.

## Evidence Boundary

This closeout uses the Local CI Gate runbook taxonomy:

- `local-ci-gate` workflow present: CI-visible gate.
- Independent workflow contract present: CI-visible regression guard for hardgate wiring.
- Required branch protection or ruleset context present: not yet verified.

Do not describe this change as `CI required gate` until GitHub API evidence shows the Local CI Gate workflow/job is required for `main`.

## Local Validation

Run from the isolated worktree:

```bash
python3 -m py_compile scripts/overlord/check_local_ci_gate_workflow_contract.py scripts/overlord/test_local_ci_gate_workflow_contract.py tools/local-ci-gate/local_ci_gate.py tools/local-ci-gate/bin/hldpro-local-ci
python3 scripts/overlord/test_local_ci_gate_workflow_contract.py
python3 scripts/overlord/check_local_ci_gate_workflow_contract.py
python3 scripts/knowledge_base/test_graphify_governance_contract.py
python3 scripts/knowledge_base/test_graphify_usage_logging_contract.py
python3 scripts/overlord/check_overlord_backlog_github_alignment.py
python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name feature/issue-277-local-ci-hardgate-enforcement --changed-files-file /tmp/issue-277-implementation-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope
python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-18-issue-277-local-ci-hardgate-enforcement-implementation.json --changed-files-file /tmp/issue-277-implementation-changed-files.txt
python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --report-dir cache/local-ci-gate/reports --json
git diff --check
```

Local results on 2026-04-18:

- Passed: `py_compile`.
- Passed: Local CI Gate workflow contract unit tests.
- Passed: Local CI Gate workflow contract checker.
- Passed: graphify governance contract.
- Passed: graphify usage logging contract.
- Passed: backlog/GitHub issue alignment.
- Passed: structured agent cycle plan validation for the #277 changed-file set.
- Passed: `git diff --check`.
- Blocked locally: `assert_execution_scope.py` and the live `hldpro-local-ci run` both stopped on `planner-boundary` because the operator machine had dirty forbidden sibling roots.

The local planner-boundary blocker is not pass-equivalent and is not suppressed. It is expected to clear in GitHub Actions because the workflow checkout does not include those dirty sibling worktrees.

## Follow-Up

- Add the `local-ci-gate` workflow/job as a required status through branch protection or an org/repo ruleset.
- Re-run GitHub API inspection after required-status configuration.
- Update this closeout and #277 with the exact required check name once GitHub reports it.
