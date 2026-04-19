#!/usr/bin/env python3
from __future__ import annotations

import unittest
from unittest import mock

import check_overlord_backlog_github_alignment as alignment


PLANNED_LINES = [
    "| Item | Issue | Priority | Est. Hours | Notes |",
    "|------|-------|----------|-----------|-------|",
    "| Open planned item | [#104](https://github.com/x/y/issues/104) | MEDIUM | 1 | still open |",
]


class TestOverlordBacklogGithubAlignment(unittest.TestCase):
    def test_in_progress_closed_issue_fails(self) -> None:
        lines = [
            "| Item | Issue | Priority | Est. Hours | Notes |",
            "|------|-------|----------|-----------|-------|",
            "| Closed in-progress item | [#200](https://github.com/x/y/issues/200) | HIGH | 1 | stale |",
        ]

        def fake_issue_state(issue_number: int) -> tuple[bool, str]:
            self.assertEqual(issue_number, 200)
            return False, "issue is 'closed', expected 'open': 'closed row'"

        with mock.patch.object(alignment, "check_github_issue_open", side_effect=fake_issue_state):
            violations = alignment.validate_section(lines, "In Progress")

        self.assertEqual(len(violations), 1)
        self.assertIn("In Progress row references non-open issue #200", violations[0])
        self.assertIn("Closed in-progress item", violations[0])

    def test_planned_open_issue_passes(self) -> None:
        with mock.patch.object(alignment, "check_github_issue_open", return_value=(True, "open row")):
            violations = alignment.validate_section(PLANNED_LINES, "Planned")

        self.assertEqual(violations, [])

    def test_missing_issue_column_reference_fails(self) -> None:
        lines = [
            "| Item | Issue | Priority | Est. Hours | Notes |",
            "|------|-------|----------|-----------|-------|",
            "| Missing issue item |  | HIGH | 1 | stale |",
        ]

        violations = alignment.validate_section(lines, "In Progress")

        self.assertEqual(len(violations), 1)
        self.assertIn("without GitHub issue reference in Issue column", violations[0])


if __name__ == "__main__":
    unittest.main()
