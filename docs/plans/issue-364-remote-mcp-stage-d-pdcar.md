# PDCAR: Issue #364 Remote MCP Stage D Proof Harness

Date: 2026-04-19
Branch: `issue-364-remote-mcp-stage-d-proof-20260419`
Issue: [#364](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/364)
Epic: [#109](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109)

## Plan

Add a governance-owned Stage D proof runner for the Remote MCP Bridge. The runner must execute the Stage D smoke/security acceptance checks against a live bridge when endpoint secrets are present, while remaining deterministic in CI through a fixture mode that exercises the same assertions and audit verifier path without exposing secrets.

## Do

1. Add `scripts/remote-mcp/stage_d_smoke.py`.
2. Cover authenticated ping, anonymous rejection, spoofed origin rejection, PII rejection, forbidden `lam.scrub_pii`, valid audit verification, tamper-negative audit verification, and local stdio proof wiring.
3. Add focused tests for fixture e2e and live-mode fail-fast configuration.
4. Update the Remote MCP runbook with live Stage D commands, required env, evidence handling, and closure rules.
5. Record structured plan, execution scope, validation, and closeout evidence.
6. Run focused tests, fixture e2e, audit verification, structured plan validation, execution scope validation, local CI, and GitHub Actions.

## Check

- `python3 -m pytest scripts/remote-mcp/tests/test_verify_audit.py scripts/remote-mcp/tests/test_stage_d_smoke.py`
- `python3 scripts/remote-mcp/stage_d_smoke.py --fixture --fixture-evidence-dir raw/remote-mcp-stage-d-fixture --json`
- `SOM_REMOTE_MCP_AUDIT_HMAC_KEY=fixture-audit-key python3 scripts/remote-mcp/verify_audit.py raw/remote-mcp-stage-d-fixture --require-hmac-key`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --require-if-issue-branch --branch-name issue-364-remote-mcp-stage-d-proof-20260419`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-364-remote-mcp-stage-d-proof-implementation.json`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`
- GitHub Actions on the PR

## Adjust

If live Cloudflare/Remote MCP secrets are absent, do not invent a live proof and do not close issue #109. Merge only the proof harness and fixture validation, then leave #109 open with explicit Stage D live-run commands and missing live-evidence status.

## Review

Final review must confirm the proof runner is payload-safe, env-driven, does not print secrets, fails fast when live config is missing, and has deterministic e2e coverage.
