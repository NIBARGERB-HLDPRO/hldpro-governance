#!/usr/bin/env python3
"""Tests for the operator inbound message preflight."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "operator_inbound_preflight.py"
sys.path.insert(0, str(SCRIPT.parent))
import operator_inbound_preflight  # noqa: E402


def test_fixture_preflight_proves_session_inbox_receive_path() -> None:
    payload, exit_code = operator_inbound_preflight.build_payload("fixture")
    checks = {item["name"]: item for item in payload["checks"]}

    assert exit_code == 0
    assert payload["ready"] is True
    assert payload["receive_path"] == "hitl-relay-session-inbox"
    assert checks["operator-inbound-session-inbox"]["status"] == "pass"
    assert payload["received_instruction"]["packet_type"] == "session_instruction"
    assert payload["received_instruction"]["target_session_id"] == operator_inbound_preflight.FIXTURE_SESSION_ID
    assert payload["received_instruction"]["action"] == "details"


def test_live_preflight_fails_closed_when_config_missing(monkeypatch) -> None:
    for name in ["SOM_OPERATOR_INBOUND_QUEUE_ROOT", "SOM_OPERATOR_INBOUND_SESSION_ID"]:
        monkeypatch.delenv(name, raising=False)

    payload, exit_code = operator_inbound_preflight.build_payload("live")

    assert exit_code == 2
    assert payload["ready"] is False
    assert "SOM_OPERATOR_INBOUND_QUEUE_ROOT" in payload["missing_live_config"]
    assert "SOM_OPERATOR_INBOUND_SESSION_ID" in payload["missing_live_config"]
    rendered = json.dumps(payload)
    assert "Bearer " not in rendered
    assert "CF-Access" not in rendered
    assert "raw_message_body" not in rendered


def test_live_preflight_fails_when_session_inbox_has_no_instruction(monkeypatch, tmp_path: Path) -> None:
    queue_root = tmp_path / "queue"
    (queue_root / "session-inbox").mkdir(parents=True)
    monkeypatch.setenv("SOM_OPERATOR_INBOUND_QUEUE_ROOT", str(queue_root))
    monkeypatch.setenv("SOM_OPERATOR_INBOUND_SESSION_ID", "missing-session")

    payload, exit_code = operator_inbound_preflight.build_payload("live")

    assert exit_code == 1
    assert payload["ready"] is False
    assert payload["missing_live_config"] == []
    checks = {item["name"]: item for item in payload["checks"]}
    assert checks["operator-inbound-session-inbox"]["status"] == "fail"


def test_cli_writes_json_output(tmp_path: Path) -> None:
    output = tmp_path / "preflight.json"
    env = os.environ.copy()
    for name in ["SOM_OPERATOR_INBOUND_QUEUE_ROOT", "SOM_OPERATOR_INBOUND_SESSION_ID"]:
        env.pop(name, None)

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--mode", "live", "--json-output", str(output)],
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["ready"] is False
    assert "SOM_OPERATOR_INBOUND_QUEUE_ROOT" in payload["missing_live_config"]
