# Issue 74 PDCA/R — Governance Diff Base

Date: 2026-04-09
Issue: [#74](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/74)
Owner: nibargerb

## Plan

- add an explicit `base_sha` input to the reusable governance workflow
- use one resolved base value for every diff/log comparison inside the workflow
- propagate the input through governed repo callers
- close the issue only after reusable workflow and caller updates are merged

## Do

- updated the reusable governance workflow to accept and resolve `base_sha`
- replaced pull-request-only and `github.event.before` diff logic with the resolved base value
- prepared governance closeout artifacts for the slice

## Check

Verification target:
- reusable workflow no longer depends on `github.event.before` under `workflow_call`
- all diff-based checks use the same resolved base value
- governed repo callers pass the correct base SHA

## Adjust

Caller propagation is part of the same acceptance path, so the issue does not close until the governed repos are updated and merged.

## Review

This slice is complete only when both the reusable workflow and its governed repo callers are merged, so multi-commit PR governance checks cover the full PR diff instead of the last commit only.
