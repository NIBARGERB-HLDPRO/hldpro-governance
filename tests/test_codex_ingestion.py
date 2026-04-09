from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "overlord"))

from codex_ingestion import Finding, validate_location  # noqa: E402


class ValidateLocationTests(unittest.TestCase):
    def test_rejects_hallucinated_anchor_on_valid_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            target = repo / "scripts" / "sample.py"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("def something_else():\n    return 1\n")

            finding = Finding(
                finding_id="F003",
                severity="MEDIUM",
                category="testing",
                file="scripts/sample.py",
                line=1,
                title="`validate_location` does not validate cited code path",
                detail="Qualification should reject drifted code references.",
                suggestion="Check the cited identifier before qualifying.",
            )

            issue = validate_location(finding, repo)
            self.assertIsNotNone(issue)
            self.assertIn("cited code does not match claim anchors", issue)

    def test_accepts_matching_anchor_on_valid_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            target = repo / "scripts" / "sample.py"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("def validate_location():\n    return None\n")

            finding = Finding(
                finding_id="F003",
                severity="MEDIUM",
                category="testing",
                file="scripts/sample.py",
                line=1,
                title="`validate_location` does not validate cited code path",
                detail="Qualification should reject drifted code references.",
                suggestion="Check the cited identifier before qualifying.",
            )

            self.assertIsNone(validate_location(finding, repo))


if __name__ == "__main__":
    unittest.main()
