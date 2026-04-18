# PDCAR: Issue #286 Execution Environment Preflight

## Problem

Local execution-scope validation can block unrelated governance work when sibling repos are dirty because they are intentionally active in another lane.

## Diagnosis

`assert_execution_scope.py` correctly treats dirty forbidden roots as blockers. The missing nuance is a scope-declared active parallel lane. Without that, the local gate cannot distinguish accidental sibling contamination from intentional parallel work.

## Constraints

- Target worktree write-boundary enforcement remains strict.
- Dirty forbidden roots remain blockers by default.
- Active parallel roots must be declared in the issue execution scope with a reason.
- Declared active roots warn instead of block.
- GitHub clean runners remain authoritative.

## Actions

1. Add issue-backed planning and execution-scope artifacts.
2. Extend execution-scope parsing with `active_parallel_roots`.
3. Add focused tests for blocking and warning behavior.
4. Add `check_execution_environment.py` as an operator-facing preflight wrapper.
5. Run local tests, Local CI Gate, and GitHub Actions.
6. Record closeout evidence.

## Results / Acceptance Criteria

- Undeclared dirty forbidden root fails.
- Declared active parallel root warns and does not fail.
- Target worktree out-of-scope dirtiness fails.
- Malformed active parallel root entries fail scope loading.
- Local and GitHub validation pass before merge.

## Review

Subagent review is required for the implementation approach and edge cases.
