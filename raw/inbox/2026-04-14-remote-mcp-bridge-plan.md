---
date: 2026-04-14
captured_by: claude-opus-4-6
type: epic-plan
status: revised-round2-waived-implementation-in-progress
depends_on: society-of-minds-epic (shipped)
parent_repo: local-ai-machine (services/som-mcp/)
cross_review_round_1: REJECTED (gpt-5.4 high)
cross_review_round_2_status: waived-by-operator-2026-04-14 (SOM-RMB-ROUND2-WAIVED-001)
---

# Epic — Cloud → Local MCP Bridge (v2, post-Codex-review revision)

Expose the Society-of-Minds local MCP daemon to remote Claude Code / Codex / CLI sessions via an authenticated HTTPS tunnel. All Tier-1 Round-1 gpt-5.4-high concerns addressed. Operator waived Round-2 re-signature (exception `SOM-RMB-ROUND2-WAIVED-001`).

## Goals (unchanged)

1. Remote CLI sessions invoke a bounded subset of local MCP tools via HTTPS.
2. Zero PII crosses the network — enforced at 3 layers (transport, app middleware, validator).
3. Audit-complete with tamper-evident hash chain.
4. Reproducible: launchd tunnel + daemon; one-command install; fail-closed on tunnel down.

## Revised architecture

### Transport

- **Cloudflare Tunnel (`cloudflared`)** — persistent URL via Cloudflare.
- **Cloudflare Access is MANDATORY** — outer identity layer. No anonymous calls permitted. Every request must carry `Cf-Access-Jwt-Assertion` header, validated against Access policy.
- **Fail-closed:** if `cloudflared` down → remote endpoint simply unreachable. stdio path on `localhost:8080` remains unaffected. No unauthenticated fallback port. Launchd restart with exponential backoff + operator-visible failure log.

### Auth (revised)

Two-layer:
- **Outer:** Cloudflare Access JWT (CF handles identity, service token or SSO).
- **Inner:** bridge-issued JWT with full claims:
  ```
  iss: "som-mcp-bridge@<machine-id>"
  aud: "som-mcp"
  sub: <stable principal id, derived from CF Access email/service-token-id>
  exp: now + 1h
  nbf: now
  jti: uuid4 (per-session)
  kid: <key id for rotation>
  rotation_version: <int; bumped on master-token rotation; invalidates outstanding JWTs with lower version>
  scope: <explicit tool list the session may call>
  ```
- **Secrets at rest:** master token stored as sha256 hash only. Comparison via `hmac.compare_digest`. JWT signing key in Keychain / `.som-mcp/signing.key` mode 0600.
- **Rotation:** `rotate-token.sh` bumps `rotation_version` in daemon config → all outstanding JWTs invalidated on next validate. Rate-limit the auth endpoint (`som.auth.begin`) to 10/min per principal to prevent token-issuance abuse.

### Tool exposure whitelist

| Tool | Remote | stdio | Why |
|---|---|---|---|
| `som.ping` | ✅ | ✅ | Health probe, no user data |
| `som.handoff` | ✅ w/PII check | ✅ | Packet write; PII middleware scans all fields |
| `som.chain` | ✅ (id-only) | ✅ | Read-only; only packet_ids accepted, no free text |
| `som.log_fallback` | ✅ w/PII check + rate limit | ✅ | Structured fields only; PII middleware scans |
| `lam.probe` | ✅ | ✅ | Read-only runtime status |
| `lam.embed` | ✅ w/PII check + rate limit | ✅ | Text input; PII middleware rejects PII-bearing calls |
| `lam.scrub_pii` | ❌ **stdio-only** | ✅ | By definition: PII inputs; must not cross network |

### Application-layer PII enforcement (NEW — addresses CRITICAL #2)

**`services/som-mcp/src/som_mcp/pii_middleware.py`** — runs BEFORE tool dispatch on every remote-exposed tool:

1. Load regex patterns from `scripts/lam/pii-patterns.yml` (shared with LAM).
2. For each string field in the request JSON, scan for matches.
3. If any match → reject with HTTP 400 + error: `{error: "pii_detected", pattern_class: "ssn|phone|email|dob|credit_card|field_marker", field_path: "$.user_prompt"}`.
4. Enforce payload size limits per tool (e.g., `lam.embed` max 8 KB input).
5. Enforce schema allowlists — each tool has a strict JSON Schema; unexpected fields rejected.

**Fail-closed:** if pii-patterns.yml is missing or malformed → middleware rejects all remote calls with `pii_patterns_unavailable` error.

### Server-stamped origin (NEW — addresses CRITICAL #1)

