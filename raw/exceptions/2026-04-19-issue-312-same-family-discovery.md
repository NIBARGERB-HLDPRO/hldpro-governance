# Issue #312 Same-Family Discovery Exception

Date: 2026-04-19
Issue: [#312](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/312)
Parent epic: [#298](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/298)

## Exception

Planner and implementer are both Codex-family for this dispatcher-side discovery/classification slice.

## Rationale

The slice is bounded to governance repository metadata, planning, validation, and registry files plus GitHub issue creation. It does not edit `EmailAssistant` source or governance files. A spawned read-only subagent independently reviewed the downstream repo state and classification decision.

## Expiry

Expires: 2026-04-20T00:30:00Z

## Guardrails

- No downstream EmailAssistant file edits.
- Downstream implementation must be issue-backed by `EmailAssistant#1` or a later repo-local issue.
- Final acceptance requires live org inventory and registry validation.
