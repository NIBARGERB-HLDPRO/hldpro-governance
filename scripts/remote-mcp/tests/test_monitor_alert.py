#!/usr/bin/env python3
"""Tests for Remote MCP monitor alert formatting."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "monitor_alert.py"
sys.path.insert(0, str(SCRIPT.parent))
import monitor_alert  # noqa: E402


def _payload(status: str = "pass", detail: str = "ok") -> dict:
    return {
        "mode": "fixture",
        "evidence_dir": "/tmp/remote-mcp-monitor",
        "results": [
            {"name": "authenticated-ping", "status": status, "detail": detail},
            {"name": "evidence-safety-scan", "status": "pass", "detail": "safe"},
        ],
    }


def test_build_alert_marks_healthy_payload() -> None:
    alert = monitor_alert.build_alert(_payload(), generated_at="2026-04-20T00:00:00Z")

    assert alert["health"] == "healthy"
    assert alert["summary"]["passed"] == 2
    assert alert["summary"]["failed"] == 0
    assert alert["recommended_action"] == "No action required."


def test_build_alert_marks_degraded_failures() -> None:
    alert = monitor_alert.build_alert(_payload("fail", "status=500"), generated_at="2026-04-20T00:00:00Z")

    assert alert["health"] == "degraded"
    assert alert["summary"]["failed"] == 1
    assert alert["failed_checks"][0]["name"] == "authenticated-ping"
    assert "Restrict or disable Remote MCP" in alert["recommended_action"]


def test_sensitive_material_is_redacted_and_degraded() -> None:
    alert = monitor_alert.build_alert(
        _payload("fail", "Bearer abc.def.ghi and SSN 123-45-6789 and eyJabc123456789.eyJdef123456789"),
        generated_at="2026-04-20T00:00:00Z",
    )
    rendered = json.dumps(alert)

    assert alert["health"] == "degraded"
    assert alert["summary"]["sensitive_findings"] >= 3
    assert "[redacted-sensitive-detail]" in rendered
    assert "123-45-6789" not in rendered
    assert "Bearer abc" not in rendered
    assert "eyJabc" not in rendered


def test_cli_writes_json_and_markdown(tmp_path: Path) -> None:
    payload_path = tmp_path / "monitor.json"
    json_path = tmp_path / "alert.json"
    markdown_path = tmp_path / "alert.md"
    payload_path.write_text(json.dumps(_payload()), encoding="utf-8")

    subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input",
            str(payload_path),
            "--json-output",
            str(json_path),
            "--markdown-output",
            str(markdown_path),
            "--fail-on-degraded",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert json.loads(json_path.read_text(encoding="utf-8"))["health"] == "healthy"
    assert "Health: HEALTHY" in markdown_path.read_text(encoding="utf-8")


def test_cli_fail_on_degraded_returns_one_without_secret_echo(tmp_path: Path) -> None:
    payload_path = tmp_path / "monitor.json"
    json_path = tmp_path / "alert.json"
    payload_path.write_text(json.dumps(_payload("fail", "Bearer abc.def.ghi")), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input",
            str(payload_path),
            "--json-output",
            str(json_path),
            "--fail-on-degraded",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "Bearer abc" not in result.stdout
    assert "Bearer abc" not in result.stderr
    assert "Bearer abc" not in json_path.read_text(encoding="utf-8")
