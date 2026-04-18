# PDCAR: Queue-First HITL Relay Prototype

Date: 2026-04-18
Repo: `hldpro-governance`
Branch: `issue-301-hitl-queue-prototype`
Issue: [#301](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/301)
Parent epic: [#296](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/296)
Status: IMPLEMENTATION_READY
Canonical plan: `docs/plans/issue-301-structured-agent-cycle-plan.json`

## Problem

The HITL relay has packet contracts, policy, and validators, but downstream AIS/MCP/session-adapter work needs a local queue-first proof that request, response, decision, instruction, resume, dead-letter, and audit behavior is enforceable before live messaging or terminal control exists.

## Plan

Add a governance-owned local queue prototype under `scripts/orchestrator/` that builds HITL request packets from local CLI checkpoint fixtures, processes verified local response fixtures, emits bounded session instructions or resume packets, and dead-letters invalid paths with explicit validation errors.

## Do

- Add `scripts/orchestrator/hitl_relay_queue.py`.
- Add focused queue tests for approval, request-changes, ambiguity, stale session, invalid duplicate/expired responses, and replay.
- Document the queue surface in schema, feature registry, and data dictionary docs.
- Record cross-review and same-family/no-HITL exception evidence.

## Check

- `python3 -m pytest scripts/orchestrator/test_hitl_relay_queue.py scripts/packet/test_validate_hitl_relay.py`
- Structured-plan governance gate.
- Planner-boundary execution-scope gate.
- Local CI Gate.

## Act

Downstream AIS/MCP/local CLI adapter slices must consume this queue contract instead of bypassing validation or writing directly to session control surfaces.

## Review

Subagent cross-review accepted the placement and reuse of existing queue patterns with follow-up boundaries for transport/runtime work. Same-family/no-HITL exception is recorded for this deterministic implementation slice.

## Acceptance Criteria

- [ ] A local CLI checkpoint fixture creates a valid HITL request packet.
- [ ] A valid local approval response fixture produces a bounded session instruction packet.
- [ ] A request-changes response fixture preserves feedback without treating it as approval.
- [ ] An ambiguous response fixture produces a clarification request and no instruction packet.
- [ ] A stale-session fixture produces a resume packet instead of targeting another session.
- [ ] Queue transitions are auditable and replayable.
- [ ] Invalid packets land in dead-letter or fail with explicit validation errors.
- [ ] Dry-run queue tests cover approval, request-changes, ambiguity, stale session, and dead-letter behavior.
- [ ] Replay test reconstructs the decision path from request, response, normalized decision, validation, and instruction evidence.
- [ ] Local CI Gate passes.
