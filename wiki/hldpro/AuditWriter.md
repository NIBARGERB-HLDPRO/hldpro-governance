# AuditWriter

> God node · 28 connections · `hldpro-governance/scripts/windows-ollama/audit.py`

## Connections by Relation

### contains
- [[audit.py]] `EXTRACTED`

### method
- [[.write_entry()]] `EXTRACTED`
- [[._write_manifest()]] `EXTRACTED`
- [[._get_prev_hash()]] `EXTRACTED`
- [[._get_today_path()]] `EXTRACTED`
- [[._read_last_entry()]] `EXTRACTED`
- [[._get_next_seq()]] `EXTRACTED`
- [[._get_today_manifest_path()]] `EXTRACTED`
- [[.__init__()]] `EXTRACTED`

### rationale_for
- [[Append-only audit log writer with hash-chain and daily manifest.]] `EXTRACTED`

### uses
- [[WindowsOllamaSubmitter]] `INFERRED`
- [[PiiDetectionError]] `INFERRED`
- [[ModelNotAllowedError]] `INFERRED`
- [[EndpointUnreachableError]] `INFERRED`
- [[Submit requests to Windows-Ollama endpoint with PII detection and allowlist enfo]] `INFERRED`
- [[Initialize the submitter.          Args:             endpoint: Windows-Ollama en]] `INFERRED`
- [[Load PII patterns from pii_patterns.yml.]] `INFERRED`
- [[Load model allowlist from model_allowlist.yml.]] `INFERRED`
- [[Scan text for PII patterns.          Returns: pattern name if detected, None oth]] `INFERRED`
- [[Verify model is in allowlist for the specified role.]] `INFERRED`
- [[Submit a request to Windows-Ollama.          Args:             model: Model name]] `INFERRED`
- [[POST to /api/generate and return response.]] `INFERRED`
- [[Raised when PII is detected or explicitly marked.]] `INFERRED`
- [[Return structured error dict for JSON output.]] `INFERRED`
- [[Raised when model is not in allowlist.]] `INFERRED`
- [[Return structured error dict for JSON output.]] `INFERRED`
- [[Raised when Windows-Ollama endpoint is unreachable.]] `INFERRED`
- [[Return structured error dict for JSON output.]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*