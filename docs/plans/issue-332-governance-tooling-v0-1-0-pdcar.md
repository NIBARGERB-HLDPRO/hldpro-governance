# PDCAR: Issue #332 Governance Tooling v0.1.0 Release

Date: 2026-04-19
Repo: `hldpro-governance`
Branch: `docs/issue-332-governance-tooling-v0-1-0-20260419`
Issue: [#332](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/332)
Related epic: [#288](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/288)
Status: IMPLEMENTATION_READY
Canonical plan: `docs/plans/issue-332-structured-agent-cycle-plan.json`

## Problem

The org governance tooling package is proven through downstream e2e evidence, but consumers still reference raw commit SHAs only. The package needs a first release tag so future downstream adoption can pin a readable release coordinate while still recording the exact SHA.

## Diagnosis

The existing package contract already anticipated semver tags after release:

- SHA pinning is mandatory.
- Semver tags are optional after release.
- Consumer records must keep the exact governance ref.

No existing governance tooling release tag is present, so `governance-tooling-v0.1.0` can become the first release coordinate after a green PR merge.

## Plan

1. Update the package manifest with first-release metadata.
2. Update the runbook with tag-plus-SHA pinning rules.
3. Add issue #332 planning and execution-scope artifacts.
4. Validate locally.
5. Open PR and require green GitHub Actions.
6. After merge, create annotated tag `governance-tooling-v0.1.0` against the merge commit.
7. Verify the remote tag points to the intended commit.
8. Comment final evidence on #332 and close out the isolated worktree.

## Do

In scope:

- `docs/governance-tooling-package.json`
- `docs/runbooks/org-governance-tooling-distribution.md`
- `docs/plans/issue-332-structured-agent-cycle-plan.json`
- `docs/plans/issue-332-governance-tooling-v0-1-0-pdcar.md`
- `raw/execution-scopes/2026-04-19-issue-332-governance-tooling-v0-1-0-planning.json`
- `raw/closeouts/2026-04-19-issue-332-governance-tooling-v0-1-0.md`
- `OVERLORD_BACKLOG.md`
- `docs/PROGRESS.md`
- closeout-hook generated `graphify-out/` and `wiki/` updates if produced

Out of scope:

- package deployer behavior
- downstream repo adoption
- existing tag mutation
- GitHub Release binary/archive publishing

## Check

Required local checks before PR:

- `python3 -m json.tool docs/governance-tooling-package.json`
- `python3 -m json.tool docs/plans/issue-332-structured-agent-cycle-plan.json`
- `python3 -m json.tool raw/execution-scopes/2026-04-19-issue-332-governance-tooling-v0-1-0-planning.json`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-332-governance-tooling-v0-1-0-planning.json --changed-files-file /tmp/issue-332-changed-files.txt`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-332-governance-tooling-v0-1-0-20260419 --changed-files-file /tmp/issue-332-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`
- `git diff --check`

Required after merge:

- `git tag -a governance-tooling-v0.1.0 <merge-commit> -m "governance tooling v0.1.0"`
- `git push origin governance-tooling-v0.1.0`
- `git ls-remote --tags origin governance-tooling-v0.1.0`
- `git rev-list -n 1 governance-tooling-v0.1.0`

## Adjust

Stop and revise if:

- `governance-tooling-v0.1.0` already exists remotely.
- The PR does not pass GitHub Actions.
- The tag cannot be verified against the merge commit.
- Any release work requires code behavior changes.

## Review

Subagent review is requested for release scope and validation. A true alternate-family reviewer is unavailable in this lane; this docs/tag-only slice uses same-family fallback plus deterministic local/GitHub checks.

## Acceptance Criteria

- Issue #332 exists.
- Structured plan and PDCAR exist.
- Package manifest and runbook document `governance-tooling-v0.1.0`.
- Local validation passes.
- PR GitHub Actions pass.
- Annotated tag `governance-tooling-v0.1.0` is pushed after merge.
- Remote tag verification proves the intended merge commit.
- Issue #332 records PR, merge commit, tag, and validation evidence.

