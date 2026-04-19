# Same-Family Exception - Issue #200 Codex Fire Fail-Fast

Date: 2026-04-19
Issue: [#200](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/200)

## Exception

This implementation is planned and executed by Codex in one local session because no separate Claude connector is available in this environment and the operator directed no HITL.

## Controls

- Scope is limited to governance-owned Codex dispatcher tooling, tests, evidence artifacts, and local memory evidence.
- No downstream repository writes are permitted.
- Fake-Codex tests cover unavailable model, preflight timeout, execution failure, and success paths without consuming live model quota.
- A focused subagent review is required before closeout.
- GitHub PR checks remain the merge gate.

## Expiry

Expires when issue #200 is merged or abandoned.
