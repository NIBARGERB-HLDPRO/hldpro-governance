# Review Packet — Issue #641 Slice C R1

**Issue:** #641 (Slice C CI fail-closed rework, item R1)
**Target:** .github/workflows/governance-check.yml
**Date:** 2026-05-01

## Change Summary

Replace all 12 bare `github.event.pull_request.(base|head).sha` references with
`inputs.(base|head)_sha || github.event.pull_request.(base|head).sha` fallback
expressions to prevent fail-closed CI on push-to-main events.

## Lines Changed

Affected lines (per grep): 175, 405, 692, 693, 702, 703, 712, 713, 730, 731,
788, 789.

base.sha occurrences: 7
head.sha occurrences: 5
Total substitutions: 12

## Review Decision

ACCEPTED — mechanical fix, correct pattern, no scope drift.
