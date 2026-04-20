# PDCAR: Issue #370 Remote MCP Live Cloudflare Proof

Date: 2026-04-19
Branch: `issue-370-remote-mcp-live-cloudflare-proof-20260419`
Issue: [#370](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/370)
Epic: [#109](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109)

## Plan

Close the remaining Stage D acceptance gap for epic #109 by running the governance proof harness through the live Cloudflare Access protected tunnel, preserving only non-secret audit evidence, and documenting the Cloudflare edge settings needed for stdlib Python clients.

## Do

1. Add explicit user-agent and resolver-override controls to the Stage D runner so the proof can pass Cloudflare edge policy and local DNS propagation without changing TLS hostname/SNI.
2. Add matching optional user-agent support to the thin Remote MCP client and update the service runbook.
3. Fix live downstream service-token auth gaps in `local-ai-machine` via merged PRs #488, #490, and #492.
4. Run the Stage D proof through `remote-mcp.hldpro.com` using a temporary Cloudflare Access service token, synthetic inner JWT/HMAC keys, and the merged downstream bridge.
5. Remove the temporary Access token from policy and delete it after the run.
6. Preserve only audit JSONL and manifest evidence.

## Check

- Focused governance tests for Stage D and thin client user-agent support.
- Full downstream `services/som-mcp` suite on merged live-auth follow-up slices.
- Live Stage D proof against the Cloudflare-protected endpoint.
- Strict audit verifier against copied live evidence.
- Structured plan and execution-scope validation.
- Local CI gate and GitHub Actions.

## Adjust

The live run required three downstream hardening slices after Cloudflare Access behavior was observed at origin: Access assertion precedence, service-token identity fallback, and partial service-token identity headers. Epic #109 can close only after this evidence PR passes and the final live proof artifacts remain secret-free.

## Review

Review must confirm the proof evidence contains no Cloudflare credentials, service-token secrets, JWTs, private HMAC keys, or raw PII; that the final Stage D ACs pass; and that the temporary Cloudflare service token was removed from policy and deleted.
