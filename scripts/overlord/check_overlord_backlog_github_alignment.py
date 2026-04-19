#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


REPO = "NIBARGERB-HLDPRO/hldpro-governance"
POLICY_LINE = (
    "GitHub Issues are the execution backlog/system of record for governance work. "
    "This file is the local roadmap/status mirror for cross-repo planning, active issue-backed work, "
    "and completed-history entries that still need governance-level visibility."
)
ISSUE_REF_RE = re.compile(r"#(\d+)\b")


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
    return ISSUE_REF_RE.search(text) is not None


def issue_numbers(text: str) -> list[int]:
    return [int(match.group(1)) for match in ISSUE_REF_RE.finditer(text)]


def issue_column_index(header_row: list[str]) -> int | None:
    for index, cell in enumerate(header_row):
        if cell.lower() == "issue":
            return index
    return None


def check_github_issue_open(issue_number: int) -> tuple[bool, str]:
    env = os.environ.copy()
    token = env.get("GH_TOKEN") or env.get("GITHUB_TOKEN")
    if token:
        env["GH_TOKEN"] = token

    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{REPO}/issues/{issue_number}"],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
    except FileNotFoundError:
        return False, "gh CLI not found; cannot verify issue state"

    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown gh api error"
        return False, detail

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return False, f"could not parse GitHub issue response: {exc}"

    title = payload.get("title", "(no title)")
    state = payload.get("state", "")
    if state != "open":
        return False, f"issue is {state!r}, expected 'open': {title!r}"
    return True, title


def validate_section(lines: list[str], section_name: str) -> list[str]:
    violations: list[str] = []
    header_row: list[str] | None = None
    issue_index: int | None = None

    for line in lines:
        row = parse_markdown_row(line)
        if not row:
            continue
        first_cell = row[0]
        if first_cell == "Item":
            header_row = row
            issue_index = issue_column_index(row)
            if issue_index is None:
                violations.append(f"- {section_name} table is missing an Issue column")
            continue

        if header_row is None or issue_index is None:
            violations.append(f"- {section_name} actionable row appears before a valid table header: {first_cell}")
            continue

        issue_cell = row[issue_index] if issue_index < len(row) else ""
        numbers = issue_numbers(issue_cell)
        if not numbers:
            violations.append(
                f"- {section_name} actionable backlog row without GitHub issue reference in Issue column: {first_cell}"
            )
            continue

        for number in numbers:
            ok, detail = check_github_issue_open(number)
            if not ok:
                violations.append(f"- {section_name} row references non-open issue #{number}: {first_cell} ({detail})")

    return violations


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    backlog_path = repo_root / "OVERLORD_BACKLOG.md"
    content = backlog_path.read_text(encoding="utf-8")

    if POLICY_LINE not in content:
        fail("OVERLORD_BACKLOG.md must state that GitHub Issues are the execution backlog/system of record.")

    lines = content.splitlines()
    planned_lines = collect_section_lines(lines, "## Planned", ["## In Progress"])
    in_progress_lines = collect_section_lines(lines, "## In Progress", ["## Done"])

    violations = validate_section(planned_lines, "Planned")
    violations.extend(validate_section(in_progress_lines, "In Progress"))

    if violations:
        fail("OVERLORD_BACKLOG.md contains actionable local backlog drift:\n" + "\n".join(violations))

    print(
        "PASS overlord-backlog-github-alignment: actionable governance backlog remains issue-backed "
        "and OVERLORD_BACKLOG stays roadmap-only"
    )


if __name__ == "__main__":
    main()
