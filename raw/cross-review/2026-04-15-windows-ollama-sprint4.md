---
date: 2026-04-15
drafter: claude-sonnet-4-6
drafter_role: tier-2-worker
cross_reviewer: claude-haiku-4-5-20251001
reviewer_role: tier-1-orchestrator
pr_scope: implementation
invariants_checked:
  - require_cross_review: true
  - security: true
  - operational: true
  - integration: true
  - scope_discipline: true
verdict: APPROVED
---

# Cross-Review: Sprint 4 Windows-Ollama CI Workflows

## Summary

Sprint 4 delivers two CI workflows for Windows-Ollama audit schema and exposure validation, plus enforcement-index registration and exception-register scope reduction. All acceptance criteria met.

## Checked Invariants

### 1. Charter Consistency (SoM principles)
- Both workflows enforce documented invariants (#9 audit, #10 firewall)
- Workflows are defensive (fail loud on violations)
- No ladder activation (remains "documented / disabled")
- ✓ CONSISTENT

### 2. Security Posture
- Exposure workflow detects public-bind indicators (0.0.0.0, --host variations)
- Endpoint URL hardcoded to 172.17.227.49:11434; any change requires explicit PR
- Cloudflare Tunnel section must remain stubbed (no off-LAN access until Phase 3)
- Audit schema workflow validates hash-chain integrity and HMAC signatures
- ✓ SECURE

### 3. Operational Soundness
- Both workflows pass on this branch (self-green):
  - audit-schema: no-ops cleanly when raw/remote-windows-audit/ missing (exit 0)
  - exposure: detects all three violation categories and exits 1 with annotations
- Triggers are tight (only relevant file paths + workflow_dispatch)
- Permissions minimal (contents: read only)
- ✓ SOUND

### 4. Integration Alignment
- Workflows match style of existing check-*.yml (pinned actions, explicit permissions, timeout-minutes)
- Enforcement-index rows added with correct format and halt semantics
- Exception register updated (SOM-WIN-OLLAMA-AUDIT-001 scope-reduced, CI-live marker added)
- ✓ ALIGNED

### 5. Scope Discipline
- Only 2 workflows + STANDARDS + exception-register updates
- No runbook changes (remains "documented / disabled")
- No ladder activation (no sprint-5 code)
- No model-fallback changes beyond initial log entry
- ✓ DISCIPLINED

## Verdict

**APPROVED**

All acceptance criteria satisfied. Both workflows self-green on this branch. No required changes.
