# Issue #445 PDCAR: Repo-Specific Lane Bootstrap Naming

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/445
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/434
Branch: `issue-445-lane-bootstrap-20260421`

## Plan

Add a governance-owned lane policy layer and bootstrap helper so repo-specific branch/worktree naming is generated and validated before issue-lane filesystem side effects.

## Do

Change only governance repository surfaces:

- `docs/lane_policies.json`
- `docs/runbooks/org-repo-intake.md`
- `hooks/branch-switch-guard.sh`
- `scripts/overlord/lane_bootstrap.py`
- `scripts/overlord/test_lane_bootstrap.py`
- `scripts/overlord/test_branch_switch_guard.py`
- issue #445 planning, scope, handoff, review, validation, and closeout evidence
- backlog/progress mirrors

## Check

Required validation:

- `python3 scripts/overlord/test_lane_bootstrap.py`
- `python3 scripts/overlord/test_branch_switch_guard.py`
- `python3 -m py_compile scripts/overlord/lane_bootstrap.py`
- `bash -n hooks/branch-switch-guard.sh`
- `python3 -m json.tool docs/lane_policies.json`
- `python3 scripts/overlord/test_validate_handoff_package.py`
- `python3 scripts/overlord/validate_handoff_package.py --root .`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-445-lane-bootstrap-20260421 --require-if-issue-branch`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-445-lane-bootstrap-implementation.json --require-lane-claim`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`

## Act

If validation and Codex QA pass, close issue #445 through PR and continue the #434 child issue loop.

## Review Notes

Codex remains orchestrator/QA. Sonnet worker execution was not used for this small guard-policy slice after prior supervised Sonnet timeouts; Codex records this as a material deviation and keeps the implementation tightly scoped with deterministic tests.
