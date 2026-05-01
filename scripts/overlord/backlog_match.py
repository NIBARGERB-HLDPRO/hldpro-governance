#!/usr/bin/env python3
"""Shared helper: check whether a given issue number has an open backlog entry.

Usage:
    python3 scripts/overlord/backlog_match.py <issue_number>

Exit codes:
    0 — open entry found in docs/PROGRESS.md or OVERLORD_BACKLOG.md
    1 — no open entry found (or issue number invalid)

Consumed by:
    hooks/backlog-check.sh
    CI backlog-alignment gates
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent

DONE_SECTION_RE = re.compile(
    r"^#{1,4}\s*(done|completed|closed|finished|archived)",
    re.IGNORECASE,
)


def _issue_pattern(issue_number: int) -> re.Pattern[str]:
    return re.compile(r"#" + str(issue_number) + r"\b")


def _is_in_done_section(lines: list[str], line_index: int) -> bool:
    """Return True if line_index falls inside a Done/Completed section heading."""
    for i in range(line_index - 1, -1, -1):
        if DONE_SECTION_RE.match(lines[i]):
            return True
        # Stop looking once we hit any other heading at same or higher level
        if re.match(r"^#{1,4}\s", lines[i]) and not DONE_SECTION_RE.match(lines[i]):
            return False
    return False


def search_file(path: Path, issue_number: int) -> bool:
    """Return True if path contains an open (non-Done) entry for issue_number."""
    if not path.exists():
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False

    pattern = _issue_pattern(issue_number)
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if pattern.search(line):
            if not _is_in_done_section(lines, idx):
                return True
    return False


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    try:
        issue_number = int(args[0])
    except ValueError:
        print(f"ERROR: issue number must be an integer, got {args[0]!r}", file=sys.stderr)
        return 1

    if issue_number <= 0:
        print(f"ERROR: issue number must be positive, got {issue_number}", file=sys.stderr)
        return 1

    progress_path = REPO_ROOT / "docs" / "PROGRESS.md"
    backlog_path = REPO_ROOT / "OVERLORD_BACKLOG.md"

    found_in_progress = search_file(progress_path, issue_number)
    found_in_backlog = search_file(backlog_path, issue_number)

    if found_in_progress:
        print(f"FOUND: #{issue_number} has an open entry in docs/PROGRESS.md")
        return 0
    if found_in_backlog:
        print(f"FOUND: #{issue_number} has an open entry in OVERLORD_BACKLOG.md")
        return 0

    print(
        f"NOT FOUND: #{issue_number} has no open entry in docs/PROGRESS.md or OVERLORD_BACKLOG.md",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
