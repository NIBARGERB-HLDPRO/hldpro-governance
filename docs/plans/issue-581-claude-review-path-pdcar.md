# Issue #581 PDCAR: Governed Claude Review Path

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/581
Branch: `issue-581-claude-review-path`

## Plan

Reproduce and fix the governed Claude specialist-review path so bounded
alternate-family packet reviews reliably return a verdict through the approved
`scripts/codex-review.sh claude` operator path.

## Do

Planning scope for issue #581:

- capture the issue-backed packet, planning execution scope, and handoff
- reproduce the failure in a clean governance worktree using the approved
  wrapper/template/supervisor path
- distinguish token/auth health from wrapper/supervisor contract defects
- define the minimal implementation slice needed to make the review path
  deterministic without introducing a parallel operator-facing path

Implementation stays blocked until alternate-family review can be completed or
an explicit repo-rule exception is documented.

## Check

Before implementation:

- structured plan, planning scope, and handoff validate
- reproduction evidence proves the failure mode through the approved path
- base Claude CLI preflight is recorded separately so auth health is not
  conflated with wrapper defects

After implementation:

- the governed wrapper returns a bounded review artifact for a packet-style
  prompt
- validation proves at least one downstream consumer replay succeeds

## Adjust

If the failure is rooted in Claude CLI behavior that cannot be corrected in the
governance wrapper/supervisor layer, stop and document the exact CLI contract
gap rather than introducing an ad hoc alternate review path.

## Review

Alternate-family review remains required before governance-surface
implementation. Issue #581 exists because the approved review path is itself
the failing surface, so planning may proceed with documented blocked status,
but implementation cannot be marked `implementation_ready` until the review
path is repaired or a governed exception is approved.
