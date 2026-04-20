# PDCAR: Issue #393 Lane-Claim Gate

Date: 2026-04-20
Issue: [#393](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/393)
Branch: `issue-393-lane-claim-gate-20260420`

## Plan

Prevent cross-session lane invasion by making lane ownership part of the existing execution-scope contract. The control must fail closed for implementation work on an `issue-*` branch unless the resolved execution scope includes a `lane_claim` whose issue number matches both the current branch and the scope's expected branch.

The incident pattern is concrete: after #386 closed, #391 was treated as the next executable lane and a local worktree was created before #391 had a plan, scope, or ownership handoff. The new rule stops that class of drift at the execution-scope gate instead of adding a parallel lock system.

## Do

1. Extend `assert_execution_scope.py` with optional `lane_claim` parsing and a `--require-lane-claim` flag.
2. Add the same flag to `check_execution_environment.py` so session-start preflight can enforce the claim before implementation work.
3. Make the governance Local CI profile require lane claims for planner-boundary execution-scope checks.
4. Make Local CI resolve execution scopes by matching `lane_claim.issue_number`, not only filename globs.
5. Add focused regression tests for matching, missing, and mismatched lane claims.
6. Document the operating rule in `STANDARDS.md` and service/feature registries.

## Check

- Missing `lane_claim` fails when lane-claim enforcement is enabled.
- Current branch issue and `expected_branch` issue must both match `lane_claim.issue_number`.
- Local CI scope resolution refuses an issue scope whose filename matches but `lane_claim.issue_number` does not.
- Historical scopes remain loadable unless a caller opts into `--require-lane-claim`, avoiding retroactive breakage for old artifacts.
- The #393 execution scope itself contains a valid lane claim and passes the new gate.

## Adjust

The specialist review recommended against a separate `raw/lane-claims/` validator. I adjusted the implementation to embed the claim in `raw/execution-scopes/*.json`, keeping root, branch, allowed paths, forbidden roots, handoff, and lane ownership in one authoritative artifact.

## Review

This gate prevents accidental implementation in another issue lane; it does not replace human coordination. Follow-up issue creation remains allowed, but execution in that follow-up lane requires its own claimed scope or an explicit planning-bootstrap path.
