# Remote mcp Verify audit

> 70 nodes · cohesion 0.05

## Key Concepts

- **stage_d_smoke.py** (19 connections) — `scripts/remote-mcp/stage_d_smoke.py`
- **verify_audit.py** (18 connections) — `scripts/remote-mcp/verify_audit.py`
- **run_stage_d()** (10 connections) — `scripts/remote-mcp/stage_d_smoke.py`
- **live_health_monitor.py** (9 connections) — `scripts/remote-mcp/live_health_monitor.py`
- **verify_audit_dir()** (9 connections) — `scripts/remote-mcp/verify_audit.py`
- **test_verify_audit.py** (8 connections) — `scripts/remote-mcp/tests/test_verify_audit.py`
- **_collect_file_errors()** (8 connections) — `scripts/remote-mcp/verify_audit.py`
- **main()** (7 connections) — `scripts/remote-mcp/stage_d_smoke.py`
- **ProofResult** (7 connections) — `scripts/remote-mcp/stage_d_smoke.py`
- **_expect()** (6 connections) — `scripts/remote-mcp/stage_d_smoke.py`
- **canonical_json()** (6 connections) — `scripts/remote-mcp/verify_audit.py`
- **compute_entry_hash()** (6 connections) — `scripts/remote-mcp/verify_audit.py`
- **compute_entry_hmac()** (6 connections) — `scripts/remote-mcp/verify_audit.py`
- **compute_sha256()** (6 connections) — `scripts/remote-mcp/verify_audit.py`
- **main()** (5 connections) — `scripts/remote-mcp/live_health_monitor.py`
- **run_fixture()** (5 connections) — `scripts/remote-mcp/stage_d_smoke.py`
- **test_stage_d_smoke.py** (5 connections) — `scripts/remote-mcp/tests/test_stage_d_smoke.py`
- **_make_chain_entries()** (5 connections) — `scripts/remote-mcp/tests/test_verify_audit.py`
- **_run_fixture()** (4 connections) — `scripts/remote-mcp/live_health_monitor.py`
- **_run_live()** (4 connections) — `scripts/remote-mcp/live_health_monitor.py`
- **_run_stdio_proof()** (4 connections) — `scripts/remote-mcp/stage_d_smoke.py`
- **_verify_audit_tamper_fails()** (4 connections) — `scripts/remote-mcp/stage_d_smoke.py`
- **_verify_audit_valid()** (4 connections) — `scripts/remote-mcp/stage_d_smoke.py`
- **test_live_health_monitor.py** (4 connections) — `scripts/remote-mcp/tests/test_live_health_monitor.py`
- **_write_audit_file()** (4 connections) — `scripts/remote-mcp/tests/test_verify_audit.py`
- *... and 45 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `scripts/remote-mcp/live_health_monitor.py`
- `scripts/remote-mcp/stage_d_smoke.py`
- `scripts/remote-mcp/tests/test_live_health_monitor.py`
- `scripts/remote-mcp/tests/test_stage_d_smoke.py`
- `scripts/remote-mcp/tests/test_verify_audit.py`
- `scripts/remote-mcp/verify_audit.py`
- `scripts/windows-ollama/verify_audit.py`

## Audit Trail

- EXTRACTED: 141 (55%)
- INFERRED: 116 (45%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*