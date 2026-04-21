# Issue #436 PDCAR: PR and Closeout Handoff Evidence Gates

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/436
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/434
Branch: `issue-436-pr-closeout-handoff-gates-20260421`

## Plan

Harden the final human-facing surfaces in the structured handoff package lifecycle:

- Update the PR template so every PR asks for structured plan, execution scope, handoff package, validation, review/gate, Local CI, closeout, and packet queue state evidence.
- Update the closeout template so the required evidence is visible before Stage 6.
- Add a deterministic closeout validator and run it inside `hooks/closeout-hook.sh` before graph/wiki refresh.
- Validate referenced plan/scope/handoff/validation/review/gate artifacts exist.
- Refuse closeouts whose residual risks or follow-ups are not issue-backed or explicitly none.
- Require closeouts that reference handoff packages to record or validate accepted/released lifecycle.

## Do

Change only governance repository surfaces:

- `.github/pull_request_template.md`
- `hooks/closeout-hook.sh`
- `raw/closeouts/TEMPLATE.md`
- `scripts/overlord/validate_closeout.py`
- `scripts/overlord/test_validate_closeout.py`
- Issue #436 plan, execution-scope, handoff, review, validation, and closeout artifacts.
- Backlog/progress mirrors for completed #437 and active #436.

## Check

Required validation:

- `python3 -m json.tool docs/plans/issue-436-structured-agent-cycle-plan.json`
- `python3 -m json.tool raw/execution-scopes/2026-04-21-issue-436-pr-closeout-handoff-gates-implementation.json`
- `python3 -m json.tool raw/handoffs/2026-04-21-issue-436-plan-to-implementation.json`
- `python3 scripts/overlord/test_validate_closeout.py`
- `python3 -m py_compile scripts/overlord/validate_closeout.py`
- `bash -n hooks/closeout-hook.sh`
- `python3 scripts/overlord/test_validate_handoff_package.py`
- `python3 scripts/overlord/validate_handoff_package.py --root .`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-436-pr-closeout-handoff-gates-20260421 --require-if-issue-branch`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-436-pr-closeout-handoff-gates-implementation.json --require-lane-claim`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`

## Act

If validation and alternate-family review pass, close issue #436 through PR. After merge, review epic #434 for closeout readiness.

## Review Notes

The bounded Claude Sonnet 4.6 worker attempt hung without output and was killed after roughly two minutes. It left no file changes. Codex continued as orchestrator/QA and recorded the worker fallback in the handoff evidence.
