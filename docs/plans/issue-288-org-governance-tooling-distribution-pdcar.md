# PDCAR: Issue #288 Org Governance Tooling Distribution

Date: 2026-04-18
Repo: `hldpro-governance`
Branch: `codex/issue-288-org-governance-tooling-distribution`
Epic: [#288](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/288)
Status: PLANNING_PACKAGE
Canonical plan: `docs/plans/issue-288-structured-agent-cycle-plan.json`

## Problem

Governed repos are still absorbing governance tooling through repeated local profiles, managed shims, runbook edits, workflow copies, and repo-specific remediation loops. That has already created friction around hardgating, local wiring, enforcement semantics, and clean-environment assumptions.

The org needs a single versioned governance tooling distribution that governed repos can pull, deploy, verify, and roll back without manually recreating each tool.

## Diagnosis

The reusable pieces already exist in fragments:

- Local CI Gate runner, profiles, managed shim deployment, and workflow coverage checks.
- Execution-scope validation and active parallel root preflight.
- Graphify hook helper and governance-hosted graph/wiki artifacts.
- Structured agent cycle plan validation, backlog alignment, and closeout conventions.
- Repo-specific adoption slices proving the current path works but is too manual.

The missing system is the distribution layer: package metadata, version pinning, downstream pull/deploy command, compatibility matrix, evidence contract, and downstream e2e proof.

## Constraints

- GitHub Issues remain the canonical backlog.
- CI remains authoritative; local gates are upstream filters.
- Downstream repos must pin the governance package version they consume.
- Repo-local overrides must be explicit and reviewable.
- Managed deployment must be idempotent and reversible.
- The final epic closeout requires a real downstream e2e proof, not documentation-only approval.
- No downstream repo edits happen in this planning slice.

## Plan

Create the issue #288 planning package, then implement the epic through child slices:

| Phase | Purpose | Required proof |
|---|---|---|
| 0 | Planning package and epic contract | Structured plan, PDCAR, review/exception, execution-scope preflight |
| 1 | Distribution contract | Package manifest, versioning rules, ownership boundaries, override policy |
| 2 | Pull and deploy mechanism | Dry-run/apply/verify/rollback command with dirty-environment refusal tests |
| 3 | Local and GitHub verification matrix | Local commands mapped to GitHub workflow surfaces and closeout evidence |
| 4 | Downstream pilot | One downstream repo pulls and deploys the package from a pinned governance version |
| 5 | Final e2e proof and epic closeout | Negative control, local pass after remediation, GitHub Actions pass, rollback proof |

## Do

For this planning slice:

1. Create GitHub issue #288 as the epic.
2. Create the canonical structured plan.
3. Create this PDCAR companion.
4. Record a review/exception artifact for the Codex-only same-family planning lane.
5. Declare the execution scope and active parallel sibling roots.
6. Update `OVERLORD_BACKLOG.md` and `docs/PROGRESS.md`.
7. Validate the plan, execution scope, backlog alignment, and Local CI Gate.
8. Open and merge a planning PR while keeping issue #288 open.

## Check

Planning checks:

- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name codex/issue-288-org-governance-tooling-distribution --changed-files-file /tmp/issue-288-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `python3 scripts/overlord/check_execution_environment.py --scope raw/execution-scopes/2026-04-18-issue-288-org-governance-tooling-distribution-planning.json --changed-files-file /tmp/issue-288-changed-files.txt`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`
- PR #NNN GitHub Actions checks pass before merge.

Implementation checks by later phase:

- Package manifest schema validation.
- Deploy command unit tests.
- Idempotency and rollback tests.
- Dirty-environment refusal tests.
- Local CI Gate evidence in governance and the pilot repo.
- Downstream GitHub Actions pass with deployed tooling.

## Adjust

Stop and revise the plan if:

- The package shape requires weakening a repo-local hardgate.
- A downstream repo needs edits before a downstream issue and execution scope exist.
- The deployer cannot identify managed files and repo-local overrides cleanly.
- The downstream pilot relies on manual file copying.
- The final e2e proof cannot demonstrate a blocker being caught before push.

## Review

Required review posture:

- Same-family planning exception is recorded because this lane has Codex and subagents but no callable alternate-family model.
- Implementation slices that modify shared tooling code must obtain a fresh review artifact or explicit exception before work starts.
- Subagent review is required before planning PR closeout.
- Local and GitHub checks must pass even for planning-only artifacts.

## Acceptance Criteria

- Issue #288 exists as the governing epic.
- Structured plan exists and validates.
- PDCAR names package shape, distribution mechanism, repo adoption flow, rollback path, and ownership boundaries.
- Backlog and progress mirrors reference issue #288.
- Execution scope preflight passes from the isolated worktree.
- The plan decomposes the epic into measurable implementation phases.
- Local-ai-machine is the default downstream pilot unless Phase 4 proves a clean-worktree or deployment-prerequisite blocker and names a replacement repo before deployment.
- Final AC: issue #288 cannot close until a downstream repo has proven pull, deploy, local enforcement, GitHub enforcement, and rollback/uninstall behavior end to end.

## Open Questions For Implementation Slices

1. Should the first package version be a repo-local manifest plus deploy script, or a tagged release artifact consumed through `gh`?
2. Should the downstream package version pin be a git SHA only, or also a semver tag once the first package contract lands?
3. Which surfaces are package core versus repo profile: Local CI Gate profiles, graphify hook helper, execution-scope checker, workflow inventory, or all of them?
4. Should managed files carry a generated header with package version and source commit?
5. What is the minimum rollback proof: dry-run diff reversal, uninstall command, or actual revert commit in the pilot repo?
