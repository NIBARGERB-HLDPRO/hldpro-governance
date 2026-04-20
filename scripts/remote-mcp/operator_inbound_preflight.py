#!/usr/bin/env python3
"""No-secret preflight for operator inbound message readiness."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "orchestrator"))
import hitl_relay_queue  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "packet"))
from validate_hitl_relay import validate_hitl_packet  # noqa: E402


LIVE_REQUIRED_GROUPS = (
    ("SOM_OPERATOR_INBOUND_QUEUE_ROOT",),
    ("SOM_OPERATOR_INBOUND_SESSION_ID",),
)
FIXTURE_SESSION_ID = "codex-issue-382-operator-inbound-fixture"
FIXTURE_REQUEST_ID = "remote-mcp-operator-inbound-382"
FIXTURE_RESPONSE_ID = "remote-mcp-operator-inbound-response-382"


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "status": self.status, "detail": self.detail}


def _missing_groups(groups: Sequence[tuple[str, ...]]) -> list[str]:
    missing: list[str] = []
    for group in groups:
        if not any(os.environ.get(name) for name in group):
            missing.append(" or ".join(group))
    return missing


def _fixture_request() -> dict[str, Any]:
    return hitl_relay_queue.build_request(
        issue_number=382,
        session_id=FIXTURE_SESSION_ID,
        cli="codex",
        request_id=FIXTURE_REQUEST_ID,
        event_type="hitl_checkpoint",
        artifacts=[
            {"kind": "plan", "ref": "docs/plans/issue-382-remote-mcp-operator-inbound-preflight-pdcar.md"},
            {
                "kind": "execution_scope",
                "ref": "raw/execution-scopes/2026-04-20-issue-382-remote-mcp-operator-inbound-preflight-implementation.json",
            },
        ],
        allowed_actions=["details", "request_changes", "pause"],
        prompt_ref="raw/remote-mcp-operator-inbound-preflight/fixture-request.md",
    )


def _packet_summary(path: Path) -> dict[str, Any]:
    packet = json.loads(path.read_text(encoding="utf-8"))
    return {
        "packet_type": packet.get("packet_type"),
        "packet_id": packet.get("packet_id"),
        "session_id": (packet.get("session") or {}).get("session_id"),
        "request_id": (packet.get("correlation") or {}).get("request_id"),
        "response_id": (packet.get("correlation") or {}).get("response_id"),
        "action": (packet.get("instruction") or {}).get("action"),
        "target_session_id": (packet.get("instruction") or {}).get("target_session_id"),
    }


def _call_fixture() -> tuple[Check, dict[str, Any]]:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _fixture_request()
        request_result = hitl_relay_queue.enqueue_request(request, queue_root=queue_root)
        if request_result.status != "ok":
            return Check("operator-inbound-session-inbox", "fail", request_result.reason), {}

        instruction_result = hitl_relay_queue.process_response(
            request,
            response_id=FIXTURE_RESPONSE_ID,
            notification_id="remote-mcp-operator-inbound-notification-382",
            action="details",
            confidence=0.98,
            raw_message_ref="raw/remote-mcp-operator-inbound-preflight/fixture-response.json",
            channel="local_fixture",
            message_id="remote-mcp-operator-inbound-message-382",
            queue_root=queue_root,
        )
        if instruction_result.status != "ok" or instruction_result.packet_path is None:
            return Check("operator-inbound-session-inbox", "fail", instruction_result.reason), {}

        summary = _packet_summary(instruction_result.packet_path)
        replay = hitl_relay_queue.replay_audit(queue_root / "audit" / "events.jsonl")
        summary["audit_packet_types"] = replay.get("packet_types", [])
        ok = (
            summary.get("packet_type") == "session_instruction"
            and summary.get("target_session_id") == FIXTURE_SESSION_ID
            and "session_instruction" in summary["audit_packet_types"]
        )
        return (
            Check(
                "operator-inbound-session-inbox",
                "pass" if ok else "fail",
                "fixture operator message reached session inbox" if ok else "fixture session inbox packet was malformed",
            ),
            summary if ok else {},
        )


def _latest_live_instruction(queue_root: Path, session_id: str) -> tuple[Check, dict[str, Any]]:
    inbox = queue_root / "session-inbox"
    if not inbox.is_dir():
        return Check("operator-inbound-session-inbox", "fail", "session-inbox directory is missing"), {}

    candidates = sorted(inbox.glob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    for candidate in candidates:
        try:
            packet = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        passed, failures = validate_hitl_packet(packet)
        if not passed:
            continue
        target_session = (packet.get("instruction") or {}).get("target_session_id")
        if packet.get("packet_type") == "session_instruction" and target_session == session_id:
            summary = _packet_summary(candidate)
            return Check("operator-inbound-session-inbox", "pass", "live session inbox contains a validated instruction"), summary

    return Check("operator-inbound-session-inbox", "fail", "no validated instruction found for configured session"), {}


def _call_live() -> tuple[Check, dict[str, Any], list[str]]:
    missing = _missing_groups(LIVE_REQUIRED_GROUPS)
    if missing:
        return Check("operator-inbound-session-inbox", "fail", "missing live configuration: " + ", ".join(missing)), {}, missing

    queue_root = Path(os.environ["SOM_OPERATOR_INBOUND_QUEUE_ROOT"]).expanduser()
    session_id = os.environ["SOM_OPERATOR_INBOUND_SESSION_ID"]
    check, summary = _latest_live_instruction(queue_root, session_id)
    return check, summary, []


def build_payload(mode: str) -> tuple[dict[str, Any], int]:
    checks = [
        Check("hitl-relay-queue-contract", "pass", "using existing HITL relay queue validator"),
        Check("remote-mcp-request-response-separation", "pass", "inbound receive is separate from som.ping request/response"),
    ]
    missing_live = _missing_groups(LIVE_REQUIRED_GROUPS)

    if mode == "fixture":
        inbox_check, instruction = _call_fixture()
        checks.append(inbox_check)
        ready = inbox_check.status == "pass"
        exit_code = 0 if ready else 1
    else:
        inbox_check, instruction, missing_from_call = _call_live()
        checks.append(inbox_check)
        missing_live = missing_from_call or missing_live
        ready = inbox_check.status == "pass"
        exit_code = 0 if ready else 2 if missing_live else 1

    blocking = [check for check in checks if check.status == "fail"]
    warnings = [check for check in checks if check.status == "warn"]
    if ready and not blocking:
        recommended_action = (
            "Fixture inbound queue path is ready; configure live inbound queue inputs to prove current-machine receive."
            if mode == "fixture"
            else "Operator inbound message receive path is ready."
        )
    else:
        recommended_action = "Configure live inbound queue root/session id or deliver a validated instruction, then rerun live preflight."

    return (
        {
            "schema_version": 1,
            "mode": mode,
            "ready": ready and not blocking,
            "receive_path": "hitl-relay-session-inbox",
            "checks": [check.to_dict() for check in checks],
            "missing_live_config": missing_live,
            "warnings": [check.name for check in warnings],
            "received_instruction": instruction,
            "recommended_action": recommended_action,
        },
        exit_code,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="No-secret Remote MCP operator inbound message preflight.")
    parser.add_argument("--mode", choices=("fixture", "live"), default="live")
    parser.add_argument("--json-output", type=Path, help="Optional path to write JSON output.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    payload, exit_code = build_payload(args.mode)
    rendered = json.dumps(payload, indent=2) + "\n"
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
