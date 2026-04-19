#!/usr/bin/env python3
"""
Tests for the Stage D Remote MCP proof runner.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "stage_d_smoke.py"
sys.path.insert(0, str(SCRIPT.parent))
import verify_audit  # noqa: E402


def test_stage_d_fixture_e2e_passes(tmp_path: Path) -> None:
    evidence_dir = tmp_path / "audit-evidence"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--fixture",
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

    assert results["authenticated-ping"] == "pass"
    assert results["anonymous-rejected"] == "pass"
    assert results["origin-spoof-non-authoritative"] == "pass"
    assert results["pii-handoff-rejected"] == "pass"
    assert results["scrub-pii-remote-rejected"] == "pass"
    assert results["audit-valid"] == "pass"
    assert results["audit-tamper-negative"] == "pass"
    assert results["stdio-after-tunnel-stop"] == "skip"
    assert sorted(path.name for path in evidence_dir.iterdir()) == [
        "2026-04-19.jsonl",
        "2026-04-19.manifest.json",
    ]
    audit_text = (evidence_dir / "2026-04-19.jsonl").read_text(encoding="utf-8")
    assert "123-45-6789" not in audit_text
    rows = [json.loads(line) for line in audit_text.splitlines() if line.strip()]
    handoff = next(row for row in rows if row["tool"] == "som.handoff")
    assert handoff["args_hmac"] == verify_audit.compute_entry_hmac(
        {"tool": "som.handoff", "arguments": {"packet": {"prompt": "patient SSN 123-45-6789"}}},
        "fixture-audit-key",
    )
    assert handoff["args_hmac"] != verify_audit.compute_entry_hmac({"tool": "som.handoff"}, "fixture-audit-key")


def test_stage_d_live_mode_fails_fast_without_required_env() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        env={},
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "missing required live proof configuration" in result.stderr
    assert "SOM_REMOTE_MCP_AUDIT_DIR or --audit-dir" in result.stderr
