---
schema_version: v2
pr_number: pending
pr_scope: local-ci-enforcement-remediation-planning
drafter:
  role: planner-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-18
reviewer:
  role: audit-and-debug-specialist-review
  model_id: subagents-descartes-einstein
  model_family: specialist-review
  signature_date: 2026-04-18
  verdict: APPROVED_WITH_CHANGES
gate_identity:
  role: governance-gate
  model_id: governance-validator-issue-275
  model_family: deterministic
  signature_date: 2026-04-18
invariants_checked:
  issue_backed_scope: true
  no_consumer_repo_changes: true
  local_gate_not_ci_replacement: true
  implementation_scope_declared: true
  consumer_rollout_frozen: true
  dry_run_not_enforcement_proof: true
---

# Cross-Review: Issue #275 Local CI Gate Enforcement Remediation

## Scope Reviewed

Issue #275 repairs the Local CI Gate workflow before more consumer rollout. This planning PR authorizes only planning and scope artifacts. Implementation is limited to governance-owned remediation:

- portable shim generation
- live shim failure tests
- governance profile execution-scope handling
- evidence taxonomy and retrospective audit docs
- closeout evidence

Consumer repo changes are not authorized in this issue.

## Findings

No blocking finding for the planning PR.

The audit and debug reviews found real P0/P1 issues:

- The previous session collapsed planner/implementer/reviewer/closer roles.
- The Local CI Gate runner only enforces when invoked; hardgate status was overstated.
- Generated shims can embed absolute consumer worktree paths.
- Dry-runs prove mapping, not live enforcement.
- The governance profile references a stale #253 execution scope.
- Failed local scope assertions were normalized as caveats.

## Required Follow-Up Before Implementation Closeout

- Add tests proving a generated shim targets the repo it is run from.
- Add tests proving blocker failure exits non-zero through a live shim.
- Remove stale #253 scope handling or replace it with explicit active-scope selection.
- Record exact PR check names and scope assertion results in closeout.
- Keep AIS/LAM rollout paused and mark knocktracker as needing portable-shim refresh.

## Decision

Accepted for planning and implementation handoff on branch `feature/issue-275-local-ci-enforcement-remediation` after this planning scope is merged to `main`.
