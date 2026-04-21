# Issue #536 Validation: CLI Supervisor And PR Contracts

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/536
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/533
Branch: `issue-536-cli-supervisor-pr-contracts`
Date: 2026-04-21

## Scope

This slice hardened existing tooling:

- `scripts/cli_session_supervisor.py` now appends `--verbose` for Claude `--output-format stream-json`.
- Codex native supervisor paths now require `--reasoning-effort` so `codex exec` emits `model_reasoning_effort`.
- Native Claude and Codex argv construction has direct regression tests.
- `scripts/overlord/automerge_policy_check.py` now separates pending checks from final blockers and emits GitHub-native merge/update guidance.
- Model-pin checks were verified as PR-visible through existing reusable governance workflows and local coverage inventory.

## Validation

- PASS: `pytest scripts/test_cli_session_supervisor.py -q`
  - `11 passed`
- PASS: `cd scripts/overlord && python3 -m unittest test_automerge_policy_check.py`
  - `Ran 7 tests`
- PASS: `python3 -m py_compile scripts/cli_session_supervisor.py .github/scripts/check_codex_model_pins.py scripts/overlord/automerge_policy_check.py`
- PASS: `python3 .github/scripts/check_codex_model_pins.py`
- PASS: `python3 .github/scripts/check_agent_model_pins.py`
- PASS: `python3 scripts/overlord/check_workflow_local_coverage.py --root .`
- PASS: `python3 scripts/overlord/validate_handoff_package.py --root . raw/handoffs/2026-04-21-issue-536-cli-supervisor-pr-contracts.json`
- PASS: `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-536-cli-supervisor-pr-contracts --changed-files-file /tmp/issue-536-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- PASS: `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-536-cli-supervisor-pr-contracts-implementation.json --changed-files-file /tmp/issue-536-changed-files.txt --require-lane-claim`
  - Declared dirty sibling roots warned; execution scope passed with no downstream edits.
- PASS: `python3 scripts/overlord/validate_closeout.py raw/closeouts/2026-04-21-issue-536-cli-supervisor-pr-contracts.md --root .`
- PASS: `python3 scripts/overlord/validate_provisioning_evidence.py --root . --changed-files-file /tmp/issue-536-changed-files.txt`
- PASS: `git diff --check`
- PASS: `tools/local-ci-gate/bin/hldpro-local-ci --profile hldpro-governance --changed-files-file /tmp/issue-536-changed-files.txt`
  - `Verdict: PASS`; blockers 0, advisories 0.

## Acceptance Criteria Mapping

- AC1: Claude stream-json mode auto-adds `--verbose` and preserves explicit `--verbose` without duplicates.
- AC2: Native fake CLI tests cover Claude and Codex argv construction without `--command` mode.
- AC3: Codex native argv preserves `-m` and requires `model_reasoning_effort`.
- AC4: Pending required checks are represented as `state: pending`, not final blockers.
- AC5: Local-main mergeability probes are blocked; merge guidance uses `gh pr update-branch` and `gh pr merge`.
- AC6: Model-pin checks are PR-visible in `.github/workflows/governance-check.yml` and reusable model-pin workflows.
- AC7: Session error pattern evidence is recorded in `docs/FAIL_FAST_LOG.md`, `docs/ERROR_PATTERNS.md`, and operator-context self-learning evidence.

## Review And Gate Identity

- Planner: `claude-opus-4-6`, family `anthropic`, role `planner`, accepted in execution scope.
- Worker: `codex-orchestrator`, family `openai`, role `implementation`.
- Reviewer: `codex-orchestrator`, model `gpt-5.4`, family `openai`, signature date 2026-04-21, verdict `ACCEPTED`.
- Gate identity: `deterministic-local-gate`, model `pytest/unittest/py_compile/model-pin-checks`, family `deterministic`, signature date 2026-04-21.

## Residual Risk

The automerge evaluator remains a dry-run contract checker. Live polling or mutation logic should be issue-backed separately if needed; this sprint intentionally records GitHub-native command guidance rather than adding another merger.
