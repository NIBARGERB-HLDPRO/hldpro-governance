# Issue #200 Validation - Codex Fire Fail-Fast

Date: 2026-04-19
Branch: `issue-200-codex-fire-failfast`
Issue: [#200](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/200)

## Acceptance Evidence

| AC | Evidence |
|---|---|
| `scripts/codex-fire.sh` created | Added wrapper with required `-m`, `-e`, `-w`, and `-b` interface plus optional `codex exec` pass-through args. Same-family exception is recorded because no separate Claude connector is available and the operator directed no HITL. |
| Preflight exits within 5 seconds on failure | `test_preflight_failure_logs_and_exits_fast` and `test_preflight_timeout_logs_and_exits_fast` force failing and sleeping fake Codex binaries with `CODEX_FIRE_TIMEOUT_SECONDS=1`; both assert elapsed time below 5 seconds. |
| Failure writes `raw/fail-fast-log.md` row | Fake-Codex preflight and execution failure tests assert rows containing `codex-exec`, the selected model, the error, and the brief file. |
| Dispatcher-visible failure signal | Failure tests assert `CODEX_FAIL: model=<model> exit=1 brief=<brief> — dispatcher must retry or escalate`. |
| Future local dispatcher Codex brief calls use wrapper | `scripts/codex-review-template.sh` audit and critique modes now call `scripts/codex-fire.sh`. Dedicated direct `codex exec` uses remain only in `scripts/codex-preflight.sh`, `.github/workflows/overlord-sweep.yml` canary paths, and `scripts/overlord/codex_ingestion.py`, which already have preflight/canary or bounded-timeout semantics and are not local dispatcher brief call sites. |
| Memory updated | Updated local auto-memory file `/Users/bennibarger/.claude/projects/-Users-bennibarger-Developer-HLDPRO-hldpro-governance/memory/feedback_codex_spark_specialist.md` to require `scripts/codex-fire.sh` for dispatcher-owned Codex briefs and to describe the `CODEX_FAIL`/`raw/fail-fast-log.md` behavior. This file is outside the repo and is recorded here as local evidence rather than committed content. |
| E2E final AC | `python3 -m pytest scripts/test_codex_fire.py` exercises unavailable model failure, preflight timeout, execution failure after successful preflight, success, and review-template failure propagation end to end with a fake `codex` executable on `PATH`. |

## Commands

| Command | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest scripts/test_codex_fire.py` | PASS; 5 tests |
| `bash -n scripts/codex-fire.sh scripts/codex-review-template.sh scripts/codex-preflight.sh` | PASS |
| `python3 .github/scripts/check_codex_model_pins.py` | PASS |
| `python3 -m py_compile scripts/test_codex_fire.py` | PASS |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-200-codex-fire-failfast --changed-files-file /tmp/issue-200-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope` | PASS; validated 59 structured plan files |
| `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-200-codex-fire-failfast-implementation.json --changed-files-file /tmp/issue-200-changed-files.txt` | PASS; dirty sibling roots were declared as active parallel work |
| `python3 scripts/overlord/check_overlord_backlog_github_alignment.py` | PASS |
| `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --repo-root . --changed-files-file /tmp/issue-200-changed-files.txt --report-dir cache/local-ci-gate/reports --json` | PASS; verdict `pass`, 23 changed files, 9 checks |
| `bash hooks/closeout-hook.sh raw/closeouts/2026-04-19-issue-200-codex-fire-failfast.md` | PASS; refreshed hldpro-governance graph/wiki artifacts, memory consolidation skipped because credentials were not configured |

## Notes

- The review template supports `CODEX_REVIEW_PERSONA` as a test/operator override because the default `docs/agents/codex-reviewer.md` path is absent in this checkout. The default path remains unchanged.
- The wrapper returns exit `1` on failures per issue #200 and preserves underlying failure details in the structured log row.
