# PDCAR: Issue #391 Native GitHub Automerge Pilot

Date: 2026-04-20
Branch: `issue-391-automerge-pilot-20260420`
Issue: [#391](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/391)
Policy dependency: [#386](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/386)

## Plan

Run the first governed automerge pilot on `hldpro-governance` using native GitHub auto-merge. The pilot must accelerate only PRs that are already mergeable by protected-branch policy; it must not weaken required checks, rulesets, review requirements, CODEOWNERS, or exception handling.

Pilot repo: `NIBARGERB-HLDPRO/hldpro-governance`.

Pre-change evidence is stored under `raw/validation/issue-391-automerge-pilot/`:

- `prechange-repo.json`
- `prechange-repo-rulesets.json`
- `prechange-org-rulesets.json`
- `prechange-branch-protection.json`
- `prechange-summary.md`

## Do

1. Capture repository, org ruleset, repo ruleset, and branch-protection snapshots before live changes.
2. Create or reuse an explicit `merge-when-green` opt-in label.
3. Enable the repository `allow_auto_merge` setting only; do not change rulesets, required checks, reviews, or workflow definitions.
4. Open a pilot PR for this issue-backed planning/evidence slice.
5. Add the opt-in label to the pilot PR.
6. Run the dry-run evaluator for both blocked and eligible fixture states.
7. Enable native GitHub auto-merge on the pilot PR after checks are queued.
8. Let GitHub merge the PR only after required checks pass.

## Check

Required local checks:

- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-20-issue-391-native-automerge-pilot-implementation.json --changed-files-file <changed-files>`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci --repo-root . --profile hldpro-governance --changed-files-file <changed-files> --json`
- `git diff --check`

Required GitHub checks:

- `check-backlog-gh-sync / validate`
- `check-pr-commit-scope / commit-scope`
- `graphify-governance-contract / contract`
- `local-ci-gate / local-ci-gate`

## Adjust

If auto-merge cannot be enabled, do not bypass the merge path. Record the blocker, disable repository auto-merge if it was enabled, remove the PR opt-in label, and keep issue #391 open with the failing evidence.

## Review

Successful pilot evidence is a PR merged by native GitHub auto-merge after required checks pass. Expansion to other repos remains blocked until this pilot records merge evidence and a rollback/fix-forward note.

## Rollback

1. Remove `merge-when-green` or `automerge` from the pilot PR.
2. Disable repository auto-merge:

   ```bash
   gh api -X PATCH repos/NIBARGERB-HLDPRO/hldpro-governance -f allow_auto_merge=false
   ```

3. Restore any setting drift from `raw/validation/issue-391-automerge-pilot/prechange-repo.json`.
4. Confirm repo ruleset `15241047` and org ruleset `14715976` still enforce the protected `main` path.
5. Record rollback evidence under `raw/validation/issue-391-automerge-pilot/`.
