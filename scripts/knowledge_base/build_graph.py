#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


GENERIC_TOKENS = {
    "app",
    "apps",
    "backend",
    "build",
    "code",
    "component",
    "components",
    "config",
    "dashboard",
    "data",
    "docs",
    "e2e",
    "edge",
    "file",
    "files",
    "fn",
    "frontend",
    "function",
    "functions",
    "helper",
    "helpers",
    "hook",
    "hooks",
    "index",
    "lib",
    "main",
    "marketing",
    "md",
    "page",
    "pages",
    "portal",
    "script",
    "scripts",
    "service",
    "services",
    "shared",
    "src",
    "test",
    "tests",
    "tools",
    "ts",
    "tsx",
    "ui",
    "user",
    "users",
    "utils",
    "wiki",
    "readonly",
    "production",
    "staging",
    "runbook",
    "contract",
    "probe",
    "journey",
    "context",
    "router",
    "layout",
    "smoke",
    "spec",
    "list",
    "get",
    "env",
}


def _split_words(text: str) -> list[str]:
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    text = text.replace("_", " ").replace("-", " ")
    return [part.lower() for part in re.findall(r"[A-Za-z0-9]+", text)]


def _normalize_phrase(parts: list[str]) -> str | None:
    cleaned = [part for part in parts if part and part.lower() not in GENERIC_TOKENS]
    if not cleaned:
        return None
    return " ".join(word.capitalize() for word in cleaned)


def _derive_path_phrase(source_root: Path, source_file: str) -> str | None:
    try:
        rel = Path(source_file).resolve().relative_to(source_root)
        raw_parts = list(rel.parts[:-1]) + [Path(rel.name).stem]
    except Exception:
        path = Path(source_file)
        raw_parts = list(path.parts[-3:-1]) + [path.stem]

    anchors = ["functions", "pages", "components", "services", "offline", "context", "e2e", "scripts", "migrations"]
    parts = raw_parts
    for anchor in anchors:
        if anchor in raw_parts:
            parts = raw_parts[raw_parts.index(anchor) + 1 :]
            break

    meaningful_parts: list[str] = []
    for part in parts:
        stem = Path(part).stem
        words = [word for word in _split_words(stem) if word not in GENERIC_TOKENS]
        if not words:
            continue
        meaningful_parts.append(" ".join(words))
        if len(meaningful_parts) >= 2:
            break

    if not meaningful_parts:
        fallback_words = [word for part in raw_parts for word in _split_words(Path(part).stem) if word not in GENERIC_TOKENS]
        meaningful_parts = fallback_words[:2]

    return _normalize_phrase(meaningful_parts[:2])


def _derive_path_tokens(source_root: Path, source_file: str) -> list[str]:
    try:
        rel = Path(source_file).resolve().relative_to(source_root)
        raw_parts = list(rel.parts[:-1]) + [Path(rel.name).stem]
    except Exception:
        path = Path(source_file)
        raw_parts = list(path.parts[-3:-1]) + [path.stem]

    tokens: list[str] = []
    for part in raw_parts:
        tokens.extend(word for word in _split_words(Path(part).stem) if word not in GENERIC_TOKENS and len(word) > 2)
    return tokens


def _community_label(G, source_root: Path, nodes: list[str], cid: int) -> str:
    if not nodes:
        return f"Community {cid}"

    phrase_counts: Counter[str] = Counter()
    token_counts: Counter[str] = Counter()

    for node in nodes:
        data = G.nodes[node]
        label = str(data.get("label") or node)
        for token in _split_words(label):
            if token not in GENERIC_TOKENS and len(token) > 2:
                token_counts[token] += 1

        source_file = data.get("source_file")
        if isinstance(source_file, str) and source_file:
            phrase = _derive_path_phrase(source_root, source_file)
            if phrase:
                phrase_counts[phrase] += 2
            for token in _derive_path_tokens(source_root, source_file):
                token_counts[token] += 1

    if phrase_counts:
        label = phrase_counts.most_common(1)[0][0]
        top_token = next((word.capitalize() for word, _ in token_counts.most_common(3) if word.capitalize().lower() not in label.lower()), None)
        return f"{label} {top_token}".strip() if top_token else label

    top_tokens = [word.capitalize() for word, _ in token_counts.most_common(3)]
    return " ".join(top_tokens) if top_tokens else f"Community {cid}"


def infer_community_labels(G, communities: dict[int, list[str]], source_root: Path) -> dict[int, str]:
    return {cid: _community_label(G, source_root, nodes, cid) for cid, nodes in communities.items()}


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
    labels = infer_community_labels(G, communities, source)
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
    (output / "community-labels.json").write_text(
        json.dumps({str(cid): label for cid, label in labels.items()}, indent=2),
        encoding="utf-8",
    )

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
