#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "overlord" / "check_worker_handoff_route.py"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


class RepoFixture:
    def __init__(self, root: Path, branch: str = "issue-448-worker-handoff-routing-20260421") -> None:
        self.root = root
        root.mkdir(parents=True, exist_ok=True)
        _git(root, "init")
        _git(root, "config", "user.name", "Worker Route Test")
        _git(root, "config", "user.email", "worker-route@example.invalid")
        (root / "README.md").write_text("base\n", encoding="utf-8")
        _git(root, "add", "README.md")
        _git(root, "commit", "-m", "base")
        _git(root, "branch", "-M", branch)

    def write_scope(self, payload: dict[str, Any], name: str = "2026-04-21-issue-448-worker-implementation.json") -> Path:
        scope_dir = self.root / "raw" / "execution-scopes"
        scope_dir.mkdir(parents=True, exist_ok=True)
        path = scope_dir / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def write_exception(self, path: str = "raw/exceptions/issue-448-same-family.md") -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("approved exception\n", encoding="utf-8")


def _scope(
    *,
    allowed: list[str] | None = None,
    issue_number: int = 448,
    planner_model: str = "claude-opus-4-6",
    implementer_model: str = "gpt-5.4-codex-qa",
    handoff_status: str = "accepted",
    exception_ref: str | None = None,
    exception_expires_at: str | None = None,
) -> dict[str, Any]:
    return {
        "expected_execution_root": ".",
        "expected_branch": "issue-448-worker-handoff-routing-20260421",
        "execution_mode": "implementation_ready",
        "allowed_write_paths": allowed or ["scripts/new_worker.py"],
        "forbidden_roots": [],
        "lane_claim": {
            "issue_number": issue_number,
            "claim_ref": f"https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/{issue_number}",
            "claimed_by": "codex",
            "claimed_at": "2026-04-21T11:10:00Z",
        },
        "handoff_evidence": {
            "status": handoff_status,
            "planner_model": planner_model,
            "implementer_model": implementer_model,
            "accepted_at": "2026-04-21T11:10:00Z",
            "evidence_paths": ["raw/handoffs/2026-04-21-issue-448-plan-to-implementation.json"],
            "active_exception_ref": exception_ref,
            "active_exception_expires_at": exception_expires_at,
        },
    }


class TestWorkerHandoffRoute(unittest.TestCase):
    def _run(self, repo: RepoFixture, target: str, role: str = "worker") -> tuple[int, dict[str, Any]]:
        result = subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "--repo-root",
                str(repo.root),
                "--target-path",
                target,
                "--branch-name",
                "issue-448-worker-handoff-routing-20260421",
                "--role",
                role,
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        return result.returncode, json.loads(result.stdout)

    def test_planner_lane_new_python_file_is_blocked_with_next_action(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo")
            repo.write_scope(_scope())

            code, payload = self._run(repo, "scripts/new_worker.py", role="planner")

        self.assertNotEqual(code, 0)
        self.assertEqual(payload["decision"], "block")
        self.assertIn("planning/orchestration lane", payload["reason"])
        self.assertIn("raw/execution-scopes/<date>-issue-448-worker-implementation.json", payload["reason"])

    def test_approved_worker_handoff_for_target_path_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo")
            repo.write_scope(_scope())

            code, payload = self._run(repo, "scripts/new_worker.py", role="claude-sonnet-worker")

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["decision"], "allow")

    def test_scope_present_but_target_path_missing_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo")
            repo.write_scope(_scope(allowed=["scripts/other.py"]))

            code, payload = self._run(repo, "scripts/new_worker.py")

        self.assertNotEqual(code, 0)
        self.assertIn("changed paths outside allowed_write_paths", payload["reason"])
        self.assertIn("target path in allowed_write_paths", payload["missing_evidence"])

    def test_worker_handoff_wrong_issue_number_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo")
            repo.write_scope(_scope(issue_number=447))

            code, payload = self._run(repo, "scripts/new_worker.py")

        self.assertNotEqual(code, 0)
        self.assertIn("lane_claim issue mismatch", payload["reason"])

    def test_same_family_worker_handoff_without_exception_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo")
            repo.write_scope(
                _scope(
                    planner_model="claude-opus-4-6",
                    implementer_model="claude-sonnet-4-6",
                )
            )

            code, payload = self._run(repo, "scripts/new_worker.py")

        self.assertNotEqual(code, 0)
        self.assertIn("active_exception_ref", payload["reason"])

    def test_same_family_worker_handoff_with_active_exception_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo")
            repo.write_exception()
            repo.write_scope(
                _scope(
                    planner_model="claude-opus-4-6",
                    implementer_model="claude-sonnet-4-6",
                    exception_ref="raw/exceptions/issue-448-same-family.md",
                    exception_expires_at="2999-01-01T00:00:00Z",
                )
            )

            code, payload = self._run(repo, "scripts/new_worker.py")

        self.assertEqual(code, 0, payload)

    def test_javascript_and_shell_targets_are_governed_code_files(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo")
            repo.write_scope(_scope(allowed=["scripts/new_worker.js", "scripts/new_worker.sh"]))

            js_code, js_payload = self._run(repo, "scripts/new_worker.js")
            sh_code, sh_payload = self._run(repo, "scripts/new_worker.sh")

        self.assertEqual(js_code, 0, js_payload)
        self.assertEqual(sh_code, 0, sh_payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
