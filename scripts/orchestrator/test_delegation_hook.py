#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / "hooks" / "code-write-gate.sh"


def _run_hook(payload: dict, *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = dict(os.environ)
    if env:
        merged_env.update(env)
    return subprocess.run(
        ["bash", str(HOOK)],
        cwd=REPO_ROOT,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        env=merged_env,
        check=False,
    )


def _payload(tool_name: str, task_text: str) -> dict:
    return {
        "tool_name": tool_name,
        "tool_input": {
            "description": task_text,
        },
    }


def test_hook_blocks_agent_owned_work_before_file_path_logic() -> None:
    with tempfile.TemporaryDirectory() as raw:
        result = _run_hook(
            _payload("Agent", "Audit SQL migrations for schema inconsistencies"),
            env={"DELEGATION_GATE_LOG": str(Path(raw) / "governance.log")},
        )

        assert result.returncode == 2
        output = json.loads(result.stdout)
        assert output["decision"] == "block"
        assert "migration-validator" in output["reason"]


def test_hook_warns_for_implementation_scoped_explore() -> None:
    with tempfile.TemporaryDirectory() as raw:
        log_path = Path(raw) / "governance.log"
        result = _run_hook(
            _payload("Explore", "Audit SQL migrations for schema inconsistencies"),
            env={"DELEGATION_GATE_LOG": str(log_path)},
        )

        assert result.returncode == 0
        assert result.stdout == ""
        assert "WARN Explore owner=migration-validator" in log_path.read_text(encoding="utf-8")


def test_hook_allows_read_even_when_text_matches_owned_work() -> None:
    with tempfile.TemporaryDirectory() as raw:
        log_path = Path(raw) / "governance.log"
        result = _run_hook(
            _payload("Read", "Audit SQL migrations for schema inconsistencies"),
            env={"DELEGATION_GATE_LOG": str(log_path)},
        )

        assert result.returncode == 0
        assert result.stdout == ""
        assert not log_path.exists()


def test_hook_bypass_allows_and_logs() -> None:
    with tempfile.TemporaryDirectory() as raw:
        log_path = Path(raw) / "governance.log"
        result = _run_hook(
            _payload("Agent", "--bypass-delegation-gate Audit SQL migrations for schema inconsistencies"),
            env={"DELEGATION_GATE_LOG": str(log_path)},
        )

        assert result.returncode == 0
        assert "BYPASS Agent" in log_path.read_text(encoding="utf-8")


def test_hook_quoted_bypass_flag_inside_prompt_does_not_bypass() -> None:
    with tempfile.TemporaryDirectory() as raw:
        result = _run_hook(
            _payload("Agent", "Audit SQL migrations; example flag `--bypass-delegation-gate` is not approval"),
            env={"DELEGATION_GATE_LOG": str(Path(raw) / "governance.log")},
        )

        assert result.returncode == 2
        output = json.loads(result.stdout)
        assert output["decision"] == "block"
        assert "migration-validator" in output["reason"]


def test_hook_blocks_task_tool_owned_work() -> None:
    with tempfile.TemporaryDirectory() as raw:
        result = _run_hook(
            _payload("Task", "Audit SQL migrations for schema inconsistencies"),
            env={"DELEGATION_GATE_LOG": str(Path(raw) / "governance.log")},
        )

        assert result.returncode == 2
        output = json.loads(result.stdout)
        assert "migration-validator" in output["reason"]


def test_hook_configured_mcp_endpoint_fails_open_on_unavailable_gate() -> None:
    with tempfile.TemporaryDirectory() as raw:
        result = _run_hook(
            _payload("Agent", "Audit SQL migrations for schema inconsistencies"),
            env={
                "DELEGATION_GATE_LOG": str(Path(raw) / "governance.log"),
                "DELEGATION_GATE_URL": "http://127.0.0.1:9/delegation-gate",
            },
        )

        assert result.returncode == 0
        assert result.stdout == ""


def test_hook_preserves_new_code_file_block() -> None:
    with tempfile.TemporaryDirectory() as raw:
        target = Path(raw) / "new_worker.py"
        result = _run_hook(
            {
                "tool_name": "Write",
                "tool_input": {
                    "file_path": str(target),
                },
            },
            env={"DELEGATION_GATE_LOG": str(Path(raw) / "governance.log")},
        )

        assert result.returncode == 2
        output = json.loads(result.stdout)
        assert output["decision"] == "block"
        assert "approved Worker" in output["reason"]
