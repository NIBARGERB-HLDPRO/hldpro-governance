from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml
try:
    from scripts.packet.run_specialist_packet import run_specialist_packet
    from scripts.packet.validate import validate_packet
except ModuleNotFoundError as exc:  # pragma: no cover - dependency-gated local env
    if exc.name != "jsonschema":
        raise
    run_specialist_packet = None
    validate_packet = None


def _packet() -> dict:
    return {
        "packet_id": "11111111-1111-4111-8111-111111111111",
        "prior": {
            "tier": 1,
            "role": "architect-codex",
            "model_id": "gpt-5.4",
            "model_family": "openai",
            "timestamp": "2026-04-29T00:00:00Z",
        },
        "next_tier": 2,
        "standards_ref": "STANDARDS.md §Society of Minds (SoT)",
        "artifacts": ["docs/plans/example.json"],
        "governance": {
            "issue_number": 587,
            "structured_plan_ref": "docs/plans/issue-587-rollout-blockers-structured-agent-cycle-plan.json",
            "execution_scope_ref": None,
            "validation_commands": ["python3 scripts/packet/test_validate.py"],
            "review_artifacts": ["raw/cross-review/example.md"],
            "fallback_log_ref": None,
            "pii_mode": "none",
            "dispatch_authorized": True,
        },
    }


@unittest.skipIf(run_specialist_packet is None, "jsonschema dependency not installed")
class RunSpecialistPacketTests(unittest.TestCase):
    def test_dry_run_emits_structured_result_and_outbound_packet(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            packet_path = root / "packet.yml"
            packet_path.write_text(yaml.safe_dump(_packet(), sort_keys=False), encoding="utf-8")
            out_dir = root / "outbound"
            result_path, outbound_path = run_specialist_packet(
                packet_path=packet_path,
                persona_id="gov-specialist-qa",
                output_root=out_dir,
                dry_run=True,
            )
            result = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(result["schema_version"], "governance-specialist-output.v1")
            self.assertEqual(result["specialist_role"], "gov-specialist-qa")
            outbound = yaml.safe_load(outbound_path.read_text(encoding="utf-8"))
            self.assertEqual(outbound["parent_packet_id"], _packet()["packet_id"])
            self.assertIn("governance", outbound)
            self.assertEqual(outbound["prior"]["tier"], _packet()["next_tier"])
            self.assertEqual(outbound["next_tier"], _packet()["next_tier"] + 1)
            passed, failures = validate_packet(outbound)
            self.assertTrue(passed, failures)


if __name__ == "__main__":
    unittest.main(verbosity=2)
