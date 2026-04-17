#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))

import packet_queue


REPO_ROOT = Path(__file__).resolve().parents[2]


def _packet(**overrides):
    payload = {
        "packet_id": "aaaaaaaa-0000-4000-a000-000000000229",
        "prior": {
            "tier": 1,
            "role": "architect-codex",
            "model_id": "gpt-5.4",
            "model_family": "openai",
            "timestamp": "2026-04-17T18:00:00Z",
        },
        "next_tier": 2,
        "artifacts": [
            "docs/plans/issue-229-structured-agent-cycle-plan.json",
            "raw/cross-review/2026-04-17-packet-queue.md",
        ],
        "standards_ref": "STANDARDS.md §Society of Minds (SoT)",
        "fallback_ladder_ref": None,
        "governance": {
            "issue_number": 229,
            "structured_plan_ref": "docs/plans/issue-229-structured-agent-cycle-plan.json",
            "execution_scope_ref": "docs/plans/issue-229-packet-queue-pdcar.md",
            "validation_commands": [
                "python3 scripts/orchestrator/test_packet_queue.py",
            ],
            "review_artifacts": [
                "raw/cross-review/2026-04-17-packet-queue.md",
            ],
            "fallback_log_ref": None,
            "pii_mode": "none",
            "dispatch_authorized": True,
        },
    }
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(payload.get(key), dict):
            payload[key].update(value)
        else:
            payload[key] = value
    return payload


