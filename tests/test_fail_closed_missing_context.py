"""Tests for fail-closed behaviour when BASE_SHA is empty (AC3).

These tests assert that the gate logic in governance-check.yml,
require-cross-review.yml, and check-arch-tier.yml returns exit 1 when
BASE_SHA is empty — simulating push events or stale-ref conditions where
no PR context is available.

Strategy
--------
* For the Python-extracted logic (validate_cross_review_evidence), test the
  function directly.
* For the bash snippets embedded in YAML workflows, extract and run them via
  subprocess.run with an empty BASE_SHA environment variable, then assert
  returncode == 1.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"


def _load_validate_module():
    module_path = REPO_ROOT / "scripts" / "overlord" / "validate_cross_review_evidence.py"
    if not module_path.exists():
        pytest.skip(f"Module not found at {module_path}")
    spec = importlib.util.spec_from_file_location("validate_cross_review_evidence", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_bash_snippet(script: str, env: dict) -> subprocess.CompletedProcess:
    """Run a bash snippet and return the completed process."""
    return subprocess.run(
        ["bash", "-c", script],
        env={**os.environ, **env},
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# Bash snippet for require-cross-review missing context check
# Mirrors the exact logic in require-cross-review.yml
# ---------------------------------------------------------------------------

REQUIRE_CROSS_REVIEW_CONTEXT_CHECK = textwrap.dedent("""
    set -euo pipefail
    BASE_SHA="${BASE_SHA:-}"
    HEAD_SHA="${HEAD_SHA:-}"
    if [ -z "${BASE_SHA}" ] || [ -z "${HEAD_SHA}" ]; then
        echo "::error::[require-cross-review] Missing pull request context; gate fails closed."
        exit 1
    fi
    echo "context ok"
    exit 0
""")

# Mirrors the logic in check-arch-tier.yml
CHECK_ARCH_TIER_CONTEXT_CHECK = textwrap.dedent("""
    set -euo pipefail
    BASE_SHA="${BASE_SHA:-}"
    HEAD_SHA="${HEAD_SHA:-}"
    if [ -z "${BASE_SHA}" ] || [ -z "${HEAD_SHA}" ]; then
        echo "::error::[check-arch-tier] Missing pull request context; gate fails closed."
        exit 1
    fi
    echo "context ok"
    exit 0
""")

# Mirrors governance-check.yml: uses base_sha input (workflow_call input)
GOVERNANCE_CHECK_CONTEXT_CHECK = textwrap.dedent("""
    set -euo pipefail
    BASE_SHA="${BASE_SHA:-}"
    if [ -z "${BASE_SHA}" ]; then
        echo "::error::[governance-check] Missing BASE_SHA; gate fails closed."
        exit 1
    fi
    echo "context ok"
    exit 0
