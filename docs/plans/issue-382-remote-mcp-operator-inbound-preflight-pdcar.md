# PDCAR: Issue #382 Remote MCP Operator Inbound Message Preflight

Date: 2026-04-20
Branch: `issue-382-remote-mcp-operator-inbound-preflight-20260420`
Issue: [#382](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/382)
Parent: [#109](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109)

## Plan

Add a no-secret preflight for the separate operator-message receive question. Keep it distinct from #380 `som.ping` request/response: fixture mode proves the existing HITL relay queue can deliver a validated instruction into a session inbox, while live mode fails closed until a queue root and target session id are configured.

## Do

1. Reconcile #380 into Done and mark #382 active in the governance mirrors.
2. Add `scripts/remote-mcp/operator_inbound_preflight.py` with fixture and live modes, JSON output, and missing live config names only.
3. Reuse `scripts/orchestrator/hitl_relay_queue.py` and `scripts/packet/validate_hitl_relay.py` for the fixture receive proof.
4. Add focused tests for fixture receive, live missing-config fail-closed behavior, configured queue/no-instruction failure, and CLI JSON output.
5. Update the Remote MCP runbook, service registry, feature registry, data dictionary, validation, closeout, and generated graph/wiki artifacts.
6. Preserve fixture and current-machine fail-closed evidence under `raw/remote-mcp-operator-inbound-preflight/`.

## Check

- Fixture preflight writes a validated `session_instruction` to a session inbox through the HITL relay queue path.
- Live preflight either finds a validated instruction for `SOM_OPERATOR_INBOUND_SESSION_ID` or exits `2` before inspecting live receive state when required config is missing.
- Output includes `ready`, `mode`, checks, missing live setup names, warnings, received instruction summary, and recommended action.
- Runbook clearly distinguishes `som.ping` request/response from inbound/operator-message receive capability.
- Evidence scan finds no raw SSNs, bearer-token material, Cloudflare Access markers, JWT fragments, credential values, or raw message bodies.
- HITL relay tests, compile checks, structured plan, execution scope, backlog alignment, registry surfaces, Local CI Gate, and PR checks pass.

## Adjust

If no live queue root/session id is configured, preserve the fail-closed live evidence and answer that inbound operator-message receive is not live-ready from this machine yet. Do not claim push transport delivery from the fixture queue proof.

## Review

Review must verify fixture mode exercises the real HITL queue validator/path, live mode does not read arbitrary raw message bodies, and the runbook prevents overclaiming #380 request/response as inbound receive.
