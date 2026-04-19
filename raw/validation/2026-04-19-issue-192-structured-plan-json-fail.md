# Validation - Issue #192 Structured Plan JSON Failure Contract

Date: 2026-04-19
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/192
Branch: `fix/issue-192-structured-plan-json-fail`

## Results

| Check | Result |
|---|---|
| `python3 -m json.tool docs/plans/issue-192-structured-agent-cycle-plan.json` | PASS |
| `python3 -m json.tool raw/execution-scopes/2026-04-19-issue-192-structured-plan-json-fail-implementation.json` | PASS |
| `python3 scripts/overlord/test_validate_structured_agent_cycle_plan.py` | PASS; 20 tests passed, including malformed JSON full-scan, governance-surface matching, duplicate-failure prevention, and read-error regressions |
| `python3 -m py_compile scripts/overlord/validate_structured_agent_cycle_plan.py scripts/overlord/test_validate_structured_agent_cycle_plan.py` | PASS |
| Temp malformed plan e2e: `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root "$tmpdir"` | PASS; emitted `FAIL docs/plans/issue-192-structured-agent-cycle-plan.json: could not parse JSON: ...`, exited 1, and emitted no traceback |
| Temp malformed governance-surface e2e: `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root "$tmpdir" --branch-name issue-192-test --changed-files-file "$tmpdir/changed.txt" --enforce-governance-surface` | PASS; emitted one parse failure, emitted the expected missing canonical-plan failure, exited 1, and emitted no traceback |
| `git diff --check` | PASS |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name fix/issue-192-structured-plan-json-fail --require-if-issue-branch` | PASS; validated 66 structured agent cycle plan files |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name fix/issue-192-structured-plan-json-fail --changed-files-file /tmp/issue-192-changed-files.txt --enforce-governance-surface` | PASS; validated 66 structured agent cycle plan files |
| `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-192-structured-plan-json-fail-implementation.json --changed-files-file /tmp/issue-192-changed-files.txt` | PASS; declared active parallel roots warned only |
| `python3 scripts/overlord/check_overlord_backlog_github_alignment.py` | PASS |
| `python3 scripts/overlord/check_progress_github_issue_staleness.py --repo NIBARGERB-HLDPRO/hldpro-governance` | PASS/SKIP by design because governance backlog is tracked in `OVERLORD_BACKLOG.md`, not `docs/PROGRESS.md` |
| `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` | PASS; 10 changed files, blockers 0, advisories 0 |
| Post-closeout `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` | PASS after adding `wiki/index.md` to the execution-scope allowlist for Stage 6 closeout generated index refresh |

## Final E2E AC

PASS. Temporary malformed `docs/plans/issue-192-structured-agent-cycle-plan.json` files produced structured `FAIL ... could not parse JSON ...` output, returned exit code 1, and produced no Python traceback in both full-scan and governance-surface modes. Governance-surface mode reports the parse failure once. The full repository plan set still validates successfully.

## Reviewer Checkpoint

Read-only reviewer `Carson` found one issue before closeout: governance-surface mode loaded the same malformed plan twice, producing duplicate parse-failure lines. The implementation now loads plan files once per run and reuses the parsed payloads for matching and full validation. Regression coverage now asserts only one `could not parse JSON` line in governance-surface mode and covers the `OSError` read-error branch with a directory that matches the structured-plan filename pattern.

Reviewer re-check verdict: no issues found. The reviewer independently reran the focused suite and observed 20 tests green. Residual risk: read-error coverage exercises `IsADirectoryError`; unusual `OSError` variants remain indirectly covered by the shared exception handler.

Post-closeout adjustment: the closeout hook refreshed `wiki/index.md`; the execution scope now explicitly allows that generated Stage 6 index artifact.