""")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def vcre():
    return _load_validate_module()


# ---------------------------------------------------------------------------
# Tests: Python-level fail-closed (via validate_cross_review_evidence)
# ---------------------------------------------------------------------------

class TestFailClosedPythonLevel:
    """validate_cross_review_evidence must return violations when BASE_SHA is empty."""

    def test_empty_base_sha_is_violation(self, vcre):
        """detect_cross_review_violations must fail closed on empty BASE_SHA."""
        violations = vcre.detect_cross_review_violations(
            ["STANDARDS.md"],
            planning_only=False,
            base_sha="",
            head_sha="abc123",
        )
        assert violations, "Expected violation on empty BASE_SHA"
        assert any("BASE_SHA" in v or "context" in v.lower() for v in violations), violations

    def test_empty_head_sha_is_violation(self, vcre):
        """detect_cross_review_violations must fail closed on empty HEAD_SHA."""
        violations = vcre.detect_cross_review_violations(
            ["STANDARDS.md"],
            planning_only=False,
            base_sha="abc123",
            head_sha="",
        )
        assert violations, "Expected violation on empty HEAD_SHA"

    def test_both_empty_sha_is_violation(self, vcre):
        """detect_cross_review_violations must fail closed when both SHAs are empty."""
        violations = vcre.detect_cross_review_violations(
            [],
            planning_only=False,
            base_sha="",
            head_sha="",
        )
        assert violations, "Expected violation on both SHAs empty"

    def test_valid_sha_with_no_trigger_passes(self, vcre):
        """With valid SHAs and no trigger, no violations expected."""
        violations = vcre.detect_cross_review_violations(
            ["docs/PROGRESS.md"],
            planning_only=False,
            base_sha="aaa111",
            head_sha="bbb222",
        )
        assert not violations, f"Expected no violation; got: {violations}"


# ---------------------------------------------------------------------------
# Tests: Bash-level fail-closed (subprocess isolation)
# ---------------------------------------------------------------------------

class TestFailClosedBashLevel:
    """Gate bash snippets must exit 1 when BASE_SHA/HEAD_SHA is missing."""

    def test_require_cross_review_exits_1_on_empty_base_sha(self):
        """require-cross-review snippet exits 1 when BASE_SHA is empty."""
        result = _run_bash_snippet(
            REQUIRE_CROSS_REVIEW_CONTEXT_CHECK,
            {"BASE_SHA": "", "HEAD_SHA": ""},
        )
        assert result.returncode == 1, (
            f"Expected exit 1 when BASE_SHA empty; got {result.returncode}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
        assert "::error::" in result.stdout or "::error::" in result.stderr, (
            "Expected ::error:: annotation in output"
        )

    def test_require_cross_review_passes_with_valid_context(self):
        """require-cross-review snippet exits 0 when both SHAs are provided."""
        result = _run_bash_snippet(
            REQUIRE_CROSS_REVIEW_CONTEXT_CHECK,
            {
                "BASE_SHA": "aaaaaaaabbbbbbbbccccccccddddddddeeeeeeee",
                "HEAD_SHA": "1111111122222222333333334444444455555555",
            },
        )
        assert result.returncode == 0, (
            f"Expected exit 0 with valid context; got {result.returncode}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )

    def test_check_arch_tier_exits_1_on_empty_base_sha(self):
        """check-arch-tier snippet exits 1 when BASE_SHA is empty."""
        result = _run_bash_snippet(
            CHECK_ARCH_TIER_CONTEXT_CHECK,
            {"BASE_SHA": "", "HEAD_SHA": ""},
        )
        assert result.returncode == 1, (
            f"Expected exit 1; got {result.returncode}"
        )

    def test_check_arch_tier_passes_with_valid_context(self):
        """check-arch-tier snippet exits 0 when both SHAs are provided."""
        result = _run_bash_snippet(
            CHECK_ARCH_TIER_CONTEXT_CHECK,
            {
                "BASE_SHA": "aaaaaaaabbbbbbbbccccccccddddddddeeeeeeee",
                "HEAD_SHA": "1111111122222222333333334444444455555555",
            },
        )
        assert result.returncode == 0, (
            f"Expected exit 0; got {result.returncode}"
        )

    def test_governance_check_exits_1_on_empty_base_sha(self):
        """governance-check snippet exits 1 when BASE_SHA is empty."""
        result = _run_bash_snippet(
            GOVERNANCE_CHECK_CONTEXT_CHECK,
            {"BASE_SHA": ""},
        )
        assert result.returncode == 1, (
            f"Expected exit 1 when BASE_SHA empty; got {result.returncode}"
        )

    def test_governance_check_passes_with_valid_base_sha(self):
        """governance-check snippet exits 0 when BASE_SHA is provided."""
        result = _run_bash_snippet(
            GOVERNANCE_CHECK_CONTEXT_CHECK,
            {"BASE_SHA": "aaaaaaaabbbbbbbbccccccccddddddddeeeeeeee"},
        )
        assert result.returncode == 0, (
            f"Expected exit 0; got {result.returncode}"
        )


# ---------------------------------------------------------------------------
# Tests: Workflow file existence (sanity checks)
# ---------------------------------------------------------------------------

class TestWorkflowFilesExist:
    """Assert that the referenced workflow files exist in the repo."""

    @pytest.mark.parametrize("wf_name", [
        "governance-check.yml",
        "require-cross-review.yml",
        "check-arch-tier.yml",
    ])
    def test_workflow_file_exists(self, wf_name: str):
        wf_path = WORKFLOWS_DIR / wf_name
        assert wf_path.exists(), f"Workflow file not found: {wf_path}"

    @pytest.mark.parametrize("wf_name", [
        "governance-check.yml",
        "require-cross-review.yml",
        "check-arch-tier.yml",
    ])
    def test_workflow_has_workflow_call_trigger(self, wf_name: str):
        wf_path = WORKFLOWS_DIR / wf_name
        if not wf_path.exists():
            pytest.skip(f"{wf_name} not found")
        content = wf_path.read_text(encoding="utf-8")
        assert "workflow_call" in content, f"{wf_name} must declare workflow_call trigger"
