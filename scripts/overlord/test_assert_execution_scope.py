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
        expected_root: Path,
        branch: str = "scope-test",
        allowed: list[str] | None = None,
        forbidden_roots: list[Path] | None = None,
    ) -> Path:
        scope = {
            "expected_execution_root": str(expected_root),
            "expected_branch": branch,
            "allowed_write_paths": allowed or ["allowed.txt", "allowed-dir/"],
            "forbidden_roots": [str(path) for path in forbidden_roots or []],
        }
        path = tmpdir / "scope.json"
        path.write_text(json.dumps(scope), encoding="utf-8")
        return path

    def _run_main(self, repo: Path, scope: Path) -> tuple[int, str]:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), _working_directory(repo):
            code = assert_execution_scope.main(["--scope", str(scope)])
        return code, stdout.getvalue()

    def test_allows_changes_in_allowed_paths(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            repo = RepoFixture(tmpdir / "repo")
            repo.write("allowed.txt")
            repo.write("allowed-dir/nested.txt")
            scope = self._scope_file(tmpdir, repo.root)

            code, output = self._run_main(repo.root, scope)

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
