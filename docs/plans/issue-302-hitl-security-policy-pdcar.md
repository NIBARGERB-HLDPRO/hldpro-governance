# PDCAR: HITL Relay Security And Data-Handling Policy

Date: 2026-04-18
Repo: `hldpro-governance`
Branch: `issue-302-hitl-security-policy`
Issue: [#302](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/302)
Parent epic: [#296](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/296)
Status: IMPLEMENTATION_READY
Canonical plan: `docs/plans/issue-302-structured-agent-cycle-plan.json`

## Problem

The HITL relay will send operator prompts and receive replies through AIS-backed channels. Before validators, AIS, MCP, or CLI adapters use that path, the system needs explicit data-handling rules for minimization, redaction, retention, sender verification, replay protection, token scope, and PII/channel behavior.

## Plan

Add a governance-owned policy runbook that downstream implementation slices must cite and enforce.

## Do

- Add `docs/runbooks/hitl-relay-security.md`.
- Define classification and channel rules.
- Define minimization and redaction requirements.
- Define raw message retention/deletion and audit reference rules.
- Define sender verification, replay, duplicate, expiration, and token scope requirements.

## Check

- `python3 -m json.tool docs/plans/issue-302-structured-agent-cycle-plan.json`
- Structured-plan governance gate.
- Planner-boundary execution-scope gate.
- Local CI Gate.

## Act

If AIS, MCP, validator, or session-adapter slices find policy gaps, update this runbook through issue-backed policy changes before enabling the affected path.

## Review

Same-family exception is recorded for this no-HITL policy slice. Later runtime and transport slices still need their own review evidence.

## Acceptance Criteria

- [ ] Policy states what data may leave local control for each classification and channel.
- [ ] Policy requires redaction or summary minimization before AIS receives HITL notification content when source artifacts may contain sensitive data.
- [ ] Policy defines raw message retention/deletion and audit-reference rules.
- [ ] Policy defines sender verification, webhook signature, replay, duplicate, and expiration requirements.
- [ ] Policy defines token/secret scope expectations.
- [ ] Policy states PII-tagged or PII-detected packets fail closed unless a local-only route is explicitly available.
