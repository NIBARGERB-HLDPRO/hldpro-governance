from __future__ import annotations

import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validate_sql_schema_probe_contract import validate_contract


ROOT = Path(__file__).resolve().parents[2]
VALID_EXAMPLE = ROOT / "docs" / "examples" / "sql-schema-drift" / "healthcareplatform-maintenance-reset.json"
VALIDATOR = ROOT / "scripts" / "overlord" / "validate_sql_schema_probe_contract.py"


def valid_contract() -> dict:
    return {
        "schema_version": "v1",
        "contract_id": "healthcareplatform-maintenance-reset",
        "repo": "HealthcarePlatform",
        "placement": "repo-local-local-ci-profile",
        "sql_surface": True,
        "metadata_probe": {
            "id": "organizations-column-probe",
            "dialect": "postgres",
            "metadata_source": "information_schema.columns",
            "metadata_query": (
                "select column_name from information_schema.columns "
                "where table_schema = 'public' and table_name = 'organizations'"
            ),
            "required_columns": [
                {"schema": "public", "table": "organizations", "column": "organization_id"}
            ],
        },
        "destructive_operations": [
            {
                "path": "scripts/maintenance/reset-organizations.sql",
                "operation": "wipe",
                "preflight_probe_id": "organizations-column-probe",
                "preflight_required_before_mutation": True,
            }
        ],
        "schema_fixture": {
            "relations": [
                {
                    "schema": "public",
                    "table": "organizations",
                    "columns": ["organization_id", "name", "created_at"],
                }
            ]
        },
        "negative_controls": [
            {
                "name": "stale-org-id-column",
                "stale_reference": {"schema": "public", "table": "organizations", "column": "org_id"},
                "expected_failure": "missing column before destructive mutation",
            }
        ],
        "local_ci_profile_hook": {
            "profile": "healthcareplatform",
            "check_id": "sql-schema-drift-probe",
            "paths": ["scripts/maintenance/**", "supabase/migrations/**"],
            "command": [
                "python3",
                "scripts/ops/sql_schema_probe.py",
                "--contract",
                "docs/sql-schema-probes/maintenance-reset.json",
            ],
        },
        "residual_risk": (
            "Repos without SQL/destructive maintenance surfaces declare sql_surface=false "
            "and record the deferral in their repo-local profile or issue."
        ),
    }


class TestValidateSqlSchemaProbeContract(unittest.TestCase):
    def test_valid_contract_passes(self) -> None:
        self.assertEqual(validate_contract(valid_contract()), [])

    def test_negative_control_stale_column_present_in_fixture_fails(self) -> None:
        payload = valid_contract()
        payload["schema_fixture"]["relations"][0]["columns"].append("org_id")

        failures = validate_contract(payload)

        self.assertIn("`negative_controls[1].stale_reference` must be absent from schema_fixture", failures)

    def test_required_column_missing_from_fixture_fails(self) -> None:
        payload = valid_contract()
        payload["schema_fixture"]["relations"][0]["columns"] = ["org_id", "name"]

        failures = validate_contract(payload)

        self.assertIn(
            "`metadata_probe.required_columns` must exist in schema_fixture: public.organizations.organization_id",
            failures,
        )

    def test_metadata_query_must_use_metadata_source(self) -> None:
        payload = valid_contract()
        payload["metadata_probe"]["metadata_query"] = "select organization_id from organizations"

        failures = validate_contract(payload)

        self.assertIn("`metadata_probe.metadata_query` must query the declared schema metadata source", failures)

    def test_destructive_operation_requires_preflight_before_mutation(self) -> None:
        payload = valid_contract()
        payload["destructive_operations"][0]["preflight_required_before_mutation"] = False

        failures = validate_contract(payload)

        self.assertIn("`destructive_operations[1].preflight_required_before_mutation` must be true", failures)

    def test_sql_surface_false_deferral_passes_with_residual_risk(self) -> None:
        payload = {
            "schema_version": "v1",
            "contract_id": "static-site-deferral",
            "repo": "seek-and-ponder",
            "placement": "documented-deferral",
            "sql_surface": False,
            "residual_risk": "No SQL migrations, wipes, or destructive maintenance scripts are present.",
        }

        self.assertEqual(validate_contract(payload), [])

    def test_default_cli_discovers_governance_example(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--root", str(ROOT)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS validated", result.stdout)

    def test_cli_reports_invalid_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            contract_path = Path(tmp) / "invalid.json"
            payload = copy.deepcopy(valid_contract())
            payload["metadata_probe"]["required_columns"][0]["column"] = "missing_column"
            contract_path.write_text(__import__("json").dumps(payload), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(contract_path), "--root", str(ROOT)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_column", result.stderr)


if __name__ == "__main__":
    unittest.main()
