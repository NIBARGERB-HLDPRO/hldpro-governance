# PDCAR: Issue #419 Bootstrap SSOT Resolution From Sibling Worktrees

Date: 2026-04-20
Branch: `issue-419-bootstrap-sibling-worktree-ssot-20260420`
Issue: [#419](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/419)

## Plan

Fix the post-merge #416 bootstrap edge case where sibling governance worktrees cannot find the primary gitignored `.env.shared` vault.

## Do

1. Extend `scripts/bootstrap-repo-env.sh` vault discovery to fall back to a sibling `hldpro-governance/.env.shared` under the shared HLDPRO root.
2. Add synthetic contract coverage for sibling-worktree execution.
3. Re-run local bootstrap from a sibling main worktree and validate generated LAM key presence without printing values.

## Check

- Synthetic contract test covers the sibling-worktree case.
- Shell syntax and Local CI pass.
- Final AC: GitHub PR checks pass before merge.

## Adjust

If the sibling primary checkout does not exist, keep failing closed with a path-neutral error message instead of guessing another vault location.

## Review

Review must verify this only changes SSOT discovery and does not alter env values or generated file commit policy.
