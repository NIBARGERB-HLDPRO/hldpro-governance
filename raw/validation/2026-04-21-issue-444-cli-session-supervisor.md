# Issue #444 Validation: CLI Session Supervisor

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/444
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/434
Branch: `issue-444-cli-session-supervisor-20260421`
Date: 2026-04-21

## Worker Handoff

- Claude Sonnet 4.6 worker handoff attempted through `claude -p --model claude-sonnet-4-6 --permission-mode bypassPermissions`.
- Result: unavailable timeout with no implementation edits after prolonged silence.
- Action: Codex implemented and QA'd the approved issue #444 scope under the material deviation rule in `docs/plans/issue-444-structured-agent-cycle-plan.json`.

## Validation

- PASS: `pytest scripts/test_cli_session_supervisor.py -q`
  - `7 passed in 2.58s`
- PASS: `python3 -m py_compile scripts/cli_session_supervisor.py .github/scripts/check_codex_model_pins.py`
- PASS: `bash -n scripts/codex-review-template.sh scripts/codex-fire.sh`
- PASS: `python3 -m json.tool docs/schemas/cli-session-event.schema.json`
- PASS: `python3 .github/scripts/check_codex_model_pins.py`
- PASS: `python3 scripts/overlord/test_validate_handoff_package.py`
  - `Ran 10 tests`
- PASS: `python3 scripts/overlord/validate_handoff_package.py --root .`
  - `PASS validated 6 package handoff file(s)`
- PASS: `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-444-cli-session-supervisor-20260421 --require-if-issue-branch`
  - `PASS validated 108 structured agent cycle plan file(s)`
- PASS: `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-444-cli-session-supervisor-implementation.json --require-lane-claim`
  - Declared dirty sibling roots warned; execution scope passed with no downstream edits.
- PASS: `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- PASS: `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`
  - Verdict: `PASS`
  - Report: `cache/local-ci-gate/reports/20260421T160441Z-hldpro-governance-git`

## Acceptance Criteria Mapping

- CLI session event contract added at `docs/schemas/cli-session-event.schema.json`.
- Supervisor added at `scripts/cli_session_supervisor.py` with stdout/stderr capture, wall timeout, silence timeout, process-group cleanup, event JSONL output, and one explicit retry when a retry prompt is supplied.
- `scripts/codex-review-template.sh claude` now routes through the supervisor with explicit model, permission mode, max turns, no session persistence, and bounded budget.
- Guard coverage in `.github/scripts/check_codex_model_pins.py` now reports direct `claude -p` calls in scripts/workflows unless allowlisted.
- Fake CLI tests cover success, nonzero failure, silent stall, intermittent output, total timeout, retry once, and max-retry halt.
