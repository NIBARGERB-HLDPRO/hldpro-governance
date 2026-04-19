# PDCAR: Issue #338 LAM Governance Tooling Adoption

Date: 2026-04-19
Repo: `hldpro-governance`
Branch: `docs/issue-338-lam-governance-tooling-adoption-20260419`
Issue: [#338](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/338)
Downstream issue: [local-ai-machine#475](https://github.com/NIBARGERB-HLDPRO/local-ai-machine/issues/475)
Release coordinate: `governance-tooling-v0.1.0`
Exact governance SHA: `8c5945e3d4f3f814dd80b4d158a9913c58a33609`
Status: IMPLEMENTATION_READY
Canonical plan: `docs/plans/issue-338-structured-agent-cycle-plan.json`

## Problem

The org governance tooling package now has a readable release tag, but the next durable proof is a real `local-ai-machine` adoption run. The previous LAM pilot halted before writes because the shared root checkout had unrelated hygiene blockers. This lane must avoid that failure mode by using a clean isolated LAM worktree and proving the managed tooling catches violations from the start.

## Diagnosis

The package contract requires exact SHA pinning in `.hldpro/governance-tooling.json`; the tag is only a human-readable release coordinate. LAM has stricter branch and session rules than a normal governed repo, including isolated session/worktree expectations and `riskfix/*` naming for high-risk governance lanes. The final AC must therefore be real e2e evidence, not a planning-only or dry-run result.

## Plan

1. Create governance epic #338 and downstream LAM issue #475.
2. Add governance PDCAR, structured plan, and execution scope.
3. Validate and publish the governance planning/status PR.
4. Create a clean LAM riskfix worktree for issue #475.
5. Acquire the LAM session lock and pass startup/worktree hygiene preflight.
6. Add LAM issue plan before implementation writes.
7. Run governance deployer `dry-run`, `apply`, and `verify` against LAM using profile `local-ai-machine`.
8. Prove a negative-control local enforcement failure by making a managed-tooling mismatch.
9. Restore/remediate and prove local pass.
10. Test or mechanically verify rollback, then reapply managed files.
11. Open LAM PR through the LAM riskfix publication path and require real GitHub Actions pass.
12. Record final closeout evidence in governance #338 and LAM #475.

## Do

Governance scope:

- `docs/plans/issue-338-structured-agent-cycle-plan.json`
- `docs/plans/issue-338-lam-governance-tooling-adoption-pdcar.md`
- `raw/execution-scopes/2026-04-19-issue-338-lam-governance-tooling-adoption-planning.json`
- `raw/closeouts/2026-04-19-issue-338-lam-governance-tooling-adoption.md`
- `OVERLORD_BACKLOG.md`
- `docs/PROGRESS.md`
- closeout-hook generated `graphify-out/` and `wiki/` updates if produced

Downstream LAM scope:

- LAM issue #475
- LAM structured plan
- managed `.hldpro/local-ci.sh`
- managed `.hldpro/governance-tooling.json`
- LAM progress/queue/runbook closeout evidence required by repo rules

Out of scope:

- unrelated LAM SoM/MCP root work
- changing governance package behavior unless a blocker proves a package defect
- tag-only downstream consumption
- manual copying of shared local CI runner logic

## Check

Governance local checks:

- `python3 -m json.tool docs/plans/issue-338-structured-agent-cycle-plan.json`
- `python3 -m json.tool raw/execution-scopes/2026-04-19-issue-338-lam-governance-tooling-adoption-planning.json`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-338-lam-governance-tooling-adoption-planning.json --changed-files-file /tmp/issue-338-changed-files.txt`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-338-lam-governance-tooling-adoption-20260419 --changed-files-file /tmp/issue-338-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`
- `git diff --check`

LAM local checks:

- session lock/preflight required by LAM startup rules
- strict worktree hygiene preflight before deployer writes
- governance deployer `dry-run`, `apply`, and `verify`
- managed shim invocation
- negative-control failure for mismatched managed tooling
- remediated local pass
- rollback or rollback proof, followed by reapply

GitHub checks:

- governance PR checks for the planning/status PR
- LAM PR checks for the downstream adoption PR

## Adjust

Stop and revise if:

- LAM cannot create a clean isolated worktree from `origin/main`.
- LAM startup/session lock preflight blocks the lane.
- The deployer refuses a clean target without a legitimate managed-path reason.
- The negative-control failure is not deterministic.
- GitHub Actions fail.

## Review

Read-only subagent review is requested for LAM-specific repo workflow constraints and e2e AC shape. A true alternate-family model is unavailable in this lane, so the final gate is deterministic: local deploy/verify, negative-control fail, remediation pass, rollback proof, and GitHub Actions pass.

## Acceptance Criteria

- Governance issue #338 exists.
- LAM issue #475 exists.
- Governance structured plan and PDCAR exist and validate.
- LAM adoption branch is clean and isolated.
- LAM session lock and startup/worktree hygiene preflight pass before deployer apply.
- LAM managed shim and consumer record are deployed by the governance package deployer.
- Consumer record preserves exact SHA `8c5945e3d4f3f814dd80b4d158a9913c58a33609`.
- Release coordinate `governance-tooling-v0.1.0` is recorded in evidence.
- Negative-control local enforcement fails before push.
- Remediated local enforcement passes.
- Rollback or rollback proof is recorded.
- LAM GitHub Actions pass, including riskfix routing and governance checks.
- Governance closeout links all evidence before issue #338 is closed.
