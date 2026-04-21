# Issue 487 PDCAR: Overlord Sweep Artifact PR Persistence

Issue: NIBARGERB-HLDPRO/hldpro-governance#487  
Date: 2026-04-21

## Plan

Run `24739372677` proved the cross-repo self-learning path and generated report issue update, but final persistence failed because the workflow pushed generated artifacts directly to protected `main`. Repository rules require changes through pull requests with required checks.

Expected implementation:

- Keep generated artifact commit behavior.
- Push generated artifact commits to an automation branch instead of `main`.
- Create a PR for the generated artifacts.
- Record PR persistence status in the sweep report issue.
- Fail only when commit, branch push, or PR creation fails.

## Do

Patch `.github/workflows/overlord-sweep.yml`, add issue-backed scope/validation evidence, run local governance checks, publish and merge, then re-run the sweep.

## Check

Acceptance criteria:

- The workflow has `pull-requests: write` permission.
- The persistence step creates an automation branch and PR when generated artifacts exist.
- No direct push to protected `main` remains in the generated artifact path.
- A manual sweep after merge does not fail with the GH013 direct-main push rejection.

## Act

If generated artifact PR checks fail, treat that PR as the authoritative persistence gate and fix it through the normal PR workflow.
