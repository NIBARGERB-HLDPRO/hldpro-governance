# Issue 68 PDCA/R — Structured Plan Rollout Across Governed Repos

Date: 2026-04-09
Issue: [#68](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/68)
Owner: nibargerb

## Plan

- normalize governed repos onto the reviewed governance-check SHA that includes the structured-plan validator
- add explicit repo-level structured-plan guidance where the contract is currently implicit or absent
- keep HealthcarePlatform on a documented compatibility shim rather than breaking its repo-specific Phase 8 execution lane
- record any additional rollout work before closure

## Do

- updated reusable governance workflow callers in governed repos
- added structured-plan adoption notes to repo entry docs
- documented HealthcarePlatform's local schema/template as a compatibility shim aligned to the governance-owned field contract
- added governance plan artifacts for this rollout branch
- merged repo rollout PRs in ai-integration-services, knocktracker, local-ai-machine, ASC-Evaluator, and HealthcarePlatform

## Check

Verification target:
- repo workflow callers point at the reviewed governance SHA containing the validator
- repo docs state where structured-plan artifacts should live and that the governance schema is canonical
- HealthcarePlatform compatibility notes do not conflict with its existing Phase 8 lane
- merged PR evidence exists for each targeted governed repo

## Adjust

Review surfaced one additional governance follow-up outside the structured-plan contract itself: issue [#70](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/70) now tracks whether borrowing root-checkout dependencies into isolated worktrees via symlinks is documented, approved, and safely wired.

## Review

This slice is complete because the governed repo rollout is visible in merged PRs:
- ai-integration-services [#859](https://github.com/NIBARGERB-HLDPRO/ai-integration-services/pull/859)
- knocktracker [#149](https://github.com/NIBARGERB-HLDPRO/knocktracker/pull/149)
- local-ai-machine [#387](https://github.com/NIBARGERB-HLDPRO/local-ai-machine/pull/387)
- ASC-Evaluator [#3](https://github.com/NIBARGERB-HLDPRO/ASC-Evaluator/pull/3)
- HealthcarePlatform [#747](https://github.com/NIBARGERB-HLDPRO/HealthcarePlatform/pull/747)

Governance closeout now records the landed adoption state rather than planned intent.
