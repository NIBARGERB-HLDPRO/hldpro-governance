#!/usr/bin/env python3
"""
Deterministic validator for Remote MCP audit logs.

Verifies:
- JSON schema shape
- per-file sequence continuity
- hash-chain continuity via prev_hash
- optional/required entry_hmac verification
- manifest consistency

Default behavior is no-op pass when audit directory does not exist.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

AUDIT_HMAC_ENV = "SOM_REMOTE_MCP_AUDIT_HMAC_KEY"
DEFAULT_AUDIT_DIR = Path("raw/remote-mcp-audit")
REQUIRED_FIELDS: Tuple[str, ...] = (
    "ts",
    "seq",
    "prev_hash",
    "principal",
    "session_jti",
    "tool",
    "args_hmac",
    "status",
    "reject_reason",
    "latency_ms",
    "entry_hmac",
)


def canonical_json(obj: Dict[str, Any]) -> bytes:
    """Return canonical JSON bytes for cryptographic checks."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def compute_sha256(data: bytes) -> str:
    """Compute SHA-256 hex digest."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def compute_entry_hmac(entry: Dict[str, Any], key: str) -> str:
    """Compute entry HMAC over every field except `entry_hmac` itself."""
    entry_copy = {k: v for k, v in entry.items() if k != "entry_hmac"}
    return hmac.new(key.encode("utf-8"), canonical_json(entry_copy), hashlib.sha256).hexdigest()


def compute_entry_hash(entry: Dict[str, Any]) -> str:
    """Compute chain hash for one entry."""
    entry_copy = {k: v for k, v in entry.items() if k != "entry_hmac"}
    return compute_sha256(canonical_json(entry_copy))


def _read_jsonl(path: Path) -> List[Tuple[int, Dict[str, Any]]]:
    """Read a JSONL file into (line_no, payload) tuples."""
    rows: List[Tuple[int, Dict[str, Any]]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw_line in enumerate(handle, 1):
            raw_line = raw_line.strip()
            if not raw_line:
                continue

            try:
                payload = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.name}:{line_no}: invalid JSON: {exc}") from exc

            rows.append((line_no, payload))
    return rows


def _validate_schema(entries: Sequence[Tuple[int, Dict[str, Any]]], path: Path) -> List[str]:
    """Validate required fields and coarse types."""
    errors: List[str] = []
    for line_no, payload in entries:
        if not isinstance(payload, dict):
            errors.append(f"{path.name}:{line_no}: entry is not an object")
            continue

        for field in REQUIRED_FIELDS:
            if field not in payload:
                errors.append(f"{path.name}:{line_no}: missing required field `{field}`")

        if not isinstance(payload.get("seq"), int) or payload.get("seq") < 0:
            errors.append(f"{path.name}:{line_no}: seq must be an integer >= 0")

        if payload.get("status") not in {"ok", "rejected", "error"}:
            errors.append(f"{path.name}:{line_no}: unknown status: {payload.get('status')!r}")

    return errors


def _verify_sequence(entries: Sequence[Tuple[int, Dict[str, Any]]], path: Path) -> List[str]:
    errors: List[str] = []
    for i, (line_no, payload) in enumerate(entries):
        expected = i
        if payload.get("seq") != expected:
            errors.append(
                f"{path.name}:{line_no}: seq {payload.get('seq')} != expected {expected}"
            )
    return errors


def _verify_chain(entries: Sequence[Tuple[int, Dict[str, Any]]], path: Path) -> List[str]:
    errors: List[str] = []
    prev_hash = "0" * 64
    for line_no, payload in entries:
        if payload.get("prev_hash") != prev_hash:
            errors.append(
                f"{path.name}:{line_no}: prev_hash mismatch (expected {prev_hash}, got {payload.get('prev_hash')})"
            )
        prev_hash = compute_entry_hash(payload)
    return errors


def _verify_manifest(path: Path, entries: Sequence[Tuple[int, Dict[str, Any]]]) -> List[str]:
    manifest_path = path.with_suffix(".manifest.json")
    errors: List[str] = []
    if not manifest_path.exists():
        if not entries:
            return errors
        errors.append(f"{manifest_path.name}: manifest file missing")
        return errors

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{manifest_path.name}: invalid json: {exc}")
        return errors

    if not isinstance(manifest, dict):
        errors.append(f"{manifest_path.name}: manifest is not an object")
        return errors

    for field in ("first_hash", "last_hash", "entry_count", "sha256_of_file"):
        if field not in manifest:
            errors.append(f"{manifest_path.name}: missing field `{field}`")

    if errors:
        return errors

    expected_count = len(entries)
    if manifest.get("entry_count") != expected_count:
        errors.append(
            f"{manifest_path.name}: entry_count {manifest.get('entry_count')} != expected {expected_count}"
        )

    payloads = [payload for _, payload in entries]
    expected_first = compute_entry_hash(payloads[0])
    expected_last = compute_entry_hash(payloads[-1])
    if manifest.get("first_hash") != expected_first:
        errors.append(f"{manifest_path.name}: first_hash mismatch")
    if manifest.get("last_hash") != expected_last:
        errors.append(f"{manifest_path.name}: last_hash mismatch")

    expected_file_sha = compute_sha256(path.read_bytes())
    if manifest.get("sha256_of_file") != expected_file_sha:
        errors.append(f"{manifest_path.name}: sha256_of_file mismatch")

    return errors


def _collect_file_errors(
    path: Path, hmac_key: Optional[str], require_hmac_key: bool
) -> List[str]:
    errors: List[str] = []
    try:
        entries = _read_jsonl(path)
    except ValueError as exc:
        return [str(exc)]

    if not entries:
        return errors

    errors.extend(_validate_schema(entries, path))
    errors.extend(_verify_sequence(entries, path))
    errors.extend(_verify_chain(entries, path))

    if require_hmac_key and not hmac_key:
        errors.append(
            f"{path.name}: SOM_REMOTE_MCP_AUDIT_HMAC_KEY is required but not set"
        )
        return errors

    if hmac_key:
        for line_no, payload in entries:
            expected = compute_entry_hmac(payload, hmac_key)
            provided = payload.get("entry_hmac")
            if not isinstance(provided, str) or not hmac.compare_digest(expected, provided):
                errors.append(f"{path.name}:{line_no}: entry_hmac mismatch")

    errors.extend(_verify_manifest(path, entries))
    return errors


def verify_audit_dir(
    audit_dir: str | Path = DEFAULT_AUDIT_DIR,
    *,
    hmac_key: Optional[str] = None,
    require_hmac_key: bool = False,
) -> Tuple[bool, List[str]]:
    """
    Verify all JSONL files under an audit directory.
    Returns (success, errors).
    """
    audit_path = Path(audit_dir)
    if not audit_path.exists():
        return True, []

    if not audit_path.is_dir():
        return False, [f"{audit_path} is not a directory"]

    errors: List[str] = []
    for path in sorted(audit_path.glob("*.jsonl")):
        errors.extend(_collect_file_errors(path, hmac_key=hmac_key, require_hmac_key=require_hmac_key))

    return len(errors) == 0, errors


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Remote MCP audit logs.")
    parser.add_argument(
        "audit_dir",
        nargs="?",
        default=str(DEFAULT_AUDIT_DIR),
        help="Audit directory (default: raw/remote-mcp-audit)",
    )
    parser.add_argument(
        "--require-hmac-key",
        action="store_true",
        help="Fail verification if SOM_REMOTE_MCP_AUDIT_HMAC_KEY is missing",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    hmac_key = os.environ.get(AUDIT_HMAC_ENV)
    success, errors = verify_audit_dir(
        args.audit_dir, hmac_key=hmac_key, require_hmac_key=args.require_hmac_key
    )
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
