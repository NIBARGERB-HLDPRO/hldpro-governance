# ModelNotAllowedError

> God node · 44 connections · `hldpro-governance/scripts/windows-ollama/submit.py`

## Connections by Relation

### calls
- [[.submit()]] `INFERRED`

### contains
- [[submit.py]] `EXTRACTED`

### inherits
- [[Exception]] `EXTRACTED`

### method
- [[.__init__()]] `EXTRACTED`
- [[.to_dict()]] `EXTRACTED`

### rationale_for
- [[Raised when model is not in allowlist.]] `EXTRACTED`

### uses
- [[AuditWriter]] `INFERRED`
- [[TestAuditIntegration]] `INFERRED`
- [[TestPiiDetection]] `INFERRED`
- [[TestEndpointReachability]] `INFERRED`
- [[TestErrorStructure]] `INFERRED`
- [[TestModelAllowlist]] `INFERRED`
- [[TestMalformedResponse]] `INFERRED`
- [[TestEmptyRationale]] `INFERRED`
- [[Create a submitter with test config.]] `INFERRED`
- [[Negative test: PII detection.]] `INFERRED`
- [[Test that SSN pattern is detected.]] `INFERRED`
- [[Test that email pattern is detected.]] `INFERRED`
- [[Test that explicit has_pii=True triggers pii_halt.]] `INFERRED`
- [[Test that clean prompt passes PII detection.]] `INFERRED`
- [[Negative test: non-allowlisted model.]] `INFERRED`
- [[Test that non-allowlisted model is rejected.]] `INFERRED`
- [[Test that allowlisted model passes allowlist check.]] `INFERRED`
- [[Negative test: unreachable endpoint.]] `INFERRED`
- [[Test that unreachable endpoint raises appropriate error.]] `INFERRED`
- [[Test that endpoint timeout is handled.]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*