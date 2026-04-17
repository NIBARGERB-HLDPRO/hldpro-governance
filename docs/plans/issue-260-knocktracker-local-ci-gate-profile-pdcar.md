# PDCAR: Issue #260 Knocktracker Local CI Gate Profile

## Problem

Knocktracker adopted the governance-managed Local CI Gate shim in PR `NIBARGERB-HLDPRO/knocktracker#172`, but that shim remains dry-run only because the only merged toolkit profile is `hldpro-governance`. Running the governance profile live inside knocktracker would call governance-only scripts that do not exist in the consumer repo.

## Plan

Land a planning/scope PR before implementation:

- Add a canonical structured agent cycle plan for issue #260.
- Add planning and implementation execution scopes.
- Add this PDCA/R and the planning cross-review artifact.
- Update `OVERLORD_BACKLOG.md` so open issue #260 is visible and closed issue #253 is no longer listed under Planned.

Then implement on `feat/issue-260-knocktracker-local-ci-profile`:

- Add `tools/local-ci-gate/profiles/knocktracker.yml`.
- Keep the profile mapped only to commands already present in knocktracker.
- Add tests that load bundled profiles and preserve report/disclaimer behavior.
- Update the Local CI Gate runbook with the knocktracker profile and consumer shim update path.
- Dogfood dry-run and live invocations against an isolated knocktracker worktree.

## Do

Planning artifacts are added in the planning branch only. No runner, deployer, profile, or downstream product changes occur in this PR.

## Check

Planning validation:

- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-260-knocktracker-local-ci-profile-plan`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-260-knocktracker-local-ci-profile-plan --changed-files-file /tmp/issue-260-planning-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-17-issue-260-knocktracker-local-ci-profile-planning.json --changed-files-file /tmp/issue-260-planning-changed-files.txt`
- `git diff --check`

Implementation validation will additionally include:

- `python3 -m pytest tools/local-ci-gate/tests/test_local_ci_gate.py scripts/overlord/test_deploy_local_ci_gate.py -q`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile knocktracker --dry-run --json`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --repo-root /Users/bennibarger/Developer/HLDPRO/_worktrees/knocktracker-issue-171-local-ci-shim-20260417 --profile knocktracker --dry-run --json`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --repo-root /Users/bennibarger/Developer/HLDPRO/_worktrees/knocktracker-issue-171-local-ci-shim-20260417 --profile knocktracker --json`

## Adjust

If knocktracker command discovery shows an intended check is absent, the profile will omit that check rather than modifying knocktracker from this governance PR. If profile implementation changes the toolkit contract rather than adding a consumer profile, the implementation branch must add a fresh architecture cross-review artifact.

## Review

This slice is a consumer-profile extension of the already approved org-level toolkit. CI remains authoritative; Local CI Gate output must continue to identify local checks as an upstream filter rather than a full CI replay.
