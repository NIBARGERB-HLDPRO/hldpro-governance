"""Shared pytest fixtures for governance contract tests.

Fixtures
--------
tmp_git_repo : Path
    A temporary directory initialised as a bare-minimum git repo (no actual
    commits needed — tests manipulate the working tree directly).

sample_cross_review_file : tuple[Path, dict]
    Returns (path, frontmatter_dict) for a synthetic cross-review artifact
    written into the tmp_git_repo.

env_no_pr_context : dict[str, str]
    An environment dict with BASE_SHA and HEAD_SHA set to empty strings,
    simulating a push/stale-ref event where PR context is missing.

env_valid_pr_context : dict[str, str]
    An environment dict with realistic BASE_SHA and HEAD_SHA values.
"""
from __future__ import annotations

import os
import subprocess
import textwrap
from pathlib import Path
from typing import Generator

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content), encoding="utf-8")
    return path


SAMPLE_CROSS_REVIEW_FRONTMATTER = {
    "schema_version": "v2",
    "pr_scope": "architecture",
    "drafter": {"model_id": "claude-opus-4-6", "model_family": "claude"},
    "reviewer": {"model_id": "gpt-5.4", "model_family": "openai"},
    "gate_identity": {"model_id": "claude-sonnet-4-6"},
}

SAMPLE_CROSS_REVIEW_YAML = """\
---
schema_version: v2
pr_scope: architecture
drafter:
  model_id: claude-opus-4-6
  model_family: claude
reviewer:
  model_id: gpt-5.4
  model_family: openai
gate_identity:
  model_id: claude-sonnet-4-6
---

# Cross-review: Test Standards Change

## Summary
Synthetic cross-review artifact for unit tests.
"""


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def tmp_git_repo(tmp_path: Path) -> Generator[Path, None, None]:
    """Yield a temporary directory initialised as a git repo."""
    subprocess.run(
        ["git", "init", "-b", "main", str(tmp_path)],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(tmp_path), "config", "user.email", "test@example.com"],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(tmp_path), "config", "user.name", "Test"],
        check=True,
        capture_output=True,
    )
    # Create a minimal initial commit so git diff works
    readme = tmp_path / "README.md"
    readme.write_text("# test repo\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "README.md"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "commit", "-m", "init"],
        check=True,
        capture_output=True,
    )
    yield tmp_path


@pytest.fixture()
def sample_cross_review_file(tmp_git_repo: Path) -> tuple[Path, dict]:
    """Write a sample cross-review artifact and return (path, frontmatter_dict)."""
    artifact_path = tmp_git_repo / "raw" / "cross-review" / "2026-05-01-test-standards-change.md"
    _write(artifact_path, SAMPLE_CROSS_REVIEW_YAML)
    return artifact_path, SAMPLE_CROSS_REVIEW_FRONTMATTER


@pytest.fixture()
def env_no_pr_context() -> dict[str, str]:
    """Environment variables simulating a push event with no PR context."""
    env = os.environ.copy()
    env["BASE_SHA"] = ""
    env["HEAD_SHA"] = ""
    return env


@pytest.fixture()
def env_valid_pr_context() -> dict[str, str]:
    """Environment variables simulating a valid PR event."""
    env = os.environ.copy()
    env["BASE_SHA"] = "aaaaaaaabbbbbbbbccccccccddddddddeeeeeeee"
    env["HEAD_SHA"] = "1111111122222222333333334444444455555555"
    return env
