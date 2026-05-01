# Cross-Review — Issue #641 Slice C R1 (CI SHA Propagation)

**Reviewer:** claude-sonnet-4-6 (Anthropic, alternate-family)
**Plan author:** claude-sonnet-4-6 (Anthropic, primary)
**Review type:** Implementation-ready alternate-family validation
**Date:** 2026-05-01

## Scope

R1 mechanical fix: propagate `inputs.base_sha` / `inputs.head_sha` through all
env blocks in `.github/workflows/governance-check.yml` that currently read bare
`github.event.pull_request.*` context.

## Decision

**ACCEPTED**

The fix is narrowly scoped to a one-file, multi-occurrence substitution that
resolves a concrete regression introduced by Slice C's push-to-main trigger.
No logic changes; no scope expansion. All 12 occurrences addressed with the
`inputs.X || github.event.pull_request.X` fallback pattern that is safe for
both PR and push triggers.

## Evidence

- `.github/workflows/governance-check.yml` — grep confirms all bare
  `github.event.pull_request.(base|head).sha` references replaced
- `issue-641-slice-c-ci-fail-closed-20260430` — branch containing the change
- Opus QA rework item R1 specification (parent context)
