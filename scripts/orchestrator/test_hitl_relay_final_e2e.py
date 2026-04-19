#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))

import hitl_relay_queue  # noqa: E402


SESSION_ID = "codex-20260419-issue-303-final-e2e"
REQUEST_ID = "hitl-20260419-303-final-e2e"
NOTIFICATION_ID = "ais-sandbox-notification-303"


def _final_request(*, pii_mode: str = "none", data_classification: str = "internal") -> dict:
    return hitl_relay_queue.build_request(
        issue_number=303,
        session_id=SESSION_ID,
        cli="codex",
        request_id=REQUEST_ID,
        event_type="hitl_checkpoint",
        artifacts=[
            {"kind": "plan", "ref": "docs/plans/issue-303-structured-agent-cycle-plan.json"},
            {
                "kind": "execution_scope",
                "ref": "raw/execution-scopes/2026-04-19-issue-303-final-e2e-proof-implementation.json",
            },
            {"kind": "pr", "ref": "hldpro-governance#305"},
            {"kind": "pr", "ref": "hldpro-governance#306"},
            {"kind": "pr", "ref": "hldpro-governance#308"},
            {"kind": "pr", "ref": "hldpro-governance#316"},
            {"kind": "pr", "ref": "ai-integration-services#1148"},
            {"kind": "pr", "ref": "local-ai-machine#470"},
            {"kind": "pr", "ref": "local-ai-machine#471"},
        ],
        allowed_actions=["merge_when_green", "request_changes", "pause", "details"],
        prompt_ref="raw/hitl-relay/queue/requests/hitl-20260419-303-final-e2e.md",
        pii_mode=pii_mode,
        data_classification=data_classification,
    )


def _process(
    queue_root: Path,
    request: dict,
    *,
    action: str,
    response_id: str,
    confidence: float = 0.98,
    session_state: str = "waiting_hitl",
    duplicate: bool = False,
    replayed: bool = False,
    expired: bool = False,
    channel: str = "local_fixture",
    message_id: str | None = None,
) -> hitl_relay_queue.QueueResult:
    return hitl_relay_queue.process_response(
        request,
        response_id=response_id,
        notification_id=NOTIFICATION_ID,
        action=action,
        confidence=confidence,
        raw_message_ref=f"raw/hitl-relay/queue/responses/{response_id}.json",
        session_state=session_state,
        duplicate=duplicate,
        replayed=replayed,
        expired=expired,
        channel=channel,
        message_id=message_id or f"ais-sandbox-message-{response_id}",
        queue_root=queue_root,
    )


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_final_e2e_approval_path_preserves_full_identity_chain() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _final_request()

        request_result = hitl_relay_queue.enqueue_request(request, queue_root=queue_root)
        assert request_result.status == "ok", request_result.reason

        instruction_result = _process(
            queue_root,
            request,
            action="merge_when_green",
            response_id="ais-sandbox-response-approval-303",
        )

        assert instruction_result.status == "ok", instruction_result.reason
        assert instruction_result.packet_path is not None
        instruction = _load(instruction_result.packet_path)
        assert instruction["packet_type"] == "session_instruction"
        assert instruction["session"]["session_id"] == SESSION_ID
        assert instruction["correlation"]["request_id"] == REQUEST_ID
        assert instruction["correlation"]["notification_id"] == NOTIFICATION_ID
        assert instruction["correlation"]["response_id"] == "ais-sandbox-response-approval-303"
        assert instruction["operator_reply"]["sender_verified"] is True
        assert instruction["operator_reply"]["message_id"] == "ais-sandbox-message-ais-sandbox-response-approval-303"
        assert instruction["normalized_decision"]["model_id"] == hitl_relay_queue.MODEL_ID
        assert instruction["normalized_decision"]["confidence"] >= 0.80
        assert instruction["normalized_decision"]["validation_required"] is True
        assert instruction["instruction"]["target_session_id"] == SESSION_ID
        assert "require_governance_validation" in instruction["instruction"]["constraints"]
        assert "raw/hitl-relay/queue/audit/events.jsonl" in instruction["instruction"]["audit_refs"]

        replay = hitl_relay_queue.replay_audit(queue_root / "audit" / "events.jsonl")
        assert replay["dead_letters"] == 0
        assert replay["request_ids"] == [REQUEST_ID]
        assert replay["session_ids"] == [SESSION_ID]
        assert replay["packet_types"] == [
            "hitl_request",
            "hitl_response",
            "normalized_decision",
            "session_instruction",
        ]


