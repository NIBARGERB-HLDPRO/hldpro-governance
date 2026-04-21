#!/usr/bin/env python3
"""
Tests for SoM Stage 4 packet validator.
Run: python3 scripts/packet/test_validate.py
"""
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import yaml

# Ensure the script directory is on the path when run from repo root.
sys.path.insert(0, str(Path(__file__).parent))

from validate import (
    validate_dual_planner,
    validate_no_self_approval,
    validate_planning_floor,
    validate_pii_floor,
    validate_packet,
    validate_schema,
    validate_tier_escalation_valid,
    validate_local_family_diversity,
    validate_fallback_logged,
    _run_cli,
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
    role="architect-claude",
    parent_packet_id=None,
    artifacts=None,
    next_tier=2,
    fallback_ladder_ref=None,
    standards_ref="STANDARDS.md §Society of Minds (SoT)",
):
    p = {
        "packet_id": "aaaaaaaa-0000-4000-a000-000000000001",
        "prior": {
            "tier": 1,
            "role": role,
            "model_id": model_id,
            "model_family": model_family,
            "timestamp": "2026-04-14T00:00:00Z",
        },
        "next_tier": next_tier,
        "artifacts": artifacts or [],
        "standards_ref": standards_ref,
    }
    if fallback_ladder_ref is not None:
        p["fallback_ladder_ref"] = fallback_ladder_ref
    if parent_packet_id:
        p["parent_packet_id"] = parent_packet_id
    return p


def _make_parent_packet(model_id="gpt-5.4", model_family="openai", role="architect-claude"):
    return {
        "packet_id": "bbbbbbbb-0000-4000-b000-000000000002",
        "prior": {
            "tier": 1,
            "role": role,
            "model_id": model_id,
            "model_family": model_family,
            "timestamp": "2026-04-14T00:00:00Z",
        },
        "next_tier": 2,
        "standards_ref": "STANDARDS.md §Society of Minds (SoT)",
        "artifacts": [],
    }


# ---------------------------------------------------------------------------
# Tests: validate_dual_planner
# ---------------------------------------------------------------------------


