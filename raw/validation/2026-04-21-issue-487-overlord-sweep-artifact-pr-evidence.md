# Issue #487 Artifact PR Evidence Automation Validation

## Gap

PR #491 proved that a generated Overlord Sweep artifact PR can pass local-ci when its branch contains `issue-487` and an issue-specific execution scope is present.

The workflow still needed to create that branch name and scope evidence automatically so the next generated artifact PR does not repeat the #490 failure.

## Change

- `overlord-sweep.yml` now names generated artifact branches `automation/issue-487-overlord-sweep-${DATE}-${GITHUB_RUN_ID}`.
- The persistence step writes the single issue #487 execution scope before committing generated artifacts.
- The generated PR body records the issue #487 reference and the source workflow run.

## Local Validation

Passed locally on 2026-04-21:

```bash
git diff --name-only origin/main...HEAD > /tmp/issue-487-artifact-pr-evidence-changed.txt
python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-487-overlord-sweep-artifact-pr-evidence --changed-files-file /tmp/issue-487-artifact-pr-evidence-changed.txt --enforce-governance-surface --enforce-planner-boundary-scope
python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-487-overlord-sweep-artifact-pr-implementation.json --changed-files-file /tmp/issue-487-artifact-pr-evidence-changed.txt --require-lane-claim
```

Observed output:

- `PASS validated 122 structured agent cycle plan file(s)`
- `PASS execution scope matches declared root, branch, write paths, and forbidden roots`
- Warning only: the primary checkout has pre-existing `raw/fail-fast-log.md` edits and is declared as an active parallel root.
