#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "overlord" / "check_execution_environment.py"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _make_repo(tmpdir: Path, branch: str = "issue-617-check-env-20260430") -> Path:
    repo = tmpdir / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.name", "Execution Env Test")
    _git(repo, "config", "user.email", "execution-env@example.invalid")
    _write(repo / "README.md", "base\n")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-m", "base")
    _git(repo, "branch", "-M", branch)
    return repo


def _write_scope(repo: Path, name: str, payload: dict[str, object]) -> Path:
    path = repo / "raw" / "execution-scopes" / name
    _write(path, json.dumps(payload, indent=2) + "\n")
    return path


def _write_plan(repo: Path, name: str, next_role: str = "codex-orchestrator") -> Path:
    path = repo / "docs" / "plans" / name
    payload = {
        "execution_handoff": {
            "next_role": next_role,
            "next_execution_step": "begin bounded startup implementation",
            "qa_gate_required": True,
        },
        "specialist_reviews": [
            {"reviewer": "startup-scope research specialist", "status": "mixed"},
            {"reviewer": "startup-scope QA specialist", "status": "mixed"},
        ],
        "alternate_model_review": {"required": True, "status": "accepted"},
    }
    _write(path, json.dumps(payload, indent=2) + "\n")
    return path


def _write_handoff(repo: Path, name: str, scope_ref: str, plan_ref: str) -> Path:
    path = repo / "raw" / "handoffs" / name
    payload = {
        "execution_scope_ref": scope_ref,
        "structured_plan_ref": plan_ref,
        "to_role": "codex-orchestrator",
        "created_at": "2026-04-30T03:35:00Z",
    }
    _write(path, json.dumps(payload, indent=2) + "\n")
    return path


def _run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )


