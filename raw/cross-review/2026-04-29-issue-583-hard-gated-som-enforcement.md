---
schema_version: v2
pr_number: pre-pr
pr_scope: standards
drafter:
  role: architect-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-29
reviewer:
  role: architect-claude
  model_id: claude-opus-4-6
  model_family: anthropic
  signature_date: 2026-04-29
  verdict: APPROVED_WITH_CHANGES
gate_identity:
  role: deterministic-local-gate
  model_id: hldpro-local-ci
  model_family: deterministic
  signature_date: 2026-04-29
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---

# Cross-Review — Issue #583 Hard-Gated Issue-Level SoM Enforcement

Source artifact: `docs/codex-reviews/2026-04-29-claude.md`

## Verdict

**APPROVED_WITH_CHANGES**

## Blocking findings

1. The planning packet originally lacked an explicit lifecycle-transition rule
   explaining when empty review/handoff refs are legal in `planning_only` and
   when they must become blocking failures.
2. The planning execution scope originally omitted the `raw/cross-review/...`
   path needed to capture the review artifact that unblocks implementation.

## Required follow-ups folded into the packet

- Added lifecycle-gated acceptance criteria that distinguish `planning_only`
  from `implementation_ready` and later states.
- Added the `raw/cross-review/...` and `docs/codex-reviews/...` artifact paths
  to the planning execution scope.
- Clarified that governance CI and the managed consumer-governance contract are
  both in scope, while direct downstream repo repair remains separate issue
  `#197`.
- Recorded the need for bounded exemption schema and structured reviewer
  identity fields before implementation-ready promotion.

## Remaining conditions before implementation

- Promote the lane to `implementation_ready` only after the implementation scope
  names the exact schema, validator, test, and CI surfaces to be changed.
- Keep the replay proof against Stampede issue `#184` as a required validation
  artifact before calling the source fix complete.
