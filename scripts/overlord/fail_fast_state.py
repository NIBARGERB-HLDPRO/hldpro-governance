#!/usr/bin/env python3
"""Shared helper: read/write ~/.claude/fail-fast-state.json for PostToolUse fail-fast gate.

Schema:
    {
      "errors": [
        {
          "pattern": str,      # normalised error substring
          "count": int,        # times seen unresolved
          "last_seen": str,    # ISO-8601 UTC timestamp
          "resolved": bool
        }
      ]
    }

Subcommands:
    check    — reads stdin for error text; exits 1 if a matching unresolved
               pattern has been seen 2+ times (recurrence detected).
    record   — reads stdin for error text; appends/updates entry, exits 0.
    resolve <pattern> — marks pattern resolved, exits 0.

Exit codes:
    0 — clean / recorded / resolved
    1 — recurrence detected (check subcommand only)
    2 — usage error
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATE_PATH = Path.home() / ".claude" / "fail-fast-state.json"

# Minimum recurrence count before check exits 1
RECURRENCE_THRESHOLD = 2

# Patterns that are too generic to track (avoid false positives)
_SKIP_PATTERNS: tuple[str, ...] = ("", "error", "warning", "failed", "exception")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"errors": []}
    try:
        raw = STATE_PATH.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, dict) or not isinstance(data.get("errors"), list):
            return {"errors": []}
        return data
    except (OSError, json.JSONDecodeError):
        return {"errors": []}


def _save_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def _extract_pattern(text: str) -> str:
    """Extract a normalised pattern string from raw error text."""
    # Take first non-empty line, strip ANSI, lowercase, trim to 120 chars
    for line in text.splitlines():
        cleaned = re.sub(r"\x1b\[[0-9;]*m", "", line).strip().lower()
        if cleaned and cleaned not in _SKIP_PATTERNS:
            return cleaned[:120]
    return ""


def _find_entry(errors: list[dict[str, Any]], pattern: str) -> dict[str, Any] | None:
    for entry in errors:
        if isinstance(entry, dict) and entry.get("pattern") == pattern:
            return entry
    return None


def cmd_check(stdin_text: str) -> int:
    """Exit 1 if a matching unresolved pattern has recurred >= RECURRENCE_THRESHOLD times."""
    pattern = _extract_pattern(stdin_text)
    if not pattern:
        return 0

    state = _load_state()
    entry = _find_entry(state["errors"], pattern)
    if entry is None:
        return 0
    if entry.get("resolved", False):
        return 0
    count = entry.get("count", 0)
    if count >= RECURRENCE_THRESHOLD:
        print(
            f"FAIL-FAST: error pattern '{pattern}' has recurred {count} time(s) without resolution.",
            file=sys.stderr,
        )
        return 1
    return 0


def cmd_record(stdin_text: str) -> int:
    """Append or increment the pattern entry; exit 0."""
    pattern = _extract_pattern(stdin_text)
    if not pattern:
        return 0

    state = _load_state()
    entry = _find_entry(state["errors"], pattern)
    if entry is None:
        state["errors"].append(
            {
                "pattern": pattern,
                "count": 1,
                "last_seen": _now_iso(),
                "resolved": False,
            }
        )
    else:
        if not entry.get("resolved", False):
            entry["count"] = entry.get("count", 0) + 1
        entry["last_seen"] = _now_iso()

    _save_state(state)
    return 0


def cmd_resolve(pattern_arg: str) -> int:
    """Mark a pattern resolved; exit 0."""
    pattern = pattern_arg.strip().lower()[:120]
    if not pattern:
        print("ERROR: resolve requires a non-empty pattern argument", file=sys.stderr)
        return 2

    state = _load_state()
    entry = _find_entry(state["errors"], pattern)
    if entry is None:
        # Not found — treat as success (idempotent)
        return 0
    entry["resolved"] = True
    entry["last_seen"] = _now_iso()
    _save_state(state)
    print(f"RESOLVED: pattern '{pattern}' marked resolved.")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    subcommand = args[0]

    try:
        if subcommand == "check":
            stdin_text = sys.stdin.read() if not sys.stdin.isatty() else ""
            return cmd_check(stdin_text)

        elif subcommand == "record":
            stdin_text = sys.stdin.read() if not sys.stdin.isatty() else ""
            return cmd_record(stdin_text)

        elif subcommand == "resolve":
            if len(args) < 2:
                print("ERROR: resolve requires a pattern argument", file=sys.stderr)
                return 2
            return cmd_resolve(args[1])

        else:
            print(f"ERROR: unknown subcommand {subcommand!r}. Use check, record, or resolve.", file=sys.stderr)
            return 2

    except Exception as exc:  # noqa: BLE001
        # Infrastructure failure — fail-open (exit 0) so the gate doesn't block
        # legitimate work due to state-file I/O issues.
        print(f"WARN fail_fast_state: infrastructure error (fail-open): {exc}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
