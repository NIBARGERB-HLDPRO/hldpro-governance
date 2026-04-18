# PDCAR: Issue #290 Governance Tooling Distribution Contract

Date: 2026-04-18
Repo: `hldpro-governance`
Branch: `codex/issue-290-governance-tooling-contract`
Parent epic: [#288](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/288)
Slice issue: [#290](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/290)
Status: IMPLEMENTATION_READY
Canonical plan: `docs/plans/issue-290-structured-agent-cycle-plan.json`

## Problem

The org-level governance tooling epic needs a concrete distribution contract before a deployer can be implemented safely. Without the contract, Phase 2 could hard-code tool assumptions, overwrite repo-local files, or produce adoption evidence that cannot be rolled back or audited.

## Diagnosis

The reusable tooling exists, but it is split across runner code, profiles, deployer scripts, validators, workflow inventories, graphify helpers, and runbooks. The missing contract is:

- what is package core versus repo-specific profile,
- what may be written into consumer repos,
- how consumer repos record the governance version they consume,
- how overrides are approved,
- how rollback/uninstall is represented,
- and which checks prove the contract.

## Constraints

- CI remains authoritative.
- Parent epic #288 remains open after this slice.
- This slice does not edit downstream repos.
- This slice does not implement the generalized Phase 2 deployer.
- Downstream consumption must be pinned by governance git SHA.
- Managed files must be marked and reversible.

## Plan

1. Create issue-backed planning and execution-scope artifacts for #290.
2. Add `docs/governance-tooling-package.json` as the machine-readable package contract.
3. Add `docs/runbooks/org-governance-tooling-distribution.md` as the operator contract and Phase 2 handoff.
4. Update backlog/progress mirrors for the active slice.
5. Validate JSON, execution scope, structured plans, backlog alignment, and Local CI Gate.
6. Close #290 only after PR checks pass; leave #288 open.

## Do

Artifacts added in this slice:

- `docs/governance-tooling-package.json`
- `docs/runbooks/org-governance-tooling-distribution.md`
- `docs/plans/issue-290-structured-agent-cycle-plan.json`
- `docs/plans/issue-290-governance-tooling-contract-pdcar.md`
- `raw/cross-review/2026-04-18-issue-290-governance-tooling-contract-plan.md`
- `raw/exceptions/2026-04-18-issue-290-same-family-contract.md`
- `raw/execution-scopes/2026-04-18-issue-290-governance-tooling-contract-implementation.json`
- closeout evidence after validation

## Check

Required local checks:

- `python3 -m json.tool docs/governance-tooling-package.json`
- `python3 -m json.tool docs/plans/issue-290-structured-agent-cycle-plan.json`
- `python3 scripts/overlord/check_execution_environment.py --scope raw/execution-scopes/2026-04-18-issue-290-governance-tooling-contract-implementation.json --changed-files-file /tmp/issue-290-changed-files.txt`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name codex/issue-290-governance-tooling-contract --changed-files-file /tmp/issue-290-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`

Required remote checks:

- PR `local-ci-gate`
- PR `validate`
- PR `contract`
- PR `commit-scope`
- CodeQL analysis

## Adjust

Stop and revise if:

- the contract allows unpinned downstream consumption,
- managed files can be overwritten without marker/backup/force rules,
- repo-local overrides can hide CI-required enforcement,
- rollback is deferred out of the contract,
- or this slice claims final downstream e2e proof.

## Review

Same-family exception is recorded because this lane has Codex and subagents but no callable alternate-family model. The exception is limited to contract artifacts and does not authorize deployer code or downstream edits.

Subagent review is required for surface classification and validation risk. Deterministic local checks and GitHub Actions are required before merge.

## Acceptance Criteria

- Issue #290 exists before backlog/progress edits.
- PDCAR and structured plan exist and validate.
- Distribution runbook names included and excluded surfaces.
- Package manifest is valid JSON and machine-readable.
- Every manifest surface has owner, version rule, consumer mode, and verification command.
- Managed-file, override, consumer-record, and rollback rules are explicit.
- Phase 2 deployer requirements are stated.
- Final downstream e2e remains a hard AC for #288 and is not marked complete here.
- Local validation and PR checks pass before #290 closes.
