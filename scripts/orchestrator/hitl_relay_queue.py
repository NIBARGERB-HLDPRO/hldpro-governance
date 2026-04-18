#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "packet"))

from validate_hitl_relay import validate_hitl_packet  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_QUEUE_ROOT = REPO_ROOT / "raw" / "hitl-relay" / "queue"
SECURITY_POLICY_REF = "docs/runbooks/hitl-relay-security.md"
RETENTION_POLICY_REF = "docs/runbooks/hitl-relay-security.md#retention"
MODEL_ID = "gpt-5.4"
MODEL_FAMILY = "openai"
APPROVAL_ACTIONS = {"approve", "merge_when_green"}
INSTRUCTION_ACTIONS = {"approve", "merge_when_green", "request_changes", "pause", "details", "create_followup_issue"}
QUEUE_DIRS = (
    "requests",
    "responses",
    "decisions",
    "session-inbox",
    "session-resume",
    "dead-letter",
    "audit",
)


@dataclass(frozen=True)
class QueueResult:
    status: str
    action: str
    packet_path: Path | None
    reason: str
    packet_id: str | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_queue(root: Path = DEFAULT_QUEUE_ROOT) -> None:
    for name in QUEUE_DIRS:
        (root / name).mkdir(parents=True, exist_ok=True)


def packet_uuid(*parts: Any) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "|".join(str(part) for part in parts)))


