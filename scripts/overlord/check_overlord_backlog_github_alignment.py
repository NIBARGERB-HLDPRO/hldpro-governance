#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


POLICY_LINE = (
    "GitHub Issues are the execution backlog/system of record for governance work. "
    "This file is the local roadmap/status mirror for cross-repo planning, active issue-backed work, "
    "and completed-history entries that still need governance-level visibility."
)


def fail(message: str) -> None:
    print(f"FAIL overlord-backlog-github-alignment: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_markdown_row(line: str) -> list[str] | None:
    if not line.strip().startswith("|"):
        return None
    cells = [cell.strip() for cell in line.split("|")[1:-1]]
    if len(cells) < 2:
        return None
    if all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells):
        return None
    return cells


def collect_section_lines(lines: list[str], start_header: str, end_headers: list[str]) -> list[str]:
    try:
        start_index = next(i for i, line in enumerate(lines) if line.strip() == start_header)
    except StopIteration:
        fail(f"missing section header: {start_header}")
    end_index = len(lines)
    for i in range(start_index + 1, len(lines)):
        if lines[i].strip() in end_headers:
            end_index = i
            break
    return lines[start_index + 1 : end_index]


def has_issue_ref(text: str) -> bool:
    return re.search(r"#\d+\b", text) is not None


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    backlog_path = repo_root / "OVERLORD_BACKLOG.md"
    content = backlog_path.read_text(encoding="utf-8")

    if POLICY_LINE not in content:
        fail("OVERLORD_BACKLOG.md must state that GitHub Issues are the execution backlog/system of record.")

    lines = content.splitlines()
    planned_lines = collect_section_lines(lines, "## Planned", ["## In Progress"])
    in_progress_lines = collect_section_lines(lines, "## In Progress", ["## Done"])

    violations: list[str] = []
    for line in planned_lines + in_progress_lines:
        row = parse_markdown_row(line)
        if not row:
            continue
        first_cell = row[0]
        if first_cell == "Item":
            continue
        if not has_issue_ref(line):
            violations.append(f"- actionable backlog row without GitHub issue reference: {first_cell}")

    if violations:
        fail("OVERLORD_BACKLOG.md contains actionable local backlog drift:\n" + "\n".join(violations))

    print(
        "PASS overlord-backlog-github-alignment: actionable governance backlog remains issue-backed "
        "and OVERLORD_BACKLOG stays roadmap-only"
    )


if __name__ == "__main__":
    main()
