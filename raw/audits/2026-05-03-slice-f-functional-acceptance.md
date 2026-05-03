# Functional Acceptance Audit — Slice F (Issue #651)

Date: 2026-05-03
Auditor: claude-sonnet-4-6 (anthropic) — cross-family from gpt-5.4 plan reviewer (openai)
Overall verdict: PASS

## Acceptance Criteria Verification

- [x] AC-F1: PASS — Governance waterfall table has `Model family` column. Session-agnostic
  prose uses tier/role references (e.g., "Tier 1 planner", "Tier 2 worker"), not hardcoded
  model family names in invariant text.
- [x] AC-F2: PASS — Invariant #3 updated with "fallup direction: if the primary planning
  model is unavailable, escalate to a more capable model or halt; do not silently downgrade."
- [x] AC-F3: PASS — Governance waterfall Tier 1 row lists both `claude-opus-4.X` (anthropic)
  and `codex-5.X @ high` (openai) as valid Tier 1 planning families.
- [x] AC-F4: PASS — Invariant #16 added: "QA cross-family required. Tier 3 QA reviewer and
  Tier 2 worker must be different model families. Same-family QA is explicitly prohibited."
- [x] AC-F5: PASS — Worker row lists `codex-5.4-medium` and `codex-spark` explicitly as
  valid worker models alongside `claude-sonnet-4.X`.
- [x] AC-F6: PASS — §PDCAR expanded with formal functional acceptance auditor gate:
  required artifact path convention, PASS/FAIL verdict requirement, cross-family auditor
  requirement, closeout evidence requirement, and no-waiver rule.
- [x] AC-F7: PASS — STANDARDS.md §Exceptions does not contain SOM-BOOTSTRAP-001.
  Confirmed retired in docs/exception-register.md §Expired or closed exceptions.
- [x] AC-F8: PASS — Cross-review at raw/cross-review/2026-05-03-slice-f-standards-rewrite.md
  is dual-signed: anthropic drafter (claude-sonnet-4-6) + openai reviewer (gpt-5.4) +
  deterministic gate identity.
- [x] AC-F9: This document constitutes the PASS verdict for AC-F9.

## Diff Review Summary

STANDARDS.md changes reviewed:
- Governance waterfall table: added `Model family` column; Tier 1 row updated with both-family
  planner validity and "Halt if unavailable; do not downgrade" constraint; Worker row updated
  with codex-5.4-medium and codex-spark.
- Invariant #3: replaced "Planning authority is dual-family" stub with explicit fallup rule.
- Invariant #16 (new): QA cross-family prohibition with explicit same-family QA ban.
- §PDCAR: expanded with formal auditor gate section.
- §Exceptions: confirmed SOM-BOOTSTRAP-001 absent (never in this section).

No CI workflows, hooks, scripts, or schema files were modified.

## Gate Results

PASS — all AC-F1 through AC-F9 verified against committed diff.
