# Issue #625 PDCAR: Execution-Scope Cross-Family Fallback Field Enforcement

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/625
Parent: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/612
Branch: `issue-625-execution-scope-fallback-enforcement-20260430`

## Plan

Produce the canonical planning-only packet for governance issue `#625`, the
first narrow implementation child under `#612`.

This child exists because `#612` is too wide to implement safely as one lane.
`#625` therefore owns only execution-scope enforcement for degraded
same-family fallback evidence. It must not absorb fallback-log schema/workflow
parity, broader handoff/queue enforcement, planning-authority workflow work,
or downstream verifier work.

Mandatory intake for this lane includes:

- `docs/PROGRESS.md`
- issue `#612` and its later routing comments
- parent policy issue `#610`
- parent governance umbrella `#615`
- the current execution-scope enforcement surfaces:
  - `docs/schemas/execution-scope.schema.json`
  - `scripts/overlord/assert_execution_scope.py`
  - `scripts/overlord/test_assert_execution_scope.py`

## Do

Planning-only scope for issue `#625`:

- record the canonical structured plan, planning execution scope, handoff,
  review packet, cross-review, and validation artifacts
- define the bounded governance-owned implementation surface for:
  - `docs/schemas/execution-scope.schema.json`
  - `scripts/overlord/assert_execution_scope.py`
  - `scripts/overlord/test_assert_execution_scope.py`
- define the fixed degraded-fallback execution-scope fields that later
  implementation must enforce:
  - `cross_family_path_unavailable`
  - `cross_family_path_ref`
  - `fallback_log_ref`
- define the exact positive and negative execution-scope proof cases later
  implementation must return
- keep fallback-log schema/workflow parity out of scope:
  - `scripts/model-fallback-log.sh`
  - `.github/scripts/check_fallback_log_schema.py`
  - `.github/workflows/check-fallback-log-schema.yml`
  - `raw/model-fallbacks/*`
- keep broader validator/workflow or packet-routing work out of scope:
  - `scripts/overlord/validate_handoff_package.py`
  - `scripts/overlord/check_worker_handoff_route.py`
  - `scripts/orchestrator/packet_queue.py`
  - `docs/schemas/som-packet.schema.yml`
- keep issue `#607` planning-authority enforcement and issue `#614`
  downstream verifier work out of scope

## Check

The packet is acceptable only if it:

- stays planning-only and does not patch schemas, validators, tests, or
  workflows in this lane
- keeps ownership bounded to the execution-scope surface only
- explicitly records why this child exists:
  `#612` is too wide, so `#625` takes the first narrow implementation slice
- names the exact required positive proof case:
  same-family degraded fallback passes only when all three fixed fields are
  present and valid
- names the exact negative proof cases:
  fail closed when any fixed field is missing, blank, generic, non-local, or
  references a non-existent artifact
- requires regression proof that ordinary cross-family or non-degraded paths
  still pass unchanged
- requires regression proof that existing same-family exception checks still
  apply alongside the new degraded-fallback fields
- does not collapse into fallback-log schema/workflow parity or broader review
  artifact enforcement

Planning validation commands:

- `python3 -m json.tool docs/plans/issue-625-execution-scope-fallback-enforcement-structured-agent-cycle-plan.json`
- `python3 -m json.tool raw/execution-scopes/2026-04-30-issue-625-execution-scope-fallback-enforcement-planning.json`
- `python3 -m json.tool raw/handoffs/2026-04-30-issue-625-execution-scope-fallback-enforcement.json`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-625-execution-scope-fallback-enforcement-20260430 --require-if-issue-branch`
- `python3 scripts/overlord/validate_handoff_package.py --root . raw/handoffs/2026-04-30-issue-625-execution-scope-fallback-enforcement.json`
- `bash scripts/cross-review/require-dual-signature.sh raw/cross-review/2026-04-30-issue-625-execution-scope-fallback-enforcement-plan.md`
- `git diff --check`

## Adjust

If the lane drifts into `scripts/model-fallback-log.sh`,
`.github/scripts/check_fallback_log_schema.py`, or CI workflow edits, stop and
route that work back to a later `#612` child.

If the lane starts editing `validate_handoff_package.py`,
`check_worker_handoff_route.py`, `packet_queue.py`, or packet schemas, stop and
keep `#625` bounded to execution-scope enforcement only.

If the governed alternate-family review path is unavailable in this clean
worktree, record that as a real blocker rather than using same-family
substitutes.

## Review

Required before completion:

- governed alternate-family specialist review through the sanctioned review
  wrapper path
- local orchestration check that the packet remains planning-only and issue
  bounded
- deterministic validator pass on the packet artifacts

Issue `#625` does not authorize implementation by itself. It establishes only
the planning packet and implementation-readiness gate for the execution-scope
child of `#612`.

Required closure proof for the later implementation lane:

- positive proof that non-planning execution scope passes only when:
  - `cross_family_path_unavailable`
  - `cross_family_path_ref`
  - `fallback_log_ref`
  are all present and valid
- negative proof for each failure class:
  - missing field
  - blank field
  - generic placeholder content
  - non-local or unsafe path
  - path to non-existent artifact
- regression proof that ordinary cross-family or non-degraded execution-scope
  paths still pass
- regression proof that existing same-family exception checks still apply
- a validation artifact with one passing fixture and the expected fail output
  for each negative fixture
