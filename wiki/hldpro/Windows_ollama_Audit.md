# Windows ollama Audit

> 33 nodes · cohesion 0.07

## Key Concepts

- **test_audit.py** (7 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **verify_audit.py** (7 connections) — `hldpro-governance/scripts/windows-ollama/verify_audit.py`
- **verify_audit_dir()** (7 connections) — `hldpro-governance/scripts/windows-ollama/verify_audit.py`
- **canonical_json()** (4 connections) — `hldpro-governance/scripts/windows-ollama/verify_audit.py`
- **compute_entry_hmac()** (4 connections) — `hldpro-governance/scripts/windows-ollama/verify_audit.py`
- **TestAuditChainIntegrity** (3 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **TestFileTruncation** (3 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **TestHmacForgery** (3 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **TestManifestMismatch** (3 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **TestReplay** (3 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **compute_sha256()** (3 connections) — `hldpro-governance/scripts/windows-ollama/verify_audit.py`
- **verify_hmac()** (3 connections) — `hldpro-governance/scripts/windows-ollama/verify_audit.py`
- **.test_tamper_line_breaks_chain()** (2 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **.test_file_truncation_detected()** (2 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **.test_hmac_forgery_detected()** (2 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **.test_manifest_first_hash_mismatch()** (2 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **.test_duplicate_line_detected()** (2 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **main()** (2 connections) — `hldpro-governance/scripts/windows-ollama/verify_audit.py`
- **Modify first_hash in manifest and verify fails.** (1 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **Test that truncated file (missing last line) breaks manifest.** (1 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **Delete last line and verify detects entry_count mismatch.** (1 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **Test that duplicate line (replay) breaks seq monotonicity.** (1 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **Duplicate a line and verify detects non-monotonic seq.** (1 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **Test that tampering with a line breaks the chain.** (1 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- **Tamper with line N and verify fails at line N+1.** (1 connections) — `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- *... and 8 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `hldpro-governance/scripts/windows-ollama/tests/test_audit.py`
- `hldpro-governance/scripts/windows-ollama/verify_audit.py`

## Audit Trail

- EXTRACTED: 65 (84%)
- INFERRED: 12 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*