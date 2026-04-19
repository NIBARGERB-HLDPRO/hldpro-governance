# PDCAR: Issue #368 Remote MCP Cloudflare Access Proof Blocker

Date: 2026-04-19
Branch: `issue-368-remote-mcp-cloudflare-access-blocker-20260419`
Issue: [#368](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/368)
Epic: [#109](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109)

## Plan

Record the live Cloudflare boundary attempt for Remote MCP Stage D. The merged bridge and governance harness are ready, but the public Cloudflare hostname returned 403 before origin dispatch, so final #109 closure remains blocked outside the repository.

## Do

1. Confirm the active Cloudflare tunnel route for the available hostname.
2. Start the real downstream Remote MCP Bridge on the routed local port with synthetic local keys.
3. Run the Stage D proof harness through the public Cloudflare hostname.
4. Attempt a temporary service-token policy path, then restore the original policy.
5. Record non-secret validation and closeout evidence.

## Check

- Live tunnel harness attempt: `scripts/remote-mcp/stage_d_smoke.py --json` against `https://critic.hldpro.com`.
- Cloudflare Access policy restore check: service-token policy include count returned to its original value.
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --require-if-issue-branch --branch-name issue-368-remote-mcp-cloudflare-access-blocker-20260419`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-368-remote-mcp-cloudflare-access-blocker-implementation.json`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`
- GitHub Actions on the PR

## Adjust

Do not close #109 from this evidence. The request reached Cloudflare, but Cloudflare returned 403 before the Remote MCP origin received dispatchable traffic, so no live audit JSONL rows were generated.

## Review

Review must confirm no Cloudflare tunnel token, Access client secret, JWT, HMAC key, or raw PII is committed.
