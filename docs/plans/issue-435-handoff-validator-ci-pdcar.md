# Issue #435 PDCAR: Handoff Validator CI Enforcement

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/435
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/434
Branch: `issue-435-handoff-validator-ci-20260421`

## Plan

Wire the package handoff validator from issue #438 into the existing governance enforcement paths:

- Local CI Gate profile runs `scripts/overlord/validate_handoff_package.py --root .` when handoff-relevant artifacts change.
- Reusable `governance-check.yml` runs the same validator for handoff-relevant diffs and fails closed if the validator is unavailable.
- GitHub planner-boundary scope assertion passes `--require-lane-claim` for implementation scopes.
- Local profile tests prove trigger/skip behavior.

## Do

Change only governance repository surfaces:

- `.github/workflows/governance-check.yml`
- `tools/local-ci-gate/profiles/hldpro-governance.yml`
- `tools/local-ci-gate/tests/test_local_ci_gate.py`
- `docs/workflow-local-coverage-inventory.json`
- Issue #435 plan, execution-scope, handoff, review, validation, and closeout artifacts.
- Backlog/progress mirrors for #435 and completed #438.

## Check

Required validation:

- `python3 -m json.tool docs/plans/issue-435-structured-agent-cycle-plan.json`
- `python3 -m json.tool raw/execution-scopes/2026-04-21-issue-435-handoff-validator-ci-implementation.json`
- `python3 -m json.tool raw/handoffs/2026-04-21-issue-435-plan-to-implementation.json`
- `python3 scripts/overlord/test_validate_handoff_package.py`
- `python3 scripts/overlord/validate_handoff_package.py --root .`
- `python3 tools/local-ci-gate/tests/test_local_ci_gate.py`
- `python3 scripts/overlord/test_workflow_local_coverage.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-435-handoff-validator-ci-20260421 --require-if-issue-branch`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-435-handoff-validator-ci-implementation.json --require-lane-claim`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`

## Act

If validation passes, close issue #435 through PR and continue the epic sequence with #437 packet/schema reconciliation, then #436 closeout/PR hardening.

## Review Notes

Codex attempted a bounded Sonnet 4.6 worker handoff through the local Claude CLI, but the process hung without output and was killed before it changed files. Codex continued as orchestrator/QA and did not claim Sonnet-authored implementation for this slice.
