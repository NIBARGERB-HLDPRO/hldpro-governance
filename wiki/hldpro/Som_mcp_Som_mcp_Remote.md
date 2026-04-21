# Som mcp Som mcp Remote

> 77 nodes · cohesion 0.06

## Key Concepts

- **RemoteMcpBridge** (20 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_bridge.py`
- **test_remote_bridge.py** (15 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- **authenticate()** (15 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_auth.py`
- **BridgeConfig** (12 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_bridge.py`
- **.handle_call()** (12 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_bridge.py`
- **test_remote_bridge_http_e2e_positive_and_negative_paths()** (11 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/tests/test_remote_bridge_e2e.py`
- **PrincipalRateLimiter** (10 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_rate_limit.py`
- **.record()** (9 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- **AuthError** (9 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_auth.py`
- **test_bridge_writes_stage_a_compatible_audit_chain()** (9 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- **remote_auth.py** (8 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_auth.py`
- **remote_bridge.py** (8 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_bridge.py`
- **remote_pii.py** (8 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_pii.py`
- **test_audit_failure_blocks_dispatch()** (8 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- **_token()** (8 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- **remote_audit.py** (7 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- **AuditWriter** (7 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- **load_patterns()** (7 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_pii.py`
- **_bridge()** (7 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- **_headers()** (7 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- **AuditConfigError** (6 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- **._write_manifest()** (6 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- **build_server()** (6 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_bridge.py`
- **PiiConfigError** (6 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_pii.py`
- **PiiRejected** (6 connections) — `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_pii.py`
- *... and 52 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_audit.py`
- `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_auth.py`
- `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_bridge.py`
- `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_pii.py`
- `hldpro-governance/repos/local-ai-machine/services/som-mcp/src/som_mcp/remote_rate_limit.py`
- `hldpro-governance/repos/local-ai-machine/services/som-mcp/tests/test_remote_bridge.py`
- `hldpro-governance/repos/local-ai-machine/services/som-mcp/tests/test_remote_bridge_e2e.py`

## Audit Trail

- EXTRACTED: 264 (68%)
- INFERRED: 127 (32%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*