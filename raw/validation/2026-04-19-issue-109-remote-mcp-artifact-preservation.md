# Validation — Issue #109 Remote MCP Artifact Preservation

Date: 2026-04-19
Branch: `issue-109-preserve-remote-mcp-plan-20260419`

## Commands

| Command | Result | Notes |
|---|---|---|
| `python3 -m json.tool docs/plans/issue-109-structured-agent-cycle-plan.json` | PASS | Structured plan JSON parses. |
| `python3 -m json.tool raw/execution-scopes/2026-04-19-issue-109-remote-mcp-artifact-preservation.json` | PASS | Initial execution-scope JSON parsed before renaming to implementation suffix. |
| `test -f raw/inbox/2026-04-14-remote-mcp-bridge-plan.md` | PASS | Remote MCP plan restored. |
| `test -f raw/cross-review/2026-04-14-remote-mcp-bridge.md` | PASS | Historical cross-review/resolution artifact restored. |
| `test -f raw/handoff/2026-04-14-session-end.md` | PASS | Session handoff restored. |
| `rg -n '_worktrees/gov-remote-mcp/raw/inbox/2026-04-14-remote-mcp-bridge-plan.md' raw wiki docs OVERLORD_BACKLOG.md` | PASS | No stale private worktree plan references remain. |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-109-preserve-remote-mcp-plan-20260419 --require-if-issue-branch` | PASS | Issue branch has structured plan coverage. |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-109-preserve-remote-mcp-plan-20260419 --changed-files-file /tmp/issue-109-changed-files.txt --enforce-governance-surface` | PASS | Governance-surface plan gate accepts the issue #109 scope. |
| `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-109-remote-mcp-artifact-preservation.json --changed-files-file /tmp/issue-109-changed-files.txt` | PASS | Initial manual assertion passed; Local CI later required the conventional `implementation` suffix. |
| `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` | FAIL, then PASS | First run failed planner-boundary because the execution scope did not match `*issue-109*implementation*.json`; after renaming to `raw/execution-scopes/2026-04-19-issue-109-remote-mcp-artifact-preservation-implementation.json`, the profile passed. A later Stage A slice renamed the preserved historical scope to `raw/execution-scopes/2026-04-19-issue-109-remote-mcp-artifact-preservation-scope.json` so current issue #109 execution scopes remain unambiguous. Final preservation report dir: `cache/local-ci-gate/reports/20260419T051218Z-hldpro-governance-git`. |
| `BASE_SHA=$(git merge-base origin/main HEAD) HEAD_SHA=HEAD python3 .github/scripts/check_no_self_approval.py` | FAIL, then PASS | First committed-branch run failed because modified historical file `raw/cross-review/2026-04-15-windows-ollama-tier2-round2.md` lacked `schema_version`; adding `schema_version: v1` made the parser pass. |
| `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` | PASS | Final committed-branch run passed with 35 changed files. Final report dir: `cache/local-ci-gate/reports/20260419T051407Z-hldpro-governance-git`. |

## Final Local CI Gate Summary

Final verdict: PASS on committed branch diff.

Checks:

- `overlord-backlog-alignment`: PASS
- `structured-agent-cycle-plans`: PASS
- `governance-surface-planning`: PASS
- `planner-boundary`: PASS
- `diff-hygiene`: PASS
- `workflow-local-coverage`: SKIPPED, no matching changed files
- `registry-surface-reconciliation`: SKIPPED, no matching changed files
- `governance-tooling-deployer-tests`: SKIPPED, no matching changed files
- `local-tool-tests`: SKIPPED, no matching changed files

## Notes

Execution-scope assertion emitted warnings for declared dirty sibling roots. Those roots are unrelated active parallel work and are listed under `active_parallel_roots` in the execution scope.
