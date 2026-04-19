# PDCAR: Issue #366 Remote MCP Stage D Live-Readiness Evidence

Date: 2026-04-19
Branch: `issue-366-remote-mcp-live-readiness-20260419`
Issue: [#366](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/366)
Epic: [#109](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109)

## Plan

Record the strongest available non-live Stage D readiness proof after the Stage D harness merged: run the governance Stage D smoke/security harness against the real downstream `local-ai-machine` Remote MCP Bridge on local loopback with synthetic secrets, preserve non-secret audit evidence, and keep epic #109 open for the required live second-machine Cloudflare proof.

## Do

1. Use a clean `local-ai-machine` worktree at merged PR #485.
2. Start `som_mcp.remote_bridge` locally with synthetic HMAC keys and a repo-local audit directory.
3. Drive it with `scripts/remote-mcp/stage_d_smoke.py` from governance `main`.
4. Preserve audit JSONL and manifest evidence without secrets or raw PII.
5. Record validation and closeout evidence.

## Check

- `python3 scripts/remote-mcp/stage_d_smoke.py --json` against local loopback real bridge.
- `SOM_REMOTE_MCP_AUDIT_HMAC_KEY=<synthetic> python3 scripts/remote-mcp/verify_audit.py raw/remote-mcp-origin-boundary-e2e --require-hmac-key`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --require-if-issue-branch --branch-name issue-366-remote-mcp-live-readiness-20260419`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-366-remote-mcp-live-readiness-implementation.json`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`
- GitHub Actions on the PR

## Adjust

This evidence is not live issue #109 closure evidence. It proves the merged downstream bridge and merged governance harness interoperate end to end on the local origin boundary. Final #109 closure still requires the Cloudflare-protected second-machine run, copied live audit evidence, tamper-negative verifier output, and local stdio proof after stopping the tunnel.

## Review

Review must confirm the artifact does not commit secrets or live endpoint data, does not close #109, and labels the e2e proof as local origin-boundary readiness only.
