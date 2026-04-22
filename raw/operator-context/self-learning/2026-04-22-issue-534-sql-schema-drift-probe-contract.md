# Self-Learning: Issue #534 SQL Schema Drift Probe Contract

Date: 2026-04-22
Issue: #534
Pattern: `sql-schema-drift-stale-column`

## Lesson

Destructive SQL maintenance should not discover schema drift after mutation-capable statements begin. A repo-local preflight must query schema metadata and fail on stale column assumptions before wipe/reset/migration work proceeds.

## Correction

Use `docs/runbooks/sql-schema-drift-probes.md` and validate contract files with `scripts/overlord/validate_sql_schema_probe_contract.py`. Preserve a negative control where the stale column is absent from the expected fixture.

## Lookup Anchors

- `organizations.organization_id`
- `organizations.org_id`
- SQL schema drift
- destructive SQL preflight
- Local CI profile hook

## Evidence

- `docs/examples/sql-schema-drift/healthcareplatform-maintenance-reset.json`
- `scripts/overlord/test_validate_sql_schema_probe_contract.py`
- `docs/runbooks/session-error-patterns.md`
