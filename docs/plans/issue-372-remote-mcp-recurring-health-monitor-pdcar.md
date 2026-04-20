# PDCAR: Issue #372 Remote MCP Recurring Health Monitor

Date: 2026-04-19
Branch: `issue-372-remote-mcp-recurring-health-monitor-20260419`
Issue: [#372](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/372)
Parent: [#109](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109)

## Plan

Convert the completed Remote MCP Stage D live proof into a repeatable operational monitor without changing invariants 11-15. The monitor must reuse the Stage D proof path, preserve payload-safe evidence, expose a scheduled CI harness, and document an operator launchd option for local recurring live checks.

## Do

1. Add `scripts/remote-mcp/live_health_monitor.py` as the recurring monitor wrapper around the Stage D runner.
2. Add focused monitor tests covering fixture success, live fail-fast configuration, and evidence-safety rejection.
3. Add `.github/workflows/remote-mcp-live-health.yml` for scheduled fixture harness proof and configured live execution.
4. Add `launchd/com.hldpro.remote-mcp-monitor.plist` as the optional local recurring scheduler template.
5. Update Remote MCP runbook, feature registry, service registry, data dictionary, workflow coverage inventory, progress, and backlog mirrors.
6. Preserve validation and closeout artifacts for issue #372.

## Check

- Focused Remote MCP pytest suite.
- Python compile checks for monitor, Stage D runner, audit verifier, and thin client.
- Fixture monitor E2E run with JSON output and evidence scan.
- Live-mode fail-fast negative proof with missing configuration.
- `plutil -lint` for the launchd template.
- Workflow local coverage validation.
- Structured plan and execution-scope validation.
- Local CI Gate.
- Stage 6 closeout hook.

## Adjust

The recurring GitHub workflow cannot assume production Cloudflare or audit-copy secrets are present. It therefore always proves fixture mode and only runs live mode when full live markers are configured. Partial live configuration fails closed so a half-configured monitor cannot report healthy.

## Review

Review must confirm the monitor never logs token material or raw payloads, that evidence scanning is wired into both fixture and live modes, and that #109 remains closed while ongoing operational work is isolated to #372.
