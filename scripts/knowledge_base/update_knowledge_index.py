#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.knowledge_base.graphify_targets import load_manifest, target_rows


DEFAULT_MANIFEST = REPO_ROOT / "docs" / "graphify_targets.json"
DEFAULT_INDEX = REPO_ROOT / "wiki" / "index.md"


def summary_line(summary_path: Path, display_name: str, report_rel: str) -> str:
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    nodes = payload.get("nodes", "?")
    edges = payload.get("edges", "?")
    communities = payload.get("communities", "?")
    return f"- {display_name}: {nodes} nodes, {edges} edges, {communities} communities — {report_rel}"


def replace_section(text: str, heading: str, replacement_lines: list[str]) -> str:
    pattern = re.compile(rf"(^## {re.escape(heading)}\n)(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    if not match:
        raise ValueError(f"section not found: {heading}")
    new_body = "\n".join(replacement_lines).rstrip() + "\n\n"
    return text[: match.start(2)] + new_body + text[match.end(2) :]


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh wiki/index.md from the graphify target manifest.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--index", default=str(DEFAULT_INDEX))
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    index_path = Path(args.index)
    manifest = load_manifest(manifest_path)
    rows = target_rows(manifest)

    covered: list[dict[str, object]] = []
    for row in rows:
        output_path = REPO_ROOT / str(row["output_path"])
        summary_path = output_path / ".graphify_summary.json"
        report_path = output_path / "GRAPH_REPORT.md"
        if summary_path.exists() and report_path.exists():
            covered.append(row)

    coverage_names = ", ".join(str(row["display_name"]) for row in covered) if covered else "none"

    platform_status = [
        "<!-- overlord-sweep writes here weekly -->",
        "- Overall: ATTENTION NEEDED",
        "- Last sweep: bootstrap graph built locally on 2026-04-09; first weekly write-back run still pending",
        f"- Graph coverage: {coverage_names} are now graphified in governance",
    ]

    knowledge_summary = [
        "<!-- Generated from docs/graphify_targets.json + per-repo .graphify_summary.json -->"
    ]
    for row in covered:
        report_rel = f"../{row['output_path']}/GRAPH_REPORT.md"
        summary_path = REPO_ROOT / str(row["output_path"]) / ".graphify_summary.json"
        knowledge_summary.append(summary_line(summary_path, str(row["display_name"]), report_rel))

    navigation = []
    for row in covered:
        navigation.append(f"- [{row['display_name']} graph articles]({row['wiki_path'].split('/', 1)[1]}/)")
    navigation.extend(
        [
            "- [Decision log](decisions/)",
            "- [Pattern library](patterns/)",
            "- [Raw feeds](../raw/)",
        ]
    )

    text = index_path.read_text(encoding="utf-8")
    text = replace_section(text, "Platform Status", platform_status)
    text = replace_section(text, "Knowledge Graph Summary", knowledge_summary)
    text = replace_section(text, "Navigation", navigation)
    index_path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
