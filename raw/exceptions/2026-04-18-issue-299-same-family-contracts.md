# Same-Family Implementation Exception: Issue #299

Date: 2026-04-18
Issue: [#299](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/299)
Parent epic: [#296](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/296)
Scope: HITL relay packet contracts
Expires: 2026-04-19T23:13:15Z

## Reason

The operator instructed this session to continue with no HITL. This slice is limited to governance schema contracts, fixtures, docs, tests, and scope artifacts. It does not implement AIS transport, MCP runtime behavior, local CLI adapters, or sibling repo changes.

## Controls

- Runtime and transport behavior remain out of scope.
- Raw external message bodies must not be accepted in executable packet shapes.
- Final E2E proof remains tracked separately by issue #303.
- Parent epic #296 remains open.
