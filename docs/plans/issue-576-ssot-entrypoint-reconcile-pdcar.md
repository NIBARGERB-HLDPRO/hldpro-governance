# Issue #576 PDCAR: Governance SSOT Entrypoint Reconciliation

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/576
Branch: `issue-576-ssot-entrypoint-reconcile-20260428`

## Plan

Reconcile the governance repo's own conflicting operator-facing entrypoints so
alternate-family review, secret/bootstrap flow, and thin-consumer ownership all
have one canonical SSOT path before downstream thin-adapter rollout proceeds.

## Do

Implementation scope for issue #576:

- add the canonical governance `scripts/codex-review.sh` wrapper surface
- normalize review documentation so `scripts/codex-review.sh claude` is the
  only operator-facing Codex -> Claude path
- normalize bootstrap and secret-seeding documentation and script behavior so
  the governance SSOT root and bootstrap command are singular
- clarify that governance package logic is thick only in `hldpro-governance`
  and consumer repos carry thin reviewed adapters only

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
- validation proves the direct operator-facing alternatives are gone or clearly
  demoted to implementation-detail status

## Adjust

If a change would break the currently working governed review pipeline, land a
minimal compatibility shim first, then tighten the documentation and template
surfaces around it in the same slice. Do not widen this issue into downstream
consumer repo rollout.

## Review

Alternate-family review is required before implementation. The review must
verify that the chosen canonical paths are singular, operator-facing, and
consistent with the issue-575 rollout gate, while preserving any necessary
lower-level helper code as implementation details only. Review outcome:
`APPROVED_WITH_CHANGES`, requiring the packet to define the wrapper-to-template
relationship explicitly, use deterministic governance-root resolution for
bootstrap, make the `.env.local` token-sourcing fix explicit, either
acceptance-gate or remove `CLAUDE.md` from scope, and add a functional wrapper
validation step beyond shell syntax checks.
