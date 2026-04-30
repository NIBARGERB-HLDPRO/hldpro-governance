Issue: `#627` Implement local governance-hook degraded-fallback proof consumption
Parent issue: `#615`
Dependency boundary: merged `#625` execution-scope degraded-fallback proof contract
Execution mode: `implementation_ready`
Branch: `issue-627-local-root-hook-fallback-proof`

Review the bounded implementation slice for issue `#627`.

This packet is intentionally self-contained for the governed no-tools Claude
review path. Use the material below as the full review scope.

## Required review questions

1. Does the implementation stay bounded to `hooks/governance-check.sh`,
   `scripts/overlord/check_governance_hook_execution_scope.py`, focused tests,
   required governance doc co-staging, `OVERLORD_BACKLOG.md`, and issue-local
   artifacts only?
2. Does the implementation consume the merged `#625` degraded-fallback proof
   contract by replaying the active implementation-capable execution scope,
   without redefining those semantics in shell?
3. Does the implementation fail closed on the local governance-hook path when
   same-family degraded fallback proof is missing, blank, unsafe, placeholder,
   or references a nonexistent file?
4. Does at least one compliant local governance-check path and one ordinary
   non-degraded path still pass?
5. Does the slice preserve `#625`, `#612`, `#607`, and `#614` as explicit
   external boundaries and avoid widening `backlog-check.sh` beyond
   backlog/parity behavior?

## Implementation summary

- This is the next narrow child under `#615` after merged `#625`.
- It owns only the local root-hook consumer path for the merged degraded-
  fallback proof contract.
- Its bounded implementation surface is limited to:
  - `hooks/governance-check.sh`
  - `scripts/overlord/check_governance_hook_execution_scope.py`
  - `scripts/overlord/test_check_governance_hook_execution_scope.py`
- Required governance doc co-staging for this slice:
  - `OVERLORD_BACKLOG.md`
  - `docs/PROGRESS.md`
  - `docs/FEATURE_REGISTRY.md`
  - `docs/FAIL_FAST_LOG.md`
- It must not absorb:
  - `hooks/backlog-check.sh` behavior beyond backlog/parity
  - `scripts/overlord/assert_execution_scope.py`
  - `scripts/overlord/test_assert_execution_scope.py`
  - `docs/schemas/execution-scope.schema.json`
  - fallback-log schema/workflow parity under `#612`
  - planning-authority work under `#607`
  - downstream verifier/drift-gate work under `#614`

## Implemented contract

Local governance hook replay now:

- discovers the active claimed execution scope for the current issue branch
- reuses `assert_execution_scope.py` as the canonical degraded-fallback policy
  owner rather than reimplementing it in shell
- treats planning-only scopes as pass/no-op for implementation replay
- fails closed on malformed or unreadable implementation scopes
- fails closed on same-family degraded fallback when any required proof field is:
  - missing
  - blank
  - placeholder-like
  - unsafe/non-local
  - nonexistent

## Proof matrix already gathered

Positive proof:
- focused helper unit proof for valid same-family degraded fallback
- focused helper unit proof for ordinary cross-family implementation path
- live `bash hooks/governance-check.sh` pass transcript on the active issue-627
  branch after branch parity and backlog mirror co-staging

Negative proof:
- focused helper unit failure for missing degraded-fallback field
- focused helper unit failure for unsafe fallback ref
- live `bash hooks/governance-check.sh` fail-closed transcript when
  `cross_family_path_ref` was temporarily removed from the issue-627
  implementation scope, then restored immediately

Regression / boundary proof:
- focused helper unit proof for planning-only no-op replay
- `hooks/backlog-check.sh` remains unchanged in this slice

## Current validation state

Focused implementation proof already run:

- `python3 scripts/overlord/test_check_governance_hook_execution_scope.py`: `PASS`
- `bash -n hooks/governance-check.sh`: `PASS`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-30-issue-627-local-root-hook-fallback-proof-implementation.json --require-lane-claim`: `PASS`
- `bash hooks/governance-check.sh`: `PASS` after backlog/branch-parity co-staging

Remaining finalization work after review:

- rewrite the issue-local validation artifact around the implementation slice
- create the Stage 6 closeout
- rerun structured plan / handoff / closeout / local-ci gates
- keep the issue bounded; do not claim broader `#615` or `#612` closure

## Files under review

- `OVERLORD_BACKLOG.md`
- `docs/FAIL_FAST_LOG.md`
- `docs/FEATURE_REGISTRY.md`
- `docs/PROGRESS.md`
- `docs/plans/issue-627-local-root-hook-fallback-proof-pdcar.md`
- `docs/plans/issue-627-local-root-hook-fallback-proof-structured-agent-cycle-plan.json`
- `raw/execution-scopes/2026-04-30-issue-627-local-root-hook-fallback-proof-implementation.json`
- `raw/handoffs/2026-04-30-issue-627-plan-to-implementation.json`
- `raw/validation/2026-04-30-issue-627-local-root-hook-fallback-proof.md`
- `hooks/governance-check.sh`
- `scripts/overlord/check_governance_hook_execution_scope.py`
- `scripts/overlord/test_check_governance_hook_execution_scope.py`
