---
schema_version: v2
pr_number: pre-pr
pr_scope: standards
drafter:
  role: architect-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-28
reviewer:
  role: architect-claude
  model_id: claude-opus-4-6
  model_family: anthropic
  signature_date: 2026-04-28
  verdict: APPROVED_WITH_CHANGES
gate_identity:
  role: deterministic-local-gate
  model_id: hldpro-local-ci
  model_family: deterministic
  signature_date: 2026-04-28
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---

# Cross-Review - Issue #573 Session Waterfall Runbook Enforcement

## Review Subject

- Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/573
- Structured plan: `docs/plans/issue-573-session-waterfall-runbook-structured-agent-cycle-plan.json`
- PDCAR: `docs/plans/issue-573-session-waterfall-runbook-pdcar.md`
- Planning scope: `raw/execution-scopes/2026-04-28-issue-573-session-waterfall-runbook-planning.json`
- Handoff package: `raw/handoffs/2026-04-28-issue-573-session-waterfall-runbook.json`

## Verdict

APPROVED_WITH_CHANGES

Claude Opus 4.6 approved the governance-first plan with changes. The required
changes were incorporated before implementation authority was granted:

1. Add a machine-checkable bootstrap sentinel so the session contract is not
   advisory-only.
2. Require non-empty `review_artifact_refs` and `gate_artifact_refs` in
   implementation-ready and later handoff states.
3. Make implementation-ready alternate-review acceptance checks unconditional
   across validator paths, not only the governance-surface enforcement path.
4. Bring `.claude/settings.json` to the STANDARDS-required PostToolUse `*`
   matcher contract.
5. Record this cross-review artifact with the required dual-signature
   frontmatter.

## Findings

### F1: The waterfall diagnosis is right, but bootstrap enforcement needed a sentinel

The plan correctly identified that the current session start injects only
`wiki/index.md` and `GRAPH_REPORT.md`. Opus required a deterministic sentinel or
equivalent machine-checkable bootstrap proof so CODEX.md and the runbook are not
advisory-only.

### F2: Implementation-ready alternate review needed unconditional validation

The current plan validator already checks accepted alternate review in the
governance-surface enforcement path, but Opus identified a loophole where an
implementation-ready plan could avoid that check outside the stricter path. The
plan now requires closing that loophole.

### F3: Implementation handoffs needed non-empty review and gate evidence

The current handoff validator proves arrays exist, but not that
`review_artifact_refs` and `gate_artifact_refs` contain real evidence for
implementation-ready and later states. The plan now requires that enforcement.

### F4: Session-start hook and settings contract needed explicit hook coverage

Opus flagged that the repo still lacks the STANDARDS-required PostToolUse `*`
matcher for error checks. The implementation surface now includes that fix.

## Required Conditions

1. Keep the bootstrap sentinel inside the accepted scope; do not stop at a
   documentation-only CODEX contract.
2. Tighten both the structured plan validator and handoff validator to make the
   required waterfall evidence non-optional for implementation-ready work.
3. Keep downstream repo adoption out of this branch and record any consumer
   rollout as follow-up work.

## Residual Risks

1. CODEX.md remains a convention surface; the real enforcement must come from
   validators, hooks, and CI.
2. Downstream repos will still drift until they adopt the governance-first
   contract through issue-backed follow-up work.
3. The same-family Codex planning and Codex subagent implementation exception is
   time-limited and must be renewed or replaced if the lane extends past the
   recorded expiry.
