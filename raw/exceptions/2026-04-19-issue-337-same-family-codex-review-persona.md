# Same-Family Exception - Issue #337 Codex Review Persona

Date: 2026-04-19
Issue: [#337](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/337)

## Exception

This implementation is planned and executed by Codex in one local session because no separate Claude connector is available in this environment and the operator directed no HITL.

## Controls

- Scope is limited to governance-owned Codex review-template support files, tests, evidence artifacts, and generated closeout artifacts.
- No downstream repository writes are permitted.
- Fake-Codex tests cover the default persona path and the `CODEX_REVIEW_PERSONA` override without consuming live model quota.
- A focused subagent review is required before closeout.
- GitHub PR checks remain the merge gate.

## Expiry

Expires when issue #337 is merged or abandoned.
