#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_graph(source: Path, output: Path, wiki_dir: Path | None, html: bool) -> dict[str, object]:
    from graphify.detect import detect
    from graphify.extract import collect_files, extract
    from graphify.build import build_from_json
    from graphify.cluster import cluster, score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate
    from graphify.export import to_json, to_html
    from graphify.wiki import to_wiki

    detection = detect(source)
    code_files = []
    for entry in detection.get("files", {}).get("code", []):
        path = Path(entry)
        code_files.extend(collect_files(path) if path.is_dir() else [path])

    result = extract(code_files)
    G = build_from_json(result)
    communities = cluster(G)
    cohesion = score_all(G, communities)
    labels = {cid: f"Community {cid}" for cid in communities}
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    questions = suggest_questions(G, communities, labels)

    output.mkdir(parents=True, exist_ok=True)
    (output / ".graphify_detect.json").write_text(json.dumps(detection, indent=2), encoding="utf-8")
    (output / ".graphify_ast.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    report = generate(
        G,
        communities,
        cohesion,
        labels,
        gods,
        surprises,
        detection,
        {"input": result.get("input_tokens", 0), "output": result.get("output_tokens", 0)},
        str(source),
        suggested_questions=questions,
    )
    (output / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    to_json(G, communities, str(output / "graph.json"))

    html_status = "skipped"
    if html:
        try:
            to_html(G, communities, str(output / "graph.html"), community_labels=labels)
            html_status = "generated"
        except Exception as exc:  # pragma: no cover - best effort only
            html_status = f"skipped: {exc}"

    article_count = 0
    if wiki_dir is not None:
        wiki_dir.mkdir(parents=True, exist_ok=True)
        article_count = to_wiki(
            G,
            communities,
            wiki_dir,
            community_labels=labels,
            cohesion=cohesion,
            god_nodes_data=gods,
        )

    summary = {
        "source": str(source),
        "output": str(output),
        "wiki_dir": str(wiki_dir) if wiki_dir else None,
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "communities": len(communities),
        "articles": article_count,
        "html_status": html_status,
        "code_files": len(code_files),
    }
    (output / ".graphify_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a graphify code graph and report for a repo.")
    parser.add_argument("--source", required=True, help="Source repo/folder to analyze")
    parser.add_argument("--output", required=True, help="Output graphify-out directory")
    parser.add_argument("--wiki-dir", help="Optional wiki output directory")
    parser.add_argument("--no-html", action="store_true", help="Skip graph.html generation")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    output = Path(args.output).resolve()
    wiki_dir = Path(args.wiki_dir).resolve() if args.wiki_dir else None

    if not source.exists():
        print(json.dumps({"error": f"Source path does not exist: {source}"}), file=sys.stderr)
        return 1

    summary = build_graph(source, output, wiki_dir, html=not args.no_html)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
