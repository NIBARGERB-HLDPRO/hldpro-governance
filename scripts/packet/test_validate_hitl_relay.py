#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))

from validate_hitl_relay import validate_hitl_packet  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = REPO_ROOT / "docs" / "schemas" / "examples" / "hitl-relay"


def _load(name: str) -> dict:
    return json.loads((EXAMPLES / "valid" / name).read_text(encoding="utf-8"))


def test_valid_examples_pass_policy_validation() -> None:
    for path in sorted((EXAMPLES / "valid").glob("*.json")):
        packet = json.loads(path.read_text(encoding="utf-8"))
        passed, failures = validate_hitl_packet(packet)
        assert passed, f"{path} failed: {failures}"


def test_invalid_examples_fail_policy_validation() -> None:
    for path in sorted((EXAMPLES / "invalid").glob("*.json")):
        packet = json.loads(path.read_text(encoding="utf-8"))
        passed, failures = validate_hitl_packet(packet)
        assert not passed, f"{path} unexpectedly passed"
        assert failures


def test_session_instruction_requires_matching_target_session() -> None:
    packet = _load("session-instruction.json")
    packet["instruction"]["target_session_id"] = "other-session"
    passed, failures = validate_hitl_packet(packet)
    assert not passed
    assert any("target_session_id" in failure for failure in failures)


def test_low_confidence_non_clarify_decision_fails_closed() -> None:
    packet = _load("session-instruction.json")
    packet["normalized_decision"]["confidence"] = 0.42
    passed, failures = validate_hitl_packet(packet)
    assert not passed
    assert any("low-confidence" in failure for failure in failures)


def test_low_confidence_clarify_decision_passes_without_instruction() -> None:
    packet = copy.deepcopy(_load("session-instruction.json"))
    packet["packet_type"] = "normalized_decision"
    packet.pop("instruction")
    packet["normalized_decision"]["action"] = "clarify"
    packet["normalized_decision"]["confidence"] = 0.42
    passed, failures = validate_hitl_packet(packet)
    assert passed, failures


def test_duplicate_reply_cannot_produce_instruction() -> None:
    packet = _load("session-instruction.json")
    packet["operator_reply"]["duplicate"] = True
    passed, failures = validate_hitl_packet(packet)
    assert not passed
    assert any("duplicate" in failure for failure in failures)


def test_expired_reply_cannot_produce_instruction() -> None:
    packet = _load("session-instruction.json")
    packet["operator_reply"]["expired"] = True
    passed, failures = validate_hitl_packet(packet)
    assert not passed
    assert any("expired" in failure for failure in failures)


def test_pii_external_channel_fails_closed() -> None:
    packet = _load("session-instruction.json")
    packet["policy"]["pii_mode"] = "detected"
    packet["policy"]["data_classification"] = "pii"
    packet["operator_reply"]["channel"] = "sms"
    passed, failures = validate_hitl_packet(packet)
    assert not passed
    assert any("external channel" in failure for failure in failures)


def test_stale_session_requires_resume_packet() -> None:
    packet = _load("session-instruction.json")
    packet["session"]["state"] = "stale"
    passed, failures = validate_hitl_packet(packet)
    assert not passed
    assert any("stale sessions" in failure for failure in failures)


def test_response_requires_notification_and_response_ids() -> None:
    packet = copy.deepcopy(_load("session-instruction.json"))
    packet["packet_type"] = "hitl_response"
    packet.pop("normalized_decision")
    packet.pop("instruction")
    packet["correlation"].pop("notification_id")
    passed, failures = validate_hitl_packet(packet)
    assert not passed
    assert any("notification_id" in failure for failure in failures)
