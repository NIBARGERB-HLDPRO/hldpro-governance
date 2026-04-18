# PDCAR: Issue #292 Governance Tooling Deployer

Date: 2026-04-18
Repo: `hldpro-governance`
Branch: `codex/issue-292-governance-tooling-deployer`
Parent epic: [#288](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/288)
Slice issue: [#292](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/292)
Status: IMPLEMENTATION_READY
Canonical plan: `docs/plans/issue-292-structured-agent-cycle-plan.json`

## Problem

Issue #290 defined the governance tooling package contract, but downstream repos still need an executable deployer that can apply the contract safely. Without the deployer, adoption remains manual copying and the final #288 downstream e2e proof cannot be reached.

## Diagnosis

The existing `deploy_local_ci_gate.py` is a narrow managed-shim installer. It already proves marker-based ownership, allowed paths, dry-run previews, and unmanaged overwrite refusal. Phase 2 needs a package-level deployer above it that writes the consumer record, verifies installed state, rolls back managed files, and refuses dirty targets by default.

## Constraints

- Parent epic #288 remains open.
- No downstream governed repos are edited in this slice.
- Existing Local CI shim deployer compatibility remains intact.
- CI remains authoritative.
- Dirty targets and unmanaged managed-path files are refused by default.
- Real in-repo fixture tests are required before closeout.

## Plan

1. Create issue-backed planning and execution-scope artifacts.
2. Add `scripts/overlord/deploy_governance_tooling.py`.
3. Add fixture e2e tests in `scripts/overlord/test_deploy_governance_tooling.py`.
4. Wire deployer tests into the hldpro-governance Local CI profile.
5. Update the package manifest and runbook with implemented command semantics.
6. Run local tests, Local CI Gate, closeout hook, and GitHub Actions.

## Do

Implementation surfaces:

- package deployer: `scripts/overlord/deploy_governance_tooling.py`
- e2e tests: `scripts/overlord/test_deploy_governance_tooling.py`
- compatibility tests retained: `scripts/overlord/test_deploy_local_ci_gate.py`
- contract docs: `docs/governance-tooling-package.json`
- runbook: `docs/runbooks/org-governance-tooling-distribution.md`
- Local CI profile: `tools/local-ci-gate/profiles/hldpro-governance.yml`

## Check

Required local checks:

- `python3 scripts/overlord/test_deploy_governance_tooling.py`
- `python3 scripts/overlord/test_deploy_local_ci_gate.py`
- `python3 -m py_compile scripts/overlord/deploy_governance_tooling.py scripts/overlord/test_deploy_governance_tooling.py`
- `python3 -m json.tool docs/governance-tooling-package.json`
- `python3 scripts/overlord/check_execution_environment.py --scope raw/execution-scopes/2026-04-18-issue-292-governance-tooling-deployer-implementation.json --changed-files-file /tmp/issue-292-changed-files.txt`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name codex/issue-292-governance-tooling-deployer --changed-files-file /tmp/issue-292-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`

Required GitHub checks:

- `local-ci-gate`
- `validate`
- `contract`
- `commit-scope`
- CodeQL analysis

## Adjust

Stop and revise if:

- deployer writes to a dirty target by default,
- deployer overwrites unmanaged files by default,
- deployer tests do not exercise a real temporary git repo,
- existing Local CI shim deployer tests regress,
- or this slice claims the parent #288 downstream pilot is complete.

## Review

Subagent review is required for implementation shape and edge cases. Same-family exception is recorded because no callable alternate-family model is available in this lane.

## Acceptance Criteria

- Issue #292 exists before backlog/progress edits.
- PDCAR and structured plan exist and validate.
- Deployer supports `dry-run`, `apply`, `verify`, and `rollback`.
- Deployer writes `.hldpro/governance-tooling.json`.
- Deployer refuses unmanaged managed-path overwrites by default.
- Deployer refuses dirty target repos by default.
- Real in-repo fixture e2e test runs dry-run -> apply -> verify -> rollback.
- Idempotency, unmanaged overwrite refusal, unmanaged record refusal, dirty target refusal, and missing-record verify failure are tested.
- Local CI Gate runs deployer tests when deployer or contract files change.
- Parent epic #288 remains open for downstream pilot and final e2e proof.