**HTTP transport overwrites `origin` server-side after authentication, before validator call.** Client-supplied `origin` in request body is discarded and a warning logged.

```python
# In http_server.py, before dispatching to tool handler:
origin = {
    "type": "remote",
    "session_jti": jwt_claims["jti"],
    "principal": jwt_claims["sub"],
    "caller_id": cf_access_email,  # required; no anonymous
    "rotation_version": jwt_claims["rotation_version"],
    "timestamp": utcnow_iso(),
}
request_body["origin"] = origin  # overwrites any client value
```

Validator refuses remote-origin packets that reference stdio-only tools. Negative tests prove client-spoofed `origin: local` gets overwritten.

### Rate limits (revised — addresses HIGH #5)

Keyed by **`sub` claim (stable principal id)**, not token material. Enforced **before** JSON parse / tool dispatch (cheap early rejection). Token-bucket per (principal, tool):

| Tool | Limit |
|---|---|
| `lam.embed` | 100/hour |
| `som.handoff` | 20/minute |
| `som.log_fallback` | 10/minute |
| `som.auth.begin` | 10/minute |
| others | 1/second soft |

Rotation or multiple concurrent JWTs under the same principal share the same bucket. Abuse of `som.auth.begin` triggers temporary principal-wide backoff (doubling on each violation).

### Audit trail — tamper-evident (NEW — addresses HIGH #4)

**`services/som-mcp/src/som_mcp/audit.py`** appends to `raw/remote-mcp-audit/YYYY-MM-DD.jsonl`:

```json
{
  "ts": "2026-04-14T23:12:45.123Z",
  "seq": 42,
  "prev_hash": "sha256 of previous entry's canonical JSON (or zero for seq=0)",
  "principal": "<sub>",
  "session_jti": "<jti>",
  "tool": "som.handoff",
  "args_hmac": "hmac-sha256(args_key, canonical_json(args))",
  "status": "ok | rejected | error",
  "reject_reason": "pii_detected | rate_limit | auth_invalid | etc. or null",
  "latency_ms": 42,
  "entry_hmac": "hmac-sha256(audit_key, canonical_json(all_above))"
}
```

- **Keyed HMAC** for `args_hmac` (key rotated with master token) — prevents dictionary attacks on known payloads
- **Per-line hash chain** via `prev_hash` — truncation or reorder breaks chain
- **entry_hmac** — per-entry signature so a truncated-then-rebuilt chain fails verification
- **Daily manifest** at `raw/remote-mcp-audit/YYYY-MM-DD.manifest.json` with: `{first_hash, last_hash, entry_count, sha256_of_file}`
- File permissions: 0600 on daily log; append-only where OS supports (`chattr +a` on Linux; macOS uses file flag `uappnd` via `chflags`)
- CI validator `.github/workflows/check-remote-audit-schema.yml` validates: schema, hash chain continuity, HMAC verification, manifest consistency

### Client library

`hldpro-governance/scripts/som-client/som_client.py` — sends `Authorization: Bearer <jwt>` + reads CF Access Service-Token env vars automatically:

```python
from som_client import SomClient
c = SomClient.from_env()  # reads SOM_MCP_URL, CF_ACCESS_CLIENT_ID, CF_ACCESS_CLIENT_SECRET, SOM_MCP_TOKEN
c.ping()
pkt_id = c.handoff(prior={...}, next_tier=3, artifacts=[...])  # server stamps origin
```

Library handles:
- CF Access service-token headers
- JWT caching (refresh before expiry)
- Automatic retry on 429 with exponential backoff
- PII-safe error messages (no payload echoes)

### Hard-rule invariant additions to STANDARDS §Society of Minds

- **Invariant #8:** Remote-origin packets never invoke stdio-only tools. Validator refuses.
- **Invariant #9:** Origin field is server-authoritative. HTTP transport overwrites; client-supplied values ignored.
- **Invariant #10:** Remote calls pass application-layer PII middleware before tool dispatch. Any PII match → reject. pii-patterns.yml unavailable → reject all.
- **Invariant #11:** Remote calls require Cloudflare Access outer identity. No anonymous principals.
- **Invariant #12:** Audit trail is hash-chained + HMAC-signed + daily-manifested. Break any link → CI validator fails; remote endpoint disabled until operator rebuilds trust.

## Threat model (explicit)