class CheckExecutionEnvironmentTests(unittest.TestCase):
    def test_startup_preflight_prefers_unique_implementation_scope(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            tmpdir = Path(raw_tmp)
            repo = _make_repo(tmpdir)
            issue_number = 617

            _write(repo / "docs" / "codex-reviews" / "2026-04-30-issue-617-claude.md", "review\n")
            plan_ref = "docs/plans/issue-617-plan.json"
            _write_plan(repo, "issue-617-plan.json")

            planning_scope_ref = "raw/execution-scopes/2026-04-30-issue-617-planning.json"
            _write_scope(
                repo,
                "2026-04-30-issue-617-planning.json",
                {
                    "expected_execution_root": ".",
                    "expected_branch": "issue-617-check-env-20260430",
                    "execution_mode": "planning_only",
                    "allowed_write_paths": ["raw/"],
                    "forbidden_roots": [],
                    "lane_claim": {
                        "issue_number": issue_number,
                        "claim_ref": "https://example.invalid/issues/617",
                        "claimed_by": "codex",
                        "claimed_at": "2026-04-30T03:00:00Z",
                    },
                },
            )
            implementation_scope_ref = "raw/execution-scopes/2026-04-30-issue-617-implementation.json"
            _write_scope(
                repo,
                "2026-04-30-issue-617-implementation.json",
                {
                    "expected_execution_root": ".",
                    "expected_branch": "issue-617-check-env-20260430",
                    "execution_mode": "implementation_ready",
                    "allowed_write_paths": ["raw/", "docs/"],
                    "forbidden_roots": [],
                    "lane_claim": {
                        "issue_number": issue_number,
                        "claim_ref": "https://example.invalid/issues/617",
                        "claimed_by": "codex",
                        "claimed_at": "2026-04-30T03:05:00Z",
                    },
                    "handoff_evidence": {
                        "status": "accepted",
                        "planner_model": "gpt-5.4",
                        "implementer_model": "gpt-5.4",
                        "accepted_at": "2026-04-30T03:35:00Z",
                        "evidence_paths": [plan_ref],
                        "active_exception_ref": "docs/codex-reviews/2026-04-30-issue-617-claude.md",
                        "active_exception_expires_at": "2026-05-01T03:35:00Z",
                    },
                },
            )
            _write_handoff(repo, "2026-04-30-issue-617.json", implementation_scope_ref, plan_ref)

            result = _run(repo, "--startup-preflight", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["scope_path"], implementation_scope_ref)
        self.assertEqual(payload["execution_mode"], "implementation_ready")
        self.assertEqual(payload["next_role"], "codex-orchestrator")
        self.assertIn("startup-scope research specialist", payload["required_specialists"])
        self.assertIn("alternate_model_review", payload["required_specialists"])

    def test_startup_preflight_blocks_when_multiple_implementation_scopes_match(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            tmpdir = Path(raw_tmp)
            repo = _make_repo(tmpdir)
            issue_number = 617
            _write(repo / "docs" / "codex-reviews" / "2026-04-30-issue-617-claude.md", "review\n")

            base_scope = {
                "expected_execution_root": ".",
                "expected_branch": "issue-617-check-env-20260430",
                "execution_mode": "implementation_ready",
                "allowed_write_paths": ["raw/", "docs/"],
                "forbidden_roots": [],
                "lane_claim": {
                    "issue_number": issue_number,
                    "claim_ref": "https://example.invalid/issues/617",
                    "claimed_by": "codex",
                    "claimed_at": "2026-04-30T03:05:00Z",
                },
                "handoff_evidence": {
                    "status": "accepted",
                    "planner_model": "gpt-5.4",
                    "implementer_model": "gpt-5.4",
                    "accepted_at": "2026-04-30T03:35:00Z",
                    "evidence_paths": ["docs/plans/placeholder.json"],
                    "active_exception_ref": "docs/codex-reviews/2026-04-30-issue-617-claude.md",
                    "active_exception_expires_at": "2026-05-01T03:35:00Z",
                },
            }
            _write_scope(repo, "2026-04-30-issue-617-implementation-a.json", base_scope)
            _write_scope(repo, "2026-04-30-issue-617-implementation-b.json", base_scope)

            result = _run(repo, "--startup-preflight")

        self.assertEqual(result.returncode, 1)
        self.assertIn("BLOCKED startup execution context", result.stdout)
        self.assertIn("multiple implementation-capable claimed scopes", result.stdout)

    def test_startup_preflight_blocks_when_multiple_planning_scopes_match(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            tmpdir = Path(raw_tmp)
            repo = _make_repo(tmpdir)
            issue_number = 617
            planning_scope = {
                "expected_execution_root": ".",
                "expected_branch": "issue-617-check-env-20260430",
                "execution_mode": "planning_only",
                "allowed_write_paths": ["raw/"],
                "forbidden_roots": [],
                "lane_claim": {
                    "issue_number": issue_number,
                    "claim_ref": "https://example.invalid/issues/617",
                    "claimed_by": "codex",
                    "claimed_at": "2026-04-30T03:05:00Z",
                },
            }
            _write_scope(repo, "2026-04-30-issue-617-planning-a.json", planning_scope)
            _write_scope(repo, "2026-04-30-issue-617-planning-b.json", planning_scope)

            result = _run(repo, "--startup-preflight")

        self.assertEqual(result.returncode, 1)
        self.assertIn("BLOCKED startup execution context", result.stdout)
        self.assertIn("multiple planning-only claimed scopes", result.stdout)

    def test_startup_preflight_blocks_on_lane_claim_branch_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            tmpdir = Path(raw_tmp)
            repo = _make_repo(tmpdir)
            _write_scope(
                repo,
                "2026-04-30-issue-617-planning.json",
                {
                    "expected_execution_root": ".",
                    "expected_branch": "issue-999-other-20260430",
                    "execution_mode": "planning_only",
                    "allowed_write_paths": ["raw/"],
                    "forbidden_roots": [],
                    "lane_claim": {
                        "issue_number": 617,
                        "claim_ref": "https://example.invalid/issues/617",
                        "claimed_by": "codex",
                        "claimed_at": "2026-04-30T03:05:00Z",
                    },
                },
            )

            result = _run(repo, "--startup-preflight")

        self.assertEqual(result.returncode, 1)
        self.assertIn("BLOCKED startup execution context", result.stdout)
        self.assertIn("no claimed execution scope matched the current issue branch", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
