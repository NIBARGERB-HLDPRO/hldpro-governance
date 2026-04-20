#!/usr/bin/env python3
"""Tests for the recurring Remote MCP live health monitor."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "live_health_monitor.py"
sys.path.insert(0, str(SCRIPT.parent))
import live_health_monitor  # noqa: E402


def test_fixture_monitor_e2e_passes_and_scans_evidence(tmp_path: Path) -> None:
    evidence_dir = tmp_path / "monitor-evidence"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--mode",
            "fixture",
            "--fixture-evidence-dir",
            str(evidence_dir),
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    results = {item["name"]: item["status"] for item in payload["results"]}

    assert payload["mode"] == "fixture"
    assert results["authenticated-ping"] == "pass"
    assert results["anonymous-rejected"] == "pass"
    assert results["audit-valid"] == "pass"
    assert results["audit-tamper-negative"] == "pass"
    assert results["evidence-safety-scan"] == "pass"
    assert (evidence_dir / "2026-04-19.jsonl").is_file()


def test_live_monitor_fails_fast_without_required_configuration() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--mode", "live", "--json"],
        env={},
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "missing required live monitor configuration" in result.stderr
    assert "SOM_MCP_URL" in result.stderr
    assert "SOM_REMOTE_MCP_AUDIT_HMAC_KEY or --audit-hmac-key" in result.stderr


def test_evidence_scan_rejects_sensitive_material(tmp_path: Path) -> None:
    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()
    (evidence_dir / "bad.jsonl").write_text(
        '{"payload":"Bearer abc.def.ghi","pii":"123-45-6789","jwt":"eyJabc123456789.eyJdef123456789"}\n',
        encoding="utf-8",
    )

    result = live_health_monitor._scan_evidence_dir(evidence_dir)

    assert result.status == "fail"
    assert "raw-ssn" in result.detail
    assert "bearer-token" in result.detail
    assert "jwt-fragment" in result.detail