def test_final_e2e_request_changes_is_not_treated_as_approval() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _final_request()

        result = _process(
            queue_root,
            request,
            action="request_changes",
            response_id="ais-sandbox-response-changes-303",
        )

        assert result.status == "ok", result.reason
        assert result.packet_path is not None
        instruction = _load(result.packet_path)
        assert instruction["instruction"]["action"] == "request_changes"
        assert instruction["normalized_decision"]["action"] != "merge_when_green"
        assert instruction["operator_reply"]["raw_message_ref"].endswith("ais-sandbox-response-changes-303.json")


def test_final_e2e_ambiguous_response_requests_clarification_without_instruction() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _final_request()

        result = _process(
            queue_root,
            request,
            action="clarify",
            response_id="ais-sandbox-response-ambiguous-303",
            confidence=0.42,
        )

        assert result.status == "clarify", result.reason
        assert not any((queue_root / "session-inbox").glob("*.json"))
        replay = hitl_relay_queue.replay_audit(queue_root / "audit" / "events.jsonl")
        assert "clarification_requested" in replay["decision_trace"]


def test_final_e2e_stale_session_creates_resume_instead_of_instruction() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _final_request()

        result = _process(
            queue_root,
            request,
            action="merge_when_green",
            response_id="ais-sandbox-response-stale-303",
            session_state="stale",
        )

        assert result.status == "ok", result.reason
        assert result.packet_path is not None
        assert result.packet_path.parent.name == "session-resume"
        assert not any((queue_root / "session-inbox").glob("*.json"))
        resume = _load(result.packet_path)
        assert resume["packet_type"] == "session_resume"
        assert resume["resume"]["reason"] == "session_stale"
        assert "raw/hitl-relay/queue/audit/events.jsonl" in resume["resume"]["resume_context_refs"]


def test_final_e2e_duplicate_replay_and_expired_replies_fail_closed() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _final_request()

        duplicate = _process(
            queue_root,
            request,
            action="merge_when_green",
            response_id="ais-sandbox-response-duplicate-303",
            duplicate=True,
        )
        replayed = _process(
            queue_root,
            request,
            action="merge_when_green",
            response_id="ais-sandbox-response-replayed-303",
            replayed=True,
        )
        expired = _process(
            queue_root,
            request,
            action="merge_when_green",
            response_id="ais-sandbox-response-expired-303",
            expired=True,
        )

        assert duplicate.status == "dead_letter"
        assert "duplicate" in duplicate.reason
        assert replayed.status == "dead_letter"
        assert "replayed" in replayed.reason
        assert expired.status == "dead_letter"
        assert "expired" in expired.reason
        assert not any((queue_root / "session-inbox").glob("*.json"))


def test_final_e2e_external_channel_pii_is_refused_without_instruction() -> None:
    with tempfile.TemporaryDirectory() as raw:
        queue_root = Path(raw)
        request = _final_request(pii_mode="detected", data_classification="pii")

        result = _process(
            queue_root,
            request,
            action="merge_when_green",
            response_id="ais-sandbox-response-pii-303",
            channel="sms",
        )

        assert result.status == "dead_letter"
        assert "cannot use external channel sms" in result.reason
        assert not any((queue_root / "session-inbox").glob("*.json"))
