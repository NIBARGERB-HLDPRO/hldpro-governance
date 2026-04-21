# Remote MCP Bridge Runbook

Last updated: 2026-04-20
Owner: Operator (`nibargerb`)
Issue: [hldpro-governance #109](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109), recurring monitor [#372](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/372), alert evidence [#374](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/374), operating mode [#376](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/376), launchd proof [#378](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/378), connectivity preflight [#380](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/380), inbound preflight [#382](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/382), vault bootstrap [#385](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/385)
Scope: Governance Remote MCP Bridge contract, proof, and operator procedure.

## Current Status

Stage A governance standards, Stage B/C downstream HTTP bridge controls, and Stage D live Cloudflare proof are merged. Issue #109 is closed. Recurring operational monitoring is tracked by issue #372 and uses the same Stage D proof runner plus evidence-safety checks. Issue #376 selects local `launchd` as the live-authoritative monitor operating mode; GitHub Actions remains the scheduled fixture harness and an optional configured-live runner. Issue #380 adds the operator connectivity preflight for the immediate question: can this machine send `som.ping` to Remote MCP and receive a response now? Issue #382 adds the separate operator inbound preflight for the immediate question: can this environment receive an operator-targeted message into a session inbox? Issue #385 bootstraps the current operator vault keys, Cloudflare Access service-token policy membership, the local Remote MCP bridge LaunchAgent on the tunnel origin port, and live no-secret readiness evidence.

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
| `SOM_REMOTE_MCP_JWT` | Alternate inner bridge bearer/JWT token used when `SOM_MCP_TOKEN` is absent. |
| `SOM_MCP_PROTOCOL` | Set to `bridge` for the merged Stage B/C bridge protocol. Leave unset for legacy JSON-RPC fixtures. |
| `SOM_MCP_CALL_PATH` | Stage B/C bridge call path, normally `mcp/call`. |
| `CF_ACCESS_CLIENT_ID` | Cloudflare Access service-token client id. |
| `CF_ACCESS_CLIENT_SECRET` | Cloudflare Access service-token client secret. |
| `SOM_MCP_USER_AGENT` | Optional client user agent for Cloudflare edge policies that block default Python transports. |
| `SOM_REMOTE_MCP_AUTH_HMAC_KEY` | HMAC key used by the local Stage B/C bridge to verify the inner JWT. |
| `SOM_REMOTE_MCP_AUDIT_HMAC_KEY` | HMAC key used by the audit verifier when audit files exist. |
| `SOM_REMOTE_MCP_AUDIENCE` | Expected inner JWT audience when enforced by the bridge. |
| `SOM_REMOTE_MCP_ROTATION_VERSION` | Inner JWT rotation marker used by the bridge and operator token. |
| `SOM_OPERATOR_INBOUND_QUEUE_ROOT` | HITL relay queue root inspected by the operator inbound preflight. |
| `SOM_OPERATOR_INBOUND_SESSION_ID` | Target CLI session id for the inbound preflight. |

Example local client smoke after provisioning the required names through `hldpro-governance/.env.shared` plus bootstrap or the provider vault:

```bash
python3 scripts/som-client/som_client.py
```

The client deliberately does not expose `lam.scrub_pii`.

## Vault Bootstrap

The local operator vault is `.env.shared` at the governance checkout root. It is gitignored and must stay local. Do not paste or commit values from it.

Issue #385 created or refreshed these live operator entries in the vault:

| Entry | No-secret status |
|---|---|
| `SOM_MCP_URL` | Set to the Cloudflare-protected Remote MCP endpoint. |
| `SOM_MCP_TOKEN` / `SOM_REMOTE_MCP_JWT` | Set to the signed inner JWT used by the Stage B/C bridge. |
| `SOM_MCP_PROTOCOL` / `SOM_MCP_CALL_PATH` | Set to the Stage B/C bridge protocol and call path. |
| `SOM_REMOTE_MCP_AUTH_HMAC_KEY` | Set for local bridge JWT verification. |
| `SOM_REMOTE_MCP_AUDIT_HMAC_KEY` | Set for audit entry and args HMAC verification. |
| `CF_ACCESS_CLIENT_ID` / `CF_ACCESS_CLIENT_SECRET` | Set from the Cloudflare Access service token created for the operator path. |
| `CF_ACCESS_SERVICE_TOKEN_ID` / `CF_ACCESS_SERVICE_TOKEN_NAME` | Set so the token can be found and rotated without exposing its secret. |
| `SOM_OPERATOR_INBOUND_QUEUE_ROOT` / `SOM_OPERATOR_INBOUND_SESSION_ID` | Set for the local inbound preflight receive proof. |

The no-secret bootstrap evidence is under `raw/remote-mcp-vault-bootstrap/`. Those files record key names, status, Cloudflare policy membership, launchd health, and live preflight results only. They must not contain bearer tokens, JWT fragments, Cloudflare client secrets, HMAC keys, raw PII, or raw MCP payloads.

Current bridge runtime:

1. `cloudflared` maps `remote-mcp.hldpro.com` to local origin `http://127.0.0.1:18082`.
2. `com.hldpro.remote-mcp-bridge` runs the downstream `local-ai-machine` Stage B/C bridge on `127.0.0.1:18082`.
3. `scripts/remote-mcp/operator_connectivity.py --mode live` sends `som.ping` through Cloudflare Access plus the inner JWT and expects `ready: true`.
4. `scripts/remote-mcp/operator_inbound_preflight.py --mode live` checks the configured HITL relay `session-inbox` for a validated instruction addressed to the configured session.

When rotating:

1. Create a new Cloudflare Access service token and add only its token id to the `remote-mcp.hldpro.com` Access policy.
2. Generate a new `SOM_REMOTE_MCP_AUTH_HMAC_KEY` and signed `SOM_REMOTE_MCP_JWT`; set `SOM_MCP_TOKEN` to the same JWT unless deliberately testing the fallback path.
3. Reload `com.hldpro.remote-mcp-bridge` after updating its local LaunchAgent environment.
4. Run the live connectivity preflight and inbound preflight.
5. Remove the old Cloudflare service token from the Access policy, then delete it.

## Operator Connectivity Preflight

Use the connectivity preflight when the operator question is "does Remote MCP request/response work from this machine right now?" The preflight sends only `som.ping`, emits JSON, reports launchd template/install/load status without reading credential values, and fails closed before a live request when required live configuration is absent.

Fixture request/response proof:

```bash
python3 scripts/remote-mcp/operator_connectivity.py \
  --mode fixture \
  --json-output raw/remote-mcp-connectivity-preflight/YYYY-MM-DD.fixture-connectivity.json
```

Live operator proof after the required names are provisioned through the approved local or CI secret surface:

```bash
python3 scripts/remote-mcp/operator_connectivity.py \
  --mode live \
  --json-output raw/remote-mcp-connectivity-preflight/YYYY-MM-DD.live-connectivity.json
```

Interpretation:

- `ready: true` in live mode means this machine sent a `som.ping` Remote MCP request through the thin client and received a response.
- `ready: true` in fixture mode means the preflight harness and thin client path work locally; run live mode to prove current-machine Remote MCP readiness.
- Exit `2` in live mode means required setup names are missing, so no live Remote MCP request was sent.
- `launchd-installed` and `launchd-loaded` warnings do not block the one-shot request/response proof; they only say the recurring monitor is not installed or loaded in this user session.
- MCP here is request/response. Inbound push messaging to the operator remains a separate relay capability and must not be inferred from a successful `som.ping`.

Preserved preflight evidence must contain missing configuration names only, never token values, Cloudflare Access material, bearer headers, JWT fragments, raw PII, or raw MCP payloads.

## Operator Inbound Message Preflight

Use the inbound preflight when the operator question is "can this environment receive a message for a local CLI session?" This is not a Remote MCP `som.ping` request/response proof. It uses the HITL relay queue contract and proves that a validated operator instruction reaches `raw/hitl-relay/queue/session-inbox/` for one target session.

Fixture receive proof:

```bash
python3 scripts/remote-mcp/operator_inbound_preflight.py \
  --mode fixture \
  --json-output raw/remote-mcp-operator-inbound-preflight/YYYY-MM-DD.fixture-inbound.json
```

Live receive proof from a configured queue:

```bash
python3 scripts/remote-mcp/operator_inbound_preflight.py \
  --mode live \
  --json-output raw/remote-mcp-operator-inbound-preflight/YYYY-MM-DD.live-inbound.json
```

Interpretation:

- `ready: true` in live mode means the configured `session-inbox` contains a validated `session_instruction` addressed to `SOM_OPERATOR_INBOUND_SESSION_ID`.
- `ready: true` in fixture mode means the local queue contract can carry an operator instruction into a session inbox; run live mode to prove current-machine receive readiness.
- Exit `2` in live mode means the queue root or session id is missing, so no live receive path was inspected.
- Exit `1` in live mode with no missing config means the queue exists but no validated instruction for the configured session is present yet.

Preserved inbound preflight evidence must contain packet ids, session ids, action names, and audit packet types only. Do not commit raw message bodies, bearer tokens, JWT fragments, Cloudflare Access material, credential values, or PII.

## Stage D Proof Runner

Use the Stage D runner for final remote-machine acceptance. A fixture run is acceptable for CI and harness regression testing, but it is not live issue-closure evidence.

Fixture e2e:

```bash
python3 scripts/remote-mcp/stage_d_smoke.py \
  --fixture \
  --fixture-evidence-dir raw/remote-mcp-stage-d-fixture \
  --json
```

Live second-machine proof after endpoint, identity, Cloudflare Access, audit, HMAC, and stdio-proof names are provisioned through the approved local or CI secret surface:

```bash
python3 scripts/remote-mcp/stage_d_smoke.py --json
```

The live proof fails fast when required endpoint, identity, audit, HMAC, or stdio proof inputs are missing. Do not close issue #109 from fixture-only evidence.

## Recurring Health Monitor

Use the recurring monitor after Stage D activation to keep the live bridge under continuous authenticated smoke and audit verification. The monitor intentionally composes `stage_d_smoke.py`; it does not introduce a second Remote MCP protocol path.

### Operating Mode

Selected live mode: install `launchd/com.hldpro.remote-mcp-monitor.plist` from the intended operator checkout and run `scripts/remote-mcp/live_health_monitor.py --mode live` locally.

Rationale:

- Live health requires access to the copied Remote MCP audit directory and the HMAC key used to verify that audit chain.
- Live health also requires `SOM_REMOTE_MCP_STDIO_PROOF_COMMAND` so local stdio continuity is proved after remote tunnel checks.
- Those inputs are local operational controls. Do not treat GitHub-hosted fixture evidence as production live health.

GitHub Actions role:

- `.github/workflows/remote-mcp-live-health.yml` is the daily scheduled fixture harness and alert-artifact regression path.
- The workflow may run live mode only when the complete live secret set, safe audit-evidence source, and stdio-proof command are intentionally configured.
- If live inputs are absent, the workflow must preserve fixture evidence and report a skip/notice, not claim live health.

Selected-mode rehearsal evidence for issue #376 is preserved in `raw/remote-mcp-monitor-operating-mode/`. It proves the monitor and alert pipeline for the selected local operating mode without production credentials. It is not a substitute for a future issue-backed live run.

Fixture harness check:

```bash
python3 scripts/remote-mcp/live_health_monitor.py \
  --mode fixture \
  --fixture-evidence-dir raw/remote-mcp-monitor-fixture \
  --json
```

Live monitor check after the complete live monitor secret set is provisioned through the approved local or CI secret surface:

```bash
python3 scripts/remote-mcp/live_health_monitor.py --mode live --json
```

`--mode auto` runs live when live configuration markers are present and fixture mode otherwise. Missing partial live configuration is a hard failure. The monitor appends an `evidence-safety-scan` result and fails if preserved evidence contains raw SSNs, bearer tokens, Cloudflare Access token markers, or JWT fragments.

Payload-safe alert summary:

```bash
python3 scripts/remote-mcp/live_health_monitor.py --mode fixture --json \
  > /tmp/remote-mcp-monitor.json
python3 scripts/remote-mcp/monitor_alert.py \
  --input /tmp/remote-mcp-monitor.json \
  --json-output /tmp/remote-mcp-monitor-alert.json \
  --markdown-output /tmp/remote-mcp-monitor-alert.md \
  --fail-on-degraded
```

Alert output contains counts, check names, redacted failure details, health, mode, evidence path, and recommended operator action. It must not include auth headers, bearer tokens, JWT fragments, Cloudflare Access material, raw SSNs, or raw MCP payloads. If sensitive material appears in monitor input, the alert formatter replaces it with `[redacted-sensitive-detail]`, marks the monitor degraded, and returns non-zero when `--fail-on-degraded` is set.

Recurring surfaces:

- macOS launchd template: `launchd/com.hldpro.remote-mcp-monitor.plist` is the selected live operating surface and runs the same monitor every 900 seconds after replacing `__REPO_ROOT__` with the checkout path.
- GitHub Actions: `.github/workflows/remote-mcp-live-health.yml` runs the fixture harness on schedule, writes a payload-safe step summary and alert artifact, and runs live mode only when the full secret set and safe live evidence inputs are configured.

Install the launchd template only from the intended operating checkout. Provision required live monitor environment names through the local operator vault/bootstrap flow before loading the job; do not use `launchctl setenv` for secret values.

```bash
mkdir -p ~/Library/LaunchAgents projects/hldpro-governance/reports
sed "s#__REPO_ROOT__#$(pwd)#g" \
  launchd/com.hldpro.remote-mcp-monitor.plist \
  > ~/Library/LaunchAgents/com.hldpro.remote-mcp-monitor.plist
plutil -lint ~/Library/LaunchAgents/com.hldpro.remote-mcp-monitor.plist
launchctl bootstrap "gui/$(id -u)" ~/Library/LaunchAgents/com.hldpro.remote-mcp-monitor.plist
launchctl kickstart -k "gui/$(id -u)/com.hldpro.remote-mcp-monitor"
```

The template runs `--mode live`, not `--mode auto`. This is intentional: the selected live surface must fail closed when required live inputs are missing rather than silently producing fixture evidence.

After installation, capture payload-safe selected-mode evidence:

```bash
python3 scripts/remote-mcp/live_health_monitor.py --mode live --json \
  > /tmp/remote-mcp-monitor-live.json
python3 scripts/remote-mcp/monitor_alert.py \
  --input /tmp/remote-mcp-monitor-live.json \
  --json-output /tmp/remote-mcp-monitor-live-alert.json \
  --markdown-output /tmp/remote-mcp-monitor-live-alert.md \
  --fail-on-degraded
```

For dry-run rehearsal without production credentials, use `--mode fixture` and preserve the monitor JSON plus alert JSON/Markdown. For live-missing-configuration proof, `env -i PATH="$PATH" python3 scripts/remote-mcp/live_health_monitor.py --mode live --json` must exit before sending requests and state the missing required configuration names only.

For issue-backed launchd proof without installing on the operator machine, render and lint the plist into raw evidence:

```bash
mkdir -p raw/remote-mcp-launchd-live-proof
sed "s#__REPO_ROOT__#$(pwd)#g" \
  launchd/com.hldpro.remote-mcp-monitor.plist \
  > raw/remote-mcp-launchd-live-proof/YYYY-MM-DD.com.hldpro.remote-mcp-monitor.rendered.plist
plutil -lint raw/remote-mcp-launchd-live-proof/YYYY-MM-DD.com.hldpro.remote-mcp-monitor.rendered.plist
```

Do not commit a rendered plist containing credential values. The tracked launchd template and rendered lint proof may contain repo paths and command arguments only.

Operator response:

- Healthy alert: keep the launchd job loaded and retain the alert summary with the monitor timestamp.
- Degraded alert: inspect failed check names first, then verify Cloudflare Access status, inner bridge token rotation, audit-copy freshness, HMAC key availability, and stdio proof command health.
- Sensitive-finding alert: quarantine the affected artifact, rotate any implicated live credential if the source was production, rerun the monitor from sanitized evidence, and attach only redacted summaries to issue closeout.

Uninstall:

```bash
launchctl bootout "gui/$(id -u)" ~/Library/LaunchAgents/com.hldpro.remote-mcp-monitor.plist
rm -f ~/Library/LaunchAgents/com.hldpro.remote-mcp-monitor.plist
launchctl unsetenv SOM_MCP_URL
launchctl unsetenv SOM_MCP_TOKEN
launchctl unsetenv SOM_REMOTE_MCP_IDENTITY_EMAIL
launchctl unsetenv SOM_REMOTE_MCP_IDENTITY_SUB
launchctl unsetenv CF_ACCESS_CLIENT_ID
launchctl unsetenv CF_ACCESS_CLIENT_SECRET
launchctl unsetenv SOM_REMOTE_MCP_AUDIT_DIR
launchctl unsetenv SOM_REMOTE_MCP_AUDIT_HMAC_KEY
launchctl unsetenv SOM_REMOTE_MCP_STDIO_PROOF_COMMAND
```

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
| Recurring monitor fails | Treat as remote-health degraded. | Read the payload-safe alert summary, disable or restrict remote endpoint, and rerun monitor only after authenticated smoke, negative checks, strict audit, tamper-negative check, and evidence scan pass again. |
| Alert formatter reports sensitive material | Treat evidence as unsafe. | Do not publish the raw monitor output. Rotate credentials if live secrets may have been exposed, preserve only redacted alert output, and create an issue-backed remediation. |
| `cloudflared` down | Remote unreachable/503; stdio continues. | Restart tunnel only after bridge health and audit checks pass. |

## Stage B/C Acceptance Criteria

Downstream `local-ai-machine` implementation must prove:

1. Cloudflare Access identity is mandatory.
2. Inner JWT validates full claims and `rotation_version`.
3. Client-supplied `origin` is non-authoritative and rejected before dispatch when it conflicts with the server-stamped remote origin.
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
3. Spoofed `origin: local` is rejected before dispatch and audited.
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
