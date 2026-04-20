# PDCAR: Issue #374 Remote MCP Monitor Alert Delivery

Date: 2026-04-20
Branch: `issue-374-remote-mcp-monitor-alerts-20260419`
Issue: [#374](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/374)
Parent: [#372](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/372)

## Plan

Add a payload-safe alert/report layer for the recurring Remote MCP monitor and preserve first recurring fixture-run evidence without exposing secrets, JWT fragments, Cloudflare Access material, bearer tokens, or raw PII.

## Do

1. Add `scripts/remote-mcp/monitor_alert.py` to summarize monitor JSON into safe JSON and Markdown alert artifacts.
2. Add focused tests for healthy, degraded, and sensitive-material redaction paths.
3. Wire `.github/workflows/remote-mcp-live-health.yml` to write alert artifacts and a GitHub step summary.
4. Preserve first recurring fixture-run monitor and alert artifacts under `raw/remote-mcp-monitor-first-run/`.
5. Update Remote MCP runbook, registries, workflow coverage inventory, progress, and backlog mirrors.

## Check

- Focused monitor alert tests.
- Full Remote MCP monitor/verifier/thin-client tests.
- Python compile checks.
- Fixture monitor plus alert generation.
- Expected live missing-config fail-fast proof.
- Structured plan and execution-scope validation.
- Workflow local coverage.
- Local CI Gate and PR checks.

## Adjust

The initial alert detector treated the safe phrase "bearer tokens" as token material. The bearer-token detector now requires token-like length so safe explanatory text is not marked degraded while actual token-looking values are still redacted.

## Review

Review must verify alert artifacts contain only status/counts/redacted details and that first-run evidence does not contain bearer material, JWT fragments, Cloudflare Access headers, raw SSNs, or raw MCP payloads.
