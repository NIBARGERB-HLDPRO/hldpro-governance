---
date: 2026-04-15
sprint: 4
epic: Windows-Ollama SoM Tier-2 integration
phase: 2
deliverable: CI workflows for audit schema + exposure validation
approver: nibargerb
approval_date: 2026-04-15
status: complete
artifacts:
  - .github/workflows/check-windows-ollama-audit-schema.yml
  - .github/workflows/check-windows-ollama-exposure.yml
  - STANDARDS.md (enforcement-index rows 16-17)
  - docs/exception-register.md (SOM-WIN-OLLAMA-AUDIT-001 scope-reduce)
  - raw/cross-review/2026-04-15-windows-ollama-sprint4.md
  - raw/gate/2026-04-15-windows-ollama-sprint4.md
qa_verdict: APPROVED
cross_review_verdict: APPROVED
gate_verdict: PASS
merge_commit: (to be set on merge)
---

# Sprint 4 Closeout — Windows-Ollama CI Workflows

## Scope Completed

### check-windows-ollama-audit-schema.yml
- Triggers: PRs touching `raw/remote-windows-audit/**`, `scripts/windows-ollama/audit.py`, or `scripts/windows-ollama/verify_audit.py`; workflow_dispatch
- Runs `python3 scripts/windows-ollama/verify_audit.py raw/remote-windows-audit/`
- No-ops cleanly (exit 0) when audit directory doesn't exist (deferred to Sprint 5 activation)
- Enforces invariant #10 (audit hash-chain + HMAC + manifest)

### check-windows-ollama-exposure.yml
- Triggers: PRs touching `docs/runbooks/windows-ollama-worker.md`, `scripts/windows-ollama/**`, or `STANDARDS.md`; workflow_dispatch
- Asserts: no public-bind indicators (0.0.0.0, --host 0.0.0.0), endpoint remains 172.17.227.49:11434, Cloudflare Tunnel remains stubbed
- Enforces invariant #9 (Windows-Ollama LAN-only binding)

### STANDARDS.md enforcement-index
- Added row 16: Windows-Ollama audit schema validation via check-windows-ollama-audit-schema.yml
- Added row 17: Windows-Ollama firewall exposure validation via check-windows-ollama-exposure.yml

### docs/exception-register.md
- Scope-reduced SOM-WIN-OLLAMA-AUDIT-001: "Partially closed — CI enforcement live as of Sprint 4; full close deferred to Sprint 5 activation."

## Acceptance Criteria (All Met)

1. ✓ check-windows-ollama-audit-schema.yml implemented and self-green
2. ✓ check-windows-ollama-exposure.yml implemented and self-green
3. ✓ Both workflows registered in STANDARDS.md enforcement-index
4. ✓ SOM-WIN-OLLAMA-AUDIT-001 scope-reduced with CI-live marker
5. ✓ Both workflows pass on this branch
6. ✓ YAML syntax valid (verified with PyYAML)
7. ✓ All governance tiers pass (QA APPROVED, cross-review APPROVED, gate PASS)

## Governance Artifacts

- Cross-review: `raw/cross-review/2026-04-15-windows-ollama-sprint4.md` — APPROVED
- Gate: `raw/gate/2026-04-15-windows-ollama-sprint4.md` — PASS
- Model fallback: `raw/model-fallbacks/2026-04-15-windows-ollama-sprint4.log` — Sonnet-4-6 (spark blocked)

## Next Steps

Sprint 5 will activate the Tier-2 ladder rung by:
- Flipping Windows rung from "documented / disabled" to ACTIVE
- Deploying the decide.sh routing script
- Closing all 3 Sprint 1 exceptions (PII-001, AUDIT-001, DISABLED-001)
- Running integration tests against live Windows host

Until then, Windows-Ollama remains off the active routing ladder.