| Attack | Mitigation |
|---|---|
| Client spoofs `origin: local` | HTTP server overwrites origin post-auth |
| PII tunneled via `som.handoff.artifacts` | pii_middleware scans every string field pre-dispatch |
| PII tunneled via `lam.embed.text` | same middleware |
| JWT replay after rotation | `rotation_version` claim compared to daemon config |
| Rate-limit bypass via multiple JWTs | limits keyed on `sub` (principal), not token |
| Audit line deletion | hash chain break detected by CI validator |
| Audit manifest forgery | `entry_hmac` uses key not present in audit file |
| Master token leak | Cloudflare Access outer layer still blocks; rotate locally |
| Anonymous caller | Cloudflare Access mandatory; no anonymous header = 403 |
| Tunnel compromised | Cloudflare Access still required; attacker also needs local JWT secret |
| Local attacker on M5 | out of scope — they have stdio access already; full local trust assumed |
| cloudflared down | fail-closed: 503 on remote, stdio continues, operator alert |
| pii-patterns.yml missing/corrupt | middleware rejects all calls with `pii_patterns_unavailable` |

## Revised artifacts

### `local-ai-machine` (single PR)

1. `services/som-mcp/src/som_mcp/http_server.py` — HTTP transport, origin stamping, CF Access header validation
2. `services/som-mcp/src/som_mcp/auth.py` — bearer + JWT with full claims, rotation_version enforcement
3. `services/som-mcp/src/som_mcp/pii_middleware.py` — **NEW** — regex + schema allowlist + size limit
4. `services/som-mcp/src/som_mcp/rate_limit.py` — principal-keyed token-bucket, pre-dispatch
5. `services/som-mcp/src/som_mcp/remote_whitelist.py` — `REMOTE_ALLOWED_TOOLS` set
6. `services/som-mcp/src/som_mcp/audit.py` — hash-chain + HMAC + manifest
7. `services/som-mcp/tests/test_remote_security.py` — **NEW** — spoofed origin, PII rejection, JWT expiry/rotation, rate-limit bypass attempts, audit chain tamper, tunnel-down stdio continuity (all negative tests)
8. `services/som-mcp/tunnel.config.yml` — cloudflared config
9. `services/som-mcp/bin/tunnel.sh` — start cloudflared
10. `services/som-mcp/bin/rotate-token.sh` — bumps rotation_version, prints new token
11. `services/som-mcp/bin/verify-audit-chain.sh` — local verifier (same logic as CI)
12. `services/som-mcp/launchd/com.hldpro.som-mcp-tunnel.plist` — boot-start, fail-closed
13. `services/som-mcp/README.md` — extends existing with Remote section

### `hldpro-governance` (single PR — this branch)

1. `STANDARDS.md §Remote MCP Bridge` — new subsection with invariants 8-12 and threat model
2. `STANDARDS.md §Society of Minds` — append invariants 8-12 to the Hard-rule list
3. `.github/workflows/check-remote-audit-schema.yml` — schema + hash-chain + HMAC verification
4. `scripts/som-client/som_client.py` — thin client
5. `scripts/som-client/README.md` — usage + env vars + CF Access setup
6. `docs/exception-register.md` — entries:
   - `SOM-RMB-ROUND2-WAIVED-001` — operator waived round 2 Tier-1 re-review (expires 2026-05-14)
7. `docs/runbooks/remote-mcp-bridge.md` — operator runbook: setup, rotation, revocation, audit verification, fail-closed response

## PDCAR — revised

- **Plan:** this capture v2; Tier-1 round 1 REJECTED; round 2 waived by operator (logged in exception register)
- **Do Stage A (this branch, feat/remote-mcp-bridge):** STANDARDS additions + client library + audit workflow + exception register + runbook
- **Do Stage B (local-ai-machine, feat/som-mcp-http):** HTTP server + auth + PII middleware + rate limit + audit + negative tests
- **Do Stage C (same LAM PR):** cloudflared + launchd + bin scripts
- **Do Stage D:** smoke test + security tests from remote machine
- **Check / Adjust / Review:** per-stage closeouts + wiki decision + umbrella closure

## Waiver (round 2 Tier-1 re-review)

**`SOM-RMB-ROUND2-WAIVED-001`** — Operator approved 2026-04-14 to skip Tier-1 round-2 re-signature after round-1 REJECTED. Justification: revised plan addresses every required change from gpt-5.4 high's round-1 review; operator accepts residual risk of proceeding on single (updated Opus) signature. Expires 2026-05-14. Review cadence: this waiver is a one-off for this specific epic; standard dual-signature protocol resumes for subsequent epics.

## Production chain

- Tier 1: claude-opus-4-6 (revised plan) · round 2 gpt-5.4 high waived
- Tier 2 Worker: codex-spark primary (preferred, if quota back) / Qwen-Coder warm daemon fallback / Sonnet fallback step 3
- Tier 3 Reviewer: claude-sonnet-4-6 per-stage
- Tier 4 Gate: claude-haiku-4-5 final verification
