from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "overlord"))

import check_progress_github_issue_staleness as staleness  # noqa: E402


class ProgressGithubIssueStalenessTests(unittest.TestCase):
    def test_collects_active_sections_and_ignores_done(self) -> None:
        content = """# Product Progress Tracker

### GitHub Issue Cross-Reference (backlog label)

| Issue | Plan | Priority |
|-------|------|----------|
| #100 | Active Item | HIGH |

## Known Bugs

| Bug | Status | Notes |
|-----|--------|-------|
| Example | IN_PROGRESS | Issue #101 |

## Done

| Item | Date | Notes |
|------|------|-------|
| Finished | 2026-04-09 | Issue #102 |
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "PROGRESS.md"
            path.write_text(content, encoding="utf-8")
            refs = staleness.collect_active_issue_refs(path)

        self.assertEqual(sorted(refs), [100, 101])
        self.assertNotIn(102, refs)

    def test_build_summary_reports_missing_open_and_stale_closed(self) -> None:
        content = """# Product Progress Tracker

### GitHub Issue Cross-Reference (backlog label)

| Issue | Plan | Priority |
|-------|------|----------|
| #200 | Closed But Still Listed | HIGH |
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "PROGRESS.md"
            path.write_text(content, encoding="utf-8")
            with patch.object(
                staleness,
                "backlog_issues",
                return_value=(
                    {201: {"number": 201, "state": "OPEN"}},
                    {200: {"number": 200, "state": "CLOSED"}},
                ),
            ):
                summary = staleness.build_summary("NIBARGERB-HLDPRO/example", path)

        self.assertEqual(summary["missing_open_issue_numbers"], [201])
        self.assertEqual(summary["stale_closed_issue_numbers"], [200])
        stale_refs = summary["stale_closed_references"]["200"]
        self.assertEqual(stale_refs[0]["section"], "### GitHub Issue Cross-Reference (backlog label)")


if __name__ == "__main__":
    unittest.main()
