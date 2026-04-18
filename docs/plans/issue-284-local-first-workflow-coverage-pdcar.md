# PDCAR: Issue #284 Local-First Workflow Coverage

## Problem

The Local CI Gate is now wired as a required repo check, but several adjacent GitHub Actions workflows still encode deterministic governance behavior that is easiest to catch only after push. That leaves operators discovering workflow drift in GitHub Actions instead of through local-first checks.

## Diagnosis

The repo has 22 workflow files. They are not all the same kind of runner:

- deterministic validators that should have local or contract coverage
- reusable governance workflows that should have workflow contract coverage
- scheduled or token-writing jobs that should have script-level or dry-run coverage only
- environment-dependent jobs that need explicit exemptions rather than pre-push replay

The gap is not "run all Actions locally." The gap is a tracked inventory and an enforcement test that fails when a workflow has no local-first coverage story.

## Constraints

- CI remains authoritative.
- Planning and execution-scope artifacts precede implementation edits.
- No consumer repo rollout is included.
- Scheduled, network-heavy, and side-effecting jobs are not blindly replayed locally.
- Real local and GitHub Actions test evidence is required before closeout.

## Actions

1. Create issue #284 as the epic.
2. Add this PDCAR, a structured plan, cross-review evidence, and execution-scope artifacts.
3. Add `docs/workflow-local-coverage-inventory.json`.
4. Add `scripts/overlord/check_workflow_local_coverage.py` and focused tests.
5. Wire the validator into the governance Local CI Gate profile and the independent contract workflow.
6. Run local negative/positive tests, Local CI Gate, and GitHub Actions.
7. Record closeout evidence with branch, commit, run IDs, and check names.

## Results / Acceptance Criteria

- Every workflow file is represented in the inventory.
- Deterministic workflows declare local, contract, or script/dry-run coverage.
- GitHub-only workflows declare explicit rationale.
- Tests fail for missing workflow inventory entries.
- Tests fail for deterministic workflows missing coverage commands.
- Local CI Gate runs the workflow coverage validator.
- GitHub Actions proves the wiring on the PR.

## Review

Subagent review is part of the workflow. The first local tooling review accepted the profile/test extension approach with one stale-context caveat; workflow classification review remains an implementation input and closeout evidence item.
