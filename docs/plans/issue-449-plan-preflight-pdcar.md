# Issue #449 PDCAR: Plan Preflight Before Code Writes

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/449
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/434
Branch: `issue-449-plan-preflight-20260421`

## Plan

Add a read-only plan preflight and stable missing-plan routing tokens so governed code/config write attempts stop at planning evidence instead of retrying alternate write paths.

## Do

Change only governance repository surfaces:

- `hooks/code-write-gate.sh`
- `hooks/schema-guard.sh`
- `scripts/overlord/check_plan_preflight.py`
- `scripts/overlord/test_check_plan_preflight.py`
- `scripts/overlord/test_schema_guard_hook.py`
- issue #449 planning, scope, handoff, worker prompt, review, validation, and closeout evidence
- backlog/progress mirrors

## Check

Required validation:

- `python3 scripts/overlord/test_check_plan_preflight.py`
- `python3 scripts/overlord/test_schema_guard_hook.py`
- `python3 -m py_compile scripts/overlord/check_plan_preflight.py`
- `bash -n hooks/code-write-gate.sh`
- `bash -n hooks/schema-guard.sh`
- `python3 scripts/overlord/test_validate_handoff_package.py`
- `python3 scripts/overlord/validate_handoff_package.py --root .`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-449-plan-preflight-20260421 --require-if-issue-branch`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-449-plan-preflight-implementation.json --require-lane-claim`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`

## Act

If validation and Codex QA pass, close issue #449 through PR and continue the #434 child issue loop.

## Review Notes

Codex remains orchestrator/QA. Sonnet 4.6 is assigned the bounded Worker implementation slice through the supervised CLI path; if it is unavailable, stalls, or makes no scoped edits, Codex records the deviation and completes the issue under QA.
