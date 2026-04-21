# Som mcp Som mcp Remote

> 77 nodes · cohesion 0.06

## Key Concepts

- **RemoteMcpBridge** (20 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_bridge.py`
- **test_remote_bridge.py** (15 connections) — `local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- **authenticate()** (15 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_auth.py`
- **BridgeConfig** (12 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_bridge.py`
- **.handle_call()** (12 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_bridge.py`
- **AuditWriter** (10 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- **PrincipalRateLimiter** (10 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_rate_limit.py`
- **test_remote_bridge_http_e2e_positive_and_negative_paths()** (10 connections) — `local-ai-machine/services/som-mcp/tests/test_remote_bridge_e2e.py`
- **AuthError** (9 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_auth.py`
- **remote_auth.py** (8 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_auth.py`
- **remote_bridge.py** (8 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_bridge.py`
- **remote_pii.py** (8 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_pii.py`
- **.record()** (8 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- **test_audit_failure_blocks_dispatch()** (8 connections) — `local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- **test_bridge_writes_stage_a_compatible_audit_chain()** (8 connections) — `local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- **_token()** (8 connections) — `local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- **remote_audit.py** (7 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- **load_patterns()** (7 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_pii.py`
- **_bridge()** (7 connections) — `local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- **_headers()** (7 connections) — `local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- **AuditConfigError** (6 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- **._write_manifest()** (6 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- **compute_entry_hash()** (6 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- **build_server()** (6 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_bridge.py`
- **PiiConfigError** (6 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/remote_pii.py`
- *... and 52 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- `local-ai-machine/services/som-mcp/src/som_mcp/remote_auth.py`
- `local-ai-machine/services/som-mcp/src/som_mcp/remote_bridge.py`
- `local-ai-machine/services/som-mcp/src/som_mcp/remote_pii.py`
- `local-ai-machine/services/som-mcp/src/som_mcp/remote_rate_limit.py`
- `local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- `local-ai-machine/services/som-mcp/tests/test_remote_bridge_e2e.py`

## Audit Trail

- EXTRACTED: 264 (68%)
- INFERRED: 124 (32%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*