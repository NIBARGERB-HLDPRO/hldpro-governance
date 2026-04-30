#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

import check_overlord_backlog_github_alignment as backlog_alignment


ISSUE_BRANCH_RE = re.compile(r"(?:^|[-_/])issue-(\d+)\b")
ACTIVE_SECTIONS = ("## Planned", "## In Progress")


def fail(message: str) -> None:
    print(f"FAIL governance-issue-branch-parity: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", default="", help="Branch name override for tests")
    parser.add_argument("--backlog-path", type=Path, default=Path("OVERLORD_BACKLOG.md"))
    return parser.parse_args()


def current_branch(explicit_branch: str) -> str:
    if explicit_branch:
        return explicit_branch
    env_branch = os.environ.get("GOVERNANCE_BRANCH_NAME", "").strip()
    if env_branch:
        return env_branch
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        fail(f"could not resolve current branch: {detail}")
    return result.stdout.strip()


def branch_issue_number(branch: str) -> int | None:
    numbers = {int(match.group(1)) for match in ISSUE_BRANCH_RE.finditer(branch)}
    if not numbers:
        return None
    if len(numbers) > 1:
        ordered = ", ".join(f"#{number}" for number in sorted(numbers))
        fail(f"branch {branch!r} contains multiple issue numbers ({ordered})")
    return next(iter(numbers))


def active_governance_issue_numbers(backlog_path: Path) -> dict[int, set[str]]:
    if not backlog_path.exists():
        fail(f"missing backlog file: {backlog_path}")
    lines = backlog_path.read_text(encoding="utf-8").splitlines()
    sections: dict[int, set[str]] = {}

    for index, section_name in enumerate(ACTIVE_SECTIONS):
        end_headers = list(ACTIVE_SECTIONS[index + 1 :]) or ["## Done"]
        section_lines = backlog_alignment.collect_section_lines(lines, section_name, end_headers)
        header_row = None
        issue_index = None
        for line in section_lines:
            row = backlog_alignment.parse_markdown_row(line)
            if not row:
                continue
            if row[0] == "Item":
                header_row = row
                issue_index = backlog_alignment.issue_column_index(row)
                if issue_index is None:
                    fail(f"{section_name} table is missing an Issue column")
                continue
            if header_row is None or issue_index is None:
                continue
            issue_cell = row[issue_index] if issue_index < len(row) else ""
            for number in backlog_alignment.issue_numbers(issue_cell):
                sections.setdefault(number, set()).add(section_name.removeprefix("## "))
    return sections


def check_branch_parity(branch: str, backlog_path: Path) -> str:
    issue_number = branch_issue_number(branch)
    if issue_number is None:
        return f"PASS governance-issue-branch-parity: branch {branch!r} is not issue-backed; no active tracker check required"

    active_issues = active_governance_issue_numbers(backlog_path)
    if issue_number not in active_issues:
        fail(
            f"branch {branch!r} maps to issue #{issue_number}, but #{issue_number} is not listed in the active "
            f"governance tracker sections of {backlog_path}"
        )

    sections = ", ".join(sorted(active_issues[issue_number]))
    return (
        f"PASS governance-issue-branch-parity: branch {branch!r} maps to active governance issue "
        f"#{issue_number} ({sections})"
    )


def main() -> None:
    args = parse_args()
    branch = current_branch(args.branch)
    print(check_branch_parity(branch, args.backlog_path))


if __name__ == "__main__":
    main()
