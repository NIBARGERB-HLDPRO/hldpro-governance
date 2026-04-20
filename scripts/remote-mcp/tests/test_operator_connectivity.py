#!/usr/bin/env python3
"""Tests for the no-secret Remote MCP operator connectivity preflight."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "operator_connectivity.py"
sys.path.insert(0, str(SCRIPT.parent))
import operator_connectivity  # noqa: E402


def test_fixture_preflight_proves_request_response_without_live_secrets() -> None:
    payload, exit_code = operator_connectivity.build_payload("fixture", Path.cwd())
    checks = {item["name"]: item for item in payload["checks"]}

    assert exit_code == 0
    assert payload["ready"] is True
    assert checks["som-ping-request-response"]["status"] == "pass"
    assert "fixture som.ping returned a response" in checks["som-ping-request-response"]["detail"]


def test_live_preflight_fails_closed_before_request_when_config_missing(monkeypatch) -> None:
    for name in [
        "SOM_MCP_URL",
        "SOM_MCP_TOKEN",
        "SOM_REMOTE_MCP_JWT",
        "CF_ACCESS_CLIENT_ID",
        "CF_ACCESS_CLIENT_SECRET",
    ]:
        monkeypatch.delenv(name, raising=False)

    payload, exit_code = operator_connectivity.build_payload("live", Path.cwd())

    assert exit_code == 2
    assert payload["ready"] is False
    assert "SOM_MCP_URL" in payload["missing_live_config"]
    assert "SOM_MCP_TOKEN or SOM_REMOTE_MCP_JWT" in payload["missing_live_config"]
    rendered = json.dumps(payload)
    assert "Bearer " not in rendered
    assert "CF-Access" not in rendered


def test_cli_writes_json_output(tmp_path: Path) -> None:
    output = tmp_path / "preflight.json"
    env = os.environ.copy()
    for name in [
        "SOM_MCP_URL",
        "SOM_MCP_TOKEN",
        "SOM_REMOTE_MCP_JWT",
        "CF_ACCESS_CLIENT_ID",
        "CF_ACCESS_CLIENT_SECRET",
    ]:
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
    assert "SOM_MCP_URL" in payload["missing_live_config"]


def test_launchctl_absence_is_non_blocking(monkeypatch) -> None:
    def missing_launchctl(*args, **kwargs):  # noqa: ANN002, ANN003
        raise FileNotFoundError("launchctl")

    monkeypatch.setattr(operator_connectivity.subprocess, "run", missing_launchctl)

    payload, exit_code = operator_connectivity.build_payload("fixture", Path.cwd())
    checks = {item["name"]: item for item in payload["checks"]}

    assert exit_code == 0
    assert payload["ready"] is True
    assert checks["launchd-loaded"]["status"] == "warn"
