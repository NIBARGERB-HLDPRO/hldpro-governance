# Issue #391 Pre-Change GitHub Snapshot

Date: 2026-04-20
Repo: `NIBARGERB-HLDPRO/hldpro-governance`

## Repo Settings

Source: `prechange-repo.json`

- `allow_auto_merge`: `false`
- `delete_branch_on_merge`: `false`
- `allow_merge_commit`: `true`
- `allow_squash_merge`: `true`
- `allow_rebase_merge`: `true`
- `allow_update_branch`: `false`
- default branch: `main`

## Protection Evidence

- Classic branch protection endpoint for `main`: not present / HTTP 404; rulesets are the protection path.
- Repo rulesets include `15241047` (`Require Local CI Gate on main`) and `14715976` (`Protect main branches`).
- Org rulesets include `14715976` (`Protect main branches`) and `14716006` (`Protect develop branches`).

## Rollback Baseline

If the pilot fails, restore `allow_auto_merge` to `false` and verify the ruleset snapshots still match `prechange-repo-rulesets.json` and `prechange-org-rulesets.json`.

## Post-Change Evidence

Source: `postchange-repo.json`

- `allow_auto_merge`: `true`

Source: `label-merge-when-green.json`

- `merge-when-green` label exists and is the explicit pilot opt-in label.

No ruleset, required-check, review, CODEOWNER, or workflow setting was changed as part of this evidence update.

## Evaluator Evidence

Sources:

- `evaluator-eligible.json`
- `evaluator-blocked.json`

The eligible fixture exits `0` with no blockers. The blocked fixture exits `2` and blocks draft, dirty mergeability, failed Local CI Gate, unresolved review threads, blocking label, missing opt-in label, and missing PDCAR.

## Final Pilot Result

Sources:

- `final-pr-394.json`
- `final-repo.json`

PR #394 merged at `2026-04-20T15:09:06Z` with merge commit `8db8fec7cbd8faf1b29140312ef63be9d35e5c2b` after `local-ci-gate`, `commit-scope`, and graphify contract checks passed. CodeQL analysis completed successfully after merge. Repository `allow_auto_merge` remains `true` so future governed PRs can opt in through `merge-when-green`.
