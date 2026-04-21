# Issue #447 Validation: Schema Guard Diagnostics

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/447
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/434
Branch: `issue-447-schema-guard-diagnostics-20260421`
Date: 2026-04-21

## Worker Handoff

- The immediately prior supervised Claude Sonnet 4.6 worker handoff for issue #448 exited at max turns with no edits.
- Action: Codex implemented and QA'd this small diagnostics slice under the material deviation rule in `docs/plans/issue-447-structured-agent-cycle-plan.json`.

## Validation

- PASS: `python3 scripts/overlord/test_schema_guard_hook.py`
  - `Ran 6 tests`
- PASS: `bash -n hooks/schema-guard.sh`
- PASS: `python3 scripts/overlord/test_branch_switch_guard.py`
  - `Ran 6 tests`
- PASS: `python3 scripts/overlord/test_validate_handoff_package.py`
  - `Ran 10 tests`
- PASS: `python3 scripts/overlord/validate_handoff_package.py --root .`
  - `PASS validated 8 package handoff file(s)`
- PASS: `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-447-schema-guard-diagnostics-20260421 --require-if-issue-branch`
  - `PASS validated 110 structured agent cycle plan file(s)`
- PASS: `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-447-schema-guard-diagnostics-implementation.json --require-lane-claim`
  - Declared dirty sibling roots warned; execution scope passed with no downstream edits.
- PASS: `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`
  - Verdict: `PASS`
  - Report: `cache/local-ci-gate/reports/20260421T162852Z-hldpro-governance-git`

## Acceptance Criteria Mapping

- `hooks/schema-guard.sh` now has explicit stderr diagnostics through `fail()`.
- Unexpected hook failures are trapped with hook name, phase, line, and command context.
- Policy block fixture emits blocked target, rule, and next action.
- Missing schema/config and validator nonzero fixtures emit explicit stderr summaries.
- Read-only Bash fixture remains allowed.
- No product repository edits were made.
