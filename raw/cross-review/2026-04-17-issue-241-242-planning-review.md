---
pr_number: TBD
pr_scope: standards
drafter:
  role: architect-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-17
reviewer:
  role: architect-claude
  model_id: claude-opus-4-6
  model_family: anthropic
  signature_date: 2026-04-17
  verdict: APPROVED_WITH_CHANGES
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---

# Cross-Review - Issues 241 and 242 Planning Split

## Subject

Planning review for:

- Issue #241: graphify-out artifact contract and ignored-cache noise.
- Issue #242: planner write-boundary for governance-surface edits.

## Drafter - `gpt-5.4`

Codex planning split:

- Keep #241 narrow: graphify artifact contract only.
- Track planner write-boundary enforcement separately in #242.
- Use pinned Tier 2 execution agents for implementation after planning approval.

## Reviewer - `claude-opus-4-6`

Verdict: `APPROVED_WITH_CHANGES`.

The reviewer confirmed that #241 and #242 should remain separate. They are orthogonal controls with different enforcement surfaces and blast radii:

- #241 is a data/artifact contract.
- #242 is an access-control and process-control gate.

The reviewer recommended shipping #241 first and resolving #242 design details before implementation.

## Required Changes Before #242 Implementation

1. Define the planning-artifact path allowlist.
2. Define the exception mechanism, including grant authority, storage path, required fields, TTL, and audit trail.
3. Add a transition plan: warning mode first, then strict mode after one full sweep cycle confirms compatibility.
4. Specify the minimal handoff evidence schema and validate it with the boundary checker tests.
5. Ensure hooks and PR gates block when strict mode is enabled; Tier 2/3 implementer briefs must require handoff evidence before DONE.

## Review Outcome

- #241 may proceed to pinned-agent implementation after planning artifacts are validated.
- #242 may proceed to pinned-agent implementation only with the required design details encoded in its plan and acceptance criteria.
- No planner role should directly implement either issue.
