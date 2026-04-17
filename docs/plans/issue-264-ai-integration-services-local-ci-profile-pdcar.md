# PDCAR: Issue #264 AI Integration Services Local CI Gate Profile

## Problem

The Local CI Gate toolkit has one live consumer profile for knocktracker. To prove the org-level model scales beyond one Expo app, governance needs a second consumer profile for `ai-integration-services`.

## Plan

Land a planning/scope PR before implementation:

- Add a canonical structured agent cycle plan for issue #264.
- Add planning and implementation execution scopes.
- Add this PDCA/R and the planning cross-review artifact.
- Update roadmap/status mirrors so #260 is complete and #264 is active.

Then implement on `feat/issue-264-ai-integration-services-local-ci-profile`:

- Add `tools/local-ci-gate/profiles/ai-integration-services.yml`.
- Use only AIS commands that already exist.
- Scope heavy app builds/tests by changed paths where practical.
- Add bundled-profile tests.
- Update the Local CI Gate runbook profile catalog.
- Dogfood dry-run and live invocations against an isolated AIS worktree.

## Do

Planning artifacts are added in the planning branch only. No runner, deployer, profile, or downstream product changes occur in this PR.

## Check

Planning validation:

- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-264-ais-local-ci-profile-plan`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-264-ais-local-ci-profile-plan --changed-files-file /tmp/issue-264-planning-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-17-issue-264-ai-integration-services-local-ci-profile-planning.json --changed-files-file /tmp/issue-264-planning-changed-files.txt`
- `bash scripts/cross-review/require-dual-signature.sh raw/cross-review/2026-04-17-issue-264-ai-integration-services-local-ci-profile-plan.md`
- `git diff --check`

Implementation validation will additionally include:

- `python3 -m pytest tools/local-ci-gate/tests/test_local_ci_gate.py scripts/overlord/test_deploy_local_ci_gate.py -q`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile ai-integration-services --dry-run --json`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --repo-root <isolated-ais-worktree> --profile ai-integration-services --dry-run --json`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --repo-root <isolated-ais-worktree> --profile ai-integration-services --json`

## Adjust

If AIS command discovery shows a candidate check is absent or too environment-heavy for local default enforcement, the profile will omit it or keep it changed-file scoped. Governance will not add AIS product scripts from this PR.

## Review

This slice is a consumer-profile extension of the already approved org-level toolkit. CI remains authoritative; Local CI Gate output must continue to identify local checks as an upstream filter rather than a full CI replay.
