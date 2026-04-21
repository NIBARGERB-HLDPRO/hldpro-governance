# Issue #537 PDCAR: Consumer Verifier And Worker Acceptance Gates

## Plan

Move consumer verifier evidence earlier in the handoff acceptance path so Worker output that touches consumer-managed governance surfaces cannot be accepted without deterministic verifier commands and evidence refs.

## Do

- Make `--governance-root` authoritative for consumer verifier manifest and desired-state resolution.
- Add direct regression coverage for malformed `local_overrides`.
- Preserve stale/mismatched reusable workflow SHA as a hard verifier failure.
- Extend handoff package validation so accepted handoffs touching consumer-managed paths require `verify_governance_consumer.py` commands and evidence refs.
- Tighten execution-scope handoff evidence refs so unsafe paths cannot authorize Worker acceptance.
- Prove Worker route blocks unsafe handoff evidence through existing route validation.

## Check

- `python3 scripts/overlord/test_verify_governance_consumer.py`
- `python3 scripts/overlord/test_validate_handoff_package.py`
- `python3 scripts/overlord/test_assert_execution_scope.py`
- `python3 scripts/overlord/test_check_worker_handoff_route.py`
- Governance handoff, plan, scope, closeout, provisioning, and local-ci validators.

## Adjust

If product repos need concrete consumer verifier rollout changes, create downstream issue-backed PRs. This slice updates the governance SSOT and acceptance gates only.

## Review

Close only after negative fixtures prove typoed governance roots, malformed `local_overrides`, stale workflow SHAs, missing consumer verifier commands, and unsafe Worker evidence refs fail before acceptance.
