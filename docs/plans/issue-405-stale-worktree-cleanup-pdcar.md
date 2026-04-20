# PDCAR: Issue #405 Stale Worktree Cleanup

Date: 2026-04-20
Issue: [#405](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/405)
Branch: `issue-405-stale-worktree-cleanup-20260420`

## Plan

Clean stale local `hldpro-governance` linked worktrees after the lane-guard rollout without invading another active session. The cleanup must be narrower than the #400 audit recommendation: remove only clean linked worktrees whose remote branch is gone and whose governing GitHub issue is closed.

## Do

1. Refresh local worktree status, remote branch presence, and GitHub issue state.
2. Record a decision matrix for every local governance worktree.
3. Preserve the primary worktree, dirty worktrees, open-issue worktrees, and worktrees with live remote branches.
4. Remove only safe stale linked worktrees.
5. Record after-cleanup evidence and validation output.

## Check

- Dirty #359 remains untouched.
- Open/dirty #403 remains untouched.
- Primary `/Users/bennibarger/Developer/HLDPRO/hldpro-governance` remains untouched.
- Current #405 worktree remains untouched.
- Clean closed/gone linked worktrees are removed.
- Execution-scope validation runs with `--require-lane-claim`.
- Local CI and GitHub checks pass before merge.

## Adjust

Branches with live remote refs are preserved even when their issue is closed. This avoids deleting work another session may still be using and keeps the rule observable.

## Review

This issue cleans local operator state only. It does not start or modify backlog #403, #177, #105, #178, #49, or any downstream repo lane.
