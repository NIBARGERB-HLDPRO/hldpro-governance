# PDCAR: Issue #378 Remote MCP Launchd Live Proof

Date: 2026-04-20
Branch: `issue-378-remote-mcp-launchd-live-proof-20260420`
Issue: [#378](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/378)
Parent: [#376](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/376)

## Plan

Harden the selected local launchd monitor surface so it runs live mode directly, document production proof steps, and preserve payload-safe render, rehearsal, and fail-closed evidence without committing live credentials or production payloads.

## Do

1. Reconcile #376 into Done and mark #378 active in the governance mirrors.
2. Change `launchd/com.hldpro.remote-mcp-monitor.plist` from `--mode auto` to `--mode live`.
3. Update the Remote MCP runbook with launchd environment setup, render/lint proof, rollback, and no-secrets evidence rules.
4. Preserve issue-specific launchd render/lint, fixture rehearsal, alert, and live-missing-config artifacts under `raw/remote-mcp-launchd-live-proof/`.
5. Update registries, data dictionary, validation, closeout, and generated graph/wiki artifacts.

## Check

- Launchd template and rendered plist lint successfully.
- Template invokes `live_health_monitor.py --mode live`.
- Fixture rehearsal and alert rendering remain payload-safe.
- Missing live configuration exits before requests with code `2`.
- Evidence scan finds no raw SSNs, bearer-token material, Cloudflare Access markers, JWT fragments, credentials, or raw MCP payloads.
- Remote MCP tests, compile checks, structured plan, execution scope, backlog alignment, registry surfaces, Local CI Gate, and PR checks pass.

## Adjust

If production launchd credentials and copied audit evidence are unavailable, preserve the fail-closed proof and do not claim production live health. A later issue may attach live runtime evidence after the operator environment is configured.

## Review

Review must verify the selected launchd surface cannot silently fall back to fixture mode, that no rendered plist contains credential values, and that #376 is no longer listed as active after its issue closure.
