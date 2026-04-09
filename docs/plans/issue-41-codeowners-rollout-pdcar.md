# Issue #41 — Sprint 1 CODEOWNERS Rollout PDCA/R

Date: 2026-04-09
Issue: `#41`
Branch: `issue-41-codeowners-rollout`

## Plan

- re-verify first-wave CODEOWNERS status from the current default branch
- correct stale governance inventory where draft-lane assumptions drifted from reality
- package minimal `.github/CODEOWNERS` repo lanes for repos still missing coverage

## Do

- checked default-branch `.github/CODEOWNERS` presence for first-wave repos
- confirmed `ai-integration-services` is already complete
- confirmed `HealthcarePlatform`, `knocktracker`, and `local-ai-machine` still need CODEOWNERS on their default branches
- created a fresh HealthcarePlatform issue to track the missing repo lane
- prepared minimal CODEOWNERS-only repo changes for the three incomplete repos

## Check

- the old Sprint 1 inventory was stale for HealthcarePlatform
- dormant repo lanes are not proof of completion until the file is merged on the default branch
- local-ai-machine now requires a `riskfix/*` branch family for the clean repo lane path

## Adjust

- keep Sprint 1 rollout scope tied to merged default-branch state
- use minimal CODEOWNERS-only branches rather than replaying stale mixed-purpose lanes

## Review

- after repo-local PRs merge, recheck default-branch coverage
- then move `#41` to done and let `#40` consume the verified coverage baseline
