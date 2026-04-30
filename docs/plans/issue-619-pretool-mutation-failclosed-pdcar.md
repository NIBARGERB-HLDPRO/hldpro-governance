# Issue #619 PDCAR: Implement Local Mutation Pre-Tool Fail-Closed Hardening

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/619
Parent: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/615
Prior child: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/617
Dependencies:
- https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/607
- https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/612
Related follow-up:
- https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/614
Branch: `issue-619-pretool-mutation-failclosed-20260430`

## Plan

Implement the next smallest residual child under issue `#615` after `#617`
merged: local mutation-time pre-tool fail-closed hardening for
governance-surface writes.

This child owns the local mutation/pre-tool path only. It must not reopen the
startup/helper surfacing already closed by `#617`, and it must not absorb the
planning-authority contract in `#607`, the degraded-fallback schema or CI
contract in `#612`, or the downstream consumer verifier work in `#614`.

Mandatory intake for this lane includes:

- `docs/PROGRESS.md`
- issue `#615` plus its critical closeout contract and routing updates
- merged child issue `#617`
- dependency issues `#607` and `#612`
- issue `#591`, `ai-integration-services#1414`, and PR `ai-integration-services#1417`
- the live local mutation surfaces:
  - `.claude/settings.json`
  - `hooks/code-write-gate.sh`
  - `hooks/schema-guard.sh`
  - `scripts/overlord/check_plan_preflight.py`

## Do

Implementation scope for issue `#619`:

- wire the local mutation gate to mutation-capable tool paths, including `Edit`
  and `MultiEdit`, rather than `Write` alone
- switch local plan-evidence preflight to canonical governed evidence under
  `docs/plans/*structured-agent-cycle-plan.json` or equivalent issue-local
  governed plan state
- harden Bash mutation detection for the named write verbs from `#615`
- remove fail-open or warning-only behavior for in-scope governance-surface
  mutation cases on the owned local path
- add focused tests and validation artifacts for blocked and allowed cases on
  the owned mutation path only
- co-stage the required governance docs for a bounded governance-surface code
  slice: `docs/PROGRESS.md`, `docs/FEATURE_REGISTRY.md`, and the relevant
  `docs/FAIL_FAST_LOG.md` entry
- produce the issue-local Stage 6 closeout artifact for the bounded mutation
  path slice

## Check

The lane is acceptable only if it:

- remains bounded to the local mutation-time pre-tool path and does not reopen
  `#617` startup/helper ownership
- keeps `#607` as the planning-authority dependency instead of absorbing that
  contract
- keeps `#612` as the degraded-fallback schema and CI enforcement lane
- keeps `#614` as the downstream consumer verifier or drift-gate lane
- keeps `hooks/backlog-check.sh`, `hooks/governance-check.sh`, CI workflows,
  and `scripts/orchestrator/delegation_gate.py` out of scope unless later
  rerouted
- returns concrete blocked and allowed proof on the local mutation path rather
  than prose-only assertions
- co-stages the required governance docs for the bounded implementation slice
- carries a valid Stage 6 closeout artifact for the issue-local implementation
  slice

Implementation validation must include:

- targeted tests for the touched mutation helper and hook surfaces
- a per-surface proof matrix covering:
  - one blocked `Edit` or `MultiEdit` governance-surface mutation without
    valid canonical governed plan evidence
  - one blocked Bash mutation using the named write verbs from `#615`
  - one blocked case proving warning-only or fail-open behavior is gone on an
    owned in-scope path
  - one allowed governance-surface mutation with valid canonical governed plan
    evidence
  - one allowed read-only or out-of-scope case
- one blocked transcript for each named local fail-closed case with exact
  command, exit code, and block message
- one compliant governance-surface allowed case and one out-of-scope or
  read-only allowed case
- bounded-write proof for the eventual implementation diff:
  - touched-file list stays inside the owned mutation surfaces, focused tests,
    required governance doc co-staging, and issue-local artifacts
  - explicit no-touch proof for `hooks/pre-session-context.sh`,
    `scripts/overlord/check_execution_environment.py`,
    `scripts/overlord/assert_execution_scope.py`, CI workflows, and other
    sibling-lane surfaces
- the repo-local Stage 6 closeout validator
- the `hldpro-governance` Local CI Gate profile
- `git diff --check`

## Adjust

If this lane starts editing `hooks/pre-session-context.sh` or
`scripts/overlord/check_execution_environment.py`, stop and keep the work on
the `#617`-successor mutation surfaces only.

If this lane starts editing `assert_execution_scope.py`, fallback-log schema
surfaces, or CI workflow enforcement that belongs to `#612`, stop and route
that work back to `#612`.

If this lane starts rewriting `hooks/backlog-check.sh`,
`hooks/governance-check.sh`, or broad policy text instead of the owned
mutation-time surfaces, stop and split or reroute the work.

If this lane starts claiming repo-wide write blocking or fresh-session
impossibility, stop and restore the anti-overclaim boundary: this is a local
mutation-time source-repo slice only.

## Review

Required before completion:

- research specialist check that the implementation write set stays bounded to
  the mutation-time surfaces above
- QA specialist proof review against the `#615` closeout contract
- critical audit review of the lane ACs and proof obligations
- governed alternate-family review of the implementation packet before
  promotion or closeout

Issue `#619` may close source-repo local mutation-time pre-tool fail-closed
hardening only. It cannot be cited as proof that `#607`, `#612`, or `#614`
are closed, and it does not close the broader pre-hook fail-closed program
still owned by `#615`.
