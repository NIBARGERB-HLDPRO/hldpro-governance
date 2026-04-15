#!/usr/bin/env python3
"""
Tests for SoM Stage 4 packet validator.
Run: python3 scripts/packet/test_validate.py
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure the script directory is on the path when run from repo root
sys.path.insert(0, str(Path(__file__).parent))

from validate import (
    validate_dual_planner,
    validate_no_self_approval,
    validate_planning_floor,
    validate_pii_floor,
    validate_packet,
    WEAK_TIER1_MODELS,
    WEAK_CODEX_MODELS,
    PII_PATTERNS_PATH,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tier1_packet(
    model_id="claude-sonnet-4-5",
    model_family="anthropic",
    role="planner",
    parent_packet_id=None,
    artifacts=None,
):
    p = {
        "packet_id": "aaaaaaaa-0000-4000-a000-000000000001",
        "prior": {
            "tier": 1,
            "role": role,
            "model_id": model_id,
            "model_family": model_family,
        },
        "next_tier": 2,
        "artifacts": artifacts or [],
    }
    if parent_packet_id:
        p["parent_packet_id"] = parent_packet_id
    return p


def _make_parent_packet(model_id="gpt-5.4", model_family="openai", role="planner"):
    return {
        "packet_id": "bbbbbbbb-0000-4000-b000-000000000002",
        "prior": {
            "tier": 1,
            "role": role,
            "model_id": model_id,
            "model_family": model_family,
        },
        "next_tier": 2,
        "artifacts": [],
    }


# ---------------------------------------------------------------------------
# Tests: validate_dual_planner
# ---------------------------------------------------------------------------

class TestDualPlanner(unittest.TestCase):

    def test_non_tier1_always_passes(self):
        packet = {
            "prior": {"tier": 2, "role": "worker", "model_id": "qwen-coder", "model_family": "qwen"},
            "artifacts": [],
        }
        passed, reason = validate_dual_planner(packet)
        self.assertTrue(passed)

    def test_tier1_without_parent_passes(self):
        packet = _tier1_packet()
        passed, reason = validate_dual_planner(packet)
        self.assertTrue(passed)

    def test_same_family_dual_planner_refused(self):
        """Cross-family independence violated: both planners are anthropic."""
        parent_id = "bbbbbbbb-0000-4000-b000-000000000002"
        packet = _tier1_packet(
            model_family="anthropic",
            parent_packet_id=parent_id,
        )
        parent = _make_parent_packet(model_family="anthropic")  # same family!

        import tempfile, yaml, os
        with tempfile.TemporaryDirectory() as tmpdir:
            pdir = Path(tmpdir)
            parent_file = pdir / f"2026-04-14-{parent_id}.yml"
            parent_file.write_text(yaml.dump(parent))

            passed, reason = validate_dual_planner(packet, packets_dir=pdir)

        self.assertFalse(passed, "Same-family dual-planner should be refused")
        self.assertIsNotNone(reason)
        self.assertIn("cross-family", reason.lower())

    def test_cross_family_dual_planner_passes(self):
        """anthropic + openai is fine."""
        parent_id = "bbbbbbbb-0000-4000-b000-000000000002"
        packet = _tier1_packet(model_family="anthropic", parent_packet_id=parent_id)
        parent = _make_parent_packet(model_family="openai")

        import tempfile, yaml
        with tempfile.TemporaryDirectory() as tmpdir:
            pdir = Path(tmpdir)
            (pdir / f"2026-04-14-{parent_id}.yml").write_text(yaml.dump(parent))
            passed, reason = validate_dual_planner(packet, packets_dir=pdir)

        self.assertTrue(passed, reason)

    def test_missing_parent_warns_but_does_not_hard_fail(self):
        """Parent file absent → warn, don't refuse."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            packet = _tier1_packet(parent_packet_id="cccccccc-0000-4000-c000-000000000003")
            passed, reason = validate_dual_planner(packet, packets_dir=Path(tmpdir))
        self.assertTrue(passed)
        self.assertIsNotNone(reason)


# ---------------------------------------------------------------------------
# Tests: validate_no_self_approval
# ---------------------------------------------------------------------------

