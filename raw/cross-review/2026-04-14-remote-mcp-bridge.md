---
schema_version: v1
pr_number: TBD
pr_scope: architecture
drafter:
  role: architect-claude
  model_id: claude-opus-4-6
  model_family: anthropic
  signature_date: 2026-04-14
reviewer:
  role: architect-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-14
  verdict: REJECTED
  round_2_status: WAIVED_BY_OPERATOR
  waiver_rule_id: SOM-RMB-ROUND2-WAIVED-001
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: false
  cross_family_independence: true
---

# Tier 1 Dual-Planner Cross-Review — Cloud → Local MCP Bridge (round 1, REJECTED)

## Subject
Plan capture: `raw/inbox/2026-04-14-remote-mcp-bridge-plan.md`

## Architect-Claude (drafter)
Initial architecture: Cloudflare Tunnel transport, bearer+JWT auth, 6/7 tools remote-exposed with `lam.scrub_pii` stdio-only, rate limits per token, JSONL audit, packet origin field, new invariant #8.

## Architect-Codex (reviewer, gpt-5.4 high) — verdict: REJECTED

### Concerns (severity-ranked)
- **CRITICAL**: origin spoofing — validator rejects remote-origin on stdio-only tools but HTTP transport doesn't stamp origin server-side; client-provided `origin: local` bypasses whitelist
- **CRITICAL**: PII floor under-enforced — whitelist hides `lam.scrub_pii` from remote but `som.handoff`, `som.chain`, `lam.embed` can still carry arbitrary PII; need app-layer PII detection/reject on all remote tools
- **HIGH**: bearer+JWT insufficient — need Cloudflare Access outer identity, full JWT claims (iss/aud/sub/exp/nbf/jti/kid/scope), hashed-at-rest, constant-time compare, rotation-invalidates-outstanding
- **HIGH**: audit tampering — JSONL editable locally; need hash chain / HMAC / daily manifest / truncation detection / CI validation
- **HIGH**: rate-limit bypass — JWT fan-out evades token-hash-keyed limits; key on stable authenticated principal
- **MEDIUM**: cloudflared failure underspecified — fail-closed + stdio continuity + no unauth fallback port
- **MEDIUM**: caller_id optional fallback to "anonymous" weakens attribution — Cloudflare Access must be mandatory or attribute as unauthenticated-metadata
- **MEDIUM**: args_hash vulnerable to confirmation attacks for small payloads — use keyed HMAC or omit for sensitive tools

### Required changes before Tier 2
(Full list preserved in the Architect-Codex review — 7 concrete requirements)

## Resolution — Architect-Claude response to REJECTED verdict

All 2 CRITICAL + 3 HIGH + 3 MEDIUM concerns addressed in revised plan capture v2. Summary:

1. **Origin spoofing (CRITICAL):** resolved — HTTP transport stamps `origin.type = remote` server-side post-authentication; client-supplied origin discarded. New invariant #9 added to STANDARDS.
2. **PII floor under-enforced (CRITICAL):** resolved — new `pii_middleware.py` scans every string field on every remote-exposed tool before dispatch; payload size limits + schema allowlists; fail-closed if pii-patterns.yml missing. New invariant #10 added.
3. **Auth too weak (HIGH):** resolved — Cloudflare Access MANDATORY as outer identity; JWT carries full claims `iss/aud/sub/exp/nbf/jti/kid/rotation_version/scope`; constant-time compare; hashed-at-rest; rotation invalidates outstanding JWTs via `rotation_version`. New invariant #11.
4. **Audit tampering (HIGH):** resolved — per-line hash chain, per-entry HMAC, daily manifest, CI validator checks schema + chain + HMACs. File permissions + append-only flag where OS supports. New invariant #12.
5. **Rate-limit bypass (HIGH):** resolved — limits keyed on JWT `sub` (stable principal), not token material; enforced pre-dispatch; fan-out under same principal shares one bucket; auth endpoint itself rate-limited.
6. **cloudflared failure (MEDIUM):** resolved — fail-closed (503 on remote, stdio continues); no unauth fallback port; launchd backoff + operator-visible log.
7. **caller_id optional (MEDIUM):** resolved — CF Access mandatory; no anonymous principals; caller_id comes from CF Access JWT assertion.
8. **args_hash weakness (MEDIUM):** resolved — keyed HMAC (`args_hmac`), key rotated with master token.

## Status

Plan round 1 REJECTED. Operator (`nibargerb`) waived round 2 re-signature on 2026-04-14 via exception `SOM-RMB-ROUND2-WAIVED-001` (docs/exception-register.md). Tier 2 Worker delegation proceeds on revised plan v2.

## Signatures
- Architect-Claude: claude-opus-4-6 · 2026-04-14 · round 1 drafted, round 2 revised
- Architect-Codex: gpt-5.4 high · 2026-04-14 · round 1 **REJECTED**; round 2 **waived by operator**
