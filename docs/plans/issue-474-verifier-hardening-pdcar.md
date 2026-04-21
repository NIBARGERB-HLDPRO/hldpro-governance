# Issue 474 PDCAR: SSOT Consumer Verifier Hardening

## Plan

Compare the duplicate `issue-454-ssot-verifier` branch with the merged issue #454 implementation on `origin/main`. Keep the merged v0.2 verifier as the base because it includes the broader package-v2 profile contract, managed-file checksum, `local_overrides`, and consumer-record compatibility work. Port only the duplicate branch hardening deltas that increase verifier coverage without regressing the merged contract.

## Do

- Harden reusable workflow reference checks so tags, short SHAs, and valid-but-mismatched SHAs fail.
- Tighten override metadata validation so required fields must be non-empty strings.
- Add forbidden override classes for HIPAA/PHI/PII/lane weakening, plan-mode disabling, LAM PII routing, package-core forks, CI-required gate disabling, and dry-run-as-live evidence.
- Preserve the merged verifier output contract, including `observed_overrides`.
- Add focused regression tests for the ported edge cases.

## Check

- Focused verifier unit tests.
- Package deployer plus verifier unit suite.
- Python compile check.
- Structured plan, handoff package, and execution-scope validation.
- Local CI Gate for `hldpro-governance`.

## Adjust

If the duplicate branch contains behavior that conflicts with the merged v0.2 contract, defer to `origin/main` and record the skipped behavior rather than reintroducing the narrower duplicate shape.
