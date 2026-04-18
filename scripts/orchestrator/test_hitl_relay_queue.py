#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))

import hitl_relay_queue  # noqa: E402


def _request() -> dict:
    return hitl_relay_queue.build_request(
        issue_number=301,
        session_id="codex-20260418-issue-301",
        cli="codex",
        request_id="hitl-20260418-301",
        event_type="hitl_checkpoint",
        artifacts=[
            {"kind": "plan", "ref": "docs/plans/issue-301-structured-agent-cycle-plan.json"},
            {
                "kind": "execution_scope",
                "ref": "raw/execution-scopes/2026-04-18-issue-301-hitl-queue-prototype-implementation.json",
            },
        ],
        allowed_actions=["merge_when_green", "request_changes", "pause", "details"],
        prompt_ref="raw/hitl-relay/queue/requests/hitl-20260418-301.md",
    )


def _process(
    queue_root: Path,
    request: dict,
    *,
    action: str,
    confidence: float = 0.98,
    response_id: str = "local-response-301",
    session_state: str = "waiting_hitl",
    duplicate: bool = False,
    expired: bool = False,
) -> hitl_relay_queue.QueueResult:
    return hitl_relay_queue.process_response(
        request,
        response_id=response_id,
        notification_id="local-notification-301",
        action=action,
        confidence=confidence,
        raw_message_ref=f"raw/hitl-relay/queue/responses/{response_id}.json",
        session_state=session_state,
        duplicate=duplicate,
        expired=expired,
        queue_root=queue_root,
    )


def test_local_cli_checkpoint_fixture_creates_valid_hitl_request() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        result = hitl_relay_queue.enqueue_request(_request(), queue_root=queue_root)

        assert result.status == "ok", result.reason
        assert result.packet_path is not None
        assert result.packet_path.parent.name == "requests"
        packet = json.loads(result.packet_path.read_text(encoding="utf-8"))
        assert packet["packet_type"] == "hitl_request"
        assert packet["session"]["state"] == "waiting_hitl"


def test_valid_approval_response_produces_bounded_session_instruction() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _request()
        hitl_relay_queue.enqueue_request(request, queue_root=queue_root)

        result = _process(queue_root, request, action="merge_when_green")

        assert result.status == "ok", result.reason
        assert result.packet_path is not None
        assert result.packet_path.parent.name == "session-inbox"
        instruction = json.loads(result.packet_path.read_text(encoding="utf-8"))
        assert instruction["packet_type"] == "session_instruction"
        assert instruction["instruction"]["action"] == "merge_when_green"
        assert instruction["instruction"]["target_session_id"] == request["session"]["session_id"]
        assert instruction["correlation"]["request_id"] == request["correlation"]["request_id"]
        assert instruction["correlation"]["notification_id"] == "local-notification-301"
        assert instruction["correlation"]["response_id"] == "local-response-301"


def test_request_changes_response_preserves_feedback_path_without_approval() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _request()

        result = _process(queue_root, request, action="request_changes", response_id="local-response-changes")

        assert result.status == "ok", result.reason
        assert result.packet_path is not None
        packet = json.loads(result.packet_path.read_text(encoding="utf-8"))
        assert packet["instruction"]["action"] == "request_changes"
        assert packet["normalized_decision"]["action"] != "merge_when_green"
        assert packet["operator_reply"]["raw_message_ref"].endswith("local-response-changes.json")


def test_ambiguous_response_produces_clarification_and_no_instruction() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _request()

        result = _process(queue_root, request, action="clarify", confidence=0.42)

        assert result.status == "clarify", result.reason
        assert not any((queue_root / "session-inbox").glob("*.json"))
        assert any((queue_root / "decisions").glob("*.json"))
        replay = hitl_relay_queue.replay_audit(queue_root / "audit" / "events.jsonl")
        assert "clarification_requested" in replay["decision_trace"]


def test_stale_session_fixture_produces_resume_packet() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _request()

        result = _process(queue_root, request, action="merge_when_green", session_state="stale")

        assert result.status == "ok", result.reason
        assert result.packet_path is not None
        assert result.packet_path.parent.name == "session-resume"
        assert not any((queue_root / "session-inbox").glob("*.json"))
        resume = json.loads(result.packet_path.read_text(encoding="utf-8"))
        assert resume["packet_type"] == "session_resume"
        assert resume["resume"]["reason"] == "session_stale"


def test_invalid_packet_lands_in_dead_letter_with_validation_errors() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _request()

        result = _process(queue_root, request, action="merge_when_green", duplicate=True)

        assert result.status == "dead_letter"
        assert result.packet_path is not None
        assert result.packet_path.parent.name == "dead-letter"
        dead = json.loads(result.packet_path.read_text(encoding="utf-8"))
        assert "duplicate" in dead["reason"]


def test_expired_response_fails_closed_to_dead_letter() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _request()

        result = _process(queue_root, request, action="merge_when_green", expired=True)

        assert result.status == "dead_letter"
        assert result.packet_path is not None
        dead = json.loads(result.packet_path.read_text(encoding="utf-8"))
        assert "expired" in dead["reason"]


def test_replay_reconstructs_decision_path() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _request()
        hitl_relay_queue.enqueue_request(request, queue_root=queue_root)
        _process(queue_root, request, action="merge_when_green")

        replay = hitl_relay_queue.replay_audit(queue_root / "audit" / "events.jsonl")

        assert replay["dead_letters"] == 0
        assert replay["request_ids"] == ["hitl-20260418-301"]
        assert replay["session_ids"] == ["codex-20260418-issue-301"]
        assert replay["packet_types"] == [
            "hitl_request",
            "hitl_response",
            "normalized_decision",
            "session_instruction",
        ]
