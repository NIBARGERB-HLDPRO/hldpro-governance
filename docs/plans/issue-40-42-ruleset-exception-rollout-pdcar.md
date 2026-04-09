# Issues #40 and #42 — Ruleset Rollout + Exception Register PDCA/R

Date: 2026-04-09
Issues:
- `#40`
- `#42`
Branch: `issue-40-42-ruleset-exception-rollout`

## Plan

- verify the current org and repo ruleset state from GitHub
- replace stale recommendation text with an actionable rollout sequence
- operationalize the exception register with explicit approvers, cadence, and current entries

## Do

- queried active org rulesets and repo-level rulesets
- confirmed current org rulesets are still branch-safety only
- captured live repo-level drift in `ai-integration-services` and `local-ai-machine`
- rewrote the rollout pack from current-state truth
- seeded current governance exceptions instead of leaving the register empty

## Check

- first-wave repos now have `.github/CODEOWNERS` on default branches
- required-check baseline and rollout pack now agree
- known non-baseline deviations are documented explicitly instead of implied

## Adjust

- keep the first enforcement pass conservative
- require every non-baseline deviation to live in the exception register with a review date
- separate admin rollout sequencing from repo-local workflow changes

## Review

- `#40` is satisfied by the updated actionable rollout pack
- `#42` is satisfied by the adopted exception register ownership/cadence plus seeded entries
- follow-on execution work belongs to later admin application or to issue `#43` metrics/tracking
