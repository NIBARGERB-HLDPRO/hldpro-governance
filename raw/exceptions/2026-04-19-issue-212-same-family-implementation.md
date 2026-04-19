# Issue #212 Same-Family Implementation Exception

Date: 2026-04-19
Issue: [#212](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/212)

## Exception

Planner, implementer, and local reviewer may all be Codex-family for this governance-owned implementation slice.

## Rationale

The slice is deterministic hook/rules/test work in hldpro-governance. It does not edit downstream repositories and is gated by structured plans, execution-scope validation, local tests, Local CI Gate, GitHub PR checks, and an isolated reviewer.

## Expiry

Expires: 2026-04-20T01:10:00Z

## Guardrails

- No downstream repo edits.
- No live MCP classifier deployment.
- Read-only routing must remain possible.
- Explore must stay warn-only unless a future issue proves false-positive safety.
