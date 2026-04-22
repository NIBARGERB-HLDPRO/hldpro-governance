# Issue #534 PDCAR: SQL Schema Drift Probe Contract

## Plan

Define a minimal, repo-local SQL/schema drift probe contract for destructive maintenance surfaces. Keep governance as the contract and validator owner, while product repos own their live schema metadata query and Local CI hook.

## Do

- Add a governance runbook that chooses repo-local Local CI profile hooks over a global SQL abstraction.
- Add a concrete HealthcarePlatform-style example contract for the `organizations.organization_id` versus stale `org_id` failure class.
- Add a deterministic validator for metadata-query placement, destructive-operation preflight requirements, fixtures, stale-column negative controls, Local CI hook metadata, and `sql_surface: false` residual-risk deferrals.
- Add focused regression coverage for valid contracts, stale negative-control failures, missing required columns, non-metadata queries, missing preflight-before-mutation, and no-SQL deferrals.
- Wire the hldpro-governance Local CI profile to run the focused contract tests when contract surfaces change.
- Update self-learning docs, registries, and progress evidence.

## Check

- `python3 scripts/overlord/test_validate_sql_schema_probe_contract.py`
- `python3 scripts/overlord/validate_sql_schema_probe_contract.py --root .`
- `python3 -m unittest tools.local-ci-gate.tests.test_local_ci_gate`
- Governance handoff, structured-plan, execution-scope, closeout, provisioning, diff, and Local CI gates.

## Adjust

Downstream product repos should adopt the contract through issue-backed profile-hook PRs. This slice does not mutate product repos and does not make a broad SQL abstraction.

## Review

Close only after the concrete example, stale-column negative control, focused tests, Local CI profile hook, and residual-risk deferral path are validated.
