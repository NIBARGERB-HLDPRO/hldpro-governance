# Issue #213 PentAGI Sweep Source Validation

Date: 2026-04-19
Issue: [#213](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/213)

## Acceptance Matrix

| AC | Evidence |
|---|---|
| Add deterministic PentAGI trigger/status step to local and CI overlord sweep path | `scripts/overlord/pentagi_sweep.py`, `.github/workflows/overlord-sweep.yml`, `agents/overlord-sweep.md` |
| If `PENTAGI_API_TOKEN` is unset, report `SKIPPED: missing PENTAGI_API_TOKEN` | `test_missing_report_skips_with_missing_token`, `test_stale_report_skips_with_missing_token`, temp-root E2E missing-token probe |
| If repo-specific PentAGI script is missing, report `SKIPPED: missing PentAGI runner` with expected path | `test_missing_runner_is_explicit_when_token_exists`, temp-root E2E missing-runner probe |
| Ensure report/dashboard derive PentAGI freshness from same repo root/ref | helper emits one JSON/Markdown payload with `repos_root`; workflow appends Markdown and persists JSON; agent docs require dashboard to consume the same helper output and forbid canonical checkout-only reports |
| Add regression test or dry-run harness for missing/stale PentAGI reports and trigger/skip status | `scripts/overlord/test_pentagi_sweep.py` plus temp-root E2E probes |
| Document whether untracked/local canonical reports count | `agents/overlord-sweep.md` documents they do not count; `test_untracked_fresh_report_does_not_count_for_audited_ref` enforces tracked-only git worktree behavior |
| E2E final AC | Temp audited-root E2E probes prove missing token, missing runner, fresh tracked report, untracked fresh report ignored, and tracked runner `--execute` path |

## Command Matrix

| Command | Outcome |
|---|---|
| `python3 -m pytest scripts/overlord/test_pentagi_sweep.py` | PASS; 8 passed |
| `python3 -m pytest scripts/overlord/test_pentagi_sweep.py scripts/overlord/test_validate_structured_agent_cycle_plan.py scripts/overlord/test_assert_execution_scope.py scripts/overlord/test_local_ci_gate_workflow_contract.py scripts/overlord/test_workflow_local_coverage.py` | PASS; 67 passed |
| `python3 -m py_compile scripts/overlord/pentagi_sweep.py` | PASS |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-213-pentagi-sweep-source --changed-files-file /tmp/issue-213-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope` | PASS; validated 57 structured agent cycle plan files |
| `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-213-pentagi-sweep-source-implementation.json --changed-files-file /tmp/issue-213-changed-files.txt` | PASS with declared active-parallel-root warnings only |
| `python3 scripts/overlord/validate_registry_surfaces.py` | PASS |
| `python3 scripts/overlord/check_overlord_backlog_github_alignment.py` | PASS |
| `git diff --check` | PASS |
| `tools/local-ci-gate/bin/hldpro-local-ci --profile tools/local-ci-gate/profiles/hldpro-governance.yml --changed-files-file /tmp/issue-213-changed-files.txt` | PASS with 26 changed files; blockers 0, advisories 0 |
| `hooks/closeout-hook.sh raw/closeouts/2026-04-19-issue-213-pentagi-sweep-source.md` | PASS; created closeout commit `e43f35a` and refreshed scoped graph/wiki artifacts |
| GitHub PR checks | Pending until PR is opened; merge is blocked until check names, conclusion, and run evidence are recorded in issue #213. |

## E2E Probe Summary

Missing token probe:

- Built a temporary audited root with tracked/stale and missing PentAGI reports.
- Ran `env -u PENTAGI_API_TOKEN python3 scripts/overlord/pentagi_sweep.py --repos-root "$TMPDIR_213" --date 2026-04-19`.
- Output included `SKIPPED: missing PENTAGI_API_TOKEN`.

Tracked-source and execute probe:

- Built a temporary audited root with git worktrees for `ai-integration-services`, `HealthcarePlatform`, and `seek-and-ponder`.
- Left an untracked fresh AIS report; it was ignored and reported as missing.
- Added a tracked fresh HealthcarePlatform report; it reported `NOT_NEEDED`.
- Added a tracked seek-and-ponder runner and ran with `PENTAGI_API_TOKEN=token --execute`; it reported `TRIGGERED`.

## Residual Risk Decision

The repository now owns the deterministic PentAGI status payload and CI/local sweep wiring. The external local dashboard script outside this repository still needs to consume that payload in operator environments; until then, the local sweep instructions require any dashboard reading a non-audited source to state that explicitly.
