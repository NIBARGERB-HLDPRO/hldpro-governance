---
date: 2026-04-15
decision: Windows-Ollama CI workflows approved and merged
status: implemented
epic: Windows-Ollama SoM Tier-2 integration
phase: 2
sprint: 4
---

# Sprint 4: Windows-Ollama CI Enforcement Workflows Live

## Decision

Merged two CI workflows (`check-windows-ollama-audit-schema.yml` and `check-windows-ollama-exposure.yml`) to enforce invariants #9 and #10 for Windows-Ollama before the Tier-2 ladder rung is activated in Sprint 5.

## Rationale

The Windows-Ollama endpoint is a high-risk fallback (on-premises GPU, unencrypted LAN, minimal auth). Invariants #9 (firewall binding) and #10 (audit trail) require CI gates to prevent accidental misconfig. Both gates are now live:

- **Audit schema check**: validates hash-chain integrity, HMAC signatures, and daily manifests on any PR touching audit files
- **Exposure check**: prevents public-bind indicators, endpoint URL drift, or removal of Cloudflare stub status

## Impact

- **SOM enforcement**: 2 new rows (16–17) in enforcement-index; no orphan rules
- **Exception handling**: SOM-WIN-OLLAMA-AUDIT-001 scope-reduced; CI now enforces #10
- **Activation status**: Windows rung remains **documented / disabled** until Sprint 5 merges the decision script (`decide.sh`)
- **Self-green**: both workflows pass on this PR; safe to merge and run in CI

## Next Phase

Sprint 5 will complete the activation flow by:
1. Implementing `decide.sh` (routes between local daemon / Windows / cloud / halt)
2. Flipping Windows rung from disabled → ACTIVE
3. Closing all 3 deferral exceptions
4. Running end-to-end integration tests

Reference: [SoM Charter §Windows Host Inference](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/blob/main/STANDARDS.md#windows-host-inference-tier-2-fallback)
