# PDCAR: Issue #386 Org-Level Automerge Policy For Green Verified PRs

Date: 2026-04-20
Branch: `issue-386-org-automerge-policy-main-20260420`
Issue: [#386](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/386)
Prerequisite: [#384](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/384)

## Plan

Define and locally test a governed automerge policy for PRs that are complete, verified, tested, and green. The policy must not weaken branch protection. It should automate only the final merge request after GitHub and governance checks already prove the PR satisfies required reviews, required status checks, mergeability, and repo-specific governance gates.

Current live findings:

- Org ruleset `14715976` protects `main`/`master` with PR-only, deletion, and non-fast-forward rules, but no org-level approving-review, code-owner-review, review-thread-resolution, or required-status-check rule.
- Org ruleset `14716006` protects `develop` from deletion and non-fast-forward pushes, but does not require PRs or checks.
- `hldpro-governance` currently has `allow_auto_merge: false`.
- Existing Enterprise docs intentionally defer broad required-check rollout until exact live check names, conditional checks, CODEOWNERS, and exceptions are reconciled.

## Do

1. Define eligibility:
   - PR is not draft.
   - PR targets a protected branch covered by the rollout.
   - PR has no merge conflicts and is mergeable.
   - All required checks are successful and no required check is pending.
   - Required reviews and CODEOWNER reviews are satisfied where configured.
   - Review threads are resolved where configured.
   - The PR has no blocking labels such as `do-not-merge`, `hold`, `security-review-required`, or `manual-merge-required`.
   - The PR has an explicit opt-in label during pilot rollout, such as `automerge` or `merge-when-green`.
   - Governance artifacts required by the repo are present, including issue-backed PDCAR/closeout evidence where applicable.
2. Add a local-only dry-run evaluator:
   - `scripts/overlord/automerge_policy_check.py` reads a PR-state fixture and returns `eligible`, blockers, warnings, and rollback steps.
   - The evaluator never calls GitHub APIs and never enables or performs merges.
3. Choose the future implementation mechanism:
   - Enable GitHub native auto-merge per target repo.
   - Add a governed reusable workflow or repo-local workflow that enables auto-merge for eligible PRs with `gh pr merge --auto` or the GraphQL `enablePullRequestAutoMerge` mutation.
   - Keep merge execution inside GitHub's protected-branch/ruleset engine; do not write a bot that force-merges or bypasses protections.
4. Stage rollout:
   - Stage 0: merge #384 so backlog alignment is green again.
   - Stage 1: hldpro-governance pilot after `allow_auto_merge` is enabled and `local-ci-gate` remains required.
   - Stage 2: repos with stable required-check baselines and CODEOWNERS coverage.
   - Stage 3: production-critical repos after repo owner acknowledgement and exception review.

## Check

- Unit tests prove eligible fixture passes.
- Unit tests prove draft, conflicted, red, unreviewed, unresolved-thread, missing-CODEOWNER, blocking-label, missing-opt-in, disabled-repo, and missing-governance-artifact states fail.
- CLI dry-run returns exit `0` only for eligible fixtures and exit `2` for blocked fixtures.
- Confirm each future target repo has `allow_auto_merge` enabled before rollout.
- Confirm target repo rulesets or branch protections require the intended checks and reviews before auto-merge is allowed.
- Confirm required checks are exact live contexts, not workflow filenames.
- Confirm actor-conditional and path-conditional checks are not treated as universal merge gates.
- Confirm Dependabot and bot PR behavior is explicitly classified before inclusion.

## Adjust

Do not implement this as a broad org toggle. GitHub auto-merge is repository/PR behavior, while rulesets define the conditions that make auto-merge safe. If a repo lacks stable required checks or review requirements, leave automerge disabled or require explicit operator opt-in until the repo's ruleset baseline is complete.

## Rollback

Rollback must be documented before any live rollout:

1. Remove the PR opt-in label (`automerge` or `merge-when-green`) to stop that PR from entering automation.
2. Disable or remove the automerge workflow entrypoint.
3. Disable the repository `allow_auto_merge` setting.
4. Restore the previous ruleset or branch-protection snapshot if rollout changed enforcement.
5. Record persistent rollback or exception state in `GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md`.

## Review

Review should verify the policy is an automation of an already-safe merge state, not a replacement for review, testing, verification, or issue-backed governance evidence.
