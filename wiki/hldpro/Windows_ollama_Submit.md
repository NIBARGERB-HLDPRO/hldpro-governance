# Windows ollama Submit

> 84 nodes · cohesion 0.03

## Key Concepts

- **test_submit.py** (11 connections) — `scripts/windows-ollama/tests/test_submit.py`
- **AuditWriter** (10 connections) — `scripts/windows-ollama/audit.py`
- **audit.py** (7 connections) — `scripts/windows-ollama/audit.py`
- **.write_entry()** (7 connections) — `scripts/windows-ollama/audit.py`
- **._write_manifest()** (7 connections) — `scripts/windows-ollama/audit.py`
- **TestAuditIntegration** (7 connections) — `scripts/windows-ollama/tests/test_submit.py`
- **._get_prev_hash()** (6 connections) — `scripts/windows-ollama/audit.py`
- **TestPiiDetection** (6 connections) — `scripts/windows-ollama/tests/test_submit.py`
- **._get_today_path()** (5 connections) — `scripts/windows-ollama/audit.py`
- **._read_last_entry()** (5 connections) — `scripts/windows-ollama/audit.py`
- **canonical_json()** (5 connections) — `scripts/windows-ollama/audit.py`
- **TestEndpointReachability** (5 connections) — `scripts/windows-ollama/tests/test_submit.py`
- **TestErrorStructure** (5 connections) — `scripts/windows-ollama/tests/test_submit.py`
- **._get_next_seq()** (4 connections) — `scripts/windows-ollama/audit.py`
- **compute_entry_hmac()** (4 connections) — `scripts/windows-ollama/audit.py`
- **compute_sha256()** (4 connections) — `scripts/windows-ollama/audit.py`
- **TestEmptyRationale** (4 connections) — `scripts/windows-ollama/tests/test_submit.py`
- **TestMalformedResponse** (4 connections) — `scripts/windows-ollama/tests/test_submit.py`
- **TestModelAllowlist** (4 connections) — `scripts/windows-ollama/tests/test_submit.py`
- **._get_today_manifest_path()** (3 connections) — `scripts/windows-ollama/audit.py`
- **submitter()** (2 connections) — `scripts/windows-ollama/tests/test_submit.py`
- **.test_audit_entry_on_endpoint_unreachable()** (2 connections) — `scripts/windows-ollama/tests/test_submit.py`
- **.test_audit_entry_on_explicit_pii_flag()** (2 connections) — `scripts/windows-ollama/tests/test_submit.py`
- **.test_audit_entry_on_model_not_allowed()** (2 connections) — `scripts/windows-ollama/tests/test_submit.py`
- **.test_audit_entry_on_pii_detection()** (2 connections) — `scripts/windows-ollama/tests/test_submit.py`
- *... and 59 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `scripts/windows-ollama/audit.py`
- `scripts/windows-ollama/tests/test_submit.py`

## Audit Trail

- EXTRACTED: 169 (85%)
- INFERRED: 30 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*