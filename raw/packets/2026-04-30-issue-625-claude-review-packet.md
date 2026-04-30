Issue: `#625` Implement execution-scope cross-family fallback field enforcement
Parent issue: `#612`
Execution mode: `implementation_ready`
Branch: `issue-625-execution-scope-fallback-enforcement-20260430`

Review the bounded implementation for issue `#625`.

This packet is intentionally self-contained for the governed no-tools Claude
review path. Use the material below as the full review scope.

## Required review questions

1. Does the implementation stay bounded to `docs/schemas/execution-scope.schema.json`,
   `scripts/overlord/assert_execution_scope.py`,
   `scripts/overlord/test_assert_execution_scope.py`, required governance doc
   co-staging, and issue-local artifacts only?
2. Does the implementation clearly exclude fallback-log schema/workflow parity,
   broader packet-routing enforcement, `#607`, and `#614`?
3. Does the implementation enforce `cross_family_path_unavailable == true`
   plus existing repo-safe `cross_family_path_ref` and `fallback_log_ref`
   only for same-family degraded fallback, without forcing those fields on
   ordinary cross-family paths?
4. Does the implementation return the intended proof matrix:
   1 positive case, 5 negative classes, and 2 regression classes?
5. Does the implementation avoid overclaiming `#612` closure and stay limited
   to the execution-scope-only slice?

## Implementation summary

- This is the first narrow implementation child under `#612`.
- It now carries the bounded implementation slice.
- Its owned implementation surface is limited to:
  - `docs/schemas/execution-scope.schema.json`
  - `scripts/overlord/assert_execution_scope.py`
  - `scripts/overlord/test_assert_execution_scope.py`
- Required governance doc co-staging for this source change:
  - `docs/PROGRESS.md`
  - `docs/FEATURE_REGISTRY.md`
  - `docs/FAIL_FAST_LOG.md`
- It must not absorb:
  - `scripts/model-fallback-log.sh`
  - `.github/scripts/check_fallback_log_schema.py`
  - `.github/workflows/check-fallback-log-schema.yml`
  - `raw/model-fallbacks/*`
  - `scripts/overlord/validate_handoff_package.py`
  - `scripts/overlord/check_worker_handoff_route.py`
  - `scripts/orchestrator/packet_queue.py`
  - `docs/schemas/som-packet.schema.yml`
  - issue `#607`
  - issue `#614`

## Implemented contract

The implementation now exposes these three fields on `handoff_evidence`:

- `cross_family_path_unavailable`
- `cross_family_path_ref`
- `fallback_log_ref`

Implemented enforcement contract:

- Positive case:
  - degraded same-family fallback passes only when all three fields are present
    and valid
- Negative cases:
  - fail closed when any required field is missing
  - fail closed when any required field is blank
  - fail closed when any required field uses generic placeholder content
  - fail closed when any required field points to a non-local or unsafe path
  - fail closed when any required field points to a non-existent artifact
- Regression cases:
  - ordinary cross-family or non-degraded execution-scope paths still pass
    unchanged
  - existing same-family exception checks still apply alongside the new fields

## Code change summary

Schema changes:
- add optional `handoff_evidence` properties for:
  - `cross_family_path_unavailable` as boolean
  - `cross_family_path_ref` as nullable string
  - `fallback_log_ref` as nullable string
- these fields are not globally required in JSON Schema because existing repo
  execution scopes would otherwise break; runtime enforcement is conditional in
  Python instead

Runtime enforcement changes:
- extend `HandoffEvidence` with the three new fields
- normalize the two new refs as repo-safe evidence refs
- reject placeholder ref values such as `TODO`, `TBD`, `n/a`, `na`, and
  `placeholder`
- in same-family non-planning mode, require:
  - `cross_family_path_unavailable == true`
  - `cross_family_path_ref`
  - `fallback_log_ref`
- require both refs to resolve to existing repo files
- preserve existing active-exception and expiry checks

Test changes:
- same-family pass fixtures now include all three new fields
- new failures cover:
  - missing required degraded-fallback field
  - false `cross_family_path_unavailable`
  - blank or placeholder ref
  - unsafe or non-local ref
  - non-existent artifact ref
- regression confirms cross-family accepted handoff still passes without the new
  fields

## Current validation state

Focused implementation proof already run:

- `python3 scripts/overlord/test_assert_execution_scope.py`: `PASS`
- `python3 -m json.tool docs/schemas/execution-scope.schema.json`: `PASS`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-30-issue-625-execution-scope-fallback-enforcement-implementation.json --require-lane-claim`: `PASS`
- `python3 scripts/overlord/validate_handoff_package.py --root . raw/handoffs/2026-04-30-issue-625-plan-to-implementation.json`: `PASS`

The remaining finalization work after review is:
- update the issue-local validation artifact with the full implementation
  command set
- complete Stage 6 closeout content
- rerun local-ci-gate and final validators
- keep the issue bounded; do not claim `#612` closure

## Files under review

- `docs/FAIL_FAST_LOG.md`
- `docs/FEATURE_REGISTRY.md`
- `docs/PROGRESS.md`
- `docs/plans/issue-625-execution-scope-fallback-enforcement-pdcar.md`
- `docs/plans/issue-625-execution-scope-fallback-enforcement-structured-agent-cycle-plan.json`
- `docs/schemas/execution-scope.schema.json`
- `raw/execution-scopes/2026-04-30-issue-625-execution-scope-fallback-enforcement-implementation.json`
- `raw/handoffs/2026-04-30-issue-625-plan-to-implementation.json`
- `raw/closeouts/2026-04-30-issue-625-execution-scope-fallback-enforcement.md`
- `raw/validation/2026-04-30-issue-625-execution-scope-fallback-enforcement.md`
- `scripts/overlord/assert_execution_scope.py`
- `scripts/overlord/test_assert_execution_scope.py`
