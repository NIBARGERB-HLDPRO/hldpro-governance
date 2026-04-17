# Issue #229 — Packet Queue and Controlled Orchestration PDCA/R

## Plan

Issue #229 adds the filesystem packet queue needed by epic #224 without executing packets or granting autonomous write authority. The queue must keep packet movement deterministic, audited, replayable, and blocked behind issue-backed structured plan approval.

## Do

- Extend `docs/schemas/som-packet.schema.yml` with optional governance dispatch metadata.
- Add `scripts/orchestrator/packet_queue.py` for queue initialization, dry-run and real state transitions, dispatch validation, and audit replay.
- Add packet queue tests under `scripts/orchestrator/test_packet_queue.py`.
- Extend governance-surface planning classification to cover packet queue paths.
- Update feature, service, and data dictionary docs with the packet queue contract.

## Check

Planned validation:

- `python3 scripts/packet/test_validate.py`
- `python3 scripts/orchestrator/test_packet_queue.py`
- `python3 scripts/overlord/test_validate_structured_agent_cycle_plan.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-229-packet-queue-20260417 --changed-files-file /tmp/issue-229-changed-files.txt --enforce-governance-surface`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-229-packet-queue-20260417 --require-if-issue-branch`
- `python3 -m py_compile scripts/orchestrator/packet_queue.py scripts/orchestrator/test_packet_queue.py scripts/packet/validate.py scripts/overlord/validate_structured_agent_cycle_plan.py scripts/overlord/test_validate_structured_agent_cycle_plan.py`
- `python3 .github/scripts/check_codex_model_pins.py`
- `python3 .github/scripts/check_agent_model_pins.py`
- `python3 scripts/knowledge_base/test_graphify_governance_contract.py`
- `python3 scripts/overlord/build_org_governance_compendium.py --check`

## Adjust

Dispatch controls are implemented as a stricter queue-layer contract while the schema extension remains optional. That preserves existing stage-4 packet compatibility and lets only queue-dispatched packets require the full issue, plan, scope, validation, review, fallback, PII, and authorization metadata set.

## Review

Alternate-family review is recorded in `raw/cross-review/2026-04-17-packet-queue.md`.