class TestDualPlanner(unittest.TestCase):

    def test_non_tier1_always_passes(self):
        packet = {
            "prior": {
                "tier": 2,
                "role": "worker",
                "model_id": "qwen-coder",
                "model_family": "qwen",
                "timestamp": "2026-04-14T00:00:00Z",
            },
            "next_tier": 3,
            "artifacts": [],
            "standards_ref": "STANDARDS.md §Society of Minds (SoT)",
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
        parent = _make_parent_packet(model_family="anthropic")  # same family

        with tempfile.TemporaryDirectory() as tmpdir:
            pdir = Path(tmpdir)
            parent_file = pdir / f"2026-04-14-{parent_id}.yml"
            parent_file.write_text(yaml.safe_dump(parent))
            passed, reason = validate_dual_planner(packet, packets_dir=pdir)

        self.assertFalse(passed, "Same-family dual-planner should be refused")
        self.assertIsNotNone(reason)
        self.assertIn("cross-family", reason.lower())

    def test_cross_family_dual_planner_passes(self):
        """anthropic + openai is fine."""
        parent_id = "bbbbbbbb-0000-4000-b000-000000000002"
        packet = _tier1_packet(model_family="anthropic", parent_packet_id=parent_id)
        parent = _make_parent_packet(model_family="openai")

        with tempfile.TemporaryDirectory() as tmpdir:
            pdir = Path(tmpdir)
            (pdir / f"2026-04-14-{parent_id}.yml").write_text(yaml.safe_dump(parent))
            passed, reason = validate_dual_planner(packet, packets_dir=pdir)

        self.assertTrue(passed, reason)

    def test_missing_parent_warns_but_does_not_hard_fail(self):
        """Parent file absent → warn, don't refuse."""
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
        shared_model = "claude-sonnet-4-5"
        parent_id = "bbbbbbbb-0000-4000-b000-000000000002"
        packet = _tier1_packet(model_id=shared_model, role="architect-codex", parent_packet_id=parent_id)
        parent = _make_parent_packet(model_id=shared_model, role="architect-claude")

        with tempfile.TemporaryDirectory() as tmpdir:
            pdir = Path(tmpdir)
            (pdir / f"2026-04-14-{parent_id}.yml").write_text(yaml.safe_dump(parent))
            passed, reason = validate_no_self_approval(packet, packets_dir=pdir)

        self.assertFalse(passed)
        self.assertIn("self-approval", reason.lower())

    def test_different_models_same_role_passes(self):
        parent_id = "bbbbbbbb-0000-4000-b000-000000000002"
        packet = _tier1_packet(model_id="claude-sonnet-4-5", role="architect-codex", parent_packet_id=parent_id)
        parent = _make_parent_packet(model_id="gpt-5.4", role="architect-claude")

        with tempfile.TemporaryDirectory() as tmpdir:
            pdir = Path(tmpdir)
            (pdir / f"2026-04-14-{parent_id}.yml").write_text(yaml.safe_dump(parent))
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
            "prior": {
                "tier": 2,
                "model_id": "claude-haiku-4-5",
                "role": "worker",
                "model_family": "anthropic",
                "timestamp": "2026-04-14T00:00:00Z",
            },
            "next_tier": 3,
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
        packet = _tier1_packet(
            role="architect-claude",
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
            role="architect-claude",
            artifacts=["docs/design.md", "src/main.py"],
        )
        passed, _ = validate_pii_floor(packet)
        self.assertTrue(passed)

    def test_missing_pii_patterns_file_hard_fails(self):
        """When pii-patterns.yml is absent, validator must refuse (not silently pass)."""
        with patch("validate.PII_PATTERNS_PATH", Path("/nonexistent/pii-patterns.yml")):
            with patch("validate._COMPILED_PII_PATTERNS", []):
                packet = _tier1_packet(role="architect-claude", artifacts=[])
                passed, reason = validate_pii_floor(packet)
        self.assertFalse(passed)
        self.assertIn("unenforceable", reason.lower())


# ---------------------------------------------------------------------------
# Tests: validate_schema
# ---------------------------------------------------------------------------


class TestSchema(unittest.TestCase):

    def test_schema_rejects_missing_required_field(self):
        packet = _tier1_packet()
        del packet["standards_ref"]
        passed, reason = validate_schema(packet)
        self.assertFalse(passed)
        self.assertIn("schema validation failed", reason.lower())

    def test_schema_accepts_minimal_valid_packet(self):
        packet = _tier1_packet()
        passed, reason = validate_schema(packet)
        self.assertTrue(passed)
        self.assertIsNone(reason)


# ---------------------------------------------------------------------------
# Tests: validate_tier_escalation_valid
# ---------------------------------------------------------------------------


class TestTierEscalation(unittest.TestCase):

    def test_valid_escalation_passes(self):
        packet = _tier1_packet(next_tier=2)
        passed, reason = validate_tier_escalation_valid(packet)
        self.assertTrue(passed, reason)

    def test_invalid_escalation_refused(self):
        packet = _tier1_packet(next_tier=3)
        passed, reason = validate_tier_escalation_valid(packet)
        self.assertFalse(passed)
        self.assertIn("expected", reason.lower())


# ---------------------------------------------------------------------------
# Tests: validate_local_family_diversity
# ---------------------------------------------------------------------------


class TestLocalFamilyDiversity(unittest.TestCase):

    def test_same_family_lam_chain_refused(self):
        parent_id = "bbbbbbbb-0000-4000-b000-000000000002"
        packet = _tier1_packet(role="worker-lam", model_family="qwen", parent_packet_id=parent_id)
        parent = _make_parent_packet(model_id="gpt-5.3-codex-spark", model_family="qwen", role="critic-lam")

        with tempfile.TemporaryDirectory() as tmpdir:
            pdir = Path(tmpdir)
            (pdir / f"2026-04-14-{parent_id}.yml").write_text(yaml.safe_dump(parent))
            passed, reason = validate_local_family_diversity(packet, packets_dir=pdir)

        self.assertFalse(passed)
        self.assertIn("local family diversity", reason.lower())

    def test_different_family_lam_chain_passes(self):
        parent_id = "bbbbbbbb-0000-4000-b000-000000000002"
        packet = _tier1_packet(role="worker-lam", model_family="qwen", parent_packet_id=parent_id)
        parent = _make_parent_packet(model_id="gpt-5.3-codex-spark", model_family="anthropic", role="critic-lam")

        with tempfile.TemporaryDirectory() as tmpdir:
            pdir = Path(tmpdir)
            (pdir / f"2026-04-14-{parent_id}.yml").write_text(yaml.safe_dump(parent))
            passed, reason = validate_local_family_diversity(packet, packets_dir=pdir)

        self.assertTrue(passed, reason)


# ---------------------------------------------------------------------------
# Tests: validate_fallback_logged
# ---------------------------------------------------------------------------


class TestFallbackLogged(unittest.TestCase):

    def test_missing_fallback_reference_passes(self):
        packet = _tier1_packet()
        passed, reason = validate_fallback_logged(packet)
        self.assertTrue(passed, reason)

    def test_nonexistent_fallback_reference_refused(self):
        packet = _tier1_packet(fallback_ladder_ref="raw/model-fallbacks/2026-04-14.md")
        with patch("validate.FALLBACK_LOG_DIR", Path("/tmp/does-not-exist-for-validator-tests")):
            passed, reason = validate_fallback_logged(packet)
        self.assertFalse(passed)
        self.assertIn("fallback log", reason.lower())

    def test_fallback_reference_outside_allowed_directory_refused(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_dir = Path(tmpdir)
            fallback_dir = tmp_dir / "raw" / "model-fallbacks"
            fallback_dir.mkdir(parents=True)
            fallback_file = tmp_dir / "not-fallback.md"
            fallback_file.write_text("placeholder")
            with patch("validate.FALLBACK_LOG_DIR", fallback_dir):
                packet = _tier1_packet(fallback_ladder_ref=str(fallback_file))
                passed, reason = validate_fallback_logged(packet)
        self.assertFalse(passed)
        self.assertIn("fallback logs must live", reason.lower())

    def test_fallback_reference_in_model_fallbacks_passes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_dir = Path(tmpdir)
            fallback_dir = tmp_dir / "raw" / "model-fallbacks"
            fallback_dir.mkdir(parents=True)
            fallback_file = fallback_dir / "2026-04-14.md"
            fallback_file.write_text("placeholder")
            with patch("validate.FALLBACK_LOG_DIR", fallback_dir):
                packet = _tier1_packet(fallback_ladder_ref=str(fallback_file))
                passed, reason = validate_fallback_logged(packet)
                self.assertTrue(passed, reason)
                self.assertEqual(packet["fallback_ladder_ref"], str(fallback_file))


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

    def test_invalid_tier_escalation_surfaces_in_failures(self):
        packet = _tier1_packet(model_id="claude-sonnet-4-5", next_tier=3)
        passed, failures = validate_packet(packet)
        self.assertFalse(passed)
        self.assertTrue(any("tier escalation" in f.lower() for f in failures))


# ---------------------------------------------------------------------------
# Tests: CLI
# ---------------------------------------------------------------------------


class TestCli(unittest.TestCase):

    def test_cli_success_json(self):
        packet = _tier1_packet(model_id="claude-sonnet-4-5", next_tier=2)
        with tempfile.TemporaryDirectory() as tmpdir:
            packet_file = Path(tmpdir) / "packet.yml"
            packet_file.write_text(yaml.safe_dump(packet))
            output = StringIO()
            with redirect_stdout(output):
                code = _run_cli([str(packet_file), "--json"])

        data = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(data["status"], "ok")


# ---------------------------------------------------------------------------
# Tests: dispatch-ready packets (governance block in schema)
# ---------------------------------------------------------------------------


def _dispatch_packet(**gov_overrides):
    """Return a schema-valid dispatch-ready packet with a full governance block."""
    gov = {
        "issue_number": 437,
        "structured_plan_ref": "docs/plans/issue-437-structured-agent-cycle-plan.json",
        "execution_scope_ref": None,
        "validation_commands": ["python3 scripts/packet/test_validate.py"],
        "review_artifacts": ["raw/cross-review/2026-04-21-packet-dispatch-reconcile.md"],
        "fallback_log_ref": None,
        "pii_mode": "none",
        "dispatch_authorized": True,
    }
    gov.update(gov_overrides)
    p = _tier1_packet()
    p["governance"] = gov
    return p


class TestDispatchPacketSchema(unittest.TestCase):

    def test_full_governance_block_passes_schema(self):
        packet = _dispatch_packet()
        passed, reason = validate_schema(packet)
        self.assertTrue(passed, reason)

    def test_minimal_packet_without_governance_still_passes_schema(self):
        """Historical compatibility: governance is optional in the schema."""
        packet = _tier1_packet()
        self.assertNotIn("governance", packet)
        passed, reason = validate_schema(packet)
        self.assertTrue(passed, reason)

    def test_governance_missing_required_field_fails_schema(self):
        """Incomplete governance block must fail schema validation."""
        packet = _dispatch_packet()
        del packet["governance"]["issue_number"]
        passed, reason = validate_schema(packet)
        self.assertFalse(passed)
        self.assertIn("schema validation failed", reason.lower())

    def test_governance_pii_mode_invalid_value_fails_schema(self):
        packet = _dispatch_packet(pii_mode="unknown_mode")
        passed, reason = validate_schema(packet)
        self.assertFalse(passed)
        self.assertIn("schema validation failed", reason.lower())

    def test_governance_empty_validation_commands_fails_schema(self):
        packet = _dispatch_packet(validation_commands=[])
        passed, reason = validate_schema(packet)
        self.assertFalse(passed)
        self.assertIn("schema validation failed", reason.lower())

    def test_governance_empty_review_artifacts_fails_schema(self):
        packet = _dispatch_packet(review_artifacts=[])
        passed, reason = validate_schema(packet)
        self.assertFalse(passed)
        self.assertIn("schema validation failed", reason.lower())

    def test_validate_packet_passes_with_full_governance(self):
        packet = _dispatch_packet()
        passed, failures = validate_packet(packet)
        self.assertTrue(passed, failures)

    def test_governance_extra_field_rejected_by_schema(self):
        """additionalProperties: false on governance block must reject unknown keys."""
        packet = _dispatch_packet()
        packet["governance"]["unexpected_field"] = "value"
        passed, reason = validate_schema(packet)
        self.assertFalse(passed)
        self.assertIn("schema validation failed", reason.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
