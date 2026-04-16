#!/usr/bin/env python3
"""
validate_backlog_gh_sync.py

Parse OVERLORD_BACKLOG.md ## Planned section and verify every row
has a valid, open GitHub issue reference in the Issue column.

Exit 0 only if all rows pass.
"""

import os
import re
import subprocess
import sys
import json

REPO = "NIBARGERB-HLDPRO/hldpro-governance"
BACKLOG_PATH = "OVERLORD_BACKLOG.md"

# Matches a #NNN issue reference (bare or markdown-linked)
ISSUE_REF_RE = re.compile(r"#(\d+)")


def find_planned_table(lines):
    """Return (header_line_index, list_of_data_lines) for the ## Planned table."""
    in_planned = False
    in_table = False
    header_idx = None
    data_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("## Planned"):
            in_planned = True
            continue

        if in_planned and stripped.startswith("## "):
            # Entered next section — stop
            break

        if in_planned and stripped.startswith("|"):
            if not in_table:
                # First pipe line is the header row
                in_table = True
                header_idx = i
                continue
            # Second pipe line is the separator row (---|---|...)
            if set(stripped.replace("|", "").replace("-", "").replace(":", "").strip()) == set():
                # It's a separator line, skip
                continue
            data_lines.append((i + 1, line))  # 1-based line number

    return header_idx, data_lines


def parse_columns(header_line, data_line):
    """
    Split a markdown table row into a dict keyed by header column names.
    Returns None if column count mismatches.
    """
    def split_row(row):
        # Strip leading/trailing pipes and split
        parts = row.strip().strip("|").split("|")
        return [p.strip() for p in parts]

    headers = split_row(header_line)
    cells = split_row(data_line)

    # Pad or trim cells to match header count
    if len(cells) < len(headers):
        cells += [""] * (len(headers) - len(cells))
    cells = cells[: len(headers)]

    return dict(zip(headers, cells))


def resolve_issue_number(cell_value):
    """
    Extract a #NNN from the cell value.
    Returns the integer issue number, or None if not found.
    """
    if not cell_value:
        return None
    # Handle em-dash and N/A markers
    normalized = cell_value.strip()
    if normalized in ("—", "-", "N/A", "n/a", "", "TBD"):
        return None
    match = ISSUE_REF_RE.search(normalized)
    if match:
        return int(match.group(1))
    return None


def check_github_issue(issue_number, token):
    """
    Call GitHub API to verify issue exists and is open.
    Returns (ok: bool, title_or_error: str)
    """
    api_url = f"repos/{REPO}/issues/{issue_number}"

    env = os.environ.copy()
    if token:
        env["GH_TOKEN"] = token

    try:
        result = subprocess.run(
            ["gh", "api", api_url],
            capture_output=True,
            text=True,
            env=env,
        )
    except FileNotFoundError:
        return False, "ERROR: 'gh' CLI not found in PATH"

    if result.returncode != 0:
        stderr = result.stderr.strip()
        if "404" in stderr or "Not Found" in stderr:
            return False, f"HTTP 404 — issue #{issue_number} not found"
        if "rate limit" in stderr.lower():
            return False, f"HTTP 429 — GitHub rate limit exceeded"
        return False, f"gh api error: {stderr or 'unknown error'}"

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return False, f"JSON parse error: {exc}"

    state = data.get("state", "")
    title = data.get("title", "(no title)")

    if state != "open":
        return False, f"Issue #{issue_number} is {state!r} (must be open): {title!r}"

    return True, title


def main():
    token = os.environ.get("GH_TOKEN", "")

    if not os.path.exists(BACKLOG_PATH):
        print(f"FAIL: {BACKLOG_PATH} not found (run from repo root)")
        sys.exit(1)

    with open(BACKLOG_PATH, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    header_idx, data_lines = find_planned_table(lines)

    if header_idx is None:
        print("FAIL: Could not find ## Planned table in OVERLORD_BACKLOG.md")
        sys.exit(1)

    if not data_lines:
        print("INFO: ## Planned table has no data rows — nothing to validate.")
        sys.exit(0)

    header_line = lines[header_idx]
    headers = [h.strip() for h in header_line.strip().strip("|").split("|")]

    has_issue_col = "Issue" in headers

    all_pass = True
    row_count = 0

    for lineno, raw_line in data_lines:
        row_count += 1
        stripped = raw_line.strip()
        if not stripped or not stripped.startswith("|"):
            continue

        row_dict = parse_columns(header_line, raw_line)

        # Determine the item label for display
        item_label = (
            row_dict.get("Item", "")
            or row_dict.get("item", "")
            or f"row {row_count}"
        )[:60]

        if not has_issue_col:
            print(
                "FAIL: ## Planned table is missing an 'Issue' column. "
                "Add an 'Issue' column with #NNN references before adding rows."
            )
            sys.exit(1)

        issue_cell = row_dict.get("Issue", "")

        issue_number = resolve_issue_number(issue_cell)

        if issue_number is None:
            issue_display = repr(issue_cell[:40]) if issue_cell else "(blank)"
            print(
                f"FAIL  [line {lineno}] {item_label!r} — "
                f"no #NNN issue reference found in Issue column "
                f"(got: {issue_display})"
            )
            all_pass = False
            continue

        ok, detail = check_github_issue(issue_number, token)
        if ok:
            print(f"PASS  [line {lineno}] {item_label!r} — #{issue_number}: {detail!r}")
        else:
            print(f"FAIL  [line {lineno}] {item_label!r} — #{issue_number}: {detail}")
            all_pass = False

    print()
    if all_pass:
        print(f"All {row_count} Planned rows reference open GitHub issues. Gate passed.")
        sys.exit(0)
    else:
        print(
            f"Gate FAILED: one or more Planned rows are missing a valid open GitHub "
            f"issue reference. Create or reopen the issue, then update OVERLORD_BACKLOG.md."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
