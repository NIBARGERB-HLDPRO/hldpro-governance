#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import check_governance_issue_branch_parity as parity


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _backlog_text(in_progress_issue: int | None = None, planned_issue: int | None = None) -> str:
    planned_row = (
        f"| Planned item | [#{planned_issue}](https://example.invalid/issues/{planned_issue}) | HIGH | 1 | planned | |\n"
        if planned_issue is not None
        else ""
    )
    in_progress_row = (
        f"| In-progress item | [#{in_progress_issue}](https://example.invalid/issues/{in_progress_issue}) | HIGH | 1 | active |\n"
        if in_progress_issue is not None
        else ""
    )
    return (
        "# Overlord Backlog\n\n"
        "> GitHub Issues are the execution backlog/system of record for governance work. "
        "This file is the local roadmap/status mirror for cross-repo planning, active issue-backed work, "
        "and completed-history entries that still need governance-level visibility.\n\n"
        "## Planned\n\n"
        "| Item | Issue | Priority | Est. Hours | Notes |\n"
        "|------|-------|----------|-----------|-------|\n"
        f"{planned_row}\n"
        "## In Progress\n\n"
        "| Item | Issue | Priority | Est. Hours | Notes |\n"
        "|------|-------|----------|-----------|-------|\n"
        f"{in_progress_row}\n"
        "## Done\n"
    )


class GovernanceIssueBranchParityTests(unittest.TestCase):
    def test_non_issue_branch_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            backlog = Path(raw_tmp) / "OVERLORD_BACKLOG.md"
            _write(backlog, _backlog_text(in_progress_issue=621))
            result = parity.check_branch_parity("main", backlog)
        self.assertIn("not issue-backed", result)

    def test_issue_branch_passes_when_listed_in_progress(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            backlog = Path(raw_tmp) / "OVERLORD_BACKLOG.md"
            _write(backlog, _backlog_text(in_progress_issue=621))
            result = parity.check_branch_parity("issue-621-backlog-commit-parity-20260430", backlog)
        self.assertIn("active governance issue #621", result)
        self.assertIn("(In Progress)", result)

    def test_issue_branch_passes_when_listed_planned(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            backlog = Path(raw_tmp) / "OVERLORD_BACKLOG.md"
            _write(backlog, _backlog_text(planned_issue=621))
            result = parity.check_branch_parity("issue-621-backlog-commit-parity-20260430", backlog)
        self.assertIn("active governance issue #621", result)
        self.assertIn("(Planned)", result)

    def test_issue_branch_fails_when_missing_from_active_sections(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            backlog = Path(raw_tmp) / "OVERLORD_BACKLOG.md"
            _write(backlog, _backlog_text(in_progress_issue=591))
            with self.assertRaises(SystemExit) as exc:
                parity.check_branch_parity("issue-621-backlog-commit-parity-20260430", backlog)
        self.assertEqual(exc.exception.code, 1)

    def test_branch_with_multiple_issue_numbers_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            backlog = Path(raw_tmp) / "OVERLORD_BACKLOG.md"
            _write(backlog, _backlog_text(in_progress_issue=621))
            with self.assertRaises(SystemExit) as exc:
                parity.check_branch_parity("issue-621-foo-issue-622", backlog)
        self.assertEqual(exc.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
