"""Tests for cross-review evidence validation (AC2).

These tests verify that a PR introducing a new ``raw/cross-review/`` file
without ``PLANNING_ONLY=true`` fails the gate logic — and that the inverse
cases pass cleanly.

The detection logic under test lives in
``scripts/overlord/validate_cross_review_evidence.py``.
"""
from __future__ import annotations

import importlib.util
import sys
import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Import the module under test from the scripts/overlord directory.
# We use importlib so the test works regardless of sys.path configuration.
# ---------------------------------------------------------------------------

def _load_module():
    """Load validate_cross_review_evidence from the repo scripts directory."""
    repo_root = Path(__file__).parent.parent
    module_path = repo_root / "scripts" / "overlord" / "validate_cross_review_evidence.py"
    if not module_path.exists():
        pytest.skip(f"Module not found at {module_path}")
    spec = importlib.util.spec_from_file_location("validate_cross_review_evidence", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def vcre():
    return _load_module()


# ---------------------------------------------------------------------------
# Helper constants
# ---------------------------------------------------------------------------

VALID_BASE = "aaaaaaaabbbbbbbbccccccccddddddddeeeeeeee"
VALID_HEAD = "1111111122222222333333334444444455555555"

STANDARDS_CHANGE = ["STANDARDS.md"]
CROSS_REVIEW_FILE = ["raw/cross-review/2026-05-01-test-review.md"]
AGENT_CHANGE = ["agents/overlord.md"]
HOOK_CHANGE = ["hooks/governance-check.sh"]
PLAIN_FILE = ["docs/PROGRESS.md"]


# ---------------------------------------------------------------------------
# Tests: fail-closed when PLANNING_ONLY is not set
# ---------------------------------------------------------------------------

class TestCrossReviewViolations:
    """A PR that introduces raw/cross-review/* without PLANNING_ONLY must fail."""

    def test_new_cross_review_without_planning_only_fails(self, vcre):
        """Introducing a cross-review artifact without PLANNING_ONLY=true is a violation."""
        diff = STANDARDS_CHANGE + CROSS_REVIEW_FILE
        violations = vcre.detect_cross_review_violations(
            diff,
            planning_only=False,
            base_sha=VALID_BASE,
            head_sha=VALID_HEAD,
        )
        assert violations, "Expected at least one violation"
        assert any("PLANNING_ONLY" in v for v in violations), (
            f"Violation should mention PLANNING_ONLY; got: {violations}"
        )

    def test_new_cross_review_with_planning_only_passes(self, vcre):
        """When PLANNING_ONLY=true is set by the caller, trusted-base rule is relaxed."""
        diff = STANDARDS_CHANGE + CROSS_REVIEW_FILE
        violations = vcre.detect_cross_review_violations(
            diff,
            planning_only=True,
            base_sha=VALID_BASE,
            head_sha=VALID_HEAD,
        )
        assert not violations, f"Expected no violations with PLANNING_ONLY; got: {violations}"

    def test_trigger_without_evidence_fails(self, vcre):
        """A trigger file (STANDARDS.md) without any cross-review artifact must fail."""
        diff = STANDARDS_CHANGE  # no raw/cross-review/ file
        violations = vcre.detect_cross_review_violations(
            diff,
            planning_only=False,
            base_sha=VALID_BASE,
            head_sha=VALID_HEAD,
        )
        assert violations, "Expected violation: trigger hit but no evidence"
        assert any("raw/cross-review" in v for v in violations), violations

    def test_agent_change_triggers_enforcement(self, vcre):
        """Changes to agents/*.md must trigger cross-review enforcement."""
        diff = AGENT_CHANGE
        violations = vcre.detect_cross_review_violations(
            diff,
            planning_only=False,
            base_sha=VALID_BASE,
            head_sha=VALID_HEAD,
        )
        # Agent change triggers but no evidence present → violation
        assert violations, f"Agent change should trigger enforcement; got no violations"

    def test_hook_change_triggers_enforcement(self, vcre):
        """Changes to hooks/*.sh must trigger cross-review enforcement."""
        diff = HOOK_CHANGE
        violations = vcre.detect_cross_review_violations(
            diff,
            planning_only=False,
            base_sha=VALID_BASE,
            head_sha=VALID_HEAD,
        )
        assert violations, f"Hook change should trigger enforcement; got no violations"

    def test_non_trigger_file_passes_without_evidence(self, vcre):
        """A plain file change (docs/PROGRESS.md) should not trigger enforcement."""
        diff = PLAIN_FILE
        violations = vcre.detect_cross_review_violations(
            diff,
            planning_only=False,
            base_sha=VALID_BASE,
            head_sha=VALID_HEAD,
        )
        assert not violations, f"Non-trigger file should pass; got: {violations}"

    def test_empty_diff_passes(self, vcre):
        """An empty diff should pass without violations."""
        violations = vcre.detect_cross_review_violations(
            [],
            planning_only=False,
            base_sha=VALID_BASE,
            head_sha=VALID_HEAD,
        )
        assert not violations, f"Empty diff should pass; got: {violations}"

    def test_check_ci_workflow_triggers_enforcement(self, vcre):
        """Changes to .github/workflows/check-*.yml must trigger enforcement."""
        diff = [".github/workflows/check-arch-tier.yml"]
        violations = vcre.detect_cross_review_violations(
            diff,
            planning_only=False,
            base_sha=VALID_BASE,
            head_sha=VALID_HEAD,
        )
        assert violations, "check-*.yml change should trigger enforcement"

    def test_agent_registry_change_triggers_enforcement(self, vcre):
        """Changes to AGENT_REGISTRY.md must trigger enforcement."""
        diff = ["AGENT_REGISTRY.md"]
        violations = vcre.detect_cross_review_violations(
            diff,
            planning_only=False,
            base_sha=VALID_BASE,
            head_sha=VALID_HEAD,
        )
        assert violations, "AGENT_REGISTRY.md change should trigger enforcement"
