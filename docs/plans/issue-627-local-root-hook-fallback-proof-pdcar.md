# Issue #627 PDCAR: Local Root-Hook Degraded-Fallback Proof Consumption

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/627
Parent: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/615
Dependency: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/625
Branch: `issue-627-local-root-hook-fallback-proof`

## Plan

Produce and then execute the bounded implementation slice for governance issue
`#627`, the next narrow child under `#615` after the merged `#625`
execution-scope slice.

This child exists because the local root-hook path still needs to consume the
now-merged degraded-fallback proof contract without widening into the remaining
validator/workflow work under `#612`.

Mandatory intake for this lane includes:

- `docs/PROGRESS.md`
- issue `#615` and its later routing comments
- issue `#625` merge outcome and closeout trail
- issue `#612` only as a boundary/dependency, not as owned implementation
- the local root-hook surfaces:
  - `hooks/backlog-check.sh`
  - `hooks/governance-check.sh`
  - the smallest shared helper path needed to consume `#625` proof

## Do

Owned implementation target:

- `hooks/governance-check.sh`
- `scripts/overlord/check_governance_hook_execution_scope.py`
- focused tests and issue-local proof artifacts only

Implementation obligations for issue `#627`:

- consume the merged `#625` execution-scope proof contract rather than
  redefining it
- fail closed when degraded same-family fallback proof is absent or invalid on
  the local governance-hook consumer path
- keep the child bounded to local root-hook consumption only

## Check

The slice is acceptable only if it:

- states clearly that `#627` is a child of `#615`, not a reopen of `#625`
- keeps ownership bounded to local root-hook degraded-fallback proof
  consumption
- requires fail-closed local behavior when `#625` proof is missing, blank,
  unsafe, or malformed on the root-hook path
- explicitly excludes fallback-log schema/workflow parity under `#612`
- explicitly excludes planning-authority work under `#607`
- explicitly excludes downstream verifier/drift-gate work under `#614`

Validation commands:

- `python3 -m json.tool docs/plans/issue-627-local-root-hook-fallback-proof-structured-agent-cycle-plan.json`
- `python3 -m json.tool raw/execution-scopes/2026-04-30-issue-627-local-root-hook-fallback-proof-implementation.json`
- `python3 -m json.tool raw/handoffs/2026-04-30-issue-627-plan-to-implementation.json`
- `python3 scripts/overlord/test_check_governance_hook_execution_scope.py`
- `bash -n hooks/governance-check.sh`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-30-issue-627-local-root-hook-fallback-proof-implementation.json --require-lane-claim`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-627-local-root-hook-fallback-proof --require-if-issue-branch`
- `python3 scripts/overlord/validate_handoff_package.py --root . raw/handoffs/2026-04-30-issue-627-plan-to-implementation.json`
- `bash hooks/governance-check.sh`
- `bash hooks/governance-check.sh` with temporary removal of `cross_family_path_ref` from the issue-627 implementation scope, followed by immediate restoration
- `python3 scripts/overlord/validate_closeout.py raw/closeouts/2026-04-30-issue-627-local-root-hook-fallback-proof.md --root .`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`
- `git diff --check`

## Adjust

If the lane drifts into fallback-log schema, validator workflow parity, or
review-artifact routing, stop and route that work back to a later `#612` child.

If the lane starts editing planning-authority or session-start surfaces beyond
what the local root hooks strictly need, stop and keep that work under `#607`
or the broader `#615` graph.

## Review

Required before lane completion:

- sanctioned alternate-family review through the governed Claude path
- deterministic validator pass on the bounded implementation artifacts

Issue `#627` closes only the local root-hook consumer slice under `#615`. It
does not claim broader `#615` or `#612` closure.
