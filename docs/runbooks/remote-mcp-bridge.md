# Remote MCP Bridge Runbook

Last updated: 2026-04-19
Owner: Operator (`nibargerb`)
Issue: [hldpro-governance #109](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109)
Scope: Governance Stage A. Downstream HTTP bridge implementation lives in `local-ai-machine` Stage B/C.

## Current Status

Remote MCP Bridge is planned and governance-ready, but not live. Stage A defines the contract, local verifier, thin client, and operator procedures. Do not expose `local-ai-machine/services/som-mcp/` over a tunnel until Stage B/C implements the HTTP bridge controls and Stage D proves remote smoke/security tests.

## Approved Remote Surface

Remote calls may use only this bounded tool set:

| Tool | Remote status | Required control |
|---|---|---|
| `som.ping` | Allowed | Authenticated health probe only. |
| `som.handoff` | Allowed | Server-stamped origin, strict schema, PII middleware. |
| `som.chain` | Allowed | Packet-id lookup only; no free text. |
| `som.log_fallback` | Allowed | Strict schema, PII middleware, principal rate limit. |
| `lam.probe` | Allowed | Runtime status only; no prompt payload. |
| `lam.embed` | Allowed | Strict schema, PII middleware, size limit, principal rate limit. |
| `lam.scrub_pii` | Forbidden | Stdio-only because inputs can contain PII. |

Any new remote tool requires an issue-backed standards update and downstream negative tests before exposure.

## Environment

The Stage A client reads:

| Variable | Purpose |
|---|---|
| `SOM_MCP_URL` | HTTPS URL for the bridge endpoint. Defaults to `http://localhost:8080` for local dev. |
| `SOM_MCP_TOKEN` | Inner bridge bearer/JWT token. |
| `CF_ACCESS_CLIENT_ID` | Cloudflare Access service-token client id. |
| `CF_ACCESS_CLIENT_SECRET` | Cloudflare Access service-token client secret. |
| `SOM_REMOTE_MCP_AUDIT_HMAC_KEY` | HMAC key used by the audit verifier when audit files exist. |

Example local client smoke after Stage B/C exists:

```bash
export SOM_MCP_URL="https://som-mcp.example.com"
export SOM_MCP_TOKEN="<inner-jwt>"
export CF_ACCESS_CLIENT_ID="<access-client-id>"
export CF_ACCESS_CLIENT_SECRET="<access-client-secret>"
python3 scripts/som-client/som_client.py
```

The client deliberately does not expose `lam.scrub_pii`.

## Token Rotation

Stage B/C must implement token rotation in `local-ai-machine` by bumping `rotation_version` and invalidating lower-version tokens. Operator procedure:

1. Stop remote traffic or announce a short remote maintenance window.
2. Run the downstream rotate-token command from `local-ai-machine`.
3. Update the operator secret store with the new token.
4. Run `som.ping` through `scripts/som-client/som_client.py`.
5. Confirm old tokens fail and the audit log records the rejected attempt without payload echo.

If any step fails, revoke the tunnel route and continue using stdio-only local MCP.

## Revocation

Revoke in this order:

1. Disable Cloudflare Access service token or user policy.
2. Rotate the inner bridge token and bump `rotation_version`.
3. Stop `cloudflared` or remove the tunnel route.
4. Verify remote endpoint returns 403/503 while local stdio MCP still works.
5. Run audit verification.

## Audit Verification

Remote MCP audit files live under `raw/remote-mcp-audit/` and use daily JSONL plus manifest files.

Local verifier:

```bash
python3 scripts/remote-mcp/verify_audit.py raw/remote-mcp-audit
```

Strict HMAC verifier:

```bash
SOM_REMOTE_MCP_AUDIT_HMAC_KEY="<key>" \
  python3 scripts/remote-mcp/verify_audit.py raw/remote-mcp-audit --require-hmac-key
```

CI verifier: `.github/workflows/check-remote-mcp-audit-schema.yml`.

No audit directory is valid before Stage B/C activation. Once audit files exist, missing HMAC key or broken chain is a hard failure and the remote endpoint must stay disabled until trust is rebuilt.

## Fail-Closed Response

| Failure | Expected behavior | Operator action |
|---|---|---|
| Cloudflare Access missing/invalid | Reject before inner token. | Fix Access policy or service token; do not bypass. |
| Inner token invalid/expired/lower rotation | Reject and audit. | Rotate or reissue token. |
| PII patterns missing/malformed | Reject all remote calls. | Restore patterns before re-enabling remote calls. |
| PII detected | Reject with payload-safe error. | Use local stdio/LAM path only. |
| Rate limit exceeded | Return 429 before dispatch. | Wait or inspect principal activity. |
| Audit verifier fails | Disable remote endpoint. | Preserve files, identify break, rotate keys if needed, rebuild trust with issue-backed closeout. |
| `cloudflared` down | Remote unreachable/503; stdio continues. | Restart tunnel only after bridge health and audit checks pass. |

## Stage B/C Acceptance Criteria

Downstream `local-ai-machine` implementation must prove:

1. Cloudflare Access identity is mandatory.
2. Inner JWT validates full claims and `rotation_version`.
3. Client-supplied `origin` is overwritten server-side.
4. Remote-origin packets cannot invoke stdio-only tools.
5. PII middleware scans every string field before dispatch and fails closed when patterns are unavailable.
6. Rate limits are keyed by principal `sub`, not token material.
7. Audit writer emits hash-chained, HMAC-signed entries and daily manifests.
8. Tamper, truncation, missing manifest, and HMAC mismatch fail verifier tests.
9. Tunnel-down behavior does not create an unauthenticated fallback.

## Stage D Acceptance Criteria

Final issue #109 closure requires a remote-machine proof:

1. `som.ping` succeeds with Cloudflare Access plus inner token.
2. Anonymous request fails.
3. Spoofed `origin: local` is overwritten and audited.
4. PII-bearing `som.handoff` or `lam.embed` is rejected before dispatch.
5. `lam.scrub_pii` remote call is rejected.
6. Audit verifier passes valid calls and fails a copied tamper sample.
7. Local stdio MCP remains usable when the tunnel is stopped.

## References

- `STANDARDS.md` Remote MCP Bridge
- `raw/inbox/2026-04-14-remote-mcp-bridge-plan.md`
- `raw/cross-review/2026-04-14-remote-mcp-bridge.md`
- `docs/exception-register.md` entry `SOM-RMB-ROUND2-WAIVED-001`
- `scripts/som-client/README.md`
