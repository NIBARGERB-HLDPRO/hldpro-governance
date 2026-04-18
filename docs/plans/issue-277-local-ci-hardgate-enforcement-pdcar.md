# PDCAR: Issue #277 Local CI Gate Hardgate Enforcement

## Problem

Issue #275 fixed Local CI Gate mechanics but intentionally did not claim repo-level hardgate wiring. The remaining gap is enforcement: a gate that is merely runnable is not the same as a required check.

The repo needs a planned slice that defines and proves exactly which enforcement layer is being added:

- manual local live gate
- pre-push hook gate
- GitHub Actions PR check
- branch-protection or ruleset-required status check

## Plan

Land a planning/scope PR first:

- Add the structured plan for issue #277.
- Add planning and implementation execution scopes.
- Add a cross-review artifact that explicitly accepts a GitHub Actions check as the first implementation target.
- Move #275 out of active status and make #277 the active Local CI hardgate lane.

Then implement on `feature/issue-277-local-ci-hardgate-enforcement`:

- Add a governance-repo Local CI Gate workflow for pull requests to `main` and pushes to `main`.
- Run the live `hldpro-governance` profile, not `--dry-run`.
- Use full checkout history or an explicit changed-files file so changed-file resolution remains reliable in GitHub Actions.
- Add a workflow contract test that prevents the workflow from drifting into mapping-only mode.
- Wire that contract test into an existing independent CI-visible workflow so the Local CI Gate workflow cannot remove both the live invocation and its own guard in one edit.
- Record exact PR check names and whether the check is only CI-visible or actually required by branch protection/rulesets.
- Update the runbook taxonomy and closeout.

## Do

This planning branch only creates planning, scope, cross-review, and status artifacts. It does not change workflows, hooks, runner code, or rulesets.

## Check

Planning validation:

- `python3 -m json.tool docs/plans/issue-277-structured-agent-cycle-plan.json >/dev/null`
- `python3 -m json.tool raw/execution-scopes/2026-04-18-issue-277-local-ci-hardgate-enforcement-planning.json >/dev/null`
- `python3 -m json.tool raw/execution-scopes/2026-04-18-issue-277-local-ci-hardgate-enforcement-implementation.json >/dev/null`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-277-local-ci-hardgate-enforcement-plan`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-277-local-ci-hardgate-enforcement-plan --changed-files-file /tmp/issue-277-planning-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `bash scripts/cross-review/require-dual-signature.sh raw/cross-review/2026-04-18-issue-277-local-ci-hardgate-enforcement-plan.md`
- `git diff --check`

Implementation validation will additionally include:

- workflow contract tests
- live Local CI Gate workflow run evidence on PR
- exact GitHub check names
- branch-protection/ruleset evidence if protected enforcement is claimed

## Adjust

If the workflow can be added but ruleset/branch-protection enforcement cannot be safely changed or verified, close only the implementation PR's CI-visible portion and keep #277 open for protected-branch required-check wiring. A child issue may exist for subtask tracking, but it does not replace #277 as the hardgate issue of record.

If live Local CI Gate is too expensive or flaky as a PR check, do not silently convert it to dry-run. Revise the plan and acceptance criteria before implementation.

## Review

Independent review must check that the implementation does not overstate enforcement. The closeout must use the runbook taxonomy and must not call a visible workflow check a required protected-branch gate unless GitHub configuration evidence proves it.
