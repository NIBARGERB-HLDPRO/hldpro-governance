# Same-Family Implementation Exception: Issue #301

Date: 2026-04-18
Issue: [#301](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/301)
Parent epic: [#296](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/296)
Scope: Queue-first HITL relay prototype
Expires: 2026-04-19T23:33:18Z

## Reason

The operator instructed this session to continue with no HITL. This slice implements a deterministic local queue prototype and tests only. It does not implement AIS transport, MCP runtime behavior, live SMS/Slack parsing, or local terminal/session control.

## Controls

- A subagent cross-review checked the intended placement and patterns before implementation.
- The prototype validates every emitted HITL packet through the deterministic #300 validator.
- Tests cover approval, request-changes, clarification, stale-session resume, duplicate/expired dead-letter, and audit replay paths.
- Parent epic #296 remains open for downstream runtime and final E2E proof.
