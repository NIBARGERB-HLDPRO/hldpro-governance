# PDCAR: Issue #400 Runtime Lane Guard Proof

Date: 2026-04-20
Issue: [#400](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/400)
Branch: `issue-400-runtime-lane-guard-proof-20260420`

## Plan

Verify the post-#397 issue-lane guard in the actual installed runtime path before starting any backlog work. The slice is intentionally limited to items 1-4 from the operator's next-step list: local worktree hygiene audit, global hook sync, live negative-control proof, and a runbook snippet for safe issue-lane startup.

## Do

1. Record the current sibling worktree state without deleting or cleaning another lane.
2. Sync `/Users/bennibarger/.claude/hooks/branch-switch-guard.sh` to the repo-owned hook when hashes differ.
3. Run the installed global hook directly with PreToolUse-style JSON for blocked and allowed command forms.
4. Document the issue-lane startup sequence in the operator runbook.
5. Keep issue #398 and other open worktrees out of the write scope.

## Check

- Unmarked `git worktree add -b issue-*` exits `2`.
- `HLDPRO_LANE_CLAIM_BOOTSTRAP=1 git worktree add -b issue-*` exits `0`.
- `HLDPRO_LANE_CLAIM_SCOPE=<scope>` allows a matching `lane_claim.issue_number`.
- A mismatched claimed scope exits `2`.
- Non-issue worktree creation exits `0`.
- Execution-scope validation runs with `--require-lane-claim`.
- Local CI and GitHub checks pass before merge.

## Adjust

The hygiene audit is evidence-only. Clean but stale worktrees are listed as cleanup candidates, but this issue does not remove them because the operator explicitly warned that other sessions may own adjacent lanes.

## Review

Do not start item 5 or any backlog issue from this lane. A future issue lane must first have a GitHub issue, planning bootstrap, PDCAR, structured plan, and a claimed execution scope before implementation writes.
