# Issue #313 Registry Surface Reconciliation Validation

Date: 2026-04-19
Governance issue: [#313](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/313)
Parent epic: [#298](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/298)

## Scope Summary

- Added explicit `seek-and-ponder` checkout steps to sweep and nightly cleanup workflows.
- Changed nightly cleanup repo iteration to `validate_governed_repos.py --print-subsystem sweep`.
- Changed raw-feed sync repo iteration to `validate_governed_repos.py --print-subsystem raw_feed_sync`.
- Changed local graphify symlink preparation to read scheduled targets from `docs/graphify_targets.json`.
- Updated README and STANDARDS to point to the executable registry as source of truth and include new repo summaries.
- Added `scripts/overlord/validate_registry_surfaces.py` and wired it into graphify contract CI plus Local CI Gate.

## Final E2E Command Outcomes

To be completed before PR publication:

| Command | Outcome |
|---|---|
| `python3 scripts/overlord/validate_governed_repos.py` | PASS |
| `python3 scripts/knowledge_base/test_graphify_governance_contract.py` | PASS |
| `python3 scripts/overlord/validate_registry_surfaces.py` | PASS |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-313-registry-surface-reconciliation-20260419 --changed-files-file /tmp/issue-313-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope` | PASS; validated 52 structured plan files |
| `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-313-registry-surface-reconciliation-implementation.json --changed-files-file /tmp/issue-313-changed-files.txt` | PASS with declared active-parallel-root warnings only |
| `python3 scripts/overlord/validate_backlog_gh_sync.py` | PASS |
| `python3 scripts/overlord/test_local_ci_gate_workflow_contract.py` | PASS |
| `python3 scripts/overlord/test_workflow_local_coverage.py` | PASS |
| `python3 -m py_compile scripts/overlord/validate_registry_surfaces.py scripts/overlord/governed_repos.py scripts/overlord/validate_governed_repos.py scripts/knowledge_base/graphify_targets.py` | PASS |
| `bash -n scripts/knowledge_base/prepare_local_graphify_repos.sh` | PASS |
| `git diff --check` | PASS |
| `tools/local-ci-gate/bin/hldpro-local-ci --profile tools/local-ci-gate/profiles/hldpro-governance.yml --changed-files-file /tmp/issue-313-changed-files.txt` | PASS |
