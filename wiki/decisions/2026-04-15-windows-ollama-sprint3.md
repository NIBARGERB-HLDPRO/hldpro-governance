# Decision: Windows-Ollama Audit Trail (Sprint 3)

**Date:** 2026-04-15  
**Decision ID:** WINDOWS-OLLAMA-AUDIT-001  
**Epic:** [#99 Society of Minds](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/99) → [#117 Windows-Ollama Stage Sprint 3](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/117)  
**Related SoM Charter:** STANDARDS.md § Society of Minds

## Summary

Windows-Ollama Tier-2 Worker submissions now emit tamper-evident audit trails with hash-chain integrity, per-entry HMAC-SHA256 signatures, and daily manifest validation. The audit system mirrors the Remote MCP Bridge audit format and allows both real-time and forensic verification of submission integrity.

## Decision

**All submission paths to Windows-Ollama must write exactly one audit entry to `raw/remote-windows-audit/YYYY-MM-DD.jsonl` with:**

1. **Sequence**: Monotonic from 0 within each day
2. **Hash chain**: prev_hash = SHA256(previous_entry_canonical_json); entry 0 = zero
3. **HMAC signing**: entry_hmac = HMAC-SHA256(key, entry_canonical_json) over all fields except entry_hmac itself
4. **Daily manifest**: `YYYY-MM-DD.manifest.json` with first_hash, last_hash, entry_count, sha256_of_file
5. **File integrity**: 0o600 permissions; append-only flag where OS supports
6. **Submission metadata**: ts, principal, session_jti, tool, status, reject_reason, latency_ms

## Rationale

### Tamper Detection

Hash-chain (prev_hash) ensures any deletion, reordering, or line modification breaks the chain. Seq monotonicity prevents replay attacks. HMAC prevents entry forgery. Manifest consistency check validates completeness without re-reading entire log.

### SoM Integration

This decision implements the "hard-rule invariant #5" from STANDARDS.md § Society of Minds: "All Tier-2 submission paths write audit entries." The audit trail feeds the SoM Reviewer tier (Tier-3) for post-hoc verification of Worker behavior.

### Real-Time + Forensic Verification

- **Real-time**: verify_audit.py CLI can validate daily logs at any time
- **Forensic**: Hash-chain and HMAC preserve evidence of tampering; CI workflows can enforce manifest consistency as a hard gate

### Graceful Degradation

- If HMAC key not available, audit continues with null fields (schema preserved)
- If append-only flag not supported, logs default to regular file (still append-only via OS buffer semantics)
- Tests disable append-only to allow rewrites; production enables it

## Specification

### Entry Schema

```json
{
  "ts": "2026-04-15T04:40:03.045Z",
  "seq": 0,
  "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "principal": "<sub>",
  "session_jti": "<jti>",
  "tool": "windows-ollama.submit",
  "args_hmac": "hmac-sha256(key, canonical_json(args))",
  "status": "ok|rejected|error",
  "reject_reason": "pii_detected|model_not_allowed|endpoint_unreachable|...",
  "latency_ms": 42,
  "entry_hmac": "hmac-sha256(key, canonical_json(entry_without_entry_hmac))"
}
```

### Canonical JSON

```python
json.dumps(obj, sort_keys=True, separators=(',',':'), ensure_ascii=False).encode('utf-8')
```

### Daily Manifest

```json
{
  "first_hash": "sha256_of_first_entry_canonical_json",
  "last_hash": "sha256_of_last_entry_canonical_json",
  "entry_count": 42,
  "sha256_of_file": "sha256_of_entire_jsonl_file"
}
```

### Submission Paths

| Path | Status | reject_reason | Example |
|------|--------|---------------|---------|
| Success | ok | null | Generated response returned |
| PII (explicit) | rejected | explicit_pii_flag | has_pii=True |
| PII (detected) | rejected | pii_detected | Pattern match in prompt |
| Model denied | rejected | model_not_allowed | Model not in allowlist |
| Endpoint error | error | endpoint_unreachable | Connection refused |

## Implementation

- **audit.py**: AuditWriter class (append-only JSONL + manifest writer)
- **verify_audit.py**: Standalone verifier (CLI tool for validation)
- **submit.py integration**: Calls audit.write_entry() on all paths
- **test_audit.py**: 5 negative tests (tamper detection, HMAC forgery, manifest mismatch, truncation, replay)
- **test_submit.py**: 5 audit integration tests (coverage of all submission paths)

## Dependencies

- Python 3.11+
- Stdlib only (hashlib, hmac, json, pathlib, datetime)
- HMAC key from env `SOM_WINDOWS_AUDIT_HMAC_KEY` (optional; graceful bypass if absent)

## Success Criteria

- ✓ All submission paths emit exactly one audit entry
- ✓ Hash-chain validates (no tampering detected in passing tests)
- ✓ HMAC validates (forgery detected in negative tests)
- ✓ Manifest validates (file completeness verified)
- ✓ 100% test coverage of all paths (21/21 pytest + 5/5 negative tests)
- ✓ CI green on merge

## References

- Remote MCP Bridge audit spec: `raw/inbox/2026-04-14-remote-mcp-bridge-plan.md` (§107-132)
- SoM hard-rule invariants: STANDARDS.md § Society of Minds (invariant #5)
- Sprint 3 PR: [#118](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/pull/118)
- Closeout: `raw/closeouts/2026-04-15-windows-ollama-sprint3.md`

## Related Decisions

- [#99 Society of Minds Epic](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/99) — Tier routing and cross-family validation
- [#106 Packet Schema + Validator](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/102) — Deterministic handoff validation
- [#117 Windows-Ollama Sprint 3](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/117) — This decision

## Transition Plan

**Sprint 4** (PII scrubbing handler): Will consume audit entries to identify high-frequency PII patterns for retraining pii_patterns.yml.

**Sprint 5** (Tier-2 ladder): Will use audit entries as evidence for Worker promotion/demotion decisions.
