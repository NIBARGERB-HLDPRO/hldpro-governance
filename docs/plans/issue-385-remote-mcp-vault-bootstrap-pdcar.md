# PDCAR: Issue #385 Remote MCP Live Key Vault Bootstrap

Date: 2026-04-20
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/385
Branch: `issue-385-remote-mcp-vault-bootstrap-20260420`

## Plan

Bootstrap the live Remote MCP operator credentials into the local gitignored `.env.shared` vault, update the service runbook, and rerun the live request/response and receive preflights without committing any secret values.

Acceptance criteria:

- Missing Remote MCP operator keys are created or refreshed in `.env.shared`.
- Cloudflare Access service-token policy membership is updated for `remote-mcp.hldpro.com`.
- The runbook documents vault bootstrap, rotation, bridge protocol, and live verification.
- The thin client supports the merged Stage B/C bridge protocol used by the live bridge.
- No-secret evidence proves vault status, Cloudflare policy status, bridge launchd health, live `som.ping`, and live inbound session-inbox readiness.

## Do

- Created issue #385 and branched from `origin/main`.
- Generated Remote MCP operator vault entries without printing values.
- Created a Cloudflare Access service token and attached it to the Remote MCP Access policy.
- Minted a signed inner JWT matching the Stage B/C bridge HMAC contract and set `SOM_MCP_TOKEN` to that JWT.
- Added `SOM_MCP_PROTOCOL=bridge` and `SOM_MCP_CALL_PATH=mcp/call` support to `SomClient`.
- Loaded `com.hldpro.remote-mcp-bridge` locally on the Cloudflare tunnel origin port `127.0.0.1:18082`.
- Seeded a bounded HITL relay queue under issue evidence and proved live inbound receive readiness.

## Check

Required checks:

- JSON parse checks for the structured plan, execution scope, vault evidence, Cloudflare policy evidence, bridge launchd evidence, and preflight outputs.
- Focused `SomClient` and Remote MCP operator preflight tests.
- Live connectivity preflight with `ready: true`.
- Live inbound preflight with `ready: true`.
- Sensitive-material denylist scan over `raw/remote-mcp-vault-bootstrap/`.
- Governance surface plan validation, execution-scope validation, registry-surface validation, backlog alignment, Local CI Gate, and Stage 6 closeout hook.

## Adjust

Initial live `som.ping` failed at Cloudflare 1010 because the default Python transport signature was blocked. Added a stable `SOM_MCP_USER_AGENT` vault entry, then the next failure moved to Cloudflare 502 because no local bridge was listening on the tunnel origin. The live bridge also uses the merged Stage B/C `/mcp/call` shape, so `SomClient` gained explicit bridge protocol support instead of forcing the older JSON-RPC fixture shape onto live traffic.

The first inbound seed used an unsupported proof channel and correctly dead-lettered. The valid proof uses the existing `other` channel and produces a validated `session_instruction`.

## Review

Subagent explorer `019dab4c-1650-72d2-bf69-6bb5a5aeea7e` reviewed the expected governance surfaces and validation checklist. No secret values are recorded in committed artifacts. Remaining operational risk is standard credential rotation and keeping the local bridge LaunchAgent loaded while the Cloudflare tunnel route is active.
