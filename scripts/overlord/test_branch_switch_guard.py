#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / "hooks" / "branch-switch-guard.sh"


def run_hook(command: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(HOOK)],
        cwd=cwd or REPO_ROOT,
        input=json.dumps({"tool_input": {"command": command}}),
        text=True,
        capture_output=True,
        check=False,
    )


class TestBranchSwitchGuard(unittest.TestCase):
    def test_blocks_unclaimed_issue_worktree_add(self) -> None:
        result = run_hook(
            "git worktree add -b issue-397-preworktree-lane-gate ../issue-397-preworktree-lane-gate origin/main"
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("Issue worktree creation requires", result.stderr)

    def test_allows_explicit_planning_bootstrap_issue_worktree_add(self) -> None:
        result = run_hook(
            "HLDPRO_LANE_CLAIM_BOOTSTRAP=1 git worktree add -b issue-397-preworktree-lane-gate ../issue-397-preworktree-lane-gate origin/main"
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_allows_non_issue_worktree_add(self) -> None:
        result = run_hook("git worktree add -b docs-readme-refresh ../wt origin/main")

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_allows_issue_worktree_add_with_matching_claimed_scope(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            root = Path(raw_tmpdir)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            scope = root / "raw" / "execution-scopes" / "issue-397-scope.json"
            scope.parent.mkdir(parents=True)
            scope.write_text(json.dumps({"lane_claim": {"issue_number": 397}}), encoding="utf-8")

            result = run_hook(
                "HLDPRO_LANE_CLAIM_SCOPE=raw/execution-scopes/issue-397-scope.json "
                "git worktree add -b issue-397-preworktree-lane-gate ../issue-397-preworktree-lane-gate origin/main",
                cwd=root,
            )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_blocks_issue_worktree_add_with_mismatched_claimed_scope(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            root = Path(raw_tmpdir)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            scope = root / "raw" / "execution-scopes" / "issue-397-scope.json"
            scope.parent.mkdir(parents=True)
            scope.write_text(json.dumps({"lane_claim": {"issue_number": 398}}), encoding="utf-8")

            result = run_hook(
                "HLDPRO_LANE_CLAIM_SCOPE=raw/execution-scopes/issue-397-scope.json "
                "git worktree add -b issue-397-preworktree-lane-gate ../issue-397-preworktree-lane-gate origin/main",
                cwd=root,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("matching issue-<n>", result.stderr)

    def test_healthcareplatform_policy_rejects_non_sandbox_branch(self) -> None:
        result = run_hook(
            "HLDPRO_REPO_SLUG=HealthcarePlatform HLDPRO_LANE_CLAIM_BOOTSTRAP=1 "
            "git worktree add -b issue-1357-chart-audit ../issue-1357-chart-audit origin/main"
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("Lane policy: invalid branch pattern", result.stderr)

    def test_healthcareplatform_policy_accepts_sandbox_pr_pending_lane(self) -> None:
        result = run_hook(
            "HLDPRO_REPO_SLUG=HealthcarePlatform HLDPRO_LANE_CLAIM_BOOTSTRAP=1 "
            "git worktree add -b sandbox/issue-1357-pr-pending-chart-audit ../issue-1357-pr-pending-chart-audit origin/main"
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_still_blocks_branch_checkout(self) -> None:
        result = run_hook("git checkout main")

        self.assertEqual(result.returncode, 2)
        self.assertIn("Branch switching is not allowed", result.stderr)

    def test_heredoc_body_does_not_trigger_branch_matching(self) -> None:
        result = run_hook("cat <<'EOF'\ngit checkout main\nEOF")

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_blocks_force_push_variants(self) -> None:
        blocked_commands = [
            "git push -f origin main",
            "git push --force origin main",
            "git push --force-with-lease origin main",
            "git push --force-with-lease=main origin main",
            "git push origin +main:main",
        ]

        for command in blocked_commands:
            with self.subTest(command=command):
                result = run_hook(command)

                self.assertEqual(result.returncode, 2)
                self.assertIn("Blocked command", result.stderr)
                self.assertIn("git push", result.stderr)


if __name__ == "__main__":
    unittest.main()
