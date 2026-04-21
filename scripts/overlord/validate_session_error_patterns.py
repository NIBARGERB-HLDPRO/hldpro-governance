#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = {
    "signature",
    "category",
    "root_cause",
    "correction",
    "guardrail",
    "validation",
    "related_files",
    "first_observed",
    "prevented_by",
}

REQUIRED_PATTERNS = {
    "hook-command-classification-false-positive",
    "claude-stream-json-verbose-required",
    "force-push-policy-advisory-only",
    "stale-governance-workflow-sha",
    "malformed-local-overrides",
    "typoed-governance-root",
    "pr-checks-pending-exit-code-eight",
    "local-multi-worktree-main-merge-conflict",
    "sql-schema-drift-stale-column",
}


def _field_key(raw: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", raw.lower()).strip("_")


def _pattern_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    for match in re.finditer(r"^## Pattern:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$", text, re.MULTILINE):
        pattern_id = match.group(1)
        start = match.end()
        next_match = re.search(r"^##\s+", text[start:], re.MULTILINE)
        sections[pattern_id] = text[start : start + next_match.start()] if next_match else text[start:]
    return sections


def _fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw in body.splitlines():
        line = raw.strip()
        if not line.startswith("|") or "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() == "field":
            continue
        key = _field_key(cells[0])
        if key:
            fields[key] = cells[1]
    return fields


def validate(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"{path}: file not found"]
    text = path.read_text(encoding="utf-8")
    sections = _pattern_sections(text)
    if not sections:
        failures.append(f"{path}: no `## Pattern: <kebab-case-id>` sections found")
        return failures

    missing_patterns = sorted(REQUIRED_PATTERNS - set(sections))
    if missing_patterns:
        failures.append(f"{path}: missing required seed pattern(s): {', '.join(missing_patterns)}")

    for pattern_id, body in sorted(sections.items()):
        fields = _fields(body)
        missing_fields = sorted(REQUIRED_FIELDS - set(fields))
        if missing_fields:
            failures.append(f"{path}: pattern {pattern_id} missing field(s): {', '.join(missing_fields)}")
        empty_fields = sorted(field for field in REQUIRED_FIELDS if field in fields and not fields[field].strip())
        if empty_fields:
            failures.append(f"{path}: pattern {pattern_id} has empty field(s): {', '.join(empty_fields)}")
        first_observed = fields.get("first_observed")
        if first_observed and not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", first_observed):
            failures.append(f"{path}: pattern {pattern_id} first_observed must be YYYY-MM-DD")
    return failures


def _run_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate session error pattern runbook entries")
    parser.add_argument("path", nargs="?", type=Path, default=Path("docs/runbooks/session-error-patterns.md"))
    args = parser.parse_args(argv)

    failures = validate(args.path)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"PASS {args.path}: session error patterns schema valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(_run_cli())
