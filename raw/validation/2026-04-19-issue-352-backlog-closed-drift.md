# Validation - Issue #352 Backlog Closed-Issue Drift

Date: 2026-04-19
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/352
Branch: `fix/issue-352-backlog-closed-drift-20260419`

## Results

| Check | Result |
|---|---|
| `python3 scripts/overlord/test_check_overlord_backlog_github_alignment.py` | PASS; 3 tests |
| `python3 scripts/overlord/check_overlord_backlog_github_alignment.py` | PASS; actionable governance backlog remains issue-backed and open-issue-backed |
| `python3 -m py_compile scripts/overlord/check_overlord_backlog_github_alignment.py scripts/overlord/test_check_overlord_backlog_github_alignment.py` | PASS |
| `python3 -m json.tool docs/plans/issue-352-structured-agent-cycle-plan.json` | PASS |
| `python3 -m json.tool raw/execution-scopes/2026-04-19-issue-352-backlog-closed-drift-implementation.json` | PASS |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name fix/issue-352-backlog-closed-drift-20260419 --require-if-issue-branch` | PASS; 69 plans validated |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name fix/issue-352-backlog-closed-drift-20260419 --changed-files-file /tmp/issue-352-changed-files.txt --enforce-governance-surface` | PASS; 69 plans validated |
| `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-352-backlog-closed-drift-implementation.json --changed-files-file /tmp/issue-352-changed-files.txt` | PASS; declared active parallel roots warned only |
| `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` | PASS; 11 changed files, blockers 0, advisories 0 |
| GitHub `local-ci-gate` first run | FAIL; Local CI workflow did not provide `GH_TOKEN` to the Overlord backlog check |

## Acceptance Criteria

| AC | Result |
|---|---|
| `OVERLORD_BACKLOG.md` has no closed issues in `Planned` or `In Progress` | PASS |
| Closed work is moved to `Done` or removed only when already represented by existing Done coverage | PASS |
| `check_overlord_backlog_github_alignment.py` fails when actionable rows reference closed issues | PASS |
| Focused e2e/unit coverage proves a closed issue in `In Progress` fails | PASS |
| PDCAR, structured plan, execution scope, validation evidence, and Stage 6 closeout are recorded | PASS pending closeout hook |
| Final AC: Local CI Gate and GitHub PR checks pass before merge | PASS locally; GitHub pending PR |

## CI Follow-Up

The first PR run showed a CI-only token gap in `.github/workflows/local-ci-gate.yml`. The workflow now grants `issues: read` and passes `GH_TOKEN: ${{ github.token }}` to the Local CI Gate runner, matching the validator's GitHub issue-state dependency.

## Reviewer Checkpoint

Read-only reviewer Pauli confirmed the stale In Progress issue refs: #200, #212, #213, #214, #223, #224, #296, and #298. The implementation reconciles those rows and adds the missing closed-issue enforcement path.
