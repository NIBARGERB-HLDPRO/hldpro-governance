# Issue #576 PDCAR: Governance SSOT Entrypoint Reconciliation

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/576
Branch: `issue-576-ssot-entrypoint-reconcile-20260428`

## Plan

Reconcile the governance repo's own conflicting operator-facing entrypoints so
alternate-family review, secret/bootstrap flow, and thin-consumer ownership all
have one canonical SSOT path before downstream thin-adapter rollout proceeds.
Also reconcile the repeated Stage 6 drift where planning-only branches pick up
graph/wiki writeback and fail planner-boundary gates despite valid closeout
evidence.

## Do

Implementation scope for issue #576:

- add the canonical governance `scripts/codex-review.sh` wrapper surface
- normalize review documentation so `scripts/codex-review.sh claude` is the
  only operator-facing Codex -> Claude path
- normalize bootstrap and secret-seeding documentation and script behavior so
  the governance SSOT root and bootstrap command are singular
- clarify that governance package logic is thick only in `hldpro-governance`
  and consumer repos carry thin reviewed adapters only
- split Stage 6 closeout behavior so planning-only slices record evidence
  without graph/wiki writeback, while implementation slices remain the only
  path that refreshes graph/wiki outputs
- correct the planning gate so planning-evidence-only governance packets are
  not forced into `implementation_ready` mode just because they change
  planning/validation/closeout artifacts

## Check

Before implementation:

- structured plan, execution scope, and handoff validate
- alternate-family review is captured through the governed wrapper path

After implementation:

- the governance repo exposes `scripts/codex-review.sh` and the wrapper works
  for Claude specialist review
- policy, runbook, and wrapper docs point to one canonical review entrypoint
- the bootstrap script and environment docs point to one canonical governance
  SSOT root and one canonical bootstrap command
- planning-only closeouts validate and complete without generating graph/wiki
  branch drift
- implementation closeouts remain the only route that writes derived
  `graphify-out/` and `wiki/` artifacts, and those writes stay explicitly
  authorized in the execution scope
- validation proves the direct operator-facing alternatives are gone or clearly
  demoted to implementation-detail status and proves the closeout/plan-gate
  contract matches actual Stage 6 behavior

## Adjust

If a change would break the currently working governed review pipeline, land a
minimal compatibility shim first, then tighten the documentation and template
surfaces around it in the same slice. Do not widen this issue into downstream
consumer repo rollout. If the planning-gate fix cannot be landed without
breaking implementation enforcement, prefer the narrower rule that only
planning-evidence surfaces may remain `planning_only` and keep all source-code
or standards mutations behind `implementation_ready`.

## Review

Alternate-family review is required before implementation. The review must
verify that the chosen canonical paths are singular, operator-facing, and
consistent with the issue-575 rollout gate, while preserving any necessary
lower-level helper code as implementation details only. Review outcome:
`APPROVED_WITH_CHANGES`, requiring the packet to define the wrapper-to-template
relationship explicitly, use deterministic governance-root resolution for
bootstrap, make the `.env.local` token-sourcing fix explicit, either
acceptance-gate or remove `CLAUDE.md` from scope, and add a functional wrapper
validation step beyond shell syntax checks. Updated review scope must also
confirm that the Stage 6 contract is singular: planning closeouts are
evidence-only, implementation closeouts own graph/wiki refresh, and planning
evidence changes do not require fake `implementation_ready` escalation.
