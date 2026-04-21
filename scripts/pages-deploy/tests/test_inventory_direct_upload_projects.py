from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "inventory_direct_upload_projects.py"
SPEC = importlib.util.spec_from_file_location("inventory_direct_upload_projects", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
inventory_direct_upload_projects = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = inventory_direct_upload_projects
SPEC.loader.exec_module(inventory_direct_upload_projects)


def test_inventory_classifies_direct_upload_projects():
    payload = inventory_direct_upload_projects.inventory(
        [
            {
                "name": "seek-and-ponder",
                "domains": ["seek-and-ponder.pages.dev", "app.seekandponder.com"],
                "source": None,
                "latest_deployment": {
                    "id": "deploy-1",
                    "created_on": "2026-04-21T22:39:00Z",
                    "deployment_trigger": {
                        "type": "ad_hoc",
                        "metadata": {"branch": "main", "commit_hash": "a" * 40, "commit_dirty": True},
                    },
                },
            },
            {
                "name": "hldpro-dashboard",
                "domains": ["hldpro-dashboard.pages.dev", "dashboard.hldpro.com"],
                "source": None,
            },
        ],
        ["seek-and-ponder", "hldpro-dashboard"],
    )

    rows = {row["cf_project_name"]: row for row in payload["projects"]}
    assert rows["seek-and-ponder"]["disposition"] == "covered"
    assert rows["seek-and-ponder"]["governance_gate_exists"] is True
    assert rows["hldpro-dashboard"]["disposition"] == "needs-consumer-adoption"
    assert rows["hldpro-dashboard"]["git_provider_status"] == "no_git_provider_direct_upload"
    assert rows["hldpro-dashboard"]["follow_up_issue"].endswith("/1478")


def test_inventory_marks_missing_expected_project_unknown():
    payload = inventory_direct_upload_projects.inventory([], ["hldpro-reseller"])

    row = payload["projects"][0]
    assert row["cf_project_name"] == "hldpro-reseller"
    assert row["disposition"] == "unknown-needs-follow-up"
    assert row["owning_repo"] == "NIBARGERB-HLDPRO/ai-integration-services"


def test_cli_offline_writes_json_and_markdown(tmp_path):
    offline = tmp_path / "projects.json"
    output_json = tmp_path / "inventory.json"
    output_md = tmp_path / "inventory.md"
    offline.write_text(
        json.dumps(
            [
                {
                    "name": "hldpro-pwa",
                    "domains": ["hldpro-pwa.pages.dev", "pwa.hldpro.com"],
                    "source": None,
                }
            ]
        ),
        encoding="utf-8",
    )

    result = inventory_direct_upload_projects.main(
        [
            "--offline-json",
            str(offline),
            "--project",
            "hldpro-pwa",
            "--output-json",
            str(output_json),
            "--output-markdown",
            str(output_md),
        ]
    )

    assert result == 0
    assert json.loads(output_json.read_text(encoding="utf-8"))["projects"][0]["cf_project_name"] == "hldpro-pwa"
    assert "hldpro-pwa.pages.dev" in output_md.read_text(encoding="utf-8")
