# Windows ollama Audit

> 57 nodes · cohesion 0.05

## Key Concepts

- **AuditWriter** (10 connections) — `scripts/windows-ollama/audit.py`
- **audit.py** (7 connections) — `scripts/windows-ollama/audit.py`
- **.write_entry()** (7 connections) — `scripts/windows-ollama/audit.py`
- **._write_manifest()** (7 connections) — `scripts/windows-ollama/audit.py`
- **test_audit.py** (7 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **verify_audit.py** (7 connections) — `scripts/windows-ollama/verify_audit.py`
- **verify_audit_dir()** (7 connections) — `scripts/windows-ollama/verify_audit.py`
- **._get_prev_hash()** (6 connections) — `scripts/windows-ollama/audit.py`
- **._get_today_path()** (5 connections) — `scripts/windows-ollama/audit.py`
- **._read_last_entry()** (5 connections) — `scripts/windows-ollama/audit.py`
- **canonical_json()** (5 connections) — `scripts/windows-ollama/audit.py`
- **._get_next_seq()** (4 connections) — `scripts/windows-ollama/audit.py`
- **compute_entry_hmac()** (4 connections) — `scripts/windows-ollama/audit.py`
- **compute_sha256()** (4 connections) — `scripts/windows-ollama/audit.py`
- **canonical_json()** (4 connections) — `scripts/windows-ollama/verify_audit.py`
- **compute_entry_hmac()** (4 connections) — `scripts/windows-ollama/verify_audit.py`
- **._get_today_manifest_path()** (3 connections) — `scripts/windows-ollama/audit.py`
- **TestAuditChainIntegrity** (3 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **TestFileTruncation** (3 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **TestHmacForgery** (3 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **TestManifestMismatch** (3 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **TestReplay** (3 connections) — `scripts/windows-ollama/tests/test_audit.py`
- **compute_sha256()** (3 connections) — `scripts/windows-ollama/verify_audit.py`
- **verify_hmac()** (3 connections) — `scripts/windows-ollama/verify_audit.py`
- **.test_tamper_line_breaks_chain()** (2 connections) — `scripts/windows-ollama/tests/test_audit.py`
- *... and 32 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `scripts/windows-ollama/audit.py`
- `scripts/windows-ollama/tests/test_audit.py`
- `scripts/windows-ollama/verify_audit.py`

## Audit Trail

- EXTRACTED: 114 (73%)
- INFERRED: 42 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*