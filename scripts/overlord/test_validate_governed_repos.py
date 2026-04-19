#!/usr/bin/env python3
"""Tests for governed repository registry validation."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.overlord.validate_governed_repos import validate_registry_shape


VALID_REGISTRY = {
    "version": 1,
    "organization": "NIBARGERB-HLDPRO",
    "repos_root_env": "HLDPRO_REPOS_ROOT",
    "default_repos_root": "~/Developer/HLDPRO",
    "repositories": [
        {
            "repo_slug": "sample-repo",
            "display_name": "sample-repo",
            "repo_dir_name": "sample-repo",
            "github_repo": "NIBARGERB-HLDPRO/sample-repo",
            "local_path": "sample-repo",
            "ci_checkout_path": "repos/sample-repo",
            "graph_output_path": "graphify-out/sample-repo",
            "wiki_path": "wiki/sample-repo",
            "project_path": "projects/sample-repo",
            "governance_tier": "standard",
            "security_tier": "baseline",
            "lifecycle_status": "active",
            "governance_status": "governed",
            "classification": {
                "owner": "governance",
                "rationale": "Fixture repository with explicit governance classification.",
                "review_date": "2026-04-18",
                "issue_refs": [
                    "#310"
                ],
            },
            "description": "Fixture repository",
            "enabled_subsystems": {
                "graphify": True,
                "sweep": True,
                "metrics": True,
                "memory_integrity": True,
                "codex_ingestion": True,
                "compendium": True,
                "raw_feed_sync": True,
                "code_governance": True,
            },
        }
    ],
}


class GovernedReposValidationTests(unittest.TestCase):
    def write_registry(self, payload: dict) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        path = Path(tmpdir.name) / "governed_repos.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    def assert_invalid(self, payload: dict) -> None:
        with self.assertRaises(SystemExit):
            validate_registry_shape(self.write_registry(payload))

    def test_valid_registry_classification_passes(self) -> None:
        validate_registry_shape(self.write_registry(copy.deepcopy(VALID_REGISTRY)))

    def test_missing_classification_fails(self) -> None:
        payload = copy.deepcopy(VALID_REGISTRY)
        del payload["repositories"][0]["classification"]
        self.assert_invalid(payload)

    def test_extra_repository_field_fails(self) -> None:
        payload = copy.deepcopy(VALID_REGISTRY)
        payload["repositories"][0]["extra"] = "not allowed"
        self.assert_invalid(payload)

    def test_extra_classification_field_fails(self) -> None:
        payload = copy.deepcopy(VALID_REGISTRY)
        payload["repositories"][0]["classification"]["extra"] = "not allowed"
        self.assert_invalid(payload)

    def test_missing_root_field_fails(self) -> None:
        payload = copy.deepcopy(VALID_REGISTRY)
        del payload["repos_root_env"]
        self.assert_invalid(payload)

    def test_invalid_lifecycle_status_fails(self) -> None:
        payload = copy.deepcopy(VALID_REGISTRY)
        payload["repositories"][0]["lifecycle_status"] = "paused"
        self.assert_invalid(payload)

    def test_invalid_governance_status_fails(self) -> None:
        payload = copy.deepcopy(VALID_REGISTRY)
        payload["repositories"][0]["governance_status"] = "maybe"
        self.assert_invalid(payload)

    def test_empty_issue_refs_fails(self) -> None:
        payload = copy.deepcopy(VALID_REGISTRY)
        payload["repositories"][0]["classification"]["issue_refs"] = []
        self.assert_invalid(payload)

    def test_bad_review_date_fails(self) -> None:
        payload = copy.deepcopy(VALID_REGISTRY)
        payload["repositories"][0]["classification"]["review_date"] = "04/18/2026"
        self.assert_invalid(payload)

    def test_non_boolean_subsystem_value_fails(self) -> None:
        payload = copy.deepcopy(VALID_REGISTRY)
        payload["repositories"][0]["enabled_subsystems"]["code_governance"] = "false"
        self.assert_invalid(payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
