---
schema_version: v2
pr_number: pre-pr
pr_scope: standards
drafter:
  role: architect-claude
  model_id: claude-sonnet-4-6
  model_family: anthropic
  signature_date: 2026-05-03
reviewer:
  role: architect-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-05-03
  verdict: APPROVED
gate_identity:
  role: deterministic-local-gate
  model_id: hldpro-local-ci
  model_family: deterministic
  signature_date: 2026-05-03
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---

# Cross-Review: Slice F — STANDARDS.md Policy Rewrite (Issue #651)

## Review Subject

- Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/651
- Scope: STANDARDS.md §SoM governance waterfall table alignment, fallback ladder fallup
  corrections, QA cross-family prohibition (invariant #16), §PDCAR functional acceptance
  auditor gate formal requirements, SOM-BOOTSTRAP-001 absence confirmation.

## Acceptance Criteria Reviewed

- AC-F1: PASS — Governance waterfall table updated with explicit `Model family` column.
  Session-agnostic section prose uses tier/role language, not hardcoded model IDs.
- AC-F2: PASS — Invariant #3 updated with explicit fallup direction: escalate or halt,
  do not silently downgrade. Tier 1 row constraint: "Halt if unavailable; do not downgrade."
- AC-F3: PASS — Tier 1 row explicitly lists both `claude-opus-4.X` (anthropic) and
  `codex-5.X @ high` (openai) as valid Tier 1 planning families.
- AC-F4: PASS — Invariant #16 added explicitly prohibiting same-family QA for all review stages.
- AC-F5: PASS — Worker row lists `codex-5.4-medium` and `codex-spark` as valid workers.
- AC-F6: PASS — §PDCAR expanded with formal functional acceptance auditor gate requirements.
- AC-F7: PASS — SOM-BOOTSTRAP-001 is not present in STANDARDS.md §Exceptions.
  It is retired in docs/exception-register.md under §Expired or closed exceptions.
- AC-F8: This artifact (anthropic drafter + openai reviewer + deterministic gate).
- AC-F9: PASS — Functional acceptance auditor report at
  raw/audits/2026-05-03-slice-f-functional-acceptance.md.

## Reviewer Notes

All changes are surgical policy text corrections. No invariants are relaxed. The fallup direction
change is more conservative (halt or escalate vs. silent downgrade). Invariant #16 codifies
existing same-family-QA prohibition prose into an enforceable numbered rule. The §PDCAR gate
formalizes an already-practiced step. SOM-BOOTSTRAP-001 confirmed absent — no action needed.

## Verdict

APPROVED
