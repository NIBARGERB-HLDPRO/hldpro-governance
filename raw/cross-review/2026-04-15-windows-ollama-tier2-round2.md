---
schema_version: v1
pr_number: 112
pr_scope: standards
round: 2
drafter:
  role: architect-claude
  model_id: claude-opus-4-6
  model_family: anthropic
  signature_date: 2026-04-15
drafter_round2:
  role: worker-claude-fallback
  model_id: claude-sonnet-4-6
  model_family: anthropic
  signature_date: 2026-04-15
reviewer:
  role: architect-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-15
  verdict: APPROVED_WITH_CHANGES
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---

## Summary

PR #112 round-2 has successfully applied all 13 must-fixes from the round-1 REJECTED verdict. The revised Stage A now documents Windows-Ollama as a disabled fallback with clear enforcement points in later sprints (Sprint 2: PII middleware, Sprint 3: audit trail, Sprint 4: CI gates, Sprint 5: activation). Charter consistency is restored: invariants 8–10 replace 13–15, enforcement rows 13–15 are added with halt semantics, and the Tier-2 ladder cell explicitly marks Windows as "documented / disabled until Sprint 5." PII floor is now hardened: invariant #8 blocks both Windows and Sonnet cloud fallback for PII payloads (LAM-only or halt). Firewall binding and audit trail are declared as hard invariants with CI enforcement. Exceptions are well-formed and properly dated. However, one acceptance criterion (AC) requires minor clarification: the runbook's Stage B acceptance criteria stub does not explicitly reference the remote-mcp-bridge plan for audit pattern matching (though it is correct that this will align in Sprint 3).

## Must-fixes applied

All 13 must-fixes from round 1 have been incorporated:

1. **Invariant numbering (8–10)** — Renumbered from 13–15. Internal references updated.
2. **Tier-2 ladder "disabled" marker** — Explicitly added: "documented / disabled until Sprint 5."
3. **PII floor (invariant #8)** — Now states unambiguously: blocks Windows AND Sonnet cloud; LAM-only or halt.
4. **Firewall binding (invariant #9)** — New invariant with explicit requirement: Mac IP allowlist, no public bind.
5. **Audit (invariant #10)** — New invariant with enforcement note: "Sprint 3 CI gate" and "endpoint disabled until rebuilt."
6. **Enforcement index rows 13–15** — All three added with halt semantics pointing to Sprint 2/3/4 artifacts.
7. **Exception register** — Expanded to three entries (PII-001, AUDIT-001, DISABLED-001), all expiring 2026-05-15.
8. **Runbook "NOT APPROVED" language** — Added in PII gate and audit sections. Stage B acceptance criteria stub lists 7 requirements.
9. **Preflight --worker/--critic modes** — Implemented with jq parsing of /api/tags JSON.
10. **Fallback log reworded** — Cites SOM-WIN-OLLAMA-DISABLED-001 exception instead of "momentum."
11. **External services runbook §4e** — Updated to document both --worker and --critic modes.

## Charter consistency reassessment

- Invariants 8–10 fit naturally into the existing charter under "Society of Minds — Code standards."
- Numbering is coherent: no gaps, no duplicates.
- Enforcement rows 13–15 align with invariants 8–10 and point to correct sprint deliverables.
- No orphan rules remain.
- **Verdict on this check: PASS.**

## Security reassessment

- **PII floor hardened** — Invariant #8 explicitly blocks Windows AND Sonnet cloud for PII-tagged payloads. This preserves the existing PII floor (invariant #4) and closes the route-through gap.
- **Firewall binding** — Invariant #9 requires explicit allowlist (Mac IP or subnet). Removes the "assumed trust" language that was questioned in round 1.
- **Audit trail** — Invariant #10 declares hard requirement: hash-chain + HMAC + manifest + CI validator. Endpoint disabled on chain break.
- **Exceptions are bounded** — All three exceptions expire 2026-05-15 (30 days), forcing re-assessment before activation.
- **Stage A correctness** — Windows rung remains disabled during Phase 1, preventing accidental selection before controls are live.
- **Verdict on this check: PASS.**

## Operational soundness reassessment

- **Stage B acceptance criteria** — Runbook now includes a clear 7-item stub (submit.py, PII middleware, audit writer, CI validator, firewall allowlist, failover rules, integration tests). Each item maps to a sprint and stage gate.
- **Exception schema** — All three entries follow the required schema: rule_id, repo, deferral_reason, approver, expiry_date, review_cadence, status. All entries are valid per `docs/exception-register.md` template.
- **Preflight contract** — Split into --worker (qwen2.5-coder:7b) and --critic (llama3.1:8b) modes. jq parsing is robust against malformed /api/tags JSON.
- **Runbook clarity** — Moved from "manual operator PII confirmation" to explicit "not approved for SoM routing until Sprint 5."
- **Verdict on this check: PASS.**

## Integration assessment

- **Preflight --worker mode** — Correctly requires qwen2.5-coder:7b for Tier-2 Worker. Uses jq to parse /api/tags JSON and exit 0 (found) or 2 (missing).
- **Preflight --critic mode** — Correctly requires llama3.1:8b for HP critic. Same jq-based logic.
- **External services runbook alignment** — §4e now documents both modes with correct exit codes and role labels.
- **Fallback log integration** — Entry now cites exception rule_id, integrating with exception-register.md schema.
- **Verdict on this check: PASS.**

## Scope discipline assessment

- **Stage A remains "documented / disabled"** — Confirmed in Tier-2 ladder cell and throughout runbook.
- **Phase 3 epics** — Future topics (Cloudflare Tunnel, WoL, health-check) are properly stubbed as deferred.
- **No premature activation** — Windows rung is explicitly NOT added to the active decision path until Sprint 5.
- **Verdict on this check: PASS.**

## Minor observations (not blockers)

1. **Remote MCP Bridge pattern matching** — Runbook stage B stub mentions "audit writer" and "CI validator" but does not explicitly state that Sprint 3 will align the audit log schema with the Remote MCP Bridge plan (`raw/inbox/2026-04-14-remote-mcp-bridge-plan.md` §"Audit trail — tamper-evident"). This is a documentation clarity issue only; the implementation will follow the correct pattern in Sprint 2–3 worker briefs.

2. **Firewall binding enforcement** — Invariant #9 declares the requirement but the CI gate `check-windows-ollama-exposure.yml` is marked as Sprint 4. This is correct per the plan, but it means Stage A documents the rule without runtime enforcement. This is acceptable because exceptions SOM-WIN-OLLAMA-DISABLED-001 keeps the rung offline.

## Verdict

**APPROVED_WITH_CHANGES**

All 13 must-fixes from round 1 are present and correct. Charter is consistent, security is hardened, operations are clear, integration points are solid, and scope is disciplined. 

**Required change:**
- Update runbook stage B acceptance criteria stub (item #4) to add a note: "CI validator pattern-matches against Remote MCP Bridge audit schema per `_worktrees/gov-remote-mcp` plan." This is a documentation clarification only; no code change required.

Once this clarification is in place, Stage A is mergeable.

---

**Cross-reviewer:** gpt-5.4 @ `model_reasoning_effort=high`  
**Review date:** 2026-04-15  
**Round:** 2  
**Artifacts reviewed:** STANDARDS.md, docs/exception-register.md, docs/runbooks/windows-ollama-worker.md, scripts/windows-ollama/preflight.sh, raw/model-fallbacks/2026-04-14.md, docs/EXTERNAL_SERVICES_RUNBOOK.md
