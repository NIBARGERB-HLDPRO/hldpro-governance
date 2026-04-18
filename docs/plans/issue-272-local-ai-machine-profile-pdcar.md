# PDCAR: Issue #272 Local AI Machine Local CI Gate Profile

## Problem

The Local CI Gate toolkit now supports governance, knocktracker, and AIS profiles, but local-ai-machine does not yet have a governance-owned profile. LAM should be onboarded without copying local check logic into the repo and without editing its currently dirty shared checkout.

## Plan

Land a planning/scope PR before implementation:

- Add a canonical structured agent cycle plan for issue #272.
- Add planning and implementation execution scopes.
- Add this PDCA/R and the planning cross-review artifact.
- Update governance mirrors so closed #265 is no longer active and #272 is active.

Then implement on `feat/issue-272-local-ai-machine-profile`:

- Add `tools/local-ci-gate/profiles/local-ai-machine.yml`.
- Use direct existing LAM commands from `origin/main` workflows instead of adding npm wrappers.
- Scope heavier checks to matching changed-file surfaces.
- Add focused runner tests for profile load and changed-file scoping.
- Update the Local CI Gate runbook profile catalog and closeout.

## Do

Planning artifacts are added in the planning branch only. No runner, deployer, profile, or downstream LAM changes occur in this PR.

## Check

Planning validation:

- `python3 -m json.tool docs/plans/issue-272-structured-agent-cycle-plan.json >/dev/null`
- `python3 -m json.tool raw/execution-scopes/2026-04-18-issue-272-local-ai-machine-profile-planning.json >/dev/null`
- `python3 -m json.tool raw/execution-scopes/2026-04-18-issue-272-local-ai-machine-profile-implementation.json >/dev/null`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-272-local-ai-machine-profile-plan`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-272-local-ai-machine-profile-plan --changed-files-file /tmp/issue-272-planning-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `bash scripts/cross-review/require-dual-signature.sh raw/cross-review/2026-04-18-issue-272-local-ai-machine-profile-plan.md`
- `git diff --check`

Implementation validation will additionally include:

- `python3 tools/local-ci-gate/tests/test_local_ci_gate.py`
- `python3 -m pytest tools/local-ci-gate/tests/test_local_ci_gate.py -q`
- dry-run checks for `hldpro-governance`, `knocktracker`, `ai-integration-services`, and `local-ai-machine`

## Adjust

If a candidate LAM command requires environment state not appropriate for local pre-push checks, keep it out of the profile or mark it advisory and changed-file scoped. CI remains authoritative.

## Review

This is a consumer profile addition for an already approved toolkit. The LAM repo itself remains out of scope until a separate consumer rollout issue installs the managed shim.
