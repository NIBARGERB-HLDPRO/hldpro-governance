# Validation: Issue #364 Remote MCP Stage D Proof Harness

Date: 2026-04-19
Branch: `issue-364-remote-mcp-stage-d-proof-20260419`
Epic: hldpro-governance #109

## Results

- Focused tests: `python3 -m pytest scripts/remote-mcp/tests/test_verify_audit.py scripts/remote-mcp/tests/test_stage_d_smoke.py` passed, 6 tests.
- Fixture e2e: `python3 scripts/remote-mcp/stage_d_smoke.py --fixture --fixture-evidence-dir raw/remote-mcp-stage-d-fixture --json` passed.
- Strict fixture audit verifier: `SOM_REMOTE_MCP_AUDIT_HMAC_KEY=fixture-audit-key python3 scripts/remote-mcp/verify_audit.py raw/remote-mcp-stage-d-fixture --require-hmac-key` passed.
- Structured plan validation: `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --require-if-issue-branch --branch-name issue-364-remote-mcp-stage-d-proof-20260419` passed.
- Execution scope validation: `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-364-remote-mcp-stage-d-proof-implementation.json` passed.
- Local CI: `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` passed with verdict `PASS`.
- Final read-only re-review: prior findings fixed; no new material issues found.

## Fixture E2E ACs

- `authenticated-ping`: pass.
- `anonymous-rejected`: pass.
- `origin-spoof-non-authoritative`: pass.
- `pii-handoff-rejected`: pass.
- `scrub-pii-remote-rejected`: pass.
- `audit-valid`: pass.
- `audit-tamper-negative`: pass.
- `stdio-after-tunnel-stop`: skipped in fixture mode only.

## Live Proof Status

Live Stage D proof was not run because the required live endpoint, identity, copied audit directory, audit HMAC key, and tunnel-stop stdio proof command were not exported in this session. The proof runner fails fast for those missing inputs by design. Issue #109 must remain open until live second-machine proof passes.

## Review Fixes

Final read-only review found two material issues before publication:

- Live mode allowed `--allow-missing-audit-dir`, which could skip audit evidence. Removed the flag and made live audit evidence mandatory.
- Fixture `args_hmac` covered only the tool name. Updated fixture audit entries to HMAC the tool plus request arguments without storing raw arguments, and added test coverage that confirms the PII string is not written to audit evidence.
