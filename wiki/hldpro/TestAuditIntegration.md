# TestAuditIntegration

> God node · 11 connections · `hldpro-governance/scripts/windows-ollama/tests/test_submit.py`

## Connections by Relation

### contains
- [[test_submit.py]] `EXTRACTED`

### method
- [[.test_audit_entry_on_success()]] `EXTRACTED`
- [[.test_audit_entry_on_pii_detection()]] `EXTRACTED`
- [[.test_audit_entry_on_explicit_pii_flag()]] `EXTRACTED`
- [[.test_audit_entry_on_model_not_allowed()]] `EXTRACTED`
- [[.test_audit_entry_on_endpoint_unreachable()]] `EXTRACTED`

### rationale_for
- [[Verify that all submission paths write exactly one audit entry.]] `EXTRACTED`

### uses
- [[WindowsOllamaSubmitter]] `INFERRED`
- [[EndpointUnreachableError]] `INFERRED`
- [[ModelNotAllowedError]] `INFERRED`
- [[PiiDetectionError]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*