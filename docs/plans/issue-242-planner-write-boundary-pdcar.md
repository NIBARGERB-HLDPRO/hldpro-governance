# Issue #242 — Planner Write-Boundary Enforcement PDCA/R

## Plan

Issue #242 closes the governance-control gap exposed during #241 planning: Tier 1 planner sessions may create planning, review, and handoff artifacts, but non-planning diffs need accepted pinned-agent handoff evidence. The durable control must bind that rule to changed files, not rely on prose.

Scope stays narrow:

- Define a machine-checkable planning artifact allowlist.
- Extend execution-scope evidence with optional pinned-agent handoff metadata.
- Wire `scripts/overlord/assert_execution_scope.py` into CI as the strict planner-boundary gate.
- Keep local hook behavior as warning or early signal only for this boundary; CI remains authoritative.
- Preserve historical structured agent cycle plans by avoiding required schema changes.
- Add tests for planning-only diff inside `allowed_write_paths` passing, planning-only diff outside `allowed_write_paths` failing, non-planning diff without handoff failing, accepted pinned-agent handoff passing, planner-model implementer handoff failing without active exception, active exception with expiry passing, and diff-mode/dirty-tree mode sharing path normalization rules.

## Do

Planned implementation package:

- Add diff-file input support to `assert_execution_scope.py` so CI checks PR changed files instead of only local dirty state.
- Add optional `execution_mode` and `handoff_evidence` support to execution-scope JSON payloads:
  - `execution_mode: planning_only` permits only `allowed_write_paths`.
  - non-planning modes require `handoff_evidence.status: accepted`.
  - planner/implementer same model or same family requires `active_exception_ref`.
  - active exceptions must include a concrete reference and expiry.
- Add a strict PR step in `.github/workflows/governance-check.yml` after changed-file resolution.
- Adjust `hooks/code-write-gate.sh` to surface planner-boundary drift as warning-only for this specific checker path while keeping existing new-code routing behavior intact.
- Update `STANDARDS.md`, `README.md`, `docs/DATA_DICTIONARY.md`, `docs/FEATURE_REGISTRY.md`, and `docs/SERVICE_REGISTRY.md`.
- Add focused tests in `scripts/overlord/test_assert_execution_scope.py`.

## Check

Planned validation:

- `python3 scripts/overlord/test_assert_execution_scope.py`
- `python3 scripts/overlord/test_validate_structured_agent_cycle_plan.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-242-planner-write-boundary --require-if-issue-branch`
- `git diff --name-only origin/main...HEAD > /tmp/issue-242-changed-files.txt`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-242-planner-write-boundary --changed-files-file /tmp/issue-242-changed-files.txt --enforce-governance-surface`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-17-issue-242-planner-write-boundary-planning.json`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-17-issue-242-planner-write-boundary-implementation.json --changed-files-file /tmp/issue-242-changed-files.txt`
- `python3 -m py_compile scripts/overlord/assert_execution_scope.py scripts/overlord/test_assert_execution_scope.py scripts/overlord/validate_structured_agent_cycle_plan.py`
- workflow YAML parse check
- `python3 scripts/overlord/validate_backlog_gh_sync.py`
- `python3 scripts/knowledge_base/test_graphify_governance_contract.py`

## Adjust

Research agents agreed that the lowest-risk implementation is the execution-scope checker, not the structured-plan schema. The structured plan contract scans historical plans and has `additionalProperties: false`; adding required fields there would risk breaking old plans. The execution-scope artifact is the correct place for path allowlist and pinned-agent handoff evidence.

The audit agent found the root gap: existing rules described planner boundaries, but earlier local enforcement only blocked new code-file writes and allowed existing-file edits plus docs/config/data files. #226 later added branch-level governance-surface gating, but #242 still needs file-scope planner/non-planning enforcement and accepted handoff evidence.

Claude review of this #242 planning package returned `APPROVED_WITH_CHANGES`. The cross-review artifact now has schema frontmatter, the execution-scope username path was verified as correct, and the PDCAR test list was reconciled with the seven-case cross-review acceptance list.

## Review

Prior alternate-family review for #241/#242 required:

1. Define a planning-artifact path allowlist.
2. Define an exception mechanism.
3. Add a warning-to-strict transition.
4. Specify minimal handoff evidence schema.
5. Ensure hooks and PR gates block in strict mode and implementer briefs require handoff.

This plan incorporates those requirements by making CI strict, local hooks early warning for the new boundary, and execution-scope evidence the handoff record.
