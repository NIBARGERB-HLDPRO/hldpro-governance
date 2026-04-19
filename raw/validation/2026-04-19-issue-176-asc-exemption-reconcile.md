# Issue #176 Validation — ASC-Evaluator Exemption Reconciliation

Date: 2026-04-19  
Governance issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/176  
ASC-Evaluator repo: https://github.com/NIBARGERB-HLDPRO/ASC-Evaluator

## Live ASC-Evaluator Evidence

- Default branch: `master`
- Workflow inspected: `.github/workflows/governance.yml`
- Workflow behavior: calls `NIBARGERB-HLDPRO/hldpro-governance/.github/workflows/governance-check.yml@f941c5637a399c8aa122bd14b6ec64987351d52f`
- Latest default-branch Governance Gate: PASS
- Run: https://github.com/NIBARGERB-HLDPRO/ASC-Evaluator/actions/runs/24578334806
- Head: `4d7ecdb3313c1aa9b586bf2b8ffd21caa50174a6`
- Job: `governance-check / governance-check`
- Completed: 2026-04-17T17:33:47Z

## Disposition

No downstream ASC-Evaluator workflow edit is required. The repository has the lightweight governance docs required by the reusable docs gate (`docs/PROGRESS.md`, `docs/FEATURE_REGISTRY.md`, `docs/FAIL_FAST_LOG.md`, `docs/DATA_DICTIONARY.md`, `docs/SERVICE_REGISTRY.md`) and the current default-branch Governance Gate passes.

`SOM-ASC-CI-001` is stale and can be closed. `SOM-EXEMPT-ASC-001` remains active, but now explicitly means exempt from code-governance requirements, not exempt from carrying a minimal docs-only governance workflow.

## Commands

| Command | Result |
|---|---|
| `gh issue view 176 --repo NIBARGERB-HLDPRO/hldpro-governance --json state,title,body,url` | PASS — issue open and AC confirmed |
| `gh repo view NIBARGERB-HLDPRO/ASC-Evaluator --json defaultBranchRef,url,nameWithOwner` | PASS — default branch is `master` |
| `git -C /Users/bennibarger/Developer/HLDPRO/ASC-Evaluator fetch origin master --prune` | PASS |
| `find /Users/bennibarger/Developer/HLDPRO/ASC-Evaluator/.github/workflows -maxdepth 1 -type f -print -exec sed -n '1,180p' {} \\;` | PASS — `governance.yml` inspected |
| `gh run view 24578334806 --repo NIBARGERB-HLDPRO/ASC-Evaluator --json status,conclusion,headBranch,headSha,url,jobs` | PASS — run completed successfully |
| `python3 -m json.tool docs/plans/issue-176-structured-agent-cycle-plan.json` | PASS |
| `python3 -m json.tool raw/execution-scopes/2026-04-19-issue-176-asc-exemption-reconcile-implementation.json` | PASS |
| `git diff --check` | PASS |
| `python3 scripts/overlord/check_overlord_backlog_github_alignment.py` | PASS |
| `python3 scripts/overlord/check_progress_github_issue_staleness.py --repo NIBARGERB-HLDPRO/hldpro-governance` | PASS — skipped by design for governance repo because governance backlog is tracked in `OVERLORD_BACKLOG.md` |
| `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-176-asc-exemption-reconcile-implementation.json --changed-files-file /tmp/issue-176-changed-files.txt` | PASS with declared active parallel-root warnings only |
| `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` | PASS — 14 changed files, blockers 0, advisories 0 |

## Acceptance Criteria

- [x] Inspect current ASC-Evaluator `governance.yml` workflow.
- [x] Confirm the exemption is compatible and document why.
- [x] Update governance exception register to close stale `SOM-ASC-CI-001`.
- [x] Preserve `SOM-EXEMPT-ASC-001` as an active code-governance exemption with clarified scope.
- [x] Record e2e evidence before issue close.
