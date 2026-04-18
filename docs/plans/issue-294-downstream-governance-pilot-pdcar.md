# PDCAR: Issue #294 Downstream Governance Tooling Pilot

Date: 2026-04-18
Repo: `hldpro-governance`
Branch: `codex/issue-294-downstream-governance-pilot`
Parent epic: [#288](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/288)
Slice issue: [#294](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/294)
Status: PLANNING_PACKAGE
Canonical plan: `docs/plans/issue-294-structured-agent-cycle-plan.json`

## Problem

The org governance tooling package now has a contract (#290) and deployer (#292), but the parent epic #288 still lacks downstream proof. The next slice needs a concrete consumer-pilot plan with hard acceptance criteria for deploy, local enforcement, GitHub Actions, and rollback.

## Diagnosis

The deployer is proven inside `hldpro-governance` with temporary git-repo fixtures. That is necessary but not enough. A governed repo must prove the package works from a clean downstream worktree, using a pinned governance ref, the generated consumer record, the managed shim, and the repo's actual local/GitHub gate surfaces.

`local-ai-machine` remains the default pilot because the package contract names it and the governance repo already owns a `local-ai-machine` Local CI profile. Its main checkout currently has active unrelated work, so the pilot must start from a clean isolated downstream worktree and must not touch the dirty main checkout.

## Constraints

- GitHub issue #294 exists before planning/backlog edits.
- Parent epic #288 remains open.
- This planning slice does not edit downstream repos.
- The pilot implementation must use a clean downstream worktree from the consumer repo default branch.
- Dirty downstream main checkouts and active sibling lanes are declared as active parallel roots, not cleaned.
- CI remains authoritative; local gates are upstream filters.
- Final downstream e2e testing is a hard AC, not optional evidence.

## Plan

1. Create issue-backed planning artifacts for #294.
2. Select `local-ai-machine` as the default downstream pilot and define fallback criteria.
3. Define the exact downstream implementation sequence and stop conditions.
4. Require negative-control enforcement proof before remediation.
5. Require local pass, GitHub Actions pass, and rollback/uninstall proof before claiming downstream completion.
6. Validate the planning package locally and through GitHub Actions.

## Do

Planning artifacts in this slice:

- `docs/plans/issue-294-structured-agent-cycle-plan.json`
- `docs/plans/issue-294-downstream-governance-pilot-pdcar.md`
- `raw/cross-review/2026-04-18-issue-294-downstream-governance-pilot-plan.md`
- `raw/exceptions/2026-04-18-issue-294-same-family-planning.md`
- `raw/execution-scopes/2026-04-18-issue-294-downstream-governance-pilot-planning.json`
- `OVERLORD_BACKLOG.md`
- `docs/PROGRESS.md`

## Check

Required local checks for this planning slice:

- `python3 -m json.tool docs/plans/issue-294-structured-agent-cycle-plan.json`
- `python3 -m json.tool raw/execution-scopes/2026-04-18-issue-294-downstream-governance-pilot-planning.json`
- `python3 scripts/overlord/check_execution_environment.py --scope raw/execution-scopes/2026-04-18-issue-294-downstream-governance-pilot-planning.json --changed-files-file /tmp/issue-294-changed-files.txt`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name codex/issue-294-downstream-governance-pilot --changed-files-file /tmp/issue-294-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`

Required GitHub checks:

- `local-ci-gate`
- `validate`
- `contract`
- `commit-scope`
- CodeQL analysis

## Adjust

Stop and revise if:

- LAM cannot create a clean pilot worktree from its remote default branch.
- LAM lacks a runnable `local-ai-machine` profile prerequisite that the pilot cannot satisfy without unrelated remediation.
- The pilot would require hand-copying managed tooling instead of running `deploy_governance_tooling.py`.
- The negative-control failure is skipped or treated as optional.
- A local pass is used as a substitute for GitHub Actions.
- Rollback/uninstall proof is deferred without a follow-up issue linked to #288.

## Review

Same-family planning exception is recorded because no callable alternate-family model is available in this lane. Mitigations:

- subagent planning review,
- deterministic structured plan validation,
- execution-scope preflight,
- backlog/GitHub alignment,
- Local CI Gate,
- GitHub Actions before merge,
- required downstream implementation issue before consumer repo edits.

## Pilot Target And Fallback Rule

Default target: `local-ai-machine`.

Fallback is allowed only if the implementation slice proves one of these blockers before any downstream writes:

- `local-ai-machine` cannot create a clean isolated worktree from its remote default branch.
- `local-ai-machine` cannot run package deployment prerequisites without unrelated remediation.
- Its repo-local governance surface is actively being changed in a way that would make the pilot evidence ambiguous.

Fallback selection order:

1. `ai-integration-services`, if its active lane is complete or a clean isolated worktree is available and the profile is current.
2. `knocktracker`, if a clean isolated worktree is available and the profile is current.
3. Do not select a repo with no governance-owned profile unless a separate issue adds that profile first.

## Downstream Implementation Sequence

The next implementation slice must:

1. Create or confirm a downstream repo issue.
2. Create a clean downstream worktree from the consumer repo remote default branch.
3. Create a downstream execution scope before writes.
4. Run `deploy_governance_tooling.py dry-run` from a pinned governance ref.
5. Run `deploy_governance_tooling.py apply`.
6. Verify `.hldpro/governance-tooling.json` records the governance repo, ref, package version, profile, managed files, local verification, GitHub verification, and overrides.
7. Invoke the managed shim directly from the downstream repo.
8. Introduce a deliberate negative-control violation that must fail locally.
9. Remove or remediate the violation and prove the local gate passes.
10. Push a downstream PR and watch GitHub Actions to completion.
11. Prove rollback or uninstall on a separate downstream test branch/worktree or fixture.
12. Record all evidence back on #288 and #294.

## Acceptance Criteria

- Issue #294 exists and links to parent #288.
- PDCAR and structured plan exist and validate.
- Plan selects `local-ai-machine` as the default pilot and defines fallback criteria.
- Plan defines downstream issue/worktree/execution-scope requirements before consumer writes.
- Plan requires managed deploy using `deploy_governance_tooling.py`, not manual copying.
- Plan requires generated consumer record verification.
- Plan requires a deliberate negative-control local failure before remediation.
- Plan requires local pass after remediation.
- Plan requires downstream GitHub Actions pass.
- Plan requires rollback/uninstall proof.
- Plan requires any fallback target to already have a governance-owned Local CI profile, or a separate profile issue must land before pilot deployment.
- Plan keeps #288 open until downstream evidence is attached.

## Final E2E AC

Issue #288 cannot close until a downstream repo proves, with links:

- clean consumer worktree,
- pinned governance ref,
- deployer dry-run/apply/verify,
- generated `.hldpro/governance-tooling.json`,
- managed shim invocation,
- deliberate local blocker caught before push,
- local pass after remediation,
- downstream GitHub Actions pass,
- rollback or uninstall proof,
- downstream and governance closeout comments.
