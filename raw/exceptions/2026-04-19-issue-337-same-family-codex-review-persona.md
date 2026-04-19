# Same-Family Exception - Issue #337 Codex Review Default Persona

Date: 2026-04-19
Issue: [#337](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/337)

## Exception

This implementation is planned and executed by Codex in one local session because the operator directed no HITL.

## Controls

- Scope is limited to governance-owned Codex review template support, tests, evidence artifacts, and local mirrors.
- No downstream repository writes are permitted.
- Fake-Codex tests prove the default persona path reaches `scripts/codex-fire.sh` without consuming live model quota.
- Existing override behavior remains under regression coverage.
- A focused review artifact is required before closeout.
- GitHub PR checks remain the merge gate.

## Expiry

Expires when issue #337 is merged or abandoned.
