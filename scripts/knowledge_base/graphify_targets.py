#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = REPO_ROOT / "docs" / "graphify_targets.json"


def load_manifest(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("manifest root must be an object")
    targets = payload.get("targets")
    if not isinstance(targets, list) or not targets:
        raise ValueError("manifest must contain a non-empty targets array")
    return payload


def target_rows(manifest: dict[str, object]) -> list[dict[str, object]]:
    rows = manifest.get("targets")
    assert isinstance(rows, list)
    return [row for row in rows if isinstance(row, dict)]


def filtered_targets(rows: list[dict[str, object]], scheduled: bool, closeout: bool) -> list[dict[str, object]]:
    result = rows
    if scheduled:
        result = [row for row in result if bool(row.get("scheduled"))]
    if closeout:
        result = [row for row in result if bool(row.get("closeout_refresh"))]
    return result


def find_target(rows: list[dict[str, object]], repo_slug: str) -> dict[str, object]:
    for row in rows:
        if row.get("repo_slug") == repo_slug:
            return row
    raise KeyError(f"repo_slug not found in manifest: {repo_slug}")


def print_json(data: object) -> None:
    json.dump(data, sys.stdout, indent=2)
    sys.stdout.write("\n")


def print_tsv(rows: list[dict[str, object]]) -> None:
    for row in rows:
        sys.stdout.write(
            "\t".join(
                [
                    str(row["repo_slug"]),
                    str(row["display_name"]),
                    str(row["source_path"]),
                    str(row["output_path"]),
                    str(row["wiki_path"]),
                ]
            )
            + "\n"
        )


def print_shell(row: dict[str, object]) -> None:
    keys = ("repo_slug", "display_name", "source_path", "output_path", "wiki_path")
    for key in keys:
        value = str(row[key]).replace('"', '\\"')
        sys.stdout.write(f'{key.upper()}="{value}"\n')


def print_stage_paths(rows: list[dict[str, object]]) -> None:
    seen: set[str] = set()
    for row in rows:
        for path_key in ("output_path", "wiki_path"):
            path = str(row[path_key])
            if path not in seen:
                seen.add(path)
                sys.stdout.write(f"{path}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read the governance graphify target manifest.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Path to graphify_targets.json")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List manifest targets")
    list_parser.add_argument("--scheduled", action="store_true", help="Only include scheduled targets")
    list_parser.add_argument("--closeout", action="store_true", help="Only include closeout-refresh targets")
    list_parser.add_argument("--format", choices=("json", "tsv"), default="json")

    show_parser = subparsers.add_parser("show", help="Show one manifest target")
    show_parser.add_argument("--repo-slug", required=True)
    show_parser.add_argument("--format", choices=("json", "shell"), default="json")

    stage_parser = subparsers.add_parser("stage-paths", help="Print artifact directories to stage")
    stage_parser.add_argument("--scheduled", action="store_true", help="Only include scheduled targets")
    stage_parser.add_argument("--closeout", action="store_true", help="Only include closeout-refresh targets")

    args = parser.parse_args()
    manifest = load_manifest(Path(args.manifest))
    rows = target_rows(manifest)

    if args.command == "list":
        selected = filtered_targets(rows, scheduled=args.scheduled, closeout=args.closeout)
        if args.format == "json":
            print_json(selected)
        else:
            print_tsv(selected)
        return 0

    if args.command == "show":
        row = find_target(rows, args.repo_slug)
        if args.format == "json":
            print_json(row)
        else:
            print_shell(row)
        return 0

    if args.command == "stage-paths":
        selected = filtered_targets(rows, scheduled=args.scheduled, closeout=args.closeout)
        print_stage_paths(selected)
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
