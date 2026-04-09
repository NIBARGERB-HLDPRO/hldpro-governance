# Issue 75 PDCA/R — Raw Feed Redaction

Date: 2026-04-09
Issue: [#75](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/75)
Owner: nibargerb

## Plan

- stop mirroring open issue body text into tracked governance files
- keep raw issue feeds useful by retaining metadata only
- sanitize the currently tracked raw issue snapshots
- record the policy change and security rationale in governance docs

## Do

- added a reusable metadata-only issue feed renderer
- updated the nightly raw-feed workflow to stop fetching issue bodies
- rewrote the tracked raw issue snapshots to the metadata-only format
- updated governance backlog/history and feature/fail-fast docs

## Check

Verification target:
- workflow no longer requests `body` from `gh issue list`
- raw/github-issues files contain metadata only
- a sensitive-pattern scan against the sanitized files finds no mirrored issue body content from the prior feed shape

## Adjust

No further follow-up was required. The safe path is metadata-only retention, so there is no reason to keep a partial body-redaction mode in this loop.

## Review

This slice is complete once the workflow and tracked raw issue snapshots both stop carrying issue body text. That closes the durable-secondary-copy risk identified in issue `#75`.
