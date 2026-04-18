#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "hitl-relay-packet.schema.json"
SECURITY_POLICY_REF = "docs/runbooks/hitl-relay-security.md"

APPROVAL_ACTIONS = {"approve", "merge_when_green"}
LOCAL_CHANNELS = {"local_fixture"}
EXTERNAL_CHANNELS = {"sms", "slack", "email", "other"}
MIN_CONFIDENCE = 0.80


def load_packet(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate_schema(packet: dict[str, Any]) -> list[str]:
    errors = sorted(_schema_validator().iter_errors(packet), key=lambda error: list(error.path))
    return [f"schema: {error.message}" for error in errors]


def _packet_type(packet: dict[str, Any]) -> str:
    return str(packet.get("packet_type", ""))


def _correlation(packet: dict[str, Any]) -> dict[str, Any]:
    value = packet.get("correlation")
    return value if isinstance(value, dict) else {}


def _session(packet: dict[str, Any]) -> dict[str, Any]:
    value = packet.get("session")
    return value if isinstance(value, dict) else {}


def _policy(packet: dict[str, Any]) -> dict[str, Any]:
    value = packet.get("policy")
    return value if isinstance(value, dict) else {}


def _operator_reply(packet: dict[str, Any]) -> dict[str, Any]:
    value = packet.get("operator_reply")
    return value if isinstance(value, dict) else {}


def _decision(packet: dict[str, Any]) -> dict[str, Any]:
    value = packet.get("normalized_decision")
    return value if isinstance(value, dict) else {}


def _instruction(packet: dict[str, Any]) -> dict[str, Any]:
    value = packet.get("instruction")
    return value if isinstance(value, dict) else {}


def validate_policy_refs(packet: dict[str, Any]) -> list[str]:
    policy = _policy(packet)
    failures: list[str] = []
    if policy.get("channel_policy_ref") != SECURITY_POLICY_REF:
        failures.append(f"policy: channel_policy_ref must be {SECURITY_POLICY_REF}")
    retention = policy.get("retention_policy_ref")
    if _packet_type(packet) in {"hitl_response", "normalized_decision", "session_instruction", "audit_record"}:
        if not retention:
            failures.append("policy: response/instruction/audit packets require retention_policy_ref")
    return failures


def validate_correlation(packet: dict[str, Any]) -> list[str]:
    packet_type = _packet_type(packet)
    correlation = _correlation(packet)
    failures: list[str] = []
    if packet_type in {"hitl_response", "normalized_decision", "session_instruction", "session_resume", "audit_record"}:
        for field in ("notification_id", "response_id"):
            if not correlation.get(field):
                failures.append(f"correlation: {packet_type} requires {field}")
    if packet_type in {"session_instruction", "session_resume"} and not correlation.get("parent_packet_id"):
        failures.append(f"correlation: {packet_type} requires parent_packet_id")
    return failures


def validate_operator_reply(packet: dict[str, Any]) -> list[str]:
    packet_type = _packet_type(packet)
    if packet_type not in {"hitl_response", "normalized_decision", "session_instruction"}:
        return []

    reply = _operator_reply(packet)
    failures: list[str] = []
    if reply.get("sender_verified") is not True:
        failures.append("operator_reply: sender_verified must be true")
    if not str(reply.get("sender_ref", "")).startswith("operator:"):
        failures.append("operator_reply: sender_ref must identify an operator")
    for flag in ("duplicate", "replayed", "expired"):
        if reply.get(flag) is True:
            failures.append(f"operator_reply: {flag} replies cannot produce decisions or instructions")
    return failures


def validate_pii_channel_policy(packet: dict[str, Any]) -> list[str]:
    policy = _policy(packet)
    reply = _operator_reply(packet)
    pii_mode = policy.get("pii_mode")
    classification = policy.get("data_classification")
    channel = reply.get("channel")
    if (pii_mode in {"tagged", "detected", "lam_only"} or classification == "pii") and channel in EXTERNAL_CHANNELS:
        return [f"policy: {pii_mode}/{classification} packets cannot use external channel {channel}"]
    return []


def validate_normalized_decision(packet: dict[str, Any]) -> list[str]:
    packet_type = _packet_type(packet)
    if packet_type not in {"normalized_decision", "session_instruction"}:
        return []

    decision = _decision(packet)
    action = decision.get("action")
    confidence = decision.get("confidence")
    failures: list[str] = []
    if decision.get("validation_required") is not True:
        failures.append("normalized_decision: validation_required must be true")
    if isinstance(confidence, (int, float)) and confidence < MIN_CONFIDENCE and action != "clarify":
        failures.append("normalized_decision: low-confidence replies must normalize to clarify")
    if action in APPROVAL_ACTIONS and not _operator_reply(packet):
        failures.append("normalized_decision: approval actions require operator_reply provenance")
    return failures


def validate_instruction(packet: dict[str, Any]) -> list[str]:
    if _packet_type(packet) != "session_instruction":
        return []

    session = _session(packet)
    decision = _decision(packet)
    instruction = _instruction(packet)
    failures: list[str] = []
    if session.get("state") == "stale":
        failures.append("instruction: stale sessions require session_resume, not session_instruction")
    if instruction.get("target_session_id") != session.get("session_id"):
        failures.append("instruction: target_session_id must match session.session_id")
    if instruction.get("action") != decision.get("action"):
        failures.append("instruction: action must match normalized_decision.action")
    if not instruction.get("audit_refs"):
        failures.append("instruction: audit_refs are required")
    return failures


def validate_resume(packet: dict[str, Any]) -> list[str]:
    if _packet_type(packet) != "session_resume":
        return []
    session = _session(packet)
    if session.get("state") not in {"stale", "blocked"}:
        return ["resume: session_resume requires stale or blocked session state"]
    return []


def validate_hitl_packet(packet: dict[str, Any]) -> tuple[bool, list[str]]:
    failures: list[str] = []
    checks = [
        validate_schema,
        validate_policy_refs,
        validate_correlation,
        validate_operator_reply,
        validate_pii_channel_policy,
        validate_normalized_decision,
        validate_instruction,
        validate_resume,
    ]
    for check in checks:
        failures.extend(check(packet))
    return (not failures, failures)


def _run_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a HITL relay packet JSON file")
    parser.add_argument("packet_file")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)

    packet_path = Path(args.packet_file)
    try:
        packet = load_packet(packet_path)
    except Exception as exc:
        payload = {"status": "refused", "reason": f"failed to read packet: {exc}", "packet_id": None}
        print(json.dumps(payload) if args.json else f"::error::{payload['reason']}")
        return 1

    passed, failures = validate_hitl_packet(packet)
    payload = {
        "status": "ok" if passed else "refused",
        "reason": "; ".join(failures) if failures else "ok",
        "packet_id": packet.get("packet_id"),
    }
    print(json.dumps(payload) if args.json else payload["reason"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(_run_cli())
