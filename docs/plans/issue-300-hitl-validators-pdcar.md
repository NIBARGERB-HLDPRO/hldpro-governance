# PDCAR: HITL Relay Validators And Policy Gates

Date: 2026-04-18
Repo: `hldpro-governance`
Branch: `issue-300-hitl-validators`
Issue: [#300](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/300)
Parent epic: [#296](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/296)
Status: IMPLEMENTATION_READY
Canonical plan: `docs/plans/issue-300-structured-agent-cycle-plan.json`

## Problem

The HITL relay has packet contracts and security policy, but downstream queue, AIS, MCP, and session adapter work needs deterministic validators that fail closed before notification or instruction dispatch.

## Plan

Add `scripts/packet/validate_hitl_relay.py` and focused tests that enforce schema, correlation, operator provenance, confidence, stale-session, duplicate/replay/expired, and PII/channel policy gates.

## Do

- Add the validator.
- Add tests for valid examples and negative controls.
- Update the schema to allow duplicate/replayed/expired metadata on inbound replies.
- Document validator responsibilities.

## Check

- `python3 -m pytest scripts/packet/test_validate_hitl_relay.py`
- `python3 -m pytest scripts/packet/test_hitl_relay_schema.py`
- Structured-plan governance gate.
- Planner-boundary execution-scope gate.
- Local CI Gate.

## Act

If later slices need more runtime metadata, update the schema/validator through issue-backed contract changes before enabling the affected path.

## Review

Same-family exception is recorded for this no-HITL deterministic validator slice. Runtime and transport slices still need their own review evidence.

## Acceptance Criteria

- [ ] Invalid HITL request/response/instruction packets fail before notification or instruction dispatch.
- [ ] Self-approval/provenance gaps are refused by requiring verified operator provenance for approval-like actions.
- [ ] Ambiguous/low-confidence replies cannot produce executable instructions.
- [ ] PII-sensitive packets fail closed for external channels.
- [ ] Stale sessions require resume packets.
- [ ] Duplicate/replayed/expired replies cannot produce instructions.
