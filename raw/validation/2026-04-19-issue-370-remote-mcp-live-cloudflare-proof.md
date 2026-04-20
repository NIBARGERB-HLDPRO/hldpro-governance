# Validation: Issue #370 Remote MCP Live Cloudflare Proof

Date: 2026-04-19
Branch: `issue-370-remote-mcp-live-cloudflare-proof-20260419`
Issue: hldpro-governance #370
Epic: hldpro-governance #109

## Live Route

The final proof targeted the dedicated Cloudflare Access protected Remote MCP hostname and the existing named tunnel route to local `127.0.0.1:18082`.

Live setup used:

- A temporary Cloudflare Access service token added to the dedicated Access policy for the proof window only.
- Merged downstream `local-ai-machine` commit `1a7af59` from PR #492, after PRs #488 and #490.
- Merged governance Stage D harness with `SOM_REMOTE_MCP_USER_AGENT` and `SOM_REMOTE_MCP_RESOLVE_IP` configured for Cloudflare edge behavior and local DNS propagation.
- Synthetic inner JWT/HMAC keys used only for this proof evidence.
- Operator venv Python for the local bridge and stdio import proof.

Cleanup result:

- Temporary service token removed from policy: PASS.
- Temporary service token deleted: PASS.

## Live Stage D Results

`python3 scripts/remote-mcp/stage_d_smoke.py --json` passed through the Cloudflare route.

Recorded result summary:

- `authenticated-ping`: pass, status 200.
- `anonymous-rejected`: pass, status 403.
- `origin-spoof-non-authoritative`: pass, status 400.
- `pii-handoff-rejected`: pass, status 400.
- `scrub-pii-remote-rejected`: pass, status 400.
- `audit-valid`: pass.
- `audit-tamper-negative`: pass; copied tamper changed sequence, hash-chain, HMAC, manifest first hash, and manifest file hash.
- `stdio-after-tunnel-stop`: pass for local stdio import proof.

Strict copied-audit verifier:

```bash
SOM_REMOTE_MCP_AUDIT_HMAC_KEY="<synthetic-proof-key>" \
  python3 scripts/remote-mcp/verify_audit.py raw/remote-mcp-live-cloudflare-e2e --require-hmac-key
```

Result: PASS.

## Preserved Evidence

- `raw/remote-mcp-live-cloudflare-e2e/2026-04-20.jsonl`
- `raw/remote-mcp-live-cloudflare-e2e/2026-04-20.manifest.json`

The evidence date is UTC because the bridge audit writer uses UTC dates; the operator session date was 2026-04-19 America/Chicago.

Evidence scan notes:

- Audit rows contain metadata and HMAC digests only.
- No raw PII payload is present.
- No Cloudflare API token, Access service-token secret, JWT, or private HMAC key is committed.
- Temporary Cloudflare token values were kept in process memory only and deleted after proof.

## Downstream Live Auth Follow-Ups

Live Cloudflare behavior required these merged `local-ai-machine` fixes before the final proof passed:

- PR #488: prefer inner `Authorization: Bearer ...` over Cloudflare Access assertion material.
- PR #490: allow service-token Access to use verified inner JWT claims when user email/id headers are absent.
- PR #492: tolerate partial service-token identity headers when Access preserves user id but strips user email.

Downstream validation:

- PR #488 GitHub Actions passed before merge.
- PR #490 GitHub Actions passed before merge.
- PR #492 GitHub Actions passed before merge.
- Full local `services/som-mcp` suite passed with 56 tests after PR #492.

## Governance Validation

- `python3 -m pytest scripts/remote-mcp/tests/test_verify_audit.py scripts/remote-mcp/tests/test_stage_d_smoke.py scripts/som-client/tests/test_som_client.py`
- `python3 -m py_compile scripts/remote-mcp/verify_audit.py scripts/remote-mcp/stage_d_smoke.py scripts/som-client/som_client.py`
- `python3 -m json.tool docs/plans/issue-370-remote-mcp-live-cloudflare-proof-structured-agent-cycle-plan.json`
- `python3 -m json.tool raw/execution-scopes/2026-04-19-issue-370-remote-mcp-live-cloudflare-proof-implementation.json`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --require-if-issue-branch --branch-name issue-370-remote-mcp-live-cloudflare-proof-20260419`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-370-remote-mcp-live-cloudflare-proof-implementation.json`
- `bash hooks/closeout-hook.sh raw/closeouts/2026-04-19-issue-370-remote-mcp-live-cloudflare-proof.md`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`

Final command outputs are recorded by local execution and PR checks.

Closeout hook result: PASS. It refreshed `graphify-out/hldpro-governance/` and `wiki/`, skipped memory writer because credentials are not configured locally, and committed the closeout artifact.

Focused tests: PASS, 10 tests.

Local CI result: PASS. Report directory: `cache/local-ci-gate/reports/20260420T001454Z-hldpro-governance-git`.
