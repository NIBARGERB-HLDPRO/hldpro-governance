#!/usr/bin/env python3
"""
Deterministic verification tests for Remote MCP audit logs.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import verify_audit  # type: ignore[import]


def _build_entry(
    *,
    seq: int,
    prev_hash: str,
    principal: str,
    session_jti: str,
    tool: str,
    status: str = "ok",
    reject_reason: Any = None,
    latency_ms: int = 0,
    args: Dict[str, Any],
    hmac_key: str,
) -> Dict[str, Any]:
    base = {
        "ts": "2026-04-14T12:00:00.000Z",
        "seq": seq,
        "prev_hash": prev_hash,
        "principal": principal,
        "session_jti": session_jti,
        "tool": tool,
        "args_hmac": verify_audit.compute_entry_hmac(args, hmac_key),
        "status": status,
        "reject_reason": reject_reason,
        "latency_ms": latency_ms,
    }
    base["entry_hmac"] = verify_audit.compute_entry_hmac(base, hmac_key)
    return base


def _write_audit_file(path: Path, entries: List[Dict[str, Any]], hmac_key: str) -> None:
    lines = [json.dumps(entry, separators=(",", ":"), ensure_ascii=False) for entry in entries]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    payload = {
        "first_hash": verify_audit.compute_entry_hash(entries[0]),
        "last_hash": verify_audit.compute_entry_hash(entries[-1]),
        "entry_count": len(entries),
        "sha256_of_file": verify_audit.compute_sha256(path.read_bytes()),
    }
    path.with_suffix(".manifest.json").write_text(
        json.dumps(payload, separators=(",", ":")),
        encoding="utf-8",
    )


def _make_chain_entries(hmac_key: str, count: int = 2) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    prev_hash = "0" * 64
    for index in range(count):
        entry = _build_entry(
            seq=index,
            prev_hash=prev_hash,
            principal=f"user-{index}",
            session_jti=f"jti-{index}",
            tool="som.ping",
            args={"arg": index},
            hmac_key=hmac_key,
        )
        prev_hash = verify_audit.compute_entry_hash(entry)
        entries.append(entry)
    return entries


def test_verify_audit_valid_chain_passes() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        audit_dir = Path(tmpdir) / "raw" / "remote-mcp-audit"
        audit_dir.mkdir(parents=True, exist_ok=True)
        hmac_key = "test-hmac-key"
        entries = _make_chain_entries(hmac_key, count=3)
        log_file = audit_dir / "2026-04-14.jsonl"

        _write_audit_file(log_file, entries, hmac_key)

        success, errors = verify_audit.verify_audit_dir(
            audit_dir, hmac_key=hmac_key, require_hmac_key=False
        )
        assert success, errors


def test_verify_audit_tamper_detects_chain_break() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        audit_dir = Path(tmpdir) / "raw" / "remote-mcp-audit"
        audit_dir.mkdir(parents=True, exist_ok=True)
        hmac_key = "test-hmac-key"
        entries = _make_chain_entries(hmac_key, count=3)
        log_file = audit_dir / "2026-04-14.jsonl"
        _write_audit_file(log_file, entries, hmac_key)

        # Tamper payload and re-hash not updated, chain should fail.
        tampered = entries.copy()
        tampered[1]["seq"] = 999
        tampered[1]["entry_hmac"] = verify_audit.compute_entry_hmac(tampered[1], hmac_key)
        _write_audit_file(log_file, tampered, hmac_key)

        success, errors = verify_audit.verify_audit_dir(
            audit_dir, hmac_key=hmac_key, require_hmac_key=False
        )
        assert not success
        assert any("seq 999" in err or "prev_hash mismatch" in err for err in errors)


def test_verify_audit_require_hmac_key_fails_when_missing() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        audit_dir = Path(tmpdir) / "raw" / "remote-mcp-audit"
        audit_dir.mkdir(parents=True, exist_ok=True)
        hmac_key = "test-hmac-key"
        entries = _make_chain_entries(hmac_key, count=1)
        log_file = audit_dir / "2026-04-14.jsonl"
        _write_audit_file(log_file, entries, hmac_key)

        old = os.environ.pop("SOM_REMOTE_MCP_AUDIT_HMAC_KEY", None)
        try:
            success, errors = verify_audit.verify_audit_dir(
                audit_dir,
                hmac_key=None,
                require_hmac_key=True,
            )
        finally:
            if old is not None:
                os.environ["SOM_REMOTE_MCP_AUDIT_HMAC_KEY"] = old

        assert not success
        assert any("SOM_REMOTE_MCP_AUDIT_HMAC_KEY is required" in err for err in errors)


def test_verify_audit_absent_dir_is_noop() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        missing_dir = Path(tmpdir) / "raw" / "remote-mcp-audit"
        success, errors = verify_audit.verify_audit_dir(missing_dir)
        assert success
        assert errors == []
