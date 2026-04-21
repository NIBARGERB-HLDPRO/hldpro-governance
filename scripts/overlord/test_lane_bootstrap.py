#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "overlord" / "lane_bootstrap.py"


def run_helper(*args: str) -> tuple[int, dict]:
    result = subprocess.run(
        ["python3", str(SCRIPT), "--repo-root", str(REPO_ROOT), "--json", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode, json.loads(result.stdout)


class TestLaneBootstrap(unittest.TestCase):
    def test_valid_healthcareplatform_lane_accepted(self) -> None:
        code, payload = run_helper(
            "--repo-slug",
            "HealthcarePlatform",
            "validate",
            "--branch-name",
            "sandbox/issue-1357-pr-pending-chart-audit",
            "--worktree-path",
            "/tmp/issue-1357-pr-pending-chart-audit",
            "--issue-number",
            "1357",
        )

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["policy"], "healthcareplatform")

    def test_invalid_healthcareplatform_branch_pattern_rejected(self) -> None:
        code, payload = run_helper(
            "--repo-slug",
            "HealthcarePlatform",
            "validate",
            "--branch-name",
            "issue-1357-chart-audit",
            "--worktree-path",
            "/tmp/issue-1357-pr-pending-chart-audit",
            "--issue-number",
            "1357",
        )

        self.assertNotEqual(code, 0)
        self.assertIn("invalid branch pattern", payload["reason"])

    def test_invalid_healthcareplatform_worktree_path_rejected(self) -> None:
        code, payload = run_helper(
            "--repo-slug",
            "HealthcarePlatform",
            "validate",
            "--branch-name",
            "sandbox/issue-1357-pr-pending-chart-audit",
            "--worktree-path",
            "/tmp/issue-1357-chart-audit",
            "--issue-number",
            "1357",
        )

        self.assertNotEqual(code, 0)
        self.assertIn("invalid worktree path pattern", payload["reason"])

    def test_branch_worktree_issue_mismatch_rejected(self) -> None:
        code, payload = run_helper(
            "--repo-slug",
            "HealthcarePlatform",
            "validate",
            "--branch-name",
            "sandbox/issue-1357-pr-pending-chart-audit",
            "--worktree-path",
            "/tmp/issue-1358-pr-pending-chart-audit",
            "--issue-number",
            "1357",
        )

        self.assertNotEqual(code, 0)
        self.assertIn("worktree issue mismatch", payload["reason"])

    def test_branch_worktree_scope_mismatch_rejected(self) -> None:
        code, payload = run_helper(
            "--repo-slug",
            "HealthcarePlatform",
            "validate",
            "--branch-name",
            "sandbox/issue-1357-pr-pending-chart-audit",
            "--worktree-path",
            "/tmp/issue-1357-pr-pending-different",
            "--issue-number",
            "1357",
        )

        self.assertNotEqual(code, 0)
        self.assertIn("scope mismatch", payload["reason"])

    def test_standard_repo_lane_policy_accepted(self) -> None:
        code, payload = run_helper(
            "--repo-slug",
            "hldpro-governance",
            "validate",
            "--branch-name",
            "issue-445-lane-bootstrap",
            "--worktree-path",
            "/tmp/issue-445-lane-bootstrap",
            "--issue-number",
            "445",
        )

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["policy"], "standard")

    def test_plan_generates_healthcareplatform_names(self) -> None:
        code, payload = run_helper(
            "--repo-slug",
            "HealthcarePlatform",
            "plan",
            "--issue-number",
            "1357",
            "--scope-slug",
            "Chart Audit",
            "--worktree-root",
            "/tmp",
        )

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["branch_name"], "sandbox/issue-1357-pr-pending-chart-audit")
        self.assertEqual(payload["worktree_path"], "/tmp/issue-1357-pr-pending-chart-audit")
        self.assertIn("HLDPRO_REPO_SLUG=HealthcarePlatform", payload["command"])

    def test_dirty_invalid_lane_cleanup_refused(self) -> None:
        code, payload = run_helper("--repo-slug", "HealthcarePlatform", "cleanup-advice", "--dirty")

        self.assertNotEqual(code, 0)
        self.assertEqual(payload["next_action"], "operator_review_required")

    def test_clean_invalid_lane_cleanup_documented(self) -> None:
        code, payload = run_helper("--repo-slug", "HealthcarePlatform", "cleanup-advice")

        self.assertEqual(code, 0, payload)
        self.assertIn("recreate", payload["next_action"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
