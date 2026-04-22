# SQL Schema Drift Probe Contract

Issue #534 chooses repo-local Local CI profile hooks as the enforcement point for SQL/schema drift probes. The contract is reusable, but each governed repo owns its own query, fixture, and destructive-script hook because SQL surfaces vary by database, migration layout, and runtime access.

## Decision

- Governance documents and validates the contract shape.
- Consumer repos with destructive SQL maintenance scripts wire the probe into their repo-local Local CI profile before mutation-capable checks run.
- Governance does not add a global SQL abstraction or global migration runner.
- Repos without SQL/destructive maintenance surfaces record `sql_surface: false` plus residual risk instead of carrying inert checks.

## Contract

Contract files use `schema_version: v1` and must be JSON objects. For `sql_surface: true`, the contract must include:

- `placement: repo-local-local-ci-profile`
- `metadata_probe` with a declared metadata source and query against schema metadata, such as `information_schema.columns`, `pg_catalog`, or SQLite `pragma_table_info`
- `metadata_probe.required_columns` listing the columns required before mutation
- `schema_fixture.relations` representing the expected live schema shape
- `negative_controls` where each stale reference exists on the fixture table but the stale column is absent
- `destructive_operations` with `preflight_required_before_mutation: true`
- `local_ci_profile_hook` naming the consumer profile check, watched paths, and command
- `residual_risk` describing what remains outside the probe

For `sql_surface: false`, the contract must carry a non-empty `residual_risk` and no inert destructive-operation hook is required.

## Example

The concrete example is `docs/examples/sql-schema-drift/healthcareplatform-maintenance-reset.json`. It captures the failure class where destructive maintenance expected `organizations.organization_id` and the stale reference `organizations.org_id` must fail as a negative control before any wipe/reset mutation runs.

## Validation

Run:

```bash
python3 scripts/overlord/validate_sql_schema_probe_contract.py --root .
python3 scripts/overlord/test_validate_sql_schema_probe_contract.py
```

The hldpro-governance Local CI profile runs `sql-schema-drift-probe-contract` when this runbook, example contracts, validator, tests, or SQL schema probe schema docs change. Product repos should add an equivalent repo-local check that scopes to their migrations, maintenance SQL, and probe command.
