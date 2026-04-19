# Same-Family Implementation Exception: Issue #310

Date: 2026-04-18
Issue: [#310](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/310)
Parent epic: [#298](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/298)

## Context

The planner and implementer are both Codex/GPT-5 family in this local session. The work is still implementation-ready because the scope is narrow, issue-backed, and constrained to registry schema enforcement in governance.

## Compensating Controls

- Alternate-family review is required before merge because this slice changes governance policy semantics.
- The execution scope restricts writes to #310 schema, validator, tests, planning, and status artifacts.
- `seek-and-ponder` and `EmailAssistant` intake are explicitly out of scope.
- Final e2e proof must include validator tests, real registry validation, live org inventory warn-only output, Local CI Gate, backlog sync, and diff hygiene.

## Expiry

This exception expires at 2026-04-19T23:55:00Z or when the #310 PR merges, whichever comes first.
