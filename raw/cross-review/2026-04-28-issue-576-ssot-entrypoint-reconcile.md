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

# Cross-Review — Issue #576 Governance SSOT Entrypoint Reconciliation

## Review Subject

Implementation packet for issue #576: reconcile the governance repo's
conflicting operator-facing entrypoints across three surfaces before issue
#575 thin-consumer rollout proceeds. Reviewed artifacts:

- `docs/plans/issue-576-ssot-entrypoint-reconcile-pdcar.md`
- `docs/plans/issue-576-ssot-entrypoint-reconcile-structured-agent-cycle-plan.json`
- `raw/execution-scopes/2026-04-28-issue-576-ssot-entrypoint-reconcile-implementation.json`
- `raw/handoffs/2026-04-28-issue-576-ssot-entrypoint-reconcile.json`

Canonical source files examined for conflict evidence: `CODEX.md`, `CLAUDE.md`,
`STANDARDS.md`, `docs/EXTERNAL_SERVICES_RUNBOOK.md`,
`docs/ENV_REGISTRY.md`, `docs/governance-tooling-package.json`,
`scripts/bootstrap-repo-env.sh`, `scripts/codex-review-template.sh`,
`scripts/session_bootstrap_contract.py`.

## Verdict

**APPROVED_WITH_CHANGES**

The packet correctly identifies all three governance-source SSOT conflicts,
chooses defensible canonical paths, and maintains a tight scope boundary that
avoids downstream consumer repo edits. The structured plan, execution scope,
lane claim, handoff, and deviation rules are well-formed and internally
consistent. Five required changes are listed below; each is addressable within
the existing scope without widening the issue.

## Findings

### F1 — Wrapper-to-template relationship undefined

Sprint 1 creates `scripts/codex-review.sh` and modifies
`scripts/codex-review-template.sh`, but no acceptance criterion specifies the
runtime relationship between these two files. Without this, the implementation
could produce two independent operator-facing scripts and recreate the very
conflict this issue exists to resolve.

### F2 — Bootstrap multi-root removal must handle worktree invocation

The plan correctly targets `scripts/bootstrap-repo-env.sh` multi-root discovery
as ambiguous, but worktrees depend on a deterministic way to reach the primary
governance `.env.shared`. The replacement needs to be explicit and singular.

### F3 — Claude review mode sources `.env` instead of `.env.local`

`scripts/codex-review-template.sh` currently sources `CLAUDE_CODE_OAUTH_TOKEN`
from `.env`, while the governance bootstrap flow writes `.env.local`. This is a
real contract mismatch and must be fixed in the wrapper/template implementation.

### F4 — Sprint 2 includes `CLAUDE.md` but does not acceptance-gate the change

`CLAUDE.md` is named in scope, but no acceptance criterion states exactly what
must change there. Either make the expected pointer normalization explicit or
remove the file from scope.

### F5 — Missing validation step for wrapper functional proof

Syntax-only validation is not enough. The wrapper needs a functional proof that
it can reach the expected mode dispatch and env-resolution path without relying
on a live Claude API call.

## Required Conditions

1. Add an explicit criterion defining whether `scripts/codex-review.sh`
   delegates to or supersedes `scripts/codex-review-template.sh` in the
   governance repo, and demote the template to implementation-detail status in
   operator-facing docs.
2. Add an explicit criterion requiring deterministic governance-root resolution
   for bootstrap, replacing climb-and-search behavior.
3. Make the `.env.local` versus `.env` token-sourcing fix an explicit task in
   Sprint 1.
4. Make the `CLAUDE.md` normalization explicit in Sprint 2 or remove the file
   from scope.
5. Add a functional wrapper validation command beyond shell syntax checks.

## Residual Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Downstream consumer repos still reference `codex-review-template.sh` directly after this slice lands | Low | Out of scope here; handled by issue-575 follow-up rollout slices |
| `session_bootstrap_contract.py` regex coupling to runbook bootstrap wording | Low | Update helper and runbook together if the canonical command text changes |
| Execution scope omission for `scripts/session_bootstrap_contract.py` if later needed | Low | Amend scope first if implementation requires touching that helper |
| Compatibility shim language could preserve ambiguity if applied too loosely | Low | Keep shim behavior tightly documented as implementation detail only |

## Packet Addendum — Stage 6 Contract Review

Follow-up governed Claude Opus 4.6 review of the widened issue-576 packet
returned `APPROVED_WITH_CHANGES` for the Stage 6 closeout/planning-gate
contract addition.

Required packet updates incorporated before implementation:

1. Handoff AC5 now uses a closed planning-evidence list:
   `docs/plans/`, `raw/cross-review/`, `raw/execution-scopes/`,
   `raw/validation/`, `raw/closeouts/`, and `raw/handoffs/`.
2. Sprint 4 task 1 now explicitly requires `hooks/closeout-hook.sh` to gate
   both graph/wiki build commands and `git add graphify-out/ wiki/` staging on
   non-planning execution modes only, failing closed when execution mode cannot
   be resolved.

Stage 6 contract reviewed in this addendum:

- planning-only closeouts remain evidence-only with no graph/wiki writeback
- implementation closeouts remain the only graph/wiki refresh path
- planning-evidence-only governance packets do not require fake
  `implementation_ready` escalation
- source-code and standards mutations remain behind implementation-ready
  planner-boundary enforcement
