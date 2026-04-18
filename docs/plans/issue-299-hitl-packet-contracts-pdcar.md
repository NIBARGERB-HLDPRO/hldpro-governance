# PDCAR: HITL Relay Packet Contracts

Date: 2026-04-18
Repo: `hldpro-governance`
Branch: `issue-299-hitl-packet-contracts`
Issue: [#299](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/299)
Parent epic: [#296](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/296)
Status: IMPLEMENTATION_READY
Canonical plan: `docs/plans/issue-299-structured-agent-cycle-plan.json`

## Problem

The HITL relay epic needs a stable packet contract before validators, AIS transport, MCP orchestration, or local CLI adapters can safely depend on it. Without a contract, external replies could be confused with executable instructions, session identity could be lost, and final E2E audit replay would be weak.

## Plan

Add a governance-owned JSON schema for HITL relay packets, valid and invalid examples, and focused tests proving the contract accepts expected packet types and rejects unsafe shapes.

## Do

- Add `docs/schemas/hitl-relay-packet.schema.json`.
- Add valid examples for HITL request, session instruction, and session resume packets.
- Add invalid examples for raw message body and missing provenance cases.
- Add a focused schema test under `scripts/packet/`.
- Document the schema in `docs/schemas/README.md`.

## Check

- `python3 -m json.tool docs/schemas/hitl-relay-packet.schema.json`
- `python3 -m pytest scripts/packet/test_hitl_relay_schema.py`
- Structured-plan governance gate.
- Planner-boundary execution-scope gate.
- Local CI Gate.

## Act

If schema tests reveal ambiguity, revise the contract before any runtime validator issue starts. If a future implementation needs a field not represented here, update the schema through an issue-backed contract-change slice.

## Review

Same-family exception is recorded for this no-HITL schema contract slice. Runtime, AIS, MCP, and final E2E slices still require their own review evidence.

## Acceptance Criteria

- [ ] Schema defines all packet types required by issue #299.
- [ ] Valid fixtures pass schema validation.
- [ ] Invalid fixtures fail schema validation.
- [ ] Raw message bodies are rejected by schema shape.
- [ ] Session instruction packets require normalized decision and audit references.
- [ ] Contract records request/session/notification/response correlation fields needed by final #296 E2E proof.
