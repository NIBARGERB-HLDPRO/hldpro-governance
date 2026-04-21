# Issue #536 PDCAR: CLI Supervisor And PR Contracts

## Plan

Stabilize the governed worker/supervisor and PR completion path by tightening existing tooling instead of introducing another orchestration layer.

## Do

- Enforce Claude `--output-format stream-json` with `--verbose` in `scripts/cli_session_supervisor.py`.
- Add direct native argv tests for Claude and Codex supervisor paths.
- Require Codex native supervisor sessions to include `model_reasoning_effort`.
- Extend `scripts/overlord/automerge_policy_check.py` so pending required checks are represented as pending, not final blocked failures.
- Add merge guidance that uses GitHub-native update/merge commands instead of local `main`.
- Record session-error and self-learning evidence.

## Check

- `pytest scripts/test_cli_session_supervisor.py -q`
- `python3 -m unittest test_automerge_policy_check.py` from `scripts/overlord`
- `python3 -m py_compile scripts/cli_session_supervisor.py .github/scripts/check_codex_model_pins.py scripts/overlord/automerge_policy_check.py`
- `python3 .github/scripts/check_codex_model_pins.py`
- `python3 .github/scripts/check_agent_model_pins.py`
- Governance handoff, plan, scope, closeout, provisioning, and local-ci validators.

## Adjust

If future PR completion work needs live GitHub polling or mutation, split it into a separate issue-backed wrapper instead of expanding the dry-run evaluator into a stateful merger.

## Review

Stage 6 closeout must show that invalid Claude stream-json invocation is impossible through the governed wrapper, pending checks are not final failures, and PR merge guidance stays GitHub-native.
