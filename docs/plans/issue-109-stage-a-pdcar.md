# Issue #109 Stage A PDCA/R

Date: 2026-04-19
Issue: [#109](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109)
Slice: Remote MCP Bridge Stage A governance controls

## Plan

The Remote MCP Bridge epic exposes a bounded subset of the local Society-of-Minds MCP daemon to authenticated remote CLI sessions. The preserved v2 plan requires governance-side Stage A before downstream `local-ai-machine` implementation:

- add a Remote MCP Bridge standards section and hard-rule invariants;
- provide a thin client contract for remote operator tooling;
- provide a deterministic audit-chain verifier and CI workflow;
- document operator setup, rotation, revocation, fail-closed behavior, and downstream acceptance gates;
- preserve validation and Stage 6 closeout evidence.

The preserved plan numbered Remote MCP invariants as 8-12, but current `STANDARDS.md` already uses invariants 8-10 for Windows-Ollama. This slice records the controlled deviation: Remote MCP invariants are added as 11-15 and enforcement rows as 18-22 to preserve the active Windows contract.

## Do

Implement only governance repo Stage A artifacts:

- `STANDARDS.md` Remote MCP Bridge section and invariants 11-15.
- `.github/workflows/check-remote-mcp-audit-schema.yml`.
- `scripts/remote-mcp/verify_audit.py` and focused tests.
- `scripts/som-client/som_client.py`, README, and focused tests.
- `docs/runbooks/remote-mcp-bridge.md`.
- governance mirrors: backlog, service registry, feature registry, workflow-local coverage inventory, validation, execution scope, and closeout.

Downstream HTTP server, Cloudflare tunnel, launchd plist, PII middleware, and live remote smoke remain Stage B-D under issue #109.

## Check

Required local checks:

- structured plan validation;
- issue-specific execution-scope validation;
- Remote MCP audit verifier unit/e2e tests;
- SOM client unit tests;
- workflow local coverage inventory test;
- registry surface reconciliation;
- Local CI Gate profile for `hldpro-governance`;
- Stage 6 closeout hook.

Final AC for this slice is an e2e local proof that the audit verifier accepts a valid hash-chained manifest and rejects tampering without needing live Cloudflare or downstream LAM services.

## Adjust

If the new workflow trips workflow-local coverage, update `docs/workflow-local-coverage-inventory.json` in the same slice. If local-ci detects multiple issue #109 implementation scopes, preserve the old scope as historical evidence under a non-matching filename and keep one current `issue-109` implementation scope for the active branch.

## Review

The preserved architecture artifact already records round-1 `gpt-5.4 high` rejection and the operator waiver `SOM-RMB-ROUND2-WAIVED-001`. This Stage A slice does not change the bridge architecture; it encodes that approved plan into governance controls and local deterministic tests. Issue #109 remains open after this slice for Stage B-D implementation and remote-machine security proof.
