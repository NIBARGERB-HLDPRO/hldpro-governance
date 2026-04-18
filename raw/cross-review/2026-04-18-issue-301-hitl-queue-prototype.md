# Cross-Review: Issue #301 Queue-First HITL Relay Prototype

Date: 2026-04-18
Issue: [#301](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/301)
Parent epic: [#296](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/296)
Reviewer: Dewey subagent
Status: ACCEPTED_WITH_FOLLOWUP

## Findings

- Reuse `scripts/orchestrator/packet_queue.py` patterns for temp-file-then-rename writes and replayable JSONL audit events.
- Place the local HITL queue prototype under `scripts/orchestrator/`, next to the existing queue orchestrator.
- Keep runtime daemon, AIS transport, and local CLI control out of this repo slice.
- Add issue-backed governance artifacts for #301: structured plan, PDCAR, execution scope, and same-family/no-HITL exception evidence.

## Implementation Response

The #301 implementation adds `scripts/orchestrator/hitl_relay_queue.py` and focused tests under `scripts/orchestrator/test_hitl_relay_queue.py`. The queue writes local HITL request, response, normalized decision, session instruction, session resume, dead-letter, and audit artifacts under `raw/hitl-relay/queue/` using atomic JSON writes. It validates every emitted packet with `scripts/packet/validate_hitl_relay.py`.

## Follow-Up Boundaries

- AIS bridge transport remains tracked by `NIBARGERB-HLDPRO/ai-integration-services#1144`.
- MCP orchestrator and local CLI adapter work remain tracked by `NIBARGERB-HLDPRO/local-ai-machine#462` and `#463`.
- Final cross-repo E2E proof remains tracked by #303.
