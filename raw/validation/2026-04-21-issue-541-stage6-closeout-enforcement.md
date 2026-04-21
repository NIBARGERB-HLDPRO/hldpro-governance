# Issue #541 Validation: Stage 6 Closeout Enforcement

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/541
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/533
Branch: `issue-541-stage6-closeout-enforcement-v2`
Date: 2026-04-21

## Scope

This slice turns Stage 6 closeout from a manual post-work convention into a merge-enforced gate for implementation/governance-surface PRs.

- `scripts/overlord/check_stage6_closeout.py` requires an issue-matching `raw/closeouts/*issue-NNN*.md` for non-planning governance-surface diffs.
- Matching closeouts are validated through the existing `scripts/overlord/validate_closeout.py`.
- Planning-only PRs remain exempt when changes are limited to plan, scope, cross-review, progress, or backlog mirror artifacts.
- `.github/workflows/governance-check.yml` and `tools/local-ci-gate/profiles/hldpro-governance.yml` call the same validator.

## Validation

- PASS: `python3 scripts/overlord/test_check_stage6_closeout.py`
  - `Ran 6 tests`
- PASS: `python3 scripts/overlord/test_workflow_local_coverage.py`
- PASS: `python3 scripts/overlord/validate_handoff_package.py --root . raw/handoffs/2026-04-21-issue-541-stage6-closeout-enforcement.json`
- PASS: `python3 scripts/overlord/validate_closeout.py raw/closeouts/2026-04-21-issue-541-stage6-closeout-enforcement.md --root .`
- PASS: `python3 scripts/overlord/check_stage6_closeout.py --root . --branch-name issue-541-stage6-closeout-enforcement-v2 --changed-files-file /tmp/issue-541-changed-files.txt`
- PASS: `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-541-stage6-closeout-enforcement-v2 --changed-files-file /tmp/issue-541-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- PASS: `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-541-stage6-closeout-enforcement-implementation.json --changed-files-file /tmp/issue-541-changed-files.txt --require-lane-claim`
- PASS: `python3 scripts/orchestrator/self_learning.py --root . lookup --query 'stage 6 closeout missing after implementation' --limit 3`
  - Top match: `raw/operator-context/self-learning/2026-04-21-issue-541-stage6-closeout-enforcement.md`
- PASS: `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`
  - Report: `cache/local-ci-gate/reports/20260421T220342Z-hldpro-governance-git`
  - New `stage6-closeout-evidence` check passed.

## Acceptance Criteria Mapping

- AC1: Missing closeout for implementation/governance-surface changes fails in `test_implementation_changes_without_closeout_fail`.
- AC2: Planning-only changes pass in `test_planning_only_changes_do_not_require_closeout`.
- AC3: Valid closeout passes and invalid closeout fails through `validate_closeout.py`.
- AC4: Multiple issue-matching closeouts fail in `test_multiple_matching_closeouts_fail`.
- AC5: Reusable governance CI and Local CI call `check_stage6_closeout.py`.
- AC6: Self-learning evidence and fail-fast/error-pattern records document the passive-gate gap.

## Review And Gate Identity

- Specialist reviewer: `stage6-closeout-enforcement-specialist`, model `gpt-5.4-mini`, family `openai`, signature date 2026-04-21, verdict `ACCEPTED`.
- Implementer/reviewer: `codex-orchestrator`, model `gpt-5.4`, family `openai`, signature date 2026-04-21, verdict `ACCEPTED`.
- Gate identity: `deterministic-local-gate`, model `python-unittest/validator`, family `deterministic`, signature date 2026-04-21.

## Residual Risk

Downstream repos that call the reusable governance workflow will inherit this gate after merge. That is intentional for governed implementation PRs, but consumer rollout should be watched through epic #533 and corrected with issue-backed exceptions if a repo has a legitimate planning-only shape not covered here.
