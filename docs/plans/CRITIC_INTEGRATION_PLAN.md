# HLDPRO Critic Integration — Comprehensive Implementation Plan

**Version:** 1.0
**Date:** 2026-04-09
**Author:** Claude (drafted) + operator (review)
**Scope:** From the current state (Phase 0.5 just shipped) to full integration across HP-App, AIS, and the eventual hosted critic infrastructure.
**Status:** Authoritative roadmap. Each phase has its own runbook for execution.

---

## Execution Status (updated 2026-04-09)

| Phase | Status | Evidence |
|---|---|---|
| 0 | ✅ DONE | PRs #398, #399 merged |
| 0.75 | ✅ DONE | PR #400 merged |
| 0.5 | ✅ DONE | PR #408 + alignment commit merged |
| 1 | ✅ DONE | PR #410 merged, issue #411 closed |
| 1.5 (minimal) | ✅ DONE | PR #410 merged, issue #412 closed. Regex-based redactor, not full shared package. |
| 1.5 (full) | PLANNED | Shared Safe Harbor scrubber package with Presidio + deny-list + allow-list layers |
| 2 | **NEXT** | AIS pilot — unblocked |
| 2.5+ | Planned | See roadmap below |

### Delta: what shipped vs what the plan describes

**Phase 1 shipped items:**
- ✅ `phi_redaction_gate` mask + `caller_mask_policy.json`
- ✅ `diff_mode_synthesizer.py` wrapping `generate_stub_bundle.py`
- ✅ `mode=diff` dispatch in `/v2/critic/evaluate` (before `apply_token_budget`)
- ✅ SQL migration `036_gh_issue_url.sql`
- ✅ `critic_issue_creator.py` with `subprocess.run(shell=False)`
- ✅ 31 contract tests (18 Phase 1 + 13 Phase 1.5)
- ✅ Critic labels created in local-ai-machine
- ✅ Governance docs updated
- ⬜ `scripts/clients/critic_call.sh` consumer wrapper — deferred to Phase 2
- ⬜ Pinned diff fixtures (tiny-APPROVED, REJECTED, over-budget, malformed, PHI-shaped) — partial

**Phase 1.5 shipped items (minimal):**
- ✅ `phi_redactor.py` — regex-based (SSN, MRN, DOB, email, phone, facility ID)
- ✅ `redaction_attestation.schema.json`
- ✅ Wired into synthesizer for HP-App callers
- ⬜ Full shared Safe Harbor package (Presidio, deny-list, allow-list, hard-fail layer) — Phase 1.5 full
- ⬜ Package published to governance — Phase 1.5 full

---
