# Issue #447 PDCAR: Schema Guard Diagnostics

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/447
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/434
Branch: `issue-447-schema-guard-diagnostics-20260421`

## Plan

Add a repo-owned Bash schema guard that fails loud with actionable stderr diagnostics for policy blocks, malformed payloads, missing schema/config, validator failures, and unexpected internal errors.

## Do

Change only governance repository surfaces:

- `.claude/settings.json`
- `hooks/schema-guard.sh`
- `scripts/overlord/test_schema_guard_hook.py`
- issue #447 planning, scope, handoff, review, validation, and closeout evidence
- backlog/progress mirrors

## Check

Required validation:

- `python3 scripts/overlord/test_schema_guard_hook.py`
- `bash -n hooks/schema-guard.sh`
- `python3 scripts/overlord/test_branch_switch_guard.py`
- `python3 scripts/overlord/test_validate_handoff_package.py`
- `python3 scripts/overlord/validate_handoff_package.py --root .`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-447-schema-guard-diagnostics-20260421 --require-if-issue-branch`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-447-schema-guard-diagnostics-implementation.json --require-lane-claim`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`

## Act

If validation and Codex QA pass, close issue #447 through PR and continue the #434 child issue loop.

## Review Notes

Codex remains orchestrator/QA. The Sonnet worker handoff was attempted for the prior #448 slice and failed at max turns without edits; for this slice Codex implements directly under the established material deviation pattern while preserving required evidence.
