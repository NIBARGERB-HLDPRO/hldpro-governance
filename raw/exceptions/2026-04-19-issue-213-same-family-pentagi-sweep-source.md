# Same-Family Exception - Issue #213 PentAGI Sweep Source

Date: 2026-04-19
Issue: [#213](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/213)

## Exception

This implementation is planned and executed by Codex in one local session because no separate Claude connector is available in this environment.

## Controls

- Scope is limited to governance-owned sweep tooling, tests, workflow wiring, and evidence artifacts.
- No downstream repository writes are permitted.
- Regression tests cover the bug class directly.
- A focused subagent review is required before closeout.
- GitHub PR checks remain the merge gate.

## Expiry

Expires when issue #213 is merged or abandoned.
