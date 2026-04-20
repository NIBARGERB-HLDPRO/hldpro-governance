# PDCAR: Issue #397 Pre-Worktree Lane Gate

Date: 2026-04-20
Issue: [#397](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/397)
Branch: `issue-397-preworktree-lane-gate-20260420`

## Plan

Issue #393 moved lane ownership into execution scopes and Local CI, but the #391 incident happened earlier: an issue worktree was created and graphify ran before an execution scope existed. This slice closes that earlier gap in the PreToolUse branch/worktree guard.

## Do

1. Extend `hooks/branch-switch-guard.sh` to inspect `git worktree add -b issue-*`.
2. Block unmarked issue worktree creation before filesystem side effects.
3. Allow explicit planning bootstrap with `HLDPRO_LANE_CLAIM_BOOTSTRAP=1`.
4. Allow issue worktree creation with `HLDPRO_LANE_CLAIM_SCOPE=<scope.json>` when that scope has a matching `lane_claim.issue_number`.
5. Preserve existing branch-switch blocking and non-issue worktree behavior.
6. Add deterministic hook tests.

## Check

- Unmarked `git worktree add -b issue-*` exits `2`.
- Bootstrap-marked issue worktree creation exits `0`.
- Matching claimed scope issue worktree creation exits `0`.
- Mismatched claimed scope exits `2`.
- Non-issue worktree creation exits `0`.
- `git checkout <branch>` remains blocked.

## Adjust

The gate intentionally does not block all `git worktree add` commands. Non-issue worktrees remain allowed because they do not imply ownership of an issue lane. Issue lanes need either explicit bootstrap or a matching claimed scope.

## Review

Use this guard with the #393 execution-scope lane claim. The bootstrap marker is for creating PDCAR, structured plan, and execution-scope artifacts only; implementation work must run through `assert_execution_scope.py --require-lane-claim`.
