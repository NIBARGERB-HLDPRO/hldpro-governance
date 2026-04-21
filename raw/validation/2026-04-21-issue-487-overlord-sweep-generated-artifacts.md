# Issue #487 Generated Artifact Persistence Validation

## Context

Overlord Sweep run `24739922689` completed successfully across the governed repository set and created PR #490 with generated graph, wiki, self-learning, Pentagi, and effectiveness baseline artifacts.

PR #490 failed `local-ci-gate` because the generated branch name did not include `issue-<number>`, so governance-surface enforcement could not resolve a canonical structured plan or execution scope.

## Corrective Action

- Created corrected branch `automation/issue-487-overlord-sweep-2026-04-21-24739922689` from PR #490's generated artifact snapshot.
- Added issue #487 structured plan evidence.
- Added issue #487 implementation execution scope with directory-bounded generated artifact permissions.

## Acceptance Criteria Mapping

- Branch contains `issue-487`: yes.
- Generated artifact paths are bounded to `graphify-out/`, `wiki/`, `metrics/effectiveness-baseline/`, `metrics/pentagi/`, `metrics/self-learning/`, and `docs/ORG_GOVERNANCE_COMPENDIUM.md`: yes.
- Governance evidence files are explicitly allowed: yes.
- No application source code writes are allowed by the execution scope: yes.

## Validation Results

Passed locally on 2026-04-21:

```bash
python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name automation/issue-487-overlord-sweep-2026-04-21-24739922689 --changed-files-file /tmp/issue-487-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope
python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-487-overlord-sweep-artifact-pr-implementation.json --changed-files-file /tmp/issue-487-changed-files.txt --require-lane-claim
```

Observed output:

- `PASS validated 121 structured agent cycle plan file(s)`
- `PASS execution scope matches declared root, branch, write paths, and forbidden roots`
- Warning only: primary checkout has pre-existing `raw/fail-fast-log.md` edits and is declared as an active parallel root.
