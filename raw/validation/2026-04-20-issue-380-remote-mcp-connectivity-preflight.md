# Validation: Issue #380 Remote MCP Operator Connectivity Preflight

Date: 2026-04-20
Branch: `issue-380-remote-mcp-connectivity-preflight-20260420`
Issue: [#380](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/380)

## Evidence

| Artifact | Result |
|---|---|
| `raw/remote-mcp-connectivity-preflight/2026-04-20.fixture-connectivity.json` | Fixture `som.ping` request/response returned `ready: true`; launchd install/load reported warnings only. |
| `raw/remote-mcp-connectivity-preflight/2026-04-20.live-missing-config.json` | Sanitized empty-env live run returned `ready: false` and listed missing setup names only. |
| `raw/remote-mcp-connectivity-preflight/2026-04-20.live-missing-config.proof.json` | Captured expected exit code `2` for missing live configuration. |
| `raw/remote-mcp-connectivity-preflight/2026-04-20.current-machine-live.json` | Current machine live run returned `ready: false` because Remote MCP live config is not present. |
| `raw/remote-mcp-connectivity-preflight/2026-04-20.current-machine-live.proof.json` | Captured current-machine live exit code `2`. |

## Commands

| Command | Result |
|---|---|
| `python3 scripts/remote-mcp/operator_connectivity.py --mode fixture --json-output raw/remote-mcp-connectivity-preflight/2026-04-20.fixture-connectivity.json` | PASS, exit 0 |
| `env -i PATH="$PATH" python3 scripts/remote-mcp/operator_connectivity.py --mode live --json-output raw/remote-mcp-connectivity-preflight/2026-04-20.live-missing-config.json` | PASS, expected exit 2 captured |
| `python3 scripts/remote-mcp/operator_connectivity.py --mode live --json-output raw/remote-mcp-connectivity-preflight/2026-04-20.current-machine-live.json` | PASS, expected unconfigured exit 2 captured |
| `python3 -m pytest scripts/remote-mcp/tests/test_operator_connectivity.py scripts/som-client/tests/test_som_client.py scripts/remote-mcp/tests/test_live_health_monitor.py scripts/remote-mcp/tests/test_monitor_alert.py scripts/remote-mcp/tests/test_verify_audit.py scripts/remote-mcp/tests/test_stage_d_smoke.py` | PASS, 23 passed |
| `python3 -m py_compile scripts/remote-mcp/operator_connectivity.py scripts/remote-mcp/live_health_monitor.py scripts/remote-mcp/monitor_alert.py scripts/som-client/som_client.py` | PASS |
| `python3 -m json.tool docs/plans/issue-380-remote-mcp-connectivity-preflight-structured-agent-cycle-plan.json >/dev/null && python3 -m json.tool raw/execution-scopes/2026-04-20-issue-380-remote-mcp-connectivity-preflight-implementation.json >/dev/null && python3 -m json.tool raw/remote-mcp-connectivity-preflight/2026-04-20.fixture-connectivity.json >/dev/null && python3 -m json.tool raw/remote-mcp-connectivity-preflight/2026-04-20.live-missing-config.json >/dev/null && python3 -m json.tool raw/remote-mcp-connectivity-preflight/2026-04-20.current-machine-live.json >/dev/null` | PASS |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-380-remote-mcp-connectivity-preflight-20260420 --changed-files-file /tmp/issue380-changed-files.txt --enforce-governance-surface` | PASS, 83 structured plans validated |
| `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-20-issue-380-remote-mcp-connectivity-preflight-implementation.json --changed-files-file /tmp/issue380-changed-files.txt` | PASS; dirty sibling roots were declared active parallel roots |
| `python3 scripts/overlord/check_overlord_backlog_github_alignment.py` | PASS |
| `python3 scripts/overlord/validate_registry_surfaces.py` | PASS |
| `rg -n "123-45-6789\|Bearer\\s+[A-Za-z0-9._~+/=-]{10,}\|CF-Access\|eyJ[A-Za-z0-9_-]{8,}\\.[A-Za-z0-9_-]{8,}\|client-secret\|cf-secret\|fixture-token" raw/remote-mcp-connectivity-preflight \|\| true` | PASS, no matches |
| `git diff --check` | PASS |
| `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --base-ref origin/main --head-ref HEAD --json` | PASS, 32 changed files, blocker checks passed |

## Current-Machine Answer

As of this validation, fixture request/response works through the thin client path. Current-machine live Remote MCP request/response is not ready because `SOM_MCP_URL`, `SOM_MCP_TOKEN` or `SOM_REMOTE_MCP_JWT`, `CF_ACCESS_CLIENT_ID`, and `CF_ACCESS_CLIENT_SECRET` are not configured in this execution environment. No live request was sent.

MCP request/response does not prove inbound push/operator messaging. Push messaging remains a separate relay capability.
