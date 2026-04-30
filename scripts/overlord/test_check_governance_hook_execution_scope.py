#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


MODULE_PATH = Path(__file__).with_name("check_governance_hook_execution_scope.py")
SPEC = importlib.util.spec_from_file_location("check_governance_hook_execution_scope", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


class RepoFixture:
    def __init__(self, root: Path, branch: str) -> None:
        self.root = root
        self.branch = branch
        root.mkdir(parents=True, exist_ok=True)
        _git(root, "init")
        _git(root, "config", "user.name", "Governance Hook Test")
        _git(root, "config", "user.email", "governance-hook-test@example.invalid")
        (root / "README.md").write_text("base\n", encoding="utf-8")
        _git(root, "add", "README.md")
        _git(root, "commit", "-m", "base")
        _git(root, "branch", "-M", branch)

    def write(self, relative_path: str, content: str = "ok\n") -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


class TestCheckGovernanceHookExecutionScope(unittest.TestCase):
    BRANCH = "issue-627-governance-hook-check"

    def _changed_files(self, repo: Path, *paths: str) -> Path:
        out = repo / "changed-files.txt"
        out.write_text("\n".join(paths) + "\n", encoding="utf-8")
        return out

    def _scope_payload(
        self,
        repo: Path,
        *,
        mode: str,
        handoff_evidence: dict[str, Any] | None,
    ) -> dict[str, Any]:
        return {
            "expected_execution_root": ".",
            "expected_branch": self.BRANCH,
            "execution_mode": mode,
            "allowed_write_paths": ["hooks/governance-check.sh"],
            "forbidden_roots": [],
            "active_parallel_roots": [],
            "lane_claim": {
                "issue_number": 627,
                "claim_ref": "https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/627",
                "claimed_by": "codex",
                "claimed_at": "2026-04-30T13:04:20Z"
            },
            "handoff_evidence": handoff_evidence,
        }

    def _handoff(
        self,
        *,
        planner_model: str,
        implementer_model: str,
        cross_family_path_unavailable: bool = False,
        cross_family_path_ref: str | None = None,
        fallback_log_ref: str | None = None,
    ) -> dict[str, Any]:
        return {
            "status": "accepted",
            "planner_model": planner_model,
            "implementer_model": implementer_model,
            "accepted_at": "2026-04-30T13:04:20Z",
            "evidence_paths": ["raw/handoffs/issue-627-plan-to-implementation.json"],
            "active_exception_ref": "docs/codex-reviews/2026-04-30-issue-627-claude.md",
            "active_exception_expires_at": "2026-05-01T13:04:20Z",
            "cross_family_path_unavailable": cross_family_path_unavailable,
            "cross_family_path_ref": cross_family_path_ref,
            "fallback_log_ref": fallback_log_ref,
        }

    def _write_scope(self, repo: Path, payload: dict[str, Any], name: str) -> Path:
        path = repo / "raw" / "execution-scopes" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def _run(self, repo: Path, changed_files_file: Path) -> tuple[int, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = module.main(
                [
                    "--root",
                    str(repo),
                    "--branch",
                    self.BRANCH,
                    "--changed-files-file",
                    str(changed_files_file),
                ]
            )
        return code, stdout.getvalue() + stderr.getvalue()

    def test_planning_only_scope_passes_without_replay(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo", self.BRANCH)
            changed = self._changed_files(repo.root, "hooks/governance-check.sh")
            payload = self._scope_payload(repo.root, mode="planning_only", handoff_evidence=None)
            self._write_scope(repo.root, payload, "2026-04-30-issue-627-planning.json")

            code, output = self._run(repo.root, changed)

        self.assertEqual(code, 0, output)
        self.assertIn("planning-only scope", output)

    def test_same_family_with_valid_proof_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo", self.BRANCH)
            repo.write("hooks/governance-check.sh")
            repo.write("docs/codex-reviews/2026-04-30-issue-627-claude.md")
            repo.write("docs/FAIL_FAST_LOG.md", "## issue-627-local-root-hook-fallback-proof\n")
            changed = self._changed_files(repo.root, "hooks/governance-check.sh")
            handoff = self._handoff(
                planner_model="gpt-5.4",
                implementer_model="gpt-5.4",
                cross_family_path_unavailable=True,
                cross_family_path_ref="docs/codex-reviews/2026-04-30-issue-627-claude.md#implementation-review",
                fallback_log_ref="docs/FAIL_FAST_LOG.md#issue-627-local-root-hook-fallback-proof",
            )
            payload = self._scope_payload(repo.root, mode="implementation_ready", handoff_evidence=handoff)
            self._write_scope(repo.root, payload, "2026-04-30-issue-627-implementation.json")

            code, output = self._run(repo.root, changed)

        self.assertEqual(code, 0, output)
        self.assertIn("validated implementation-capable scope", output)

    def test_same_family_missing_proof_field_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo", self.BRANCH)
            repo.write("hooks/governance-check.sh")
            repo.write("docs/codex-reviews/2026-04-30-issue-627-claude.md")
            repo.write("docs/FAIL_FAST_LOG.md", "## issue-627-local-root-hook-fallback-proof\n")
            changed = self._changed_files(repo.root, "hooks/governance-check.sh")
            handoff = self._handoff(
                planner_model="gpt-5.4",
                implementer_model="gpt-5.4",
                cross_family_path_unavailable=True,
                cross_family_path_ref=None,
                fallback_log_ref="docs/FAIL_FAST_LOG.md#issue-627-local-root-hook-fallback-proof",
            )
            payload = self._scope_payload(repo.root, mode="implementation_ready", handoff_evidence=handoff)
            self._write_scope(repo.root, payload, "2026-04-30-issue-627-implementation.json")

            code, output = self._run(repo.root, changed)

        self.assertEqual(code, 1, output)
        self.assertIn("cross_family_path_ref", output)

    def test_same_family_unsafe_fallback_ref_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo", self.BRANCH)
            repo.write("hooks/governance-check.sh")
            repo.write("docs/codex-reviews/2026-04-30-issue-627-claude.md")
            changed = self._changed_files(repo.root, "hooks/governance-check.sh")
            handoff = self._handoff(
                planner_model="gpt-5.4",
                implementer_model="gpt-5.4",
                cross_family_path_unavailable=True,
                cross_family_path_ref="docs/codex-reviews/2026-04-30-issue-627-claude.md#implementation-review",
                fallback_log_ref="../outside.md",
            )
            payload = self._scope_payload(repo.root, mode="implementation_ready", handoff_evidence=handoff)
            self._write_scope(repo.root, payload, "2026-04-30-issue-627-implementation.json")

            code, output = self._run(repo.root, changed)

        self.assertEqual(code, 1, output)
        self.assertIn("must not traverse parent directories", output)

    def test_same_family_nonexistent_proof_ref_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo", self.BRANCH)
            repo.write("hooks/governance-check.sh")
            repo.write("docs/codex-reviews/2026-04-30-issue-627-claude.md")
            repo.write("docs/FAIL_FAST_LOG.md", "## issue-627-local-root-hook-fallback-proof\n")
            changed = self._changed_files(repo.root, "hooks/governance-check.sh")
            handoff = self._handoff(
                planner_model="gpt-5.4",
                implementer_model="gpt-5.4",
                cross_family_path_unavailable=True,
                cross_family_path_ref="docs/codex-reviews/missing.md#implementation-review",
                fallback_log_ref="docs/FAIL_FAST_LOG.md#issue-627-local-root-hook-fallback-proof",
            )
            payload = self._scope_payload(repo.root, mode="implementation_ready", handoff_evidence=handoff)
            self._write_scope(repo.root, payload, "2026-04-30-issue-627-implementation.json")

            code, output = self._run(repo.root, changed)

        self.assertEqual(code, 1, output)
        self.assertIn("cross_family_path_ref must reference an existing repo file path", output)

    def test_same_family_blank_proof_ref_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo", self.BRANCH)
            repo.write("hooks/governance-check.sh")
            repo.write("docs/codex-reviews/2026-04-30-issue-627-claude.md")
            repo.write("docs/FAIL_FAST_LOG.md", "## issue-627-local-root-hook-fallback-proof\n")
            changed = self._changed_files(repo.root, "hooks/governance-check.sh")
            handoff = self._handoff(
                planner_model="gpt-5.4",
                implementer_model="gpt-5.4",
                cross_family_path_unavailable=True,
                cross_family_path_ref="",
                fallback_log_ref="docs/FAIL_FAST_LOG.md#issue-627-local-root-hook-fallback-proof",
            )
            payload = self._scope_payload(repo.root, mode="implementation_ready", handoff_evidence=handoff)
            self._write_scope(repo.root, payload, "2026-04-30-issue-627-implementation.json")

            code, output = self._run(repo.root, changed)

        self.assertEqual(code, 1, output)
        self.assertIn("must be null or a non-empty string", output)

    def test_same_family_placeholder_proof_ref_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo", self.BRANCH)
            repo.write("hooks/governance-check.sh")
            repo.write("docs/codex-reviews/2026-04-30-issue-627-claude.md")
            repo.write("docs/FAIL_FAST_LOG.md", "## issue-627-local-root-hook-fallback-proof\n")
            changed = self._changed_files(repo.root, "hooks/governance-check.sh")
            handoff = self._handoff(
                planner_model="gpt-5.4",
                implementer_model="gpt-5.4",
                cross_family_path_unavailable=True,
                cross_family_path_ref="TODO",
                fallback_log_ref="docs/FAIL_FAST_LOG.md#issue-627-local-root-hook-fallback-proof",
            )
            payload = self._scope_payload(repo.root, mode="implementation_ready", handoff_evidence=handoff)
            self._write_scope(repo.root, payload, "2026-04-30-issue-627-implementation.json")

            code, output = self._run(repo.root, changed)

        self.assertEqual(code, 1, output)
        self.assertIn("must not use placeholder text", output)

    def test_same_family_nonexistent_fallback_log_ref_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo", self.BRANCH)
            repo.write("hooks/governance-check.sh")
            repo.write("docs/codex-reviews/2026-04-30-issue-627-claude.md")
            repo.write("docs/FAIL_FAST_LOG.md", "## issue-627-local-root-hook-fallback-proof\n")
            changed = self._changed_files(repo.root, "hooks/governance-check.sh")
            handoff = self._handoff(
                planner_model="gpt-5.4",
                implementer_model="gpt-5.4",
                cross_family_path_unavailable=True,
                cross_family_path_ref="docs/codex-reviews/2026-04-30-issue-627-claude.md#implementation-review",
                fallback_log_ref="docs/missing-log.md#issue-627-local-root-hook-fallback-proof",
            )
            payload = self._scope_payload(repo.root, mode="implementation_ready", handoff_evidence=handoff)
            self._write_scope(repo.root, payload, "2026-04-30-issue-627-implementation.json")

            code, output = self._run(repo.root, changed)

        self.assertEqual(code, 1, output)
        self.assertIn("fallback_log_ref must reference an existing repo file path", output)

    def test_cross_family_implementation_path_still_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = RepoFixture(Path(raw) / "repo", self.BRANCH)
            repo.write("hooks/governance-check.sh")
            repo.write("docs/codex-reviews/2026-04-30-issue-627-claude.md")
            changed = self._changed_files(repo.root, "hooks/governance-check.sh")
            handoff = self._handoff(
                planner_model="gpt-5.4",
                implementer_model="claude-opus-4-6",
            )
            payload = self._scope_payload(repo.root, mode="implementation_ready", handoff_evidence=handoff)
            self._write_scope(repo.root, payload, "2026-04-30-issue-627-implementation.json")

            code, output = self._run(repo.root, changed)

        self.assertEqual(code, 0, output)
        self.assertIn("validated implementation-capable scope", output)


if __name__ == "__main__":
    unittest.main()
