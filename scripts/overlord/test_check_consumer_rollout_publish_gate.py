#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys


MODULE_PATH = Path(__file__).with_name("check_consumer_rollout_publish_gate.py")
SPEC = importlib.util.spec_from_file_location("check_consumer_rollout_publish_gate", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class TestCheckConsumerRolloutPublishGate(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.repo = self.root / "consumer"
        self.repo.mkdir()
        subprocess.run(["git", "init"], cwd=self.repo, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.repo, check=True)
        (self.repo / "README.md").write_text("# consumer\n", encoding="utf-8")
        (self.repo / "docs" / "sprint").mkdir(parents=True)
        (self.repo / "docs" / "sprint" / "runner-status.md").write_text("Last updated: 2026-04-29\n", encoding="utf-8")
        (self.repo / "docs" / "file-index.txt").write_text("docs/sprint/runner-status.md\n", encoding="utf-8")
        (self.repo / "check-file-index.js").write_text("process.exit(0)\n", encoding="utf-8")
        package = {
            "name": "consumer",
            "version": "1.0.0",
            "scripts": {
                "file-index:check": "node check-file-index.js"
            }
        }
        (self.repo / "package.json").write_text(json.dumps(package), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=self.repo, check=True, capture_output=True, text=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=self.repo, check=True)
        subprocess.run(["git", "update-ref", "refs/remotes/origin/main", "HEAD"], cwd=self.repo, check=True)
        self.pr_body = self.repo / "pr.md"
        self.pr_body.write_text(
            "## Summary\nok\n\n## Acceptance Criteria Status\nok\n\n## Validation\nok\n\n## Blockers and Dependencies\nnone\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _invoke(self, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = module.main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def _base_args(self) -> list[str]:
        return [
            "--target-repo",
            str(self.repo),
            "--base-ref",
            "origin/main",
            "--pr-title",
            "[Issue #1] Example lane",
            "--pr-body-file",
            str(self.pr_body),
        ]

    def test_passes_when_title_body_and_repo_local_gates_are_satisfied(self) -> None:
        code, stdout, stderr = self._invoke(*self._base_args())
        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["failures"], [])

    def test_fails_when_pr_body_missing_required_sections(self) -> None:
        self.pr_body.write_text("## Summary\nonly\n", encoding="utf-8")
        code, stdout, stderr = self._invoke(*self._base_args())
        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("PR body is missing required sections", "\n".join(payload["failures"]))

    def test_fails_when_workflow_changes_without_runner_status_update(self) -> None:
        workflow = self.repo / ".github" / "workflows" / "governance.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text("name: governance\n", encoding="utf-8")
        subprocess.run(["git", "add", ".github/workflows/governance.yml"], cwd=self.repo, check=True)
        code, stdout, stderr = self._invoke(*self._base_args())
        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("docs/sprint/runner-status.md was not updated", "\n".join(payload["failures"]))

    def test_fails_when_untracked_workflow_changes_without_runner_status_update(self) -> None:
        workflow = self.repo / ".github" / "workflows" / "governance.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text("name: governance\n", encoding="utf-8")
        code, stdout, stderr = self._invoke(*self._base_args())
        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("docs/sprint/runner-status.md was not updated", "\n".join(payload["failures"]))

    def test_fails_when_file_index_check_fails(self) -> None:
        (self.repo / "check-file-index.js").write_text("process.exit(1)\n", encoding="utf-8")
        code, stdout, stderr = self._invoke(*self._base_args())
        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("file-index check failed", "\n".join(payload["failures"]))

    def test_fails_cleanly_when_pr_body_file_is_missing(self) -> None:
        missing = self.repo / "missing-pr.md"
        code, stdout, stderr = self._invoke(
            "--target-repo",
            str(self.repo),
            "--base-ref",
            "origin/main",
            "--pr-title",
            "[Issue #1] Example lane",
            "--pr-body-file",
            str(missing),
        )
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("could not read PR body file", stderr)


if __name__ == "__main__":
    unittest.main()
