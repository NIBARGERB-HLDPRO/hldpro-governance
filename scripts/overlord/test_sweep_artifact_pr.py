from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.overlord.sweep_artifact_pr import (
    ARTIFACT_ISSUE_NUMBER,
    ARTIFACT_SCOPE_PATH,
    artifact_branch,
    artifact_scope,
    write_scope,
)


class SweepArtifactPrTest(unittest.TestCase):
    def test_branch_uses_permanent_issue_anchor(self) -> None:
        self.assertEqual(
            artifact_branch("2026-04-21", "12345"),
            "automation/issue-503-overlord-sweep-2026-04-21-12345",
        )

    def test_scope_uses_branch_issue_and_generated_write_paths(self) -> None:
        branch = artifact_branch("2026-04-21", "12345")
        scope = artifact_scope(
            branch,
            "12345",
            "https://github.com",
            "NIBARGERB-HLDPRO/hldpro-governance",
        )

        self.assertEqual(scope["expected_branch"], branch)
        self.assertEqual(scope["lane_claim"]["issue_number"], ARTIFACT_ISSUE_NUMBER)  # type: ignore[index]
        self.assertIn("graphify-out/", scope["allowed_write_paths"])
        self.assertIn("metrics/self-learning/", scope["allowed_write_paths"])
        self.assertIn(ARTIFACT_SCOPE_PATH, scope["allowed_write_paths"])
        self.assertIn(
            "https://github.com/NIBARGERB-HLDPRO/hldpro-governance/actions/runs/12345",
            scope["handoff_evidence"]["evidence_paths"],  # type: ignore[index]
        )

    def test_write_scope_creates_json_file(self) -> None:
        branch = artifact_branch("2026-04-21", "12345")
        scope = artifact_scope(branch, "12345", "https://github.com", "owner/repo")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ARTIFACT_SCOPE_PATH
            write_scope(path, scope)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), scope)


if __name__ == "__main__":
    unittest.main()
