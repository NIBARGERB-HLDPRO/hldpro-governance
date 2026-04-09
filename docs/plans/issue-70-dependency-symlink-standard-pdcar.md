# Issue 70 PDCA/R — Shared Dependency Symlink Standard

Date: 2026-04-09
Issue: [#70](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/70)
Owner: nibargerb

## Plan

- review current governance guidance for any existing worktree dependency-sharing standard
- decide whether borrowing installed dependencies from a root checkout into an isolated worktree is approved
- if approved, document the narrow allowlist, verification rules, and cleanup expectations
- if manual setup still looks error-prone after review, create a helper follow-up before closure

## Do

- reviewed the existing worktree governance baseline and confirmed there was no explicit standard for shared dependency symlinks
- documented the approved pattern in `STANDARDS.md`
- updated `OVERLORD_BACKLOG.md` to mark issue `#70` done and add helper follow-up issue `#72`
- added the structured JSON plan and this PDCA/R closeout artifact
- proofed the pattern in a temporary `ai-integration-services` worktree by borrowing the root checkout `node_modules/`, verifying lockfile parity, resolving `typescript`, and running `npm exec --yes tsc --version`

## Check

Verification target:
- governance now has an explicit position on the pattern
- the standard names allowed artifacts, forbidden artifacts, verification requirements, and cleanup expectations
- any required helper/runbook follow-up is issue-backed before issue closure
- real worktree proof succeeds under the documented constraints

## Adjust

Review concluded that the manual pattern is approved, but repeated setup is still error-prone. Issue [#72](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/72) now tracks a helper/runbook command for parity checks, linking, and cleanup.

## Review

This slice is complete once the governance standard lands because issue `#70` was a policy review and standardization task, not the helper implementation itself. The remaining helper work is explicitly separated and tracked in `#72`.
