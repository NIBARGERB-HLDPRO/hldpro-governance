# PDCAR: Issue #275 Local CI Gate Enforcement Remediation

## Problem

Recent Local CI Gate work added profiles, tests, and deployer behavior, but audit/debug review found enforcement gaps:

- profile dry-runs were treated as stronger proof than they are
- generated consumer shims can embed absolute target worktree paths
- hardgate wiring is not visibly required in governance CI or hooks
- the governance profile still references the old #253 execution scope
- session closeouts did not adequately evidence independent review, scope assertion status, or verify-completion

## Plan

Land a planning/scope PR before implementation:

- Add a structured plan for issue #275.
- Add planning and implementation execution scopes.
- Add this PDCA/R and a planning cross-review artifact grounded in the audit/debug reports.
- Update governance mirrors so #275 is the active Local CI Gate remediation lane.

Then implement on `feature/issue-275-local-ci-enforcement-remediation`:

- Make generated shims portable by resolving target repo root and shim path at runtime.
- Keep governance-root override through `HLDPRO_GOVERNANCE_ROOT`.
- Add live shim tests proving blocker failures exit non-zero through the shim.
- Remove stale #253 execution-scope wiring from the governance profile.
- Update runbook/status taxonomy and retrospective audit evidence.

## Do

Planning artifacts are added in the planning branch only. No runner, deployer, profile, workflow, or consumer repo implementation changes occur in this PR.

## Check

Planning validation:

- `python3 -m json.tool docs/plans/issue-275-structured-agent-cycle-plan.json >/dev/null`
- `python3 -m json.tool raw/execution-scopes/2026-04-18-issue-275-local-ci-enforcement-remediation-planning.json >/dev/null`
- `python3 -m json.tool raw/execution-scopes/2026-04-18-issue-275-local-ci-enforcement-remediation-implementation.json >/dev/null`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-275-local-ci-enforcement-remediation-plan`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-275-local-ci-enforcement-remediation-plan --changed-files-file /tmp/issue-275-planning-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `bash scripts/cross-review/require-dual-signature.sh raw/cross-review/2026-04-18-issue-275-local-ci-enforcement-remediation-plan.md`
- `git diff --check`

Implementation validation will additionally include:

- deployer tests for runtime target repo resolution
- live shim blocker-failure proof
- runner/report tests for governance root/ref and shim path evidence
- governance profile scope-resolution tests
- Local CI Gate profile dry-runs labeled mapping-only

## Adjust

If hardgate wiring cannot be made visibly required in repository files alone, record the limitation and require an operator-controlled ruleset/branch-protection follow-up. Do not call the gate hard-wired until that proof exists.

## Review

This remediation freezes further consumer rollout until the P0 issues are resolved. Knocktracker should be the first consumer follow-up after portable shim generation is fixed because its current shim may embed stale worktree paths.
