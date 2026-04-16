#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ACTIVE_SECTION_PREFIXES = (
    "## Plans",
    "## Known Bugs",
    "## Feature Requests",
    "## Operational Items",
    "# Backlog",
    "## Backlog — Open Plans & Action Items",
    "### GitHub Issue Cross-Reference",
)

INACTIVE_SECTION_PREFIXES = (
    "## Done",
    "## Platform Infrastructure",
    "## E2E Testing & QA",
    "## Edge Functions",
    "## Marketing Site",
    "## Portal",
    "## Dashboard",
    "## Operator Dashboard",
    "## Reseller Platform",
)

ISSUE_RE = re.compile(r"#(\d+)\b")


@dataclass
class IssueRef:
    number: int
    line_number: int
    section: str
    line: str


def fail(message: str) -> None:
    print(f"FAIL progress-github-issue-staleness: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="", help="GitHub repo slug, e.g. NIBARGERB-HLDPRO/ai-integration-services")
    parser.add_argument("--progress-path", type=Path, default=Path("docs/PROGRESS.md"))
    parser.add_argument("--json", action="store_true", help="Print machine-readable summary")
    return parser.parse_args()


def current_repo_slug(args_repo: str) -> str:
    if args_repo:
        return args_repo
    env_repo = os.environ.get("GITHUB_REPOSITORY", "")
    if env_repo:
        return env_repo
    fail("missing --repo and GITHUB_REPOSITORY")


def gh_json(*args: str) -> list[dict[str, object]]:
    cmd = ["gh", *args]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        fail(f"gh command failed: {' '.join(cmd)}\n{result.stderr.strip()}")
    try:
        return json.loads(result.stdout or "[]")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON from gh command {' '.join(cmd)}: {exc}")


def backlog_issues(repo_slug: str) -> tuple[dict[int, dict[str, object]], dict[int, dict[str, object]]]:
    issues = gh_json(
        "issue",
        "list",
        "--repo",
        repo_slug,
        "--state",
        "all",
        "--limit",
        "200",
        "--search",
        "label:backlog",
        "--json",
        "number,state,title,labels",
    )
    open_issues: dict[int, dict[str, object]] = {}
    closed_issues: dict[int, dict[str, object]] = {}
    for issue in issues:
        number = int(issue["number"])
        state = str(issue.get("state", "")).upper()
        if state == "OPEN":
            open_issues[number] = issue
        elif state == "CLOSED":
            closed_issues[number] = issue
    return open_issues, closed_issues


def normalize_heading(line: str) -> str:
    return line.strip()


def section_state(section: str) -> bool:
    if any(section.startswith(prefix) for prefix in ACTIVE_SECTION_PREFIXES):
        return True
    if any(section.startswith(prefix) for prefix in INACTIVE_SECTION_PREFIXES):
        return False
    return False


def collect_active_issue_refs(progress_path: Path) -> dict[int, list[IssueRef]]:
    refs: dict[int, list[IssueRef]] = {}
    current_section = ""
    active = False
    for idx, raw in enumerate(progress_path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("#"):
            current_section = normalize_heading(stripped)
            active = section_state(current_section)
        if not active:
            continue
        for match in ISSUE_RE.finditer(raw):
            number = int(match.group(1))
            refs.setdefault(number, []).append(
                IssueRef(number=number, line_number=idx, section=current_section, line=raw.strip())
            )
    return refs


def build_summary(repo_slug: str, progress_path: Path) -> dict[str, object]:
    open_issues, closed_issues = backlog_issues(repo_slug)
    active_refs = collect_active_issue_refs(progress_path)

    missing_open = sorted(number for number in open_issues if number not in active_refs)
    stale_closed = sorted(number for number in closed_issues if number in active_refs)

    return {
        "repo": repo_slug,
        "progress_path": str(progress_path),
        "open_backlog_issue_count": len(open_issues),
        "closed_backlog_issue_count": len(closed_issues),
        "missing_open_issue_numbers": missing_open,
        "stale_closed_issue_numbers": stale_closed,
        "active_progress_issue_numbers": sorted(active_refs),
        "stale_closed_references": {
            str(number): [
                {
                    "line_number": ref.line_number,
                    "section": ref.section,
                    "line": ref.line,
                }
                for ref in active_refs.get(number, [])
            ]
            for number in stale_closed
        },
    }


def main() -> None:
    args = parse_args()
    repo_slug = current_repo_slug(args.repo)
    if repo_slug == "NIBARGERB-HLDPRO/hldpro-governance":
        summary = {
            "repo": repo_slug,
            "progress_path": str(args.progress_path),
            "skipped": True,
            "reason": "governance backlog is tracked in OVERLORD_BACKLOG.md, not docs/PROGRESS.md",
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
        return
    if not args.progress_path.exists():
        fail(f"missing progress file: {args.progress_path}")

    summary = build_summary(repo_slug, args.progress_path)

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return

    violations: list[str] = []
    if summary["missing_open_issue_numbers"]:
        issues = ", ".join(f"#{num}" for num in summary["missing_open_issue_numbers"])
        violations.append(f"open backlog issues missing from active PROGRESS backlog sections: {issues}")
    if summary["stale_closed_issue_numbers"]:
        details: list[str] = []
        stale_refs: dict[str, list[dict[str, object]]] = summary["stale_closed_references"]  # type: ignore[assignment]
        for number in summary["stale_closed_issue_numbers"]:
            refs = stale_refs.get(str(number), [])
            if refs:
                first = refs[0]
                details.append(f"#{number} at {first['section']} line {first['line_number']}")
            else:
                details.append(f"#{number}")
        violations.append("closed backlog issues still listed as active in PROGRESS.md: " + ", ".join(details))

    if violations:
        fail("\n".join(violations))

    print(
        "PASS progress-github-issue-staleness: active PROGRESS backlog entries match open backlog-labeled GitHub issues"
    )


if __name__ == "__main__":
    main()
