#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path
from typing import Any


MODULE_PATH = Path(__file__).with_name("assert_execution_scope.py")
SPEC = importlib.util.spec_from_file_location("assert_execution_scope", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
assert_execution_scope = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = assert_execution_scope
SPEC.loader.exec_module(assert_execution_scope)


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


class RepoFixture:
    def __init__(self, root: Path, branch: str = "scope-test") -> None:
        self.root = root
        self.branch = branch
        root.mkdir(parents=True, exist_ok=True)
        _git(root, "init")
        _git(root, "config", "user.name", "Scope Test")
        _git(root, "config", "user.email", "scope-test@example.invalid")
        (root / "README.md").write_text("base\n", encoding="utf-8")
        _git(root, "add", "README.md")
        _git(root, "commit", "-m", "base")
        _git(root, "branch", "-M", branch)

    def write(self, relative_path: str, content: str = "changed\n") -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


class TestAssertExecutionScope(unittest.TestCase):
    def _scope_file(
        self,
        tmpdir: Path,
        expected_root: Path | str,
        branch: str = "scope-test",
        allowed: list[str] | None = None,
        forbidden_roots: list[Path] | None = None,
        active_parallel_roots: list[dict[str, str]] | None = None,
        execution_mode: str | None = None,
        lane_claim: dict[str, Any] | None = None,
        handoff_evidence: dict[str, Any] | None = None,
    ) -> Path:
        scope = {
            "expected_execution_root": str(expected_root),
            "expected_branch": branch,
            "allowed_write_paths": allowed or ["allowed.txt", "allowed-dir/"],
            "forbidden_roots": [str(path) for path in forbidden_roots or []],
        }
        if active_parallel_roots is not None:
            scope["active_parallel_roots"] = active_parallel_roots
        if execution_mode is not None:
            scope["execution_mode"] = execution_mode
        if lane_claim is not None:
            scope["lane_claim"] = lane_claim
        if handoff_evidence is not None:
            scope["handoff_evidence"] = handoff_evidence
        path = tmpdir / "scope.json"
        path.write_text(json.dumps(scope), encoding="utf-8")
        return path

    def _run_main(
        self,
        repo: Path,
        scope: Path,
        changed_files_file: Path | None = None,
        require_lane_claim: bool = False,
    ) -> tuple[int, str]:
        args = ["--scope", str(scope)]
        if changed_files_file is not None:
            args.extend(["--changed-files-file", str(changed_files_file)])
        if require_lane_claim:
            args.append("--require-lane-claim")
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr), _working_directory(repo):
            code = assert_execution_scope.main(args)
        return code, stdout.getvalue() + stderr.getvalue()

    def _changed_files_file(self, tmpdir: Path, paths: list[str], name: str = "changed-files.txt") -> Path:
        path = tmpdir / name
        path.write_text("\n".join(paths) + "\n", encoding="utf-8")
        return path

    def _write_exception_file(self, repo: RepoFixture, relative_path: str) -> None:
        repo.write(relative_path, "approved exception\n")

    def _handoff(
        self,
        *,
        planner_model: str,
        implementer_model: str,
        status: str = "accepted",
        active_exception_ref: str | None = None,
        active_exception_expires_at: str | None = None,
    ) -> dict[str, Any]:
        return {
            "status": status,
            "planner_model": planner_model,
            "implementer_model": implementer_model,
            "accepted_at": "2026-04-17T00:00:00Z",
            "evidence_paths": ["raw/closeouts/issue-242-handoff.md"],
            "active_exception_ref": active_exception_ref,
            "active_exception_expires_at": active_exception_expires_at,
        }

    def _lane_claim(self, issue_number: int = 393) -> dict[str, Any]:
        return {
            "issue_number": issue_number,
            "claim_ref": f"https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/{issue_number}",
            "claimed_by": "codex",
            "claimed_at": "2026-04-20T15:05:17Z",
        }

    def test_allows_changes_in_allowed_paths_dirty_tree_mode(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            repo.write("allowed.txt")
            repo.write("allowed-dir/nested.txt")
            scope = self._scope_file(tmpdir, repo.root)

            code, output = self._run_main(repo.root, scope)

        self.assertEqual(code, 0, output)
        self.assertIn("PASS execution scope", output)

    def test_planning_only_diff_inside_allowed_paths_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            changed = self._changed_files_file(tmpdir, ["./allowed-dir/nested.txt"])
            scope = self._scope_file(tmpdir, repo.root, execution_mode="planning_only")

            code, output = self._run_main(repo.root, scope, changed_files_file=changed)

        self.assertEqual(code, 0, output)
        self.assertIn("PASS execution scope", output)

    def test_planning_only_diff_outside_allowed_paths_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            changed = self._changed_files_file(tmpdir, ["./not-allowed.txt"])
            scope = self._scope_file(tmpdir, repo.root, execution_mode="planning_only")

            code, output = self._run_main(repo.root, scope, changed_files_file=changed)

        self.assertNotEqual(code, 0)
        self.assertIn("changed paths outside allowed_write_paths", output)
        self.assertIn("not-allowed.txt", output)

    def test_non_planning_without_handoff_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            changed = self._changed_files_file(tmpdir, ["allowed.txt"])
            scope = self._scope_file(tmpdir, repo.root, execution_mode="implementation_ready")

            code, output = self._run_main(repo.root, scope, changed_files_file=changed)

        self.assertNotEqual(code, 0)
        self.assertIn("requires `handoff_evidence.status` == 'accepted'", output)

    def test_non_planning_with_accepted_handoff_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            changed = self._changed_files_file(tmpdir, ["allowed.txt"])
            scope = self._scope_file(
                tmpdir,
                repo.root,
                execution_mode="implementation_ready",
                handoff_evidence=self._handoff(
                    planner_model="gpt-5",
                    implementer_model="claude-3-7-sonnet",
                ),
            )

            code, output = self._run_main(repo.root, scope, changed_files_file=changed)

        self.assertEqual(code, 0, output)
        self.assertIn("PASS execution scope", output)

    def test_same_model_or_family_without_active_exception_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            changed = self._changed_files_file(tmpdir, ["allowed.txt"])
            scope = self._scope_file(
                tmpdir,
                repo.root,
                execution_mode="implementation_ready",
                handoff_evidence=self._handoff(
                    planner_model="gpt-5",
                    implementer_model="gpt-5-mini",
                ),
            )

            code, output = self._run_main(repo.root, scope, changed_files_file=changed)

        self.assertNotEqual(code, 0)
        self.assertIn("active_exception_ref", output)

    def test_gpt_major_decimal_variants_without_active_exception_fail(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            changed = self._changed_files_file(tmpdir, ["allowed.txt"])
            scope = self._scope_file(
                tmpdir,
                repo.root,
                execution_mode="implementation_ready",
                handoff_evidence=self._handoff(
                    planner_model="gpt-5.3-codex",
                    implementer_model="openai/gpt-5.4",
                ),
            )

            code, output = self._run_main(repo.root, scope, changed_files_file=changed)

        self.assertNotEqual(code, 0)
        self.assertIn("active_exception_ref", output)

    def test_gpt_major_decimal_variants_with_active_exception_pass(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            changed = self._changed_files_file(tmpdir, ["allowed.txt"])
            self._write_exception_file(repo, "raw/exceptions/issue-242-gpt5-major-line.md")
            scope = self._scope_file(
                tmpdir,
                repo.root,
                execution_mode="implementation_ready",
                handoff_evidence=self._handoff(
                    planner_model="gpt-5.3-codex",
                    implementer_model="openai/gpt-5.4",
                    active_exception_ref="raw/exceptions/issue-242-gpt5-major-line.md",
                    active_exception_expires_at="2999-01-01T00:00:00Z",
                ),
            )

            code, output = self._run_main(repo.root, scope, changed_files_file=changed)

        self.assertEqual(code, 0, output)
        self.assertIn("PASS execution scope", output)

    def test_active_exception_with_expiry_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            changed = self._changed_files_file(tmpdir, ["allowed.txt"])
            self._write_exception_file(repo, "raw/exceptions/issue-242-gpt5-exception.md")
            scope = self._scope_file(
                tmpdir,
                repo.root,
                execution_mode="implementation_ready",
                handoff_evidence=self._handoff(
                    planner_model="gpt-5",
                    implementer_model="gpt-5-mini",
                    active_exception_ref="raw/exceptions/issue-242-gpt5-exception.md",
                    active_exception_expires_at="2999-01-01T00:00:00Z",
                ),
            )

            code, output = self._run_main(repo.root, scope, changed_files_file=changed)

        self.assertEqual(code, 0, output)
        self.assertIn("PASS execution scope", output)

    def test_active_exception_ref_nonexistent_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            changed = self._changed_files_file(tmpdir, ["allowed.txt"])
            scope = self._scope_file(
                tmpdir,
                repo.root,
                execution_mode="implementation_ready",
                handoff_evidence=self._handoff(
                    planner_model="gpt-5",
                    implementer_model="gpt-5-mini",
                    active_exception_ref="raw/exceptions/missing.md",
                    active_exception_expires_at="2999-01-01T00:00:00Z",
                ),
            )

            code, output = self._run_main(repo.root, scope, changed_files_file=changed)

        self.assertNotEqual(code, 0)
        self.assertIn("active_exception_ref must reference an existing repo file path", output)
        self.assertIn("raw/exceptions/missing.md", output)

    def test_active_exception_ref_existing_file_with_anchor_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            changed = self._changed_files_file(tmpdir, ["allowed.txt"])
            self._write_exception_file(repo, "raw/exceptions/issue-242-anchor.md")
            scope = self._scope_file(
                tmpdir,
                repo.root,
                execution_mode="implementation_ready",
                handoff_evidence=self._handoff(
                    planner_model="gpt-5",
                    implementer_model="gpt-5-mini",
                    active_exception_ref="raw/exceptions/issue-242-anchor.md#issue-242",
                    active_exception_expires_at="2999-01-01T00:00:00Z",
                ),
            )

            code, output = self._run_main(repo.root, scope, changed_files_file=changed)

        self.assertEqual(code, 0, output)
        self.assertIn("PASS execution scope", output)

    def test_diff_mode_and_dirty_tree_mode_share_path_normalization(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            repo.write("allowed-dir/nested.txt")
            changed = self._changed_files_file(tmpdir, ["./allowed-dir/nested.txt"])
            scope = self._scope_file(tmpdir, repo.root)

            dirty_code, dirty_output = self._run_main(repo.root, scope)
            diff_code, diff_output = self._run_main(repo.root, scope, changed_files_file=changed)

        self.assertEqual(dirty_code, 0, dirty_output)
        self.assertEqual(diff_code, 0, diff_output)

    def test_portable_expected_root_sentinel_passes_in_copied_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            source_repo = RepoFixture(tmpdir / "source")
            copied_repo_root = tmpdir / "copied"
            shutil.copytree(source_repo.root, copied_repo_root)
            scope = self._scope_file(tmpdir, "{repo_root}")

            code, output = self._run_main(copied_repo_root, scope)

        self.assertEqual(code, 0, output)
        self.assertIn("PASS execution scope", output)

    def test_refuses_wrong_root(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            other = RepoFixture(tmpdir / "other")
            scope = self._scope_file(tmpdir, other.root)

            code, output = self._run_main(repo.root, scope)

        self.assertNotEqual(code, 0)
        self.assertIn("execution root mismatch", output)

    def test_refuses_wrong_branch(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            scope = self._scope_file(tmpdir, repo.root, branch="different-branch")

            code, output = self._run_main(repo.root, scope)

        self.assertNotEqual(code, 0)
        self.assertIn("branch mismatch", output)

    def test_require_lane_claim_passes_when_issue_matches_branch_and_scope(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo", branch="issue-393-lane-claim-gate-20260420")
            changed = self._changed_files_file(tmpdir, ["allowed.txt"])
            scope = self._scope_file(
                tmpdir,
                repo.root,
                branch="issue-393-lane-claim-gate-20260420",
                lane_claim=self._lane_claim(393),
            )

            code, output = self._run_main(repo.root, scope, changed_files_file=changed, require_lane_claim=True)

        self.assertEqual(code, 0, output)
        self.assertIn("PASS execution scope", output)

    def test_require_lane_claim_fails_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo", branch="issue-393-lane-claim-gate-20260420")
            scope = self._scope_file(tmpdir, repo.root, branch="issue-393-lane-claim-gate-20260420")

            code, output = self._run_main(repo.root, scope, require_lane_claim=True)

        self.assertNotEqual(code, 0)
        self.assertIn("requires `lane_claim`", output)

    def test_require_lane_claim_fails_when_current_branch_issue_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo", branch="issue-393-lane-claim-gate-20260420")
            scope = self._scope_file(
                tmpdir,
                repo.root,
                branch="issue-393-lane-claim-gate-20260420",
                lane_claim=self._lane_claim(391),
            )

            code, output = self._run_main(repo.root, scope, require_lane_claim=True)

        self.assertNotEqual(code, 0)
        self.assertIn("lane_claim issue mismatch", output)

    def test_require_lane_claim_fails_when_expected_branch_issue_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo", branch="issue-393-lane-claim-gate-20260420")
            scope = self._scope_file(
                tmpdir,
                repo.root,
                branch="feature/no-issue-token",
                lane_claim=self._lane_claim(393),
            )

            code, output = self._run_main(repo.root, scope, require_lane_claim=True)

        self.assertNotEqual(code, 0)
        self.assertIn("expected_branch to contain `issue-<number>`", output)

    def test_detached_checkout_uses_github_head_ref(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo", branch="issue-324-detached-source")
            head = _git(repo.root, "rev-parse", "HEAD").stdout.strip()
            _git(repo.root, "checkout", "--detach", head)
            changed = self._changed_files_file(tmpdir, ["allowed.txt"])
            scope = self._scope_file(tmpdir, repo.root, branch="issue-324-detached-source")

            with mock.patch.dict(
                "os.environ",
                {"GITHUB_HEAD_REF": "issue-324-detached-source"},
                clear=False,
            ):
                code, output = self._run_main(repo.root, scope, changed_files_file=changed)

        self.assertEqual(code, 0, output)
        self.assertIn("PASS execution scope", output)

    def test_refuses_dirty_forbidden_root(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            forbidden = RepoFixture(tmpdir / "forbidden")
            forbidden.write("leak.txt")
            scope = self._scope_file(tmpdir, repo.root, forbidden_roots=[forbidden.root])

            code, output = self._run_main(repo.root, scope)

        self.assertNotEqual(code, 0)
        self.assertIn("forbidden root is dirty", output)
        self.assertIn("leak.txt", output)

    def test_declared_active_parallel_root_warns_instead_of_failing(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            forbidden = RepoFixture(tmpdir / "forbidden")
            forbidden.write("active-lane.txt")
            scope = self._scope_file(
                tmpdir,
                repo.root,
                forbidden_roots=[forbidden.root],
                active_parallel_roots=[
                    {
                        "path": str(forbidden.root),
                        "reason": "parallel lane under test",
                    }
                ],
            )

            code, output = self._run_main(repo.root, scope)

        self.assertEqual(code, 0, output)
        self.assertIn("WARN active parallel root declared", output)
        self.assertIn("active-lane.txt", output)
        self.assertIn("PASS execution scope", output)

    def test_active_parallel_root_does_not_hide_inactive_dirty_root(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            active = RepoFixture(tmpdir / "active")
            inactive = RepoFixture(tmpdir / "inactive")
            active.write("active-lane.txt")
            inactive.write("inactive-lane.txt")
            scope = self._scope_file(
                tmpdir,
                repo.root,
                forbidden_roots=[active.root, inactive.root],
                active_parallel_roots=[
                    {
                        "path": str(active.root),
                        "reason": "parallel lane under test",
                    }
                ],
            )

            code, output = self._run_main(repo.root, scope)

        self.assertNotEqual(code, 0)
        self.assertIn("WARN active parallel root declared", output)
        self.assertIn("inactive-lane.txt", output)
        self.assertIn("FAIL forbidden root is dirty", output)

    def test_clean_active_parallel_root_does_not_warn(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            forbidden = RepoFixture(tmpdir / "forbidden")
            scope = self._scope_file(
                tmpdir,
                repo.root,
                forbidden_roots=[forbidden.root],
                active_parallel_roots=[
                    {
                        "path": str(forbidden.root),
                        "reason": "parallel lane under test",
                    }
                ],
            )

            code, output = self._run_main(repo.root, scope)

        self.assertEqual(code, 0, output)
        self.assertNotIn("WARN active parallel root declared", output)

    def test_refuses_active_parallel_root_not_in_forbidden_roots(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            other = RepoFixture(tmpdir / "other")
            scope = self._scope_file(
                tmpdir,
                repo.root,
                forbidden_roots=[],
                active_parallel_roots=[
                    {
                        "path": str(other.root),
                        "reason": "parallel lane under test",
                    }
                ],
            )

            code, output = self._run_main(repo.root, scope)

        self.assertEqual(code, 2)
        self.assertIn("must also appear in `forbidden_roots`", output)

    def test_refuses_active_parallel_root_without_reason(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            forbidden = RepoFixture(tmpdir / "forbidden")
            scope = self._scope_file(
                tmpdir,
                repo.root,
                forbidden_roots=[forbidden.root],
                active_parallel_roots=[
                    {
                        "path": str(forbidden.root),
                        "reason": "",
                    }
                ],
            )

            code, output = self._run_main(repo.root, scope)

        self.assertEqual(code, 2)
        self.assertIn("reason` must be a non-empty string", output)

    def test_refuses_out_of_scope_changes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            repo.write("not-allowed.txt")
            scope = self._scope_file(tmpdir, repo.root)

            code, output = self._run_main(repo.root, scope)

        self.assertNotEqual(code, 0)
        self.assertIn("changed paths outside allowed_write_paths", output)
        self.assertIn("not-allowed.txt", output)


@contextlib.contextmanager
def _working_directory(path: Path):
    original = Path.cwd()
    try:
        import os

        os.chdir(path)
        yield
    finally:
        os.chdir(original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
