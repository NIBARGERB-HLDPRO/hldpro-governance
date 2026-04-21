# Issue #444 PDCAR: CLI Session Supervisor

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/444
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/434
Branch: `issue-444-cli-session-supervisor-20260421`

## Plan

Add a governed runtime supervisor for called Claude/Codex CLI subprocesses so silent stalls and total runtime overruns produce structured evidence instead of hanging worker lanes.

## Do

Change only governance repository surfaces:

- `docs/schemas/cli-session-event.schema.json`
- `scripts/cli_session_supervisor.py`
- `scripts/test_cli_session_supervisor.py`
- `scripts/codex-review-template.sh`
- `.github/scripts/check_codex_model_pins.py`
- issue #444 planning, scope, handoff, review, validation, and closeout evidence
- backlog/progress mirrors

## Check

Required validation:

- `pytest scripts/test_cli_session_supervisor.py -q`
- `python3 -m py_compile scripts/cli_session_supervisor.py .github/scripts/check_codex_model_pins.py`
- `bash -n scripts/codex-review-template.sh scripts/codex-fire.sh`
- `python3 .github/scripts/check_codex_model_pins.py`
- `python3 scripts/overlord/test_validate_handoff_package.py`
- `python3 scripts/overlord/validate_handoff_package.py --root .`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-444-cli-session-supervisor-20260421 --require-if-issue-branch`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-444-cli-session-supervisor-implementation.json --require-lane-claim`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`

## Act

If validation and alternate-family review pass, close issue #444 through PR and continue the #434 follow-up loop.

## Review Notes

Codex remains orchestrator/QA. A bounded Sonnet worker handoff was attempted for the implementation files, but the Claude Sonnet 4.6 CLI session produced no output for multiple minutes and was killed with no edits. Codex implemented the approved scope under the plan's material deviation rule and retained the Sonnet timeout as evidence.
