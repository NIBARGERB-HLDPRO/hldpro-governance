# Issue #58 — Nightly Cleanup Timezone Policy PDCA/R

## Plan
- replace the brittle fixed-UTC nightly cleanup timing with a stable America/Chicago local-time policy
- keep the workflow simple and observable rather than introducing an external scheduler
- correct the roadmap pointer so the policy tracks against a canonical issue instead of the generated nightly report

## Do
- schedule both candidate UTC hours in `overlord-nightly-cleanup.yml`
- add an in-workflow local-time guard that only runs at 11:00 PM America/Chicago
- update the backlog mirror and fail-fast log

## Check
- verify the workflow syntax remains valid
- verify the policy logic is readable from the workflow itself
- verify the backlog now points to issue `#58`

## Adjust
- if GitHub Actions behavior around multi-cron dispatch produces noisy skipped runs, keep the policy but record a follow-up operational issue instead of silently reverting to fixed UTC timing

## Review
- issue `#58` is complete when the policy is explicit, year-round stable, and tracked under the correct canonical issue
