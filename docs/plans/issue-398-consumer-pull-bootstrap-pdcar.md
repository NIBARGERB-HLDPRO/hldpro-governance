# Issue #398 — Consumer-Pulled Governance Package Bootstrap PDCAR

## Plan

Move governed repos toward a pull-shaped governance package model without allowing downstream repos to silently rewrite central GitHub policy.

The first slice keeps mutation out of scope and adds a deterministic verifier:

- governance remains the package source of truth;
- consumer repos record an exact governance git SHA in `.hldpro/governance-tooling.json`;
- consumer-side checks verify local managed files and package metadata;
- org rulesets, repository rulesets, bypass actors, and repository settings remain centrally applied by issue-backed governance work.

## Do

- Add `docs/governance-consumer-pull-state.json` as the first machine-readable consumer-pull desired-state contract.
- Add `scripts/overlord/verify_governance_consumer.py` for non-mutating consumer verification.
- Add focused tests for valid pinned records, missing records, non-SHA refs, marker drift, profile mismatch, and missing managed files.
- Register the verifier in the governance package manifest and Local CI Gate profile.
- Update the org-governance tooling distribution runbook with the repo-pulled versus centrally-applied boundary.

## Check

Required validation:

- `python3 scripts/overlord/test_verify_governance_consumer.py`
- `python3 -m unittest scripts.overlord.test_deploy_governance_tooling scripts.overlord.test_verify_governance_consumer`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-20-issue-398-consumer-pull-bootstrap-implementation.json --changed-files-file <changed-files> --require-lane-claim`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci --repo-root . --profile hldpro-governance --changed-files-file <changed-files> --json`

## Adjust / Review

This slice intentionally stops before downstream rollout. The follow-up adoption loop should be issue-backed per consumer repo or repo class:

- add minimal repo-side workflow/shim invocation;
- run the consumer verifier against the pinned SHA;
- add an update-PR workflow for governance package ref bumps;
- report central GitHub settings/ruleset drift without mutating it from the consumer repo.

## Rollback

Revert this governance PR to remove the verifier and desired-state contract from the package.

Downstream repos are not modified by this slice. Existing downstream managed files remain controlled by the existing package deployer rollback:

```bash
python3 scripts/overlord/deploy_governance_tooling.py rollback --target-repo /path/to/consumer --profile <profile> --governance-ref <sha>
```