class TestNoSelfApproval(unittest.TestCase):

    def test_no_parent_passes(self):
        packet = _tier1_packet()
        passed, _ = validate_no_self_approval(packet)
        self.assertTrue(passed)

    def test_same_model_different_roles_refused(self):
        """Same model_id appearing as both planner and reviewer in the chain."""
        import tempfile, yaml
        shared_model = "claude-sonnet-4-5"
        parent_id = "bbbbbbbb-0000-4000-b000-000000000002"
        packet = _tier1_packet(model_id=shared_model, role="reviewer", parent_packet_id=parent_id)
        parent = _make_parent_packet(model_id=shared_model, role="planner")

        with tempfile.TemporaryDirectory() as tmpdir:
            pdir = Path(tmpdir)
            (pdir / f"2026-04-14-{parent_id}.yml").write_text(yaml.dump(parent))
            passed, reason = validate_no_self_approval(packet, packets_dir=pdir)

        self.assertFalse(passed)
        self.assertIn("self-approval", reason.lower())

    def test_different_models_same_role_passes(self):
        import tempfile, yaml
        parent_id = "bbbbbbbb-0000-4000-b000-000000000002"
        packet = _tier1_packet(model_id="claude-sonnet-4-5", role="reviewer", parent_packet_id=parent_id)
        parent = _make_parent_packet(model_id="gpt-5.4", role="planner")

        with tempfile.TemporaryDirectory() as tmpdir:
            pdir = Path(tmpdir)
            (pdir / f"2026-04-14-{parent_id}.yml").write_text(yaml.dump(parent))
            passed, _ = validate_no_self_approval(packet, packets_dir=pdir)

        self.assertTrue(passed)


# ---------------------------------------------------------------------------
# Tests: validate_planning_floor
# ---------------------------------------------------------------------------

class TestPlanningFloor(unittest.TestCase):

    def test_weak_tier1_model_refused(self):
        for model in list(WEAK_TIER1_MODELS)[:2]:
            packet = _tier1_packet(model_id=model)
            passed, reason = validate_planning_floor(packet)
            self.assertFalse(passed, f"{model} should be refused")
            self.assertIn("planning floor", reason.lower())

    def test_weak_codex_model_refused(self):
        for model in list(WEAK_CODEX_MODELS)[:2]:
            packet = _tier1_packet(model_id=model)
            passed, reason = validate_planning_floor(packet)
            self.assertFalse(passed, f"{model} should be refused")

    def test_strong_models_pass(self):
        for model in ["claude-sonnet-4-5", "gpt-5.4", "gpt-5.3-codex-spark"]:
            packet = _tier1_packet(model_id=model)
            passed, _ = validate_planning_floor(packet)
            self.assertTrue(passed, f"{model} should pass planning floor")

    def test_non_tier1_always_passes(self):
        packet = {
            "prior": {"tier": 2, "model_id": "claude-haiku-4-5", "role": "worker", "model_family": "anthropic"},
            "artifacts": [],
        }
        passed, _ = validate_planning_floor(packet)
        self.assertTrue(passed)


# ---------------------------------------------------------------------------
# Tests: validate_pii_floor
# ---------------------------------------------------------------------------

class TestPiiFloor(unittest.TestCase):

    def test_pii_patterns_file_exists(self):
        """Sanity: the patterns file should be present in this worktree."""
        self.assertTrue(PII_PATTERNS_PATH.exists(), f"Missing {PII_PATTERNS_PATH}")

    def test_pii_artifact_without_lam_role_refused(self):
        """Non-LAM role with PII artifact path must be refused."""
        # SSN-matching artifact path
        packet = _tier1_packet(
            role="planner",  # NOT in _LAM_ROLES
            artifacts=["patient-records/ssn-123-45-6789.json"],
        )
        passed, reason = validate_pii_floor(packet)
        self.assertFalse(passed, "Non-LAM role with PII artifact should be refused")
        self.assertIsNotNone(reason)
        self.assertIn("PII", reason)

    def test_pii_artifact_with_lam_role_passes(self):
        """worker-lam role is allowed to handle PII artifacts."""
        packet = _tier1_packet(
            role="worker-lam",
            artifacts=["patient-records/ssn-123-45-6789.json"],
        )
        passed, _ = validate_pii_floor(packet)
        self.assertTrue(passed)

    def test_no_pii_artifact_passes(self):
        packet = _tier1_packet(
            role="planner",
            artifacts=["docs/design.md", "src/main.py"],
        )
        passed, _ = validate_pii_floor(packet)
        self.assertTrue(passed)

    def test_missing_pii_patterns_file_hard_fails(self):
        """When pii-patterns.yml is absent, validator must refuse (not silently pass)."""
        with patch("validate.PII_PATTERNS_PATH", Path("/nonexistent/pii-patterns.yml")):
            with patch("validate._COMPILED_PII_PATTERNS", []):
                packet = _tier1_packet(role="planner", artifacts=[])
                passed, reason = validate_pii_floor(packet)
        self.assertFalse(passed)
        self.assertIn("unenforceable", reason.lower())


# ---------------------------------------------------------------------------
# Tests: validate_packet (integration)
# ---------------------------------------------------------------------------

class TestValidatePacket(unittest.TestCase):

    def test_clean_packet_passes_all(self):
        packet = _tier1_packet(model_id="claude-sonnet-4-5", artifacts=["docs/spec.md"])
        passed, failures = validate_packet(packet)
        self.assertTrue(passed, failures)
        self.assertEqual(failures, [])

    def test_weak_model_surfaces_in_failures(self):
        packet = _tier1_packet(model_id="claude-haiku-4-5")
        passed, failures = validate_packet(packet)
        self.assertFalse(passed)
        self.assertTrue(any("planning floor" in f.lower() for f in failures))


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
