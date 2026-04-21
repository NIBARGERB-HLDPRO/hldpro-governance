# Issue #437 PDCAR: Packet Dispatch Reconciliation

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/437
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/434
Branch: `issue-437-packet-dispatch-reconcile-20260421`

## Plan

Reconcile the SoM packet schema, packet emitter, packet validator, and orchestrator queue so there is one clear packet lifecycle:

- `docs/schemas/som-packet.schema.yml` remains the canonical packet schema.
- Minimal historical packets remain schema-valid.
- Dispatch-ready packets carry an optional `governance` block with issue, plan, scope, validation, review, fallback, PII, and authorization metadata.
- `scripts/orchestrator/packet_queue.py` remains the dispatch hardgate and refuses schema-valid packets that lack complete dispatch governance metadata.
- Focused tests prove emitter creation, schema validation, queue refusal for missing governance, and historical compatibility.

## Do

Change only governance repository surfaces:

- `docs/schemas/som-packet.schema.yml`
- `scripts/packet/emit.py`
- `scripts/packet/test_emit.py`
- `scripts/packet/test_validate.py`
- `scripts/orchestrator/test_packet_queue.py`
- Issue #437 plan, execution-scope, handoff, review, validation, and closeout artifacts.
- Backlog/progress mirrors for completed #435 and active #437.

## Check

Required validation:

- `python3 -m json.tool docs/plans/issue-437-structured-agent-cycle-plan.json`
- `python3 -m json.tool raw/execution-scopes/2026-04-21-issue-437-packet-dispatch-reconcile-implementation.json`
- `python3 -m json.tool raw/handoffs/2026-04-21-issue-437-plan-to-implementation.json`
- `python3.11 scripts/packet/test_emit.py`
- `python3.11 scripts/packet/test_validate.py`
- `python3.11 scripts/orchestrator/test_packet_queue.py`
- `python3.11 -m py_compile scripts/packet/emit.py scripts/packet/validate.py scripts/orchestrator/packet_queue.py`
- `python3 scripts/overlord/test_validate_handoff_package.py`
- `python3 scripts/overlord/validate_handoff_package.py --root .`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-437-packet-dispatch-reconcile-20260421 --require-if-issue-branch`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-437-packet-dispatch-reconcile-implementation.json --require-lane-claim`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`

## Act

If validation and alternate-family review pass, close issue #437 through PR and continue the epic sequence with issue #436 PR/closeout hardening.

## Review Notes

The initial Claude Sonnet 4.6 worker attempt hung without returning a summary. It left bounded packet/schema/test edits in the issue worktree before the process was killed. Codex continued as orchestrator/QA, reviewed the partial worker edits, added the missing CLI positive coverage and issue evidence, and will rely on alternate-family review plus deterministic gates before merge.
