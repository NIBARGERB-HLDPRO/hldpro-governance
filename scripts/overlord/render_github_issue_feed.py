#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def render_issue(issue: dict) -> list[str]:
    labels = ", ".join(label["name"] for label in issue.get("labels", [])) or "none"
    created = issue.get("createdAt", "")[:10] or "unknown"
    updated = issue.get("updatedAt", "")[:10] or "unknown"
    url = issue.get("url", "")
    lines = [
        f"## #{issue['number']}: {issue['title']}",
        f"Labels: {labels} | Created: {created} | Updated: {updated}",
    ]
    if url:
        lines.append(f"URL: {url}")
    lines.append("---")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Render metadata-only GitHub issue feed markdown.")
    parser.add_argument("--input", required=True, help="Path to issue-list JSON from gh issue list")
    parser.add_argument("--output", required=True, help="Markdown output path")
    parser.add_argument("--repo", required=True, help="Repo slug/name label for the report")
    parser.add_argument("--date", required=True, help="UTC date string for the report header")
    args = parser.parse_args()

    issues = json.loads(Path(args.input).read_text())
    out_lines = [f"# GitHub Issues — {args.repo}", f"Date: {args.date}", ""]

    if not issues:
        out_lines.append("_No open issues._")
    else:
        for issue in issues:
            out_lines.extend(render_issue(issue))

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    main()
