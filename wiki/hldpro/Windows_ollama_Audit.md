# Windows ollama Audit

> 45 nodes · cohesion 0.06

## Key Concepts

- **AuditWriter** (10 connections) — `scripts/windows-ollama/audit.py`
- **audit.py** (7 connections) — `scripts/windows-ollama/audit.py`
- **.write_entry()** (7 connections) — `scripts/windows-ollama/audit.py`
- **._write_manifest()** (7 connections) — `scripts/windows-ollama/audit.py`
- **test_audit.py** (7 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **._get_prev_hash()** (6 connections) — `scripts/windows-ollama/audit.py`
- **._get_today_path()** (5 connections) — `scripts/windows-ollama/audit.py`
- **._read_last_entry()** (5 connections) — `scripts/windows-ollama/audit.py`
- **canonical_json()** (5 connections) — `scripts/windows-ollama/audit.py`
- **._get_next_seq()** (4 connections) — `scripts/windows-ollama/audit.py`
- **compute_entry_hmac()** (4 connections) — `scripts/windows-ollama/audit.py`
- **compute_sha256()** (4 connections) — `scripts/windows-ollama/audit.py`
- **._get_today_manifest_path()** (3 connections) — `scripts/windows-ollama/audit.py`
- **TestAuditChainIntegrity** (3 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **TestFileTruncation** (3 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **TestHmacForgery** (3 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **TestManifestMismatch** (3 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **TestReplay** (3 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **.test_tamper_line_breaks_chain()** (2 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **.test_file_truncation_detected()** (2 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **.test_hmac_forgery_detected()** (2 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **.test_manifest_first_hash_mismatch()** (2 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **.test_duplicate_line_detected()** (2 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **.__init__()** (1 connections) — `scripts/windows-ollama/audit.py`
- **Write an audit entry. Returns True if successful, False otherwise.          Args** (1 connections) — `scripts/windows-ollama/audit.py`
- *... and 20 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `scripts/windows-ollama/audit.py`
- `scripts/windows-ollama/tests/test_audit.py`

## Audit Trail

- EXTRACTED: 91 (75%)
- INFERRED: 30 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*