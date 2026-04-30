#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("check_fallback_log_schema.py").resolve()


def _run_git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)


def _init_repo() -> tuple[tempfile.TemporaryDirectory[str], Path, str]:
    raw = tempfile.TemporaryDirectory()
    root = Path(raw.name)
    _run_git(root, "init")
    _run_git(root, "config", "user.email", "tests@example.com")
    _run_git(root, "config", "user.name", "Tests")
    (root / "README.md").write_text("repo\n", encoding="utf-8")
    _run_git(root, "add", "README.md")
    _run_git(root, "commit", "-m", "base")
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return raw, root, base


def _commit_fallback(root: Path, content: str, message: str = "fallback") -> str:
    path = root / "raw/model-fallbacks/2026-04-30.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    _run_git(root, "add", path.as_posix())
    _run_git(root, "commit", "-m", message)
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _run_checker(root: Path, *, base_sha: str | None, head_sha: str | None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if base_sha is None:
        env.pop("BASE_SHA", None)
    else:
        env["BASE_SHA"] = base_sha
    if head_sha is None:
        env.pop("HEAD_SHA", None)
    else:
        env["HEAD_SHA"] = head_sha
    return subprocess.run(
        ["python3", str(SCRIPT)],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


GENERIC_BLOCK = textwrap.dedent(
    """\
    ---
    date: 2026-04-30
    session_id: abc123
    tier: 1
    primary_model: gpt-5.4
    fallback_model: gpt-5.3-codex-spark
    reason: gpt-5.4 unavailable; Spark used for same-family specialist critique
    caller_script: scripts/codex-review.sh
    ---
    """
)


DEGRADED_BLOCK = textwrap.dedent(
    """\
    ---
    date: 2026-04-30
    session_id: abc123
    tier: 1
    primary_model: gpt-5.4
    fallback_model: gpt-5.3-codex-spark
    reason: gpt-5.4 unavailable; Spark used for same-family specialist critique
    caller_script: scripts/codex-review.sh
    fallback_scope: alternate_model_review
    cross_family_path_unavailable: true
    cross_family_path_ref: docs/codex-reviews/2026-04-30-issue-629-claude.md
    ---
    """
)


class CheckFallbackLogSchemaTests(unittest.TestCase):
    def test_skip_when_pr_context_missing(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            result = _run_checker(root, base_sha=None, head_sha=None)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Missing pull request context; skipping", result.stdout)

    def test_passes_generic_changed_fallback_file(self) -> None:
        raw_ctx, root, base = _init_repo()
        try:
            head = _commit_fallback(root, GENERIC_BLOCK)
            result = _run_checker(root, base_sha=base, head_sha=head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        finally:
            raw_ctx.cleanup()

    def test_passes_degraded_changed_fallback_file(self) -> None:
        raw_ctx, root, base = _init_repo()
        try:
            head = _commit_fallback(root, DEGRADED_BLOCK)
            result = _run_checker(root, base_sha=base, head_sha=head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        finally:
            raw_ctx.cleanup()

    def test_passes_multi_block_append(self) -> None:
        raw_ctx, root, base = _init_repo()
        try:
            head = _commit_fallback(root, GENERIC_BLOCK + "\n" + DEGRADED_BLOCK)
            result = _run_checker(root, base_sha=base, head_sha=head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        finally:
            raw_ctx.cleanup()

    def test_fails_degraded_entry_with_generic_reason(self) -> None:
        raw_ctx, root, base = _init_repo()
        try:
            block = DEGRADED_BLOCK.replace(
                "reason: gpt-5.4 unavailable; Spark used for same-family specialist critique",
                "reason: other",
            )
            head = _commit_fallback(root, block)
            result = _run_checker(root, base_sha=base, head_sha=head)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("reason must be specific, not generic", result.stdout)
        finally:
            raw_ctx.cleanup()

    def test_fails_missing_required_field(self) -> None:
        raw_ctx, root, base = _init_repo()
        try:
            block = GENERIC_BLOCK.replace("caller_script: scripts/codex-review.sh\n", "")
            head = _commit_fallback(root, block)
            result = _run_checker(root, base_sha=base, head_sha=head)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required fields: caller_script", result.stdout)
        finally:
            raw_ctx.cleanup()

    def test_fails_blank_required_field(self) -> None:
        raw_ctx, root, base = _init_repo()
        try:
            block = GENERIC_BLOCK.replace("primary_model: gpt-5.4", "primary_model: ")
            head = _commit_fallback(root, block)
            result = _run_checker(root, base_sha=base, head_sha=head)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("primary_model must be non-empty", result.stdout)
        finally:
            raw_ctx.cleanup()

    def test_fails_semantically_inconsistent_degraded_metadata(self) -> None:
        raw_ctx, root, base = _init_repo()
        try:
            block = GENERIC_BLOCK.replace(
                "caller_script: scripts/codex-review.sh",
                "caller_script: scripts/codex-review.sh\ncross_family_path_unavailable: true",
            )
            head = _commit_fallback(root, block)
            result = _run_checker(root, base_sha=base, head_sha=head)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("degraded fallback metadata requires fallback_scope", result.stdout)
        finally:
            raw_ctx.cleanup()

    def test_fails_placeholder_cross_family_path_ref(self) -> None:
        raw_ctx, root, base = _init_repo()
        try:
            block = DEGRADED_BLOCK.replace(
                "cross_family_path_ref: docs/codex-reviews/2026-04-30-issue-629-claude.md",
                "cross_family_path_ref: TODO",
            )
            head = _commit_fallback(root, block)
            result = _run_checker(root, base_sha=base, head_sha=head)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("cross_family_path_ref must not use placeholder text", result.stdout)
        finally:
            raw_ctx.cleanup()

    def test_fails_placeholder_primary_model(self) -> None:
        raw_ctx, root, base = _init_repo()
        try:
            block = GENERIC_BLOCK.replace("primary_model: gpt-5.4", "primary_model: TODO")
            head = _commit_fallback(root, block)
            result = _run_checker(root, base_sha=base, head_sha=head)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("primary_model must not use placeholder text", result.stdout)
        finally:
            raw_ctx.cleanup()


if __name__ == "__main__":
    unittest.main()
