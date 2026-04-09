# Issue 72 PDCA/R — Worktree Dependency Helper

Date: 2026-04-09
Issue: [#72](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/72)
Owner: nibargerb

## Plan

- create a reusable helper for linking approved dependency artifacts from a root checkout into an isolated worktree
- enforce same-repo and lockfile parity checks before linking
- provide safe cleanup that only removes helper-managed symlinks
- prove the helper on a real ai-integration-services worktree before closing the issue

## Do

- added a governance-owned helper script with `link` and `clean` commands
- kept the helper scoped to approved dependency artifacts only
- stored cleanup manifest state in the git metadata path instead of the worktree
- updated governance docs to point at the helper as the preferred path for the approved pattern
- proved the helper in a temporary `ai-integration-services` worktree by linking root `node_modules`, resolving TypeScript, running `npm exec --yes tsc --version`, then cleaning the symlink and manifest successfully

## Check

Verification target:
- the helper rejects unsafe or mismatched setups
- the helper links approved artifacts successfully when parity checks pass
- the helper cleans up only the symlinks it created
- a real proof run succeeds in a temporary ai-integration-services worktree

## Adjust

The first proof surfaced a real portability bug: `mapfile` is unavailable in the default macOS Bash 3.2 runtime. The helper was fixed in-slice to use a shell-compatible manifest reader instead of leaving cleanup broken on the main operator machine. No additional follow-up was required beyond that repair because the rerun completed successfully and closed the main remaining gap from issue `#70`.

## Review

This slice is complete once the helper lands and the governance backlog marks issue `#72` done with proof evidence from the temporary ai-integration-services worktree.