class TestPacketQueue(unittest.TestCase):
    def _write_inbound(self, root: Path, payload: dict, name: str = "packet.yml") -> Path:
        inbound = root / "inbound"
        inbound.mkdir(parents=True, exist_ok=True)
        path = inbound / name
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        return path

    def test_valid_packet_dry_run_replays_through_queue_without_moving(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            queue_root = Path(raw)
            packet_path = self._write_inbound(queue_root, _packet())

            transitions = [
                ("inbound", "dispatched"),
                ("dispatched", "review"),
                ("review", "gate"),
                ("gate", "done"),
            ]
            for from_state, to_state in transitions:
                decision = packet_queue.transition_packet(
                    packet_path,
                    from_state,
                    to_state,
                    queue_root=queue_root,
                    repo_root=REPO_ROOT,
                    dry_run=True,
                )
                self.assertTrue(decision.allowed, decision.reason)

            self.assertTrue(packet_path.exists(), "dry-run must not move the packet")
            self.assertFalse((queue_root / "done" / packet_path.name).exists())

            replay = packet_queue.replay_audit(queue_root / "audit.jsonl")
            self.assertEqual(replay["events"], 4)
            self.assertEqual(replay["dry_run_events"], 4)
            self.assertEqual(replay["latest_states"]["aaaaaaaa-0000-4000-a000-000000000229"], "done")

    def test_valid_packet_real_dispatch_moves_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            queue_root = Path(raw)
            packet_path = self._write_inbound(queue_root, _packet())

            decision = packet_queue.transition_packet(
                packet_path,
                "inbound",
                "dispatched",
                queue_root=queue_root,
                repo_root=REPO_ROOT,
                dry_run=False,
            )

            destination = queue_root / "dispatched" / packet_path.name
            self.assertTrue(decision.allowed, decision.reason)
            self.assertEqual(decision.status, "moved")
            self.assertFalse(packet_path.exists())
            self.assertTrue(destination.exists())

    def test_invalid_packet_fails_schema_before_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            queue_root = Path(raw)
            invalid = _packet()
            invalid.pop("packet_id")
            packet_path = self._write_inbound(queue_root, invalid)

            decision = packet_queue.transition_packet(
                packet_path,
                "inbound",
                "dispatched",
                queue_root=queue_root,
                repo_root=REPO_ROOT,
                dry_run=False,
            )

            self.assertFalse(decision.allowed)
            self.assertEqual(decision.status, "refused")
            self.assertIn("schema", decision.reason.lower())
            self.assertTrue(packet_path.exists(), "invalid packet must not move")

    def test_pii_packet_halts_before_non_lam_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            queue_root = Path(raw)
            packet_path = self._write_inbound(
                queue_root,
                _packet(governance={"pii_mode": "detected"}),
            )

            decision = packet_queue.transition_packet(
                packet_path,
                "inbound",
                "dispatched",
                queue_root=queue_root,
                repo_root=REPO_ROOT,
                dry_run=False,
            )

            self.assertFalse(decision.allowed)
            self.assertEqual(decision.status, "halted")
            self.assertIn("requires LAM role", decision.reason)
            self.assertTrue(packet_path.exists())

    def test_repeated_known_failure_context_halts_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            queue_root = Path(raw)
            packet_path = self._write_inbound(
                queue_root,
                _packet(
                    governance={
                        "known_failure_context": [
                            {
                                "title": "stale graph update",
                                "summary": "Repeated stale generated artifact",
                                "source_path": "docs/FAIL_FAST_LOG.md",
                                "evidence_paths": ["docs/FAIL_FAST_LOG.md"],
                                "repeat_count": 2,
                            }
                        ]
                    }
                ),
            )

            decision = packet_queue.transition_packet(
                packet_path,
                "inbound",
                "dispatched",
                queue_root=queue_root,
                repo_root=REPO_ROOT,
                dry_run=False,
            )

            self.assertFalse(decision.allowed)
            self.assertEqual(decision.status, "halted")
            self.assertIn("known failure", decision.reason)

    def test_pii_halt_reason_takes_precedence_over_known_failure_halt(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            queue_root = Path(raw)
            packet_path = self._write_inbound(
                queue_root,
                _packet(
                    governance={
                        "pii_mode": "detected",
                        "known_failure_context": [
                            {
                                "title": "repeated failure",
                                "summary": "Repeated failure",
                                "source_path": "docs/FAIL_FAST_LOG.md",
                                "evidence_paths": ["docs/FAIL_FAST_LOG.md"],
                                "repeat_count": 2,
                            }
                        ],
                    }
                ),
            )

            decision = packet_queue.transition_packet(
                packet_path,
                "inbound",
                "dispatched",
                queue_root=queue_root,
                repo_root=REPO_ROOT,
                dry_run=False,
            )

            self.assertFalse(decision.allowed)
            self.assertEqual(decision.status, "halted")
            self.assertIn("PII mode detected requires LAM role", decision.reason)

    def test_dispatch_requires_approved_issue_backed_plan(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            queue_root = Path(raw)
            packet_path = self._write_inbound(
                queue_root,
                _packet(governance={"structured_plan_ref": "docs/plans/missing-plan.json"}),
            )

            decision = packet_queue.transition_packet(
                packet_path,
                "inbound",
                "dispatched",
                queue_root=queue_root,
                repo_root=REPO_ROOT,
                dry_run=False,
            )

            self.assertFalse(decision.allowed)
            self.assertEqual(decision.status, "refused")
            self.assertIn("structured plan not found", decision.reason)

    def test_dispatch_requires_local_review_artifact_refs_to_exist(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            queue_root = Path(raw)
            packet_path = self._write_inbound(
                queue_root,
                _packet(governance={"review_artifacts": ["raw/cross-review/missing-packet-review.md"]}),
            )

            decision = packet_queue.transition_packet(
                packet_path,
                "inbound",
                "dispatched",
                queue_root=queue_root,
                repo_root=REPO_ROOT,
                dry_run=False,
            )

            self.assertFalse(decision.allowed)
            self.assertEqual(decision.status, "refused")
            self.assertIn("review_artifacts reference not found", decision.reason)

    def test_replay_counts_refused_events_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            queue_root = Path(raw)
            packet_path = self._write_inbound(queue_root, _packet(governance={"dispatch_authorized": False}))
            decision = packet_queue.transition_packet(
                packet_path,
                "inbound",
                "dispatched",
                queue_root=queue_root,
                repo_root=REPO_ROOT,
                dry_run=True,
            )
            self.assertFalse(decision.allowed)

            replay = packet_queue.replay_audit(queue_root / "audit.jsonl")
            self.assertEqual(replay["events"], 1)
            self.assertEqual(replay["refused_events"], 1)
            self.assertEqual(replay["accepted_transitions"], 0)

    def test_dry_run_authorization_does_not_allow_real_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            queue_root = Path(raw)
            packet_path = self._write_inbound(
                queue_root,
                _packet(governance={"dispatch_authorized": False, "dry_run_authorized": True}),
            )
            dry_run_decision = packet_queue.transition_packet(
                packet_path,
                "inbound",
                "dispatched",
                queue_root=queue_root,
                repo_root=REPO_ROOT,
                dry_run=True,
            )
            live_decision = packet_queue.transition_packet(
                packet_path,
                "inbound",
                "dispatched",
                queue_root=queue_root,
                repo_root=REPO_ROOT,
                dry_run=False,
            )

            self.assertTrue(dry_run_decision.allowed, dry_run_decision.reason)
            self.assertFalse(live_decision.allowed)
            self.assertEqual(live_decision.status, "refused")


if __name__ == "__main__":
    unittest.main(verbosity=2)
