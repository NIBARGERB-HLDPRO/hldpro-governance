# PDCAR: Issue #380 Remote MCP Operator Connectivity Preflight

Date: 2026-04-20
Branch: `issue-380-remote-mcp-connectivity-preflight-20260420`
Issue: [#380](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/380)
Parent: [#109](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109)

## Plan

Add a no-secret operator preflight that answers whether this machine can send a Remote MCP `som.ping` request and receive a response now. Keep fixture mode deterministic for CI, make live mode fail closed before sending a request when setup is incomplete, and document how to interpret the result without implying push/inbound messaging support.

## Do

1. Reconcile #378 into Done and mark #380 active in the governance mirrors.
2. Add `scripts/remote-mcp/operator_connectivity.py` with fixture and live modes, launchd status checks, JSON output, and no-secret missing-configuration reporting.
3. Update `SomClient.from_env()` to accept `SOM_REMOTE_MCP_JWT` when `SOM_MCP_TOKEN` is absent.
4. Add focused tests for fixture request/response, live missing-config fail-closed behavior, CLI JSON output, launchctl absence, and JWT fallback.
5. Update the Remote MCP runbook, service registry, feature registry, data dictionary, validation, closeout, and generated graph/wiki artifacts.
6. Preserve fixture and current-machine live fail-closed evidence under `raw/remote-mcp-connectivity-preflight/`.

## Check

- Fixture preflight sends `som.ping` through `SomClient` and returns `ready: true`.
- Live preflight either returns `ready: true` after `som.ping` succeeds or exits `2` before request when required setup is missing.
- Output includes `ready`, `mode`, `checks`, missing setup names, warnings, and recommended action.
- Launchd template/install/load status is reported without reading or printing credentials.
- Evidence scan finds no raw SSNs, bearer-token material, Cloudflare Access markers, JWT fragments, credential values, or raw MCP payloads.
- Remote MCP tests, compile checks, structured plan, execution scope, backlog alignment, registry surfaces, Local CI Gate, and PR checks pass.

## Adjust

If production Remote MCP configuration is absent, preserve the fail-closed live evidence and answer that request/response is not live-ready from this machine yet. Do not claim inbound push messaging from `som.ping`; MCP request/response and operator push relay are separate capabilities.

## Review

Review must verify the preflight is no-secret, fixture mode exercises the real thin client path, live mode does not send a request when required setup is missing, and the runbook gives an operator-safe answer to "does it work now?"
