# Issue #39 — Required-Check Baseline Verification PDCA/R

Date: 2026-04-09
Issue: `#39`
Branch: `issue-39-required-check-baseline`

## Plan

- verify live first-wave check names from current PRs
- resolve the three open policy questions called out in the backlog
- update the baseline and ruleset docs so they reflect current actor/path-conditional behavior
- move the backlog item to `Done` once the documentation truth is consistent

## Do

- sampled live PR checks in:
  - `ai-integration-services`
  - `HealthcarePlatform`
  - `knocktracker`
  - `local-ai-machine`
- inspected repo-local workflow conditions for:
  - `governance-check`
  - `playwright-gate`
  - local-ai-machine specialized workflows
- updated governance baseline and ruleset guidance accordingly

## Check

- knocktracker `governance-check` skip behavior is intentional, not a bug
- local-ai-machine specialized checks are not safe first-pass org required checks
- HealthcarePlatform `build` is baseline-safe now
- HealthcarePlatform `playwright-gate` remains conditional because it skips Dependabot

## Adjust

- treat actor-conditional and path-conditional checks as non-baseline until workflow policy changes
- keep first org ruleset pass conservative

## Review

- this issue closes the stale assumptions in the older draft baseline
- follow-on rollout work belongs in `#40`, `#41`, and `#42`, not in this issue
