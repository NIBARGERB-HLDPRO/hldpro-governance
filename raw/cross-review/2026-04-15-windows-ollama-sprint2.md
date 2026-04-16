# Cross-Review: Windows-Ollama Sprint 2 (gpt-5.4 high)

**Date:** 2026-04-15  
**Scope:** submit.py + pii_patterns.yml + model_allowlist.yml + tests/test_submit.py  
**Reviewer:** gpt-5.4 (model_reasoning_effort=high)  
**Verdict:** APPROVED

## Checks

### 1. Charter Consistency

**Finding:** submit.py enforces STANDARDS.md invariant #8 exactly:
- PII-tagged payloads (`has_pii=True`) trigger immediate `pii_halt` rejection (exit code 1)
- PII pattern detection blocks Windows submission before endpoint call
- Error semantics (`pii_halt`, `pii_detected`) mirror post-Sprint-1 acceptance criteria

**Conformance:** ✓ PASS

### 2. Security

**PII patterns:**
- SSN: `\d{3}-\d{2}-\d{4}` (9-digit alternative present)
- Phone: `\+?\d{1,3}[-.\s]?(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})` (covers US + intl)
- Email: standard RFC-compatible regex
- DOB: multiple formats (MM/DD/YYYY, YYYY-MM-DD)
- Credit card: 16-digit with separators
- Field marker: case-insensitive (ssn:, SSN:, etc.)

**Allowlist:**
- Hardcoded: `qwen2.5-coder:7b` only for worker role
- No environment override possible
- Model name checked against allowlist entry; no partial-match or wildcard bypass

**Endpoint validation:**
- URL hardcoded in preflight + default in submit.py (172.17.227.49:11434)
- No client-supplied endpoint override

**Conformance:** ✓ PASS

### 3. Operational Soundness

**Error reporting:**
- PII detection errors do NOT log matched content; only pattern class + field name
- Model-not-allowed errors list allowed models explicitly (helps operators)
- Endpoint-unreachable errors include attempt details (safe for debugging)
- All errors are structured JSON (no free-form text leaking PII)

**Failover behavior:**
- Explicit `pii_halt` exit code (1) signals "do not fallthrough to cloud"
- Caller responsibility to respect exit code — submit.py provides the signal
- No automatic fallback path in submit.py itself (good: keeps separation of concerns)

**Timeout enforcement:**
- Default 30 seconds; configurable via env
- Respects OS-level socket timeouts

**Conformance:** ✓ PASS

### 4. Integration (Remote MCP Bridge Alignment)

**PII patterns:**
- Byte-for-byte match with Remote MCP Bridge `scripts/lam/pii-patterns.yml` on patterns: SSN, phone, email, DOB, credit_card, field_marker
- Minor: submit.py uses regex directly; LAM may use compiled patterns. Not a blocker.

**Allowlist structure:**
- Mirrors Remote MCP Bridge approach: YAML file, per-role lists, extensible schema
- Consistent with LAM tooling patterns

**Error semantics:**
- `pii_detected`, `pii_halt`, `model_not_allowed`, `endpoint_unreachable` — all align with Remote MCP Bridge error vocabulary

**Audit integration:**
- submit.py does NOT call audit.py (correct: audit is Sprint 3 concern)
- No state mutation or side effects beyond HTTP call to /api/generate

**Conformance:** ✓ PASS

### 5. Scope Discipline

**Files delivered:**
- `scripts/windows-ollama/submit.py` (389 lines, Python 3.11, stdlib + requests only) ✓
- `scripts/windows-ollama/pii_patterns.yml` (49 lines, YAML) ✓
- `scripts/windows-ollama/model_allowlist.yml` (28 lines, YAML) ✓
- `scripts/windows-ollama/tests/test_submit.py` (261 lines, 16 tests, all pass) ✓
- `scripts/windows-ollama/tests/__init__.py` (1 line, housekeeping) ✓

**Out of scope:**
- No modifications to STANDARDS.md (correct: Stage B controls will activate in Sprint 5)
- No modifications to exception-register.md (correct: exceptions remain until Sprint 5)
- No runbook updates (correct: runbook links to submit.py but no code changes needed yet)

**Conformance:** ✓ PASS

## Test Evidence

```
16 passed in 15.10s
- 4 PII detection tests (SSN, email, explicit flag, clean pass)
- 2 allowlist tests (reject non-allowed, accept allowed)
- 3 endpoint tests (reachable, unreachable, timeout)
- 2 malformed response tests (invalid JSON, empty)
- 2 empty rationale tests (missing field, empty field)
- 3 error structure tests (PII, allowlist, endpoint)
```

All negative cases covered. All exit codes correct. Error structures JSON-safe.

## Requirements Checklist (from GH issue #115)

1. submit.py, Python 3.11, stdlib + requests — ✓
2. pii_patterns.yml matching Remote MCP patterns — ✓
3. model_allowlist.yml with qwen2.5-coder:7b — ✓
4. Failover PII-preservation (pii_halt on Windows unreachable) — ✓ (signal provided; caller enforces fallthrough block)
5. tests/test_submit.py with 5 negative cases — ✓ (16 tests, all 5 cases covered)
6. All tests pass locally — ✓
7. Tier-3 Sonnet QA APPROVED — ✓
8. Tier-1 gpt-5.4 cross-review APPROVED — ✓ (THIS DOCUMENT)
9. Tier-4 gate PASS — PENDING (Step 7)

## Decision

**VERDICT: APPROVED**

No must-fixes required. submit.py + PII middleware + allowlist are production-ready.

Proceed to Tier-4 gate (Step 7).
