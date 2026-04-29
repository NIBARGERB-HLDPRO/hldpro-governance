# Issue #583 PDCAR: Hard-Gated Issue-Level SoM Enforcement

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/583
Branch: `issue-583-hard-gated-som-enforcement`

## Plan

Hard-gate issue-level Society of Minds enforcement so governed consumer repos
cannot merge self-reviewed planning packets or packets missing independent
review and handoff evidence.

This lane exists because the recent thin-adapter rollout improved repo
entrypoints but did not actually bind the issue-level waterfall. The immediate
proof is Stampede issue `#184`, where the active planning packet records
orchestrator self-review, bypasses alternate-family review, and carries no
governed handoff or review artifact references.

## Do

Implementation scope for issue `#583`:

- harden the structured-plan schema and validator so governed plans record
  enough identity metadata to prove reviewer independence
- reject orchestrator self-review for governed plans
- allow `alternate_model_review.required=false` only when a bounded exemption
  is recorded and validator-legal
- require non-empty `review_artifact_refs` for governed plans and require
  non-null handoff refs for non-draft plans intended to continue through the
  waterfall
- wire the plan and handoff validators into the consumer governance CI contract
- add regression tests that reproduce the bad Stampede issue `#184` shape and
  prove the hardened rules reject it
- keep downstream product-repo repair out of this source-fix lane except for
  validation replay and proof

## Check

Before implementation:

- the issue-backed planning packet validates locally
- the acceptance criteria are phrased as hard gates, not advisory wording
- alternate-family review is captured through the governed
  `scripts/codex-review.sh claude` path before implementation-ready promotion

After implementation:

- a plan with self-review or missing reviewer-family metadata fails the
  structured-plan validator
- a plan with `alternate_model_review.required=false` and no legal exemption
  fails the structured-plan validator
- lifecycle gates are explicit:
  - `planned` / `planning_only` may defer populated review and gate refs only
    while alternate-family review is still pending
  - promotion to `implementation_ready` requires accepted alternate-family
    review evidence and non-empty `review_artifact_refs`
  - continuing governed handoffs from `implementation_ready` onward require
    non-null handoff evidence and fail closed when missing
- the structured-plan and handoff validators enforce those lifecycle gates
- governance CI and the managed consumer-governance contract both run the plan
  and handoff validators as blocking steps
- proof includes a downstream replay showing the old Stampede issue `#184`
  packet shape would now fail under the hardened rules

## Adjust

If the current schema cannot encode reviewer/author independence cleanly,
introduce the minimum new fields needed and document them in the standards and
schema examples. Do not add a weaker warning-only path or repo-local exception
to get the bad packet shape through CI.

If managed consumer workflow rollout cannot happen inside this source-fix lane,
the implementation must still land the blocking source contract and record a
downstream replay proof plus a separate issue-backed consumer rollout follow-up.
Do not blur "source contract fixed" and "all consumers upgraded" into the same
completion claim.

## Review

This issue must not be called fixed until alternate-family review accepts the
hard-gated acceptance criteria, the source validators/CI are green, and the
downstream replay proves the old failure shape is blocked.