def atomic_write_json(payload: dict[str, Any], destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = destination.with_name(f".{destination.name}.{datetime.now(timezone.utc).timestamp()}.tmp")
    tmp_path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    tmp_path.replace(destination)
    return destination


def append_audit(root: Path, event: dict[str, Any]) -> None:
    audit_dir = root / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    with (audit_dir / "events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"timestamp": utc_now(), **event}, sort_keys=True) + "\n")


def load_packet(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"packet must be a JSON object: {path}")
    return payload


def _base_packet(
    *,
    packet_type: str,
    issue_number: int,
    session: dict[str, Any],
    correlation: dict[str, Any],
    policy: dict[str, Any] | None = None,
    packet_id: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "packet_id": packet_id or packet_uuid(packet_type, correlation.get("request_id"), correlation.get("response_id", "")),
        "packet_type": packet_type,
        "created_at": utc_now(),
        "issue_number": issue_number,
        "repo": {"owner": "NIBARGERB-HLDPRO", "name": "hldpro-governance"},
        "session": session,
        "correlation": correlation,
        "policy": policy
        or {
            "pii_mode": "none",
            "data_classification": "internal",
            "channel_policy_ref": SECURITY_POLICY_REF,
        },
    }


def build_request(
    *,
    issue_number: int,
    session_id: str,
    cli: str,
    request_id: str,
    event_type: str,
    artifacts: list[dict[str, str]],
    allowed_actions: list[str],
    prompt_ref: str,
    pii_mode: str = "none",
    data_classification: str = "internal",
) -> dict[str, Any]:
    packet = _base_packet(
        packet_type="hitl_request",
        issue_number=issue_number,
        session={"session_id": session_id, "cli": cli, "state": "waiting_hitl"},
        correlation={"request_id": request_id},
        policy={
            "pii_mode": pii_mode,
            "data_classification": data_classification,
            "channel_policy_ref": SECURITY_POLICY_REF,
        },
        packet_id=packet_uuid("hitl_request", issue_number, session_id, request_id),
    )
    packet.update(
        {
            "event_type": event_type,
            "artifacts": artifacts,
            "requested_decision": {
                "decision_type": "approval" if any(action in APPROVAL_ACTIONS for action in allowed_actions) else "feedback",
                "allowed_actions": allowed_actions,
                "prompt_ref": prompt_ref,
            },
        }
    )
    return packet


def enqueue_request(packet: dict[str, Any], *, queue_root: Path = DEFAULT_QUEUE_ROOT) -> QueueResult:
    ensure_queue(queue_root)
    return _validated_write(packet, queue_root / "requests" / f"{packet.get('packet_id', 'unknown')}.json", queue_root)


def process_response(
    request_packet: dict[str, Any],
    *,
    response_id: str,
    notification_id: str,
    action: str,
    confidence: float,
    raw_message_ref: str,
    sender_ref: str = "operator:ben",
    message_id: str = "local-message-001",
    channel: str = "local_fixture",
    session_state: str = "waiting_hitl",
    duplicate: bool = False,
    replayed: bool = False,
    expired: bool = False,
    queue_root: Path = DEFAULT_QUEUE_ROOT,
) -> QueueResult:
    ensure_queue(queue_root)
    response_packet = _build_response_packet(
        request_packet,
        response_id=response_id,
        notification_id=notification_id,
        sender_ref=sender_ref,
        message_id=message_id,
        raw_message_ref=raw_message_ref,
        channel=channel,
        session_state=session_state,
        duplicate=duplicate,
        replayed=replayed,
        expired=expired,
    )
    response_result = _validated_write(
        response_packet,
        queue_root / "responses" / f"{response_packet['packet_id']}.json",
        queue_root,
    )
    if response_result.status != "ok":
        return response_result

    decision_packet = _build_decision_packet(response_packet, action=action, confidence=confidence)
    decision_result = _validated_write(
        decision_packet,
        queue_root / "decisions" / f"{decision_packet['packet_id']}.json",
        queue_root,
    )
    if decision_result.status != "ok":
        return decision_result

    if action == "clarify" or confidence < 0.80:
        append_audit(
            queue_root,
            {
                "event": "clarification_requested",
                "request_id": response_packet["correlation"]["request_id"],
                "response_id": response_id,
                "decision_packet_id": decision_packet["packet_id"],
                "reason": "ambiguous_or_low_confidence",
            },
        )
        return QueueResult("clarify", "clarify", decision_result.packet_path, "clarification requested", decision_packet["packet_id"])

    if session_state == "stale":
        resume_packet = _build_resume_packet(decision_packet)
        resume_result = _validated_write(
            resume_packet,
            queue_root / "session-resume" / f"{resume_packet['packet_id']}.json",
            queue_root,
        )
        return QueueResult(resume_result.status, "resume_session", resume_result.packet_path, resume_result.reason, resume_packet["packet_id"])

    if action not in INSTRUCTION_ACTIONS:
        return _dead_letter(
            decision_packet,
            queue_root,
            f"unsupported normalized action for queue instruction: {action}",
        )

    instruction_packet = _build_instruction_packet(decision_packet)
    instruction_result = _validated_write(
        instruction_packet,
        queue_root / "session-inbox" / f"{instruction_packet['packet_id']}.json",
        queue_root,
    )
    return QueueResult(
        instruction_result.status,
        action,
        instruction_result.packet_path,
        instruction_result.reason,
        instruction_packet["packet_id"],
    )


def _build_response_packet(
    request_packet: dict[str, Any],
    *,
    response_id: str,
    notification_id: str,
    sender_ref: str,
    message_id: str,
    raw_message_ref: str,
    channel: str,
    session_state: str,
    duplicate: bool,
    replayed: bool,
    expired: bool,
) -> dict[str, Any]:
    session = dict(request_packet["session"])
    session["state"] = session_state
    policy = dict(request_packet["policy"])
    policy["retention_policy_ref"] = RETENTION_POLICY_REF
    correlation = {
        "request_id": request_packet["correlation"]["request_id"],
        "parent_packet_id": request_packet["packet_id"],
        "notification_id": notification_id,
        "response_id": response_id,
    }
    packet = _base_packet(
        packet_type="hitl_response",
        issue_number=int(request_packet["issue_number"]),
        session=session,
        correlation=correlation,
        policy=policy,
        packet_id=packet_uuid("hitl_response", request_packet["packet_id"], response_id),
    )
    reply: dict[str, Any] = {
        "channel": channel,
        "sender_ref": sender_ref,
        "message_id": message_id,
        "received_at": utc_now(),
        "raw_message_ref": raw_message_ref,
        "sender_verified": True,
    }
    for flag, enabled in (("duplicate", duplicate), ("replayed", replayed), ("expired", expired)):
        if enabled:
            reply[flag] = True
    packet["operator_reply"] = reply
    return packet


def _build_decision_packet(response_packet: dict[str, Any], *, action: str, confidence: float) -> dict[str, Any]:
    packet = dict(response_packet)
    packet["packet_type"] = "normalized_decision"
    packet["packet_id"] = packet_uuid("normalized_decision", response_packet["packet_id"], action, confidence)
    packet["created_at"] = utc_now()
    packet["normalized_decision"] = {
        "action": action,
        "confidence": confidence,
        "model_id": MODEL_ID,
        "model_family": MODEL_FAMILY,
        "raw_message_ref": response_packet["operator_reply"]["raw_message_ref"],
        "validation_required": True,
    }
    return packet


def _build_instruction_packet(decision_packet: dict[str, Any]) -> dict[str, Any]:
    packet = dict(decision_packet)
    action = packet["normalized_decision"]["action"]
    packet["packet_type"] = "session_instruction"
    packet["packet_id"] = packet_uuid("session_instruction", decision_packet["packet_id"], action)
    packet["created_at"] = utc_now()
    packet["instruction"] = {
        "action": action,
        "target_session_id": packet["session"]["session_id"],
        "constraints": ["require_governance_validation", "require_audit_replay"],
        "audit_refs": [
            f"raw/hitl-relay/queue/requests/{packet['correlation']['parent_packet_id']}.json",
            packet["operator_reply"]["raw_message_ref"],
            "raw/hitl-relay/queue/audit/events.jsonl",
        ],
    }
    return packet


def _build_resume_packet(decision_packet: dict[str, Any]) -> dict[str, Any]:
    packet = {
        key: value
        for key, value in decision_packet.items()
        if key not in {"operator_reply", "normalized_decision"}
    }
    packet["packet_type"] = "session_resume"
    packet["packet_id"] = packet_uuid("session_resume", decision_packet["packet_id"])
    packet["created_at"] = utc_now()
    packet["resume"] = {
        "reason": "session_stale",
        "resume_context_refs": [
            f"raw/hitl-relay/queue/requests/{packet['correlation']['parent_packet_id']}.json",
            decision_packet["operator_reply"]["raw_message_ref"],
            "raw/hitl-relay/queue/audit/events.jsonl",
        ],
    }
    return packet


def _validated_write(packet: dict[str, Any], destination: Path, queue_root: Path) -> QueueResult:
    passed, failures = validate_hitl_packet(packet)
    if not passed:
        return _dead_letter(packet, queue_root, "; ".join(failures))
    atomic_write_json(packet, destination)
    append_audit(
        queue_root,
        {
            "event": "packet_written",
            "packet_id": packet["packet_id"],
            "packet_type": packet["packet_type"],
            "path": str(destination),
            "request_id": packet["correlation"]["request_id"],
            "response_id": packet["correlation"].get("response_id"),
            "session_id": packet["session"]["session_id"],
        },
    )
    return QueueResult("ok", packet["packet_type"], destination, "validated and written", packet["packet_id"])


def _dead_letter(packet: dict[str, Any], queue_root: Path, reason: str) -> QueueResult:
    dead_id = str(packet.get("packet_id") or packet_uuid("dead-letter", reason, utc_now()))
    destination = queue_root / "dead-letter" / f"{dead_id}.json"
    atomic_write_json({"reason": reason, "packet": packet}, destination)
    append_audit(
        queue_root,
        {
            "event": "dead_letter",
            "packet_id": packet.get("packet_id"),
            "packet_type": packet.get("packet_type"),
            "path": str(destination),
            "request_id": (packet.get("correlation") or {}).get("request_id"),
            "reason": reason,
        },
    )
    return QueueResult("dead_letter", str(packet.get("packet_type") or "unknown"), destination, reason, packet.get("packet_id"))


def replay_audit(audit_path: Path) -> dict[str, Any]:
    events = []
    for line in audit_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    decision_trace = [event["event"] for event in events]
    return {
        "events": len(events),
        "dead_letters": sum(1 for event in events if event.get("event") == "dead_letter"),
        "request_ids": sorted({str(event["request_id"]) for event in events if event.get("request_id")}),
        "session_ids": sorted({str(event["session_id"]) for event in events if event.get("session_id")}),
        "packet_types": [event["packet_type"] for event in events if event.get("event") == "packet_written"],
        "decision_trace": decision_trace,
    }


def _run_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local HITL relay queue operations")
    parser.add_argument("--queue-root", type=Path, default=DEFAULT_QUEUE_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    enqueue = subparsers.add_parser("enqueue-request")
    enqueue.add_argument("request_json", type=Path)

    process = subparsers.add_parser("process-response")
    process.add_argument("request_json", type=Path)
    process.add_argument("--response-id", required=True)
    process.add_argument("--notification-id", required=True)
    process.add_argument("--action", required=True)
    process.add_argument("--confidence", type=float, required=True)
    process.add_argument("--raw-message-ref", required=True)
    process.add_argument("--session-state", default="waiting_hitl")

    replay = subparsers.add_parser("replay")
    replay.add_argument("--audit", type=Path)

    args = parser.parse_args(argv)
    if args.command == "enqueue-request":
        result = enqueue_request(load_packet(args.request_json), queue_root=args.queue_root)
    elif args.command == "process-response":
        result = process_response(
            load_packet(args.request_json),
            response_id=args.response_id,
            notification_id=args.notification_id,
            action=args.action,
            confidence=args.confidence,
            raw_message_ref=args.raw_message_ref,
            session_state=args.session_state,
            queue_root=args.queue_root,
        )
    else:
        audit_path = args.audit or args.queue_root / "audit" / "events.jsonl"
        print(json.dumps(replay_audit(audit_path), sort_keys=True))
        return 0

    print(json.dumps(result.__dict__, default=str, sort_keys=True))
    return 0 if result.status in {"ok", "clarify"} else 1


if __name__ == "__main__":
    raise SystemExit(_run_cli())
