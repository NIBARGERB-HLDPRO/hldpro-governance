# Validation: Issue #366 Remote MCP Stage D Live-Readiness Evidence

Date: 2026-04-19
Branch: `issue-366-remote-mcp-live-readiness-20260419`
Epic: hldpro-governance #109

## Live Prerequisite Check

The current session did not have these live-proof inputs exported:

- `SOM_MCP_URL`
- `SOM_MCP_TOKEN` or `SOM_REMOTE_MCP_JWT`
- `SOM_REMOTE_MCP_IDENTITY_EMAIL`
- `SOM_REMOTE_MCP_IDENTITY_SUB`
- `SOM_REMOTE_MCP_AUDIT_DIR`
- `SOM_REMOTE_MCP_AUDIT_HMAC_KEY`
- `SOM_REMOTE_MCP_STDIO_PROOF_COMMAND`

No copied `raw/remote-mcp-audit` directory was found under the local HLDPRO workspace. Therefore epic #109 cannot be closed from this run.

## Origin-Boundary E2E

Used a clean detached `local-ai-machine` worktree at `origin/main` commit `f44039dc197c43b3a847f0c7570f1dc1256e2763`, started `som_mcp.remote_bridge` locally with synthetic public HMAC keys, and ran the merged governance Stage D harness against the real bridge on loopback.

Command shape:

```bash
SOM_MCP_URL="http://127.0.0.1:<local-port>" \
SOM_MCP_TOKEN="<synthetic-jwt>" \
SOM_REMOTE_MCP_IDENTITY_EMAIL="operator@example.invalid" \
SOM_REMOTE_MCP_IDENTITY_SUB="stage-d-local-readiness" \
SOM_REMOTE_MCP_AUDIT_DIR="raw/remote-mcp-origin-boundary-e2e" \
SOM_REMOTE_MCP_AUDIT_HMAC_KEY="issue-366-origin-boundary-audit-key" \
SOM_REMOTE_MCP_STDIO_PROOF_COMMAND="<local-stdio-import-proof>" \
python3 scripts/remote-mcp/stage_d_smoke.py --json
```

Results:

- `authenticated-ping`: pass.
- `anonymous-rejected`: pass.
- `origin-spoof-non-authoritative`: pass.
- `pii-handoff-rejected`: pass.
- `scrub-pii-remote-rejected`: pass.
- `audit-valid`: pass.
- `audit-tamper-negative`: pass.
- `stdio-after-tunnel-stop`: pass for local stdio import proof.

Strict audit verifier:

```bash
SOM_REMOTE_MCP_AUDIT_HMAC_KEY="issue-366-origin-boundary-audit-key" \
  python3 scripts/remote-mcp/verify_audit.py raw/remote-mcp-origin-boundary-e2e --require-hmac-key
```

Result: passed.

## Governance Validation

- Structured plan validation: `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --require-if-issue-branch --branch-name issue-366-remote-mcp-live-readiness-20260419` passed.
- Execution scope validation: `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-366-remote-mcp-live-readiness-implementation.json` passed.
- Local CI: `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` passed with verdict `PASS`.

## Evidence Hygiene

Preserved evidence:

- `raw/remote-mcp-origin-boundary-e2e/2026-04-19.jsonl`
- `raw/remote-mcp-origin-boundary-e2e/2026-04-19.manifest.json`

Evidence scan found no JWTs, private HMAC keys, Cloudflare credentials, live endpoint hostnames, or raw PII payloads. The JSONL contains only audit metadata and HMAC digests. The validation command uses a public synthetic audit key so future strict verification of this non-live artifact remains reproducible.

## Remaining Epic Work

Epic #109 remains open. Final closure requires the same Stage D harness against the live Cloudflare-protected endpoint from a second machine, copied live audit evidence, strict verifier output, tamper-negative proof, and local stdio MCP proof after stopping the tunnel.
