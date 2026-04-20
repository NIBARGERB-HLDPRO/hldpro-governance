# PDCAR: Issue #376 Remote MCP Monitor Operating Mode

Date: 2026-04-20
Branch: `issue-376-remote-mcp-monitor-operating-mode-20260420`
Issue: [#376](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/376)
Parent: [#372](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/372), [#374](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/374)

## Plan

Select the live Remote MCP monitor operating mode, document why that mode is authoritative under current operational constraints, and preserve payload-safe rehearsal plus fail-closed evidence without claiming production live health.

## Do

1. Mark issue #376 as the active Remote MCP monitor operating-mode proof in the governance backlog mirrors.
2. Document local `launchd` as the selected live operating mode and GitHub Actions as the scheduled fixture harness plus optional configured-live runner.
3. Preserve local selected-mode rehearsal evidence under `raw/remote-mcp-monitor-operating-mode/`.
4. Preserve explicit live-missing-configuration fail-closed evidence.
5. Update governance registries and data contracts for the operating-mode proof artifacts.

## Check

- Fixture monitor rehearsal emits payload-safe monitor JSON.
- Alert formatter emits payload-safe JSON and Markdown from the rehearsal.
- Live mode exits before requests when required production configuration is absent.
- Evidence scan finds no raw SSNs, bearer-token material, Cloudflare Access markers, or JWT fragments.
- Structured plan, execution scope, backlog alignment, Remote MCP tests, compile checks, and Local CI Gate pass.

## Adjust

If live credentials and copied audit evidence are later available in the operator environment, run the same selected local `launchd` path in live mode and attach issue-backed live evidence before claiming recurring live health. GitHub Actions may run live only when separately configured with a safe audit-evidence source and stdio-proof command.

## Review

Review must verify that the runbook does not imply fixture evidence is production health, that GitHub Actions is not treated as live-authoritative without full configuration, and that all preserved artifacts remain payload-safe.
