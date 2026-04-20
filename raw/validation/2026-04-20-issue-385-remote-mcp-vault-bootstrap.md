# Validation — Issue #385 Remote MCP Live Key Vault Bootstrap

Date: 2026-04-20
Branch: `issue-385-remote-mcp-vault-bootstrap-20260420`

## Acceptance Results

| Acceptance criterion | Result | Evidence |
|---|---|---|
| Remote MCP operator keys stored in gitignored vault only | PASS | `.env.shared` is not tracked; no-secret manifests under `raw/remote-mcp-vault-bootstrap/` record key status only |
| Cloudflare Access service token created and attached to Remote MCP policy | PASS | `raw/remote-mcp-vault-bootstrap/2026-04-20-cloudflare-access-policy.json` |
| Thin client supports the merged Stage B/C bridge protocol | PASS | `scripts/som-client/som_client.py`; focused tests passed |
| Local Remote MCP bridge loaded on Cloudflare tunnel origin port | PASS | `raw/remote-mcp-vault-bootstrap/2026-04-20-remote-bridge-launchd.json` |
| Final live request/response AC | PASS | `raw/remote-mcp-vault-bootstrap/2026-04-20-connectivity-live-after-bridge.json` has `ready: true` |
| Final live inbound receive AC | PASS | `raw/remote-mcp-vault-bootstrap/2026-04-20-inbound-live-after-valid-seed.json` has `ready: true` |
| No committed secret values in evidence | PASS | Sensitive-material denylist scan over `raw/remote-mcp-vault-bootstrap/` returned no matches |

## Commands

| Command | Result |
|---|---|
| `python3 -m pytest scripts/som-client/tests/test_som_client.py scripts/remote-mcp/tests/test_operator_connectivity.py scripts/remote-mcp/tests/test_operator_inbound_preflight.py` | PASS, 13 passed |
| `python3 -m py_compile scripts/som-client/som_client.py scripts/remote-mcp/operator_connectivity.py scripts/remote-mcp/operator_inbound_preflight.py` | PASS |
| `python3 -m json.tool docs/plans/issue-385-remote-mcp-vault-bootstrap-structured-agent-cycle-plan.json` | PASS |
| `python3 -m json.tool raw/execution-scopes/2026-04-20-issue-385-remote-mcp-vault-bootstrap-implementation.json` | PASS |
| `find raw/remote-mcp-vault-bootstrap -name '*.json' -maxdepth 3 -print0 | xargs -0 -n1 python3 -m json.tool` | PASS |
| `python3 scripts/remote-mcp/operator_connectivity.py --mode live --json-output raw/remote-mcp-vault-bootstrap/2026-04-20-connectivity-live-after-bridge.json` | PASS, exit 0 |
| `python3 scripts/remote-mcp/operator_inbound_preflight.py --mode live --json-output raw/remote-mcp-vault-bootstrap/2026-04-20-inbound-live-after-valid-seed.json` | PASS, exit 0 |
| `rg -n "Bearer\\s+[A-Za-z0-9._~+/=-]{10,}|CF-Access|eyJ[A-Za-z0-9_-]{8,}\\.[A-Za-z0-9_-]{8,}|client_secret|AUTH_HMAC_KEY=.*[A-Za-z0-9]|AUDIT_HMAC_KEY=.*[A-Za-z0-9]|som_live_|cfut_|cfat_" raw/remote-mcp-vault-bootstrap || true` | PASS, no matches |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-385-remote-mcp-vault-bootstrap-20260420 --require-if-issue-branch` | PASS, 114 plans |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-385-remote-mcp-vault-bootstrap-20260420 --changed-files-file /tmp/issue385-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope` | PASS, 114 plans |
| `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-20-issue-385-remote-mcp-vault-bootstrap-implementation.json --changed-files-file /tmp/issue385-changed-files.txt` | PASS with warnings for declared dirty sibling roots |
| `python3 scripts/overlord/validate_registry_surfaces.py` | PASS |
| `python3 scripts/overlord/check_overlord_backlog_github_alignment.py` | PASS |
| `git diff --check` | PASS |
| `bash hooks/governance-check.sh` | PASS |
| `bash hooks/closeout-hook.sh raw/closeouts/2026-04-20-issue-385-remote-mcp-vault-bootstrap.md` | PASS; closeout template validated, graph/wiki refreshed, memory writer skipped because credentials were not configured |
| `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` | PASS; final post-closeout report `cache/local-ci-gate/reports/20260420T144508Z-hldpro-governance-git` |

## Notes

- The initial live request reached Cloudflare but failed with 1010 browser-signature denial. Setting a stable `SOM_MCP_USER_AGENT` moved the request past that edge-policy blocker.
- The next live request failed with Cloudflare 502 because no local bridge was listening on the tunnel origin. Loading `com.hldpro.remote-mcp-bridge` on `127.0.0.1:18082` resolved the origin blocker.
- The first inbound seed dead-lettered because the proof channel was not in the HITL relay schema enum. The valid proof uses channel `other`.
- `.env.shared` and the installed local LaunchAgent contain secret values and remain untracked local runtime state.
