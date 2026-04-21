# Issue #538 PDCAR: Hook Guardrail Reliability

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/538
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/533
Branch: `issue-538-hook-guardrail-reliability`

## Plan

Repair existing hook guardrails in place so session commands are classified by actual mutation intent instead of brittle raw-string matches. The sprint addresses three concrete error classes:

- read-only `awk`/`jq` comparisons misclassified as Bash file writes;
- heredoc bodies or commit-message text influencing branch-switch policy;
- documented no-force-push policy lacking local enforcement.

## Do

Change only the hook/classifier sprint surfaces:

- `hooks/schema-guard.sh`
- `hooks/branch-switch-guard.sh`
- `scripts/overlord/check_plan_preflight.py`
- `scripts/overlord/test_check_plan_preflight.py`
- `scripts/overlord/test_schema_guard_hook.py`
- `scripts/overlord/test_branch_switch_guard.py`
- issue #538 planning, scope, validation, closeout, and self-learning evidence

Prefer one command-classification path for Bash write detection. Add force-push prevention to the existing branch/worktree guard rather than creating a new hook layer.

## Check

Required validation:

- `python3 scripts/overlord/test_schema_guard_hook.py`
- `python3 scripts/overlord/test_check_plan_preflight.py`
- `python3 scripts/overlord/test_branch_switch_guard.py`
- `bash -n hooks/schema-guard.sh hooks/branch-switch-guard.sh hooks/code-write-gate.sh`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-538-hook-guardrail-reliability --changed-files-file /tmp/issue-538-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-538-hook-guardrail-reliability-implementation.json --require-lane-claim`

Negative controls must prove:

- read-only `awk`/`jq` commands pass;
- real Bash writes still block;
- heredoc bodies containing `git checkout main` do not trigger branch switching blocks;
- force-push forms are blocked.

## Adjust

If command parsing needs broader shell coverage than the observed failure shapes, keep the parser conservative and issue-backed. Do not normalize a broad shell interpreter rewrite inside this sprint unless the focused tests cannot be made reliable.

## Review

Closeout must cite the tests, updated session-error pattern evidence, and any residual command forms intentionally left out of scope.
