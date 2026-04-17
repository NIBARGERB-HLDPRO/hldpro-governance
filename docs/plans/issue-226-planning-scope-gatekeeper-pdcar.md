# Issue #226 — Planning and Scope Gatekeeper PDCA/R

## Plan

Issue #226 implements the Phase 2 gatekeeper slice from epic #224. The target failure mode is implementation-first governance work: governance-surface edits must not proceed on `main`, feature branches, or Markdown-only planning artifacts. They need a GitHub issue, canonical structured JSON plan, accepted review status, and implementation-ready handoff.

The slice stays inside deterministic governance enforcement:

- Extend `validate_structured_agent_cycle_plan.py` with governance-surface path classification and changed-file enforcement.
- Wire that validator into reusable governance CI and the local write gate.
- Keep execution-root, branch, dirty forbidden-root, and allowed-write-path enforcement in `assert_execution_scope.py`.
- Add tests that prove governed paths fail without issue-specific planning and non-governed paths do not get over-gated.

## Do

- Added governance-surface file and prefix classification to the structured-plan validator.
- Added `--changed-files-file` and `--enforce-governance-surface` inputs.
- Required governance-surface changes to have an issue branch, matching `issue_number`, `approved: true`, implementation-ready or complete handoff, and accepted alternate review when required.
- Added validator unit tests for non-issue branches, missing matching plans, non-governed path allowance, implementation mode, and required review readiness.
- Added regression coverage for dot-directory governance paths such as `.github/scripts/` and `.github/workflows/`.
- Wired `.github/workflows/governance-check.yml` to persist changed files and run the shared validator.
- Wired `hooks/code-write-gate.sh` to run the same validator for local file writes.

## Check

Planned validation:

- `python3 scripts/overlord/test_validate_structured_agent_cycle_plan.py`
- `python3 scripts/overlord/test_assert_execution_scope.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-226-planning-scope-gatekeeper-20260417 --require-if-issue-branch`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-226-planning-scope-gatekeeper-20260417 --changed-files-file /tmp/issue-226-changed-files.txt --enforce-governance-surface`
- `python3 -m py_compile scripts/overlord/validate_structured_agent_cycle_plan.py scripts/overlord/test_validate_structured_agent_cycle_plan.py scripts/overlord/assert_execution_scope.py scripts/overlord/test_assert_execution_scope.py`
- workflow YAML parse check
- `python3 .github/scripts/check_codex_model_pins.py`
- `python3 .github/scripts/check_agent_model_pins.py`
- `python3 scripts/knowledge_base/test_graphify_governance_contract.py`
- `python3 scripts/overlord/build_org_governance_compendium.py --check`

## Adjust

The implementation intentionally does not make `not_requested` an accepted state for required alternate-model review. If review is required, the plan must record `accepted` or `accepted_with_followup` before governance-surface implementation proceeds.

Alternate review found that `.github/scripts/` was missing and path normalization stripped the leading dot from `.github/...` paths. Both were fixed before closeout validation.

The issue body names `hooks/governance-check.sh`, but this checkout has `hooks/code-write-gate.sh` as the local write-time gate. This slice wires the existing hook instead of introducing a duplicate hook name.

## Review

Alternate-family review is recorded in `raw/cross-review/2026-04-17-planning-scope-gatekeeper.md`.
