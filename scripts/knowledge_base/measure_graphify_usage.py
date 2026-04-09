#!/usr/bin/env python3
"""Compare graph-guided retrieval with repo-search baselines on repeatable scenarios."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TEXT_EXTENSIONS = {
    ".md",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".json",
    ".yml",
    ".yaml",
    ".sh",
}
STOPWORDS = {
    "the",
    "and",
    "for",
    "that",
    "with",
    "from",
    "into",
    "where",
    "find",
    "only",
    "does",
    "being",
    "whether",
    "weekly",
    "issue",
    "real",
    "line",
    "file",
    "this",
    "when",
    "what",
    "through",
    "about",
    "should",
    "while",
}


@dataclass
class Scenario:
    id: str
    issue_number: int
    repo: str
    repo_path: str | None
    graph_key: str
    task_type: str
    prompt: str
    query_terms: list[str]
    expected_files: list[str]
    expected_terms: list[str]


@dataclass
class GraphData:
    nodes: list[dict[str, Any]]
    links: list[dict[str, Any]]
    community_labels: dict[str, str]
    node_by_id: dict[str, dict[str, Any]]


def estimate_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def normalize_tokens(values: list[str]) -> list[str]:
    tokens: list[str] = []
    for value in values:
        for token in re.findall(r"[A-Za-z0-9_.-]+", value.casefold()):
            if len(token) < 3 or token in STOPWORDS:
                continue
            if token not in tokens:
                tokens.append(token)
    return tokens


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repos-root", type=Path, required=True)
    parser.add_argument("--graph-root", type=Path, default=Path("graphify-out"))
    parser.add_argument("--scenario-file", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("metrics/graphify-evals"))
    parser.add_argument("--date", required=True)
    return parser.parse_args()


def load_scenarios(path: Path) -> list[Scenario]:
    payload = json.loads(path.read_text())
    return [Scenario(**raw) for raw in payload.get("scenarios", [])]


def resolve_graph_path(graph_root: Path, graph_key: str) -> Path:
    scoped = graph_root / graph_key / "graph.json"
    if scoped.exists():
        return scoped
    if graph_key == "hldpro-governance":
        return graph_root / "graph.json"
    return scoped


def resolve_label_path(graph_root: Path, graph_key: str) -> Path | None:
    path = graph_root / graph_key / "community-labels.json"
    return path if path.exists() else None


def load_graph(graph_root: Path, graph_key: str) -> GraphData:
    payload = json.loads(resolve_graph_path(graph_root, graph_key).read_text())
    label_path = resolve_label_path(graph_root, graph_key)
    community_labels: dict[str, str] = {}
    if label_path:
        community_labels = json.loads(label_path.read_text())
    nodes = payload.get("nodes", [])
    links = payload.get("links", [])
    node_by_id = {str(node.get("id")): node for node in nodes}
    return GraphData(nodes=nodes, links=links, community_labels=community_labels, node_by_id=node_by_id)


def relativize_source_file(source_file: str, repo_root: Path) -> str:
    path = Path(source_file)
    if path.is_absolute():
        try:
            return str(path.relative_to(repo_root))
        except ValueError:
            return path.name
    return source_file


def score_text(text: str, tokens: list[str]) -> float:
    lowered = text.casefold()
    score = 0.0
    for token in tokens:
        if token not in lowered:
            continue
        score += 1.0
        basename = lowered.rsplit("/", 1)[-1]
        if token in basename:
            score += 0.75
        if re.search(rf"(^|[^a-z0-9]){re.escape(token)}([^a-z0-9]|$)", lowered):
            score += 0.5
    return score


def aggregate_file_scores(file_scores: dict[str, float], evidence: dict[str, list[str]]) -> tuple[list[str], dict[str, list[str]]]:
    ranked = sorted(file_scores.items(), key=lambda item: (-item[1], item[0]))
    top_files = [path for path, _ in ranked[:5]]
    trimmed_evidence = {path: evidence.get(path, [])[:5] for path in top_files}
    return top_files, trimmed_evidence


def evaluate_relevance(top_files: list[str], evidence_text: str, scenario: Scenario) -> dict[str, Any]:
    file_hits = sum(1 for expected in scenario.expected_files if expected in top_files)
    expected_terms = normalize_tokens(scenario.expected_terms)
    lowered = evidence_text.casefold()
    term_hits = sum(1 for term in expected_terms if term in lowered)
    relevance_score = file_hits * 3 + term_hits
    materially_relevant = file_hits > 0 or relevance_score >= 3
    return {
        "file_hits": file_hits,
        "term_hits": term_hits,
        "relevance_score": relevance_score,
        "materially_relevant": materially_relevant,
    }


def graphify_results(graph_root: Path, repos_root: Path, scenario: Scenario) -> dict[str, Any]:
    repo_root = Path(scenario.repo_path) if scenario.repo_path else repos_root / scenario.repo
    graph = load_graph(graph_root, scenario.graph_key)
    tokens = normalize_tokens([scenario.prompt] + scenario.query_terms + scenario.expected_terms)

    node_scores: dict[str, float] = defaultdict(float)
    file_scores: dict[str, float] = defaultdict(float)
    community_scores: dict[str, float] = defaultdict(float)
    evidence: dict[str, list[str]] = defaultdict(list)

    for node in graph.nodes:
        source_file_raw = str(node.get("source_file", "") or "")
        if not source_file_raw:
            continue
        source_file = relativize_source_file(source_file_raw, repo_root)
        label = str(node.get("label", "") or "")
        community_id = str(node.get("community", ""))
        community_label = graph.community_labels.get(community_id, "")
        direct_score = score_text(" ".join([label, source_file, community_label]), tokens)
        if direct_score <= 0:
            continue
        node_id = str(node.get("id"))
        node_scores[node_id] += direct_score
        file_scores[source_file] += direct_score * 2.0
        community_scores[community_id] += direct_score
        evidence[source_file].append(f"direct:{label}")
        if community_label:
            evidence[source_file].append(f"community:{community_label}")

    for node in graph.nodes:
        source_file_raw = str(node.get("source_file", "") or "")
        if not source_file_raw:
            continue
        source_file = relativize_source_file(source_file_raw, repo_root)
        community_id = str(node.get("community", ""))
        community_boost = min(community_scores.get(community_id, 0.0), 6.0) * 0.35
        if community_boost > 0:
            file_scores[source_file] += community_boost
            community_label = graph.community_labels.get(community_id, "")
            if community_label:
                evidence[source_file].append(f"cluster:{community_label}")

    for link in graph.links:
        src_id = str(link.get("source"))
        tgt_id = str(link.get("target"))
        src_node = graph.node_by_id.get(src_id)
        tgt_node = graph.node_by_id.get(tgt_id)
        if not src_node or not tgt_node:
            continue
        src_file = relativize_source_file(str(src_node.get("source_file", "") or ""), repo_root)
        tgt_file = relativize_source_file(str(tgt_node.get("source_file", "") or ""), repo_root)
        if not src_file or not tgt_file:
            continue
        confidence = float(link.get("confidence_score", 1.0) or 1.0)
        relation = str(link.get("relation", "") or "")
        relation_boost = 0.25 if score_text(relation, tokens) > 0 else 0.0

        src_seed = node_scores.get(src_id, 0.0)
        tgt_seed = node_scores.get(tgt_id, 0.0)
        if src_seed > 0:
            propagated = src_seed * max(confidence, 0.2) * 0.5 + relation_boost
            file_scores[tgt_file] += propagated
            evidence[tgt_file].append(f"edge:{relation}:{src_node.get('label','')}")
        if tgt_seed > 0:
            propagated = tgt_seed * max(confidence, 0.2) * 0.5 + relation_boost
            file_scores[src_file] += propagated
            evidence[src_file].append(f"edge:{relation}:{tgt_node.get('label','')}")

    top_files, top_evidence = aggregate_file_scores(file_scores, evidence)
    evidence_text = "\n".join(
        [path + "\n" + "\n".join(items) for path, items in top_evidence.items()]
    )
    relevance = evaluate_relevance(top_files, evidence_text, scenario)
    return {
        "strategy": "graphify-guided",
        "top_files": top_files,
        "top_evidence": top_evidence,
        "quality_hit": relevance["materially_relevant"],
        "retrieval_count": len(top_files),
        "estimated_tokens": estimate_tokens(evidence_text),
        **relevance,
    }


def iter_repo_text_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.casefold() not in TEXT_EXTENSIONS:
            continue
        if ".git/" in str(path):
            continue
        files.append(path)
    return files


def baseline_results(repos_root: Path, scenario: Scenario) -> dict[str, Any]:
    repo_root = Path(scenario.repo_path) if scenario.repo_path else repos_root / scenario.repo
    tokens = normalize_tokens([scenario.prompt] + scenario.query_terms + scenario.expected_terms)
    scored: list[tuple[float, str, str]] = []
    for path in iter_repo_text_files(repo_root):
        rel = str(path.relative_to(repo_root))
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        text = f"{rel}\n{content[:8000]}"
        score = score_text(text, tokens)
        if score <= 0:
            continue
        snippet = "\n".join(content.splitlines()[:20])
        scored.append((score, rel, snippet))
    scored.sort(key=lambda item: (-item[0], item[1]))
    top_files: list[str] = []
    snippets: dict[str, list[str]] = {}
    for _, rel, snippet in scored:
        if rel not in top_files:
            top_files.append(rel)
            snippets[rel] = [snippet]
        if len(top_files) == 5:
            break
    evidence_text = "\n".join(f"{path}\n{items[0]}" for path, items in snippets.items())
    relevance = evaluate_relevance(top_files, evidence_text, scenario)
    return {
        "strategy": "repo-search",
        "top_files": top_files,
        "top_evidence": snippets,
        "quality_hit": relevance["materially_relevant"],
        "retrieval_count": len(top_files),
        "estimated_tokens": estimate_tokens(evidence_text),
        **relevance,
    }


def build_summary(scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    graphify_hits = sum(int(item["graphify"]["quality_hit"]) for item in scenarios)
    baseline_hits = sum(int(item["baseline"]["quality_hit"]) for item in scenarios)
    graphify_tokens = sum(item["graphify"]["estimated_tokens"] for item in scenarios)
    baseline_tokens = sum(item["baseline"]["estimated_tokens"] for item in scenarios)
    graphify_wins = sum(
        1
        for item in scenarios
        if item["graphify"]["relevance_score"] > item["baseline"]["relevance_score"]
        and item["graphify"]["estimated_tokens"] < item["baseline"]["estimated_tokens"]
    )
    recommendation = (
        "No second non-graph baseline is recommended yet; improve graph-guided ranking against the existing repo-search baseline first."
        if graphify_wins > 0
        else "A stronger second non-graph baseline may be warranted if graph-guided retrieval still cannot beat repo search after ranking improvements."
    )
    return {
        "scenario_count": len(scenarios),
        "graphify_hits": graphify_hits,
        "baseline_hits": baseline_hits,
        "graphify_estimated_tokens": graphify_tokens,
        "baseline_estimated_tokens": baseline_tokens,
        "graphify_smaller_and_better_count": graphify_wins,
        "second_baseline_recommended": graphify_wins == 0,
        "second_baseline_rationale": recommendation,
    }


def write_outputs(output_dir: Path, date: str, results: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{date}-graphify-vs-search.json"
    md_path = output_dir / f"{date}-graphify-vs-search.md"
    json_path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")

    lines = [
        f"# Graphify Measurement — {date}",
        "",
        "## Summary",
        "",
        f"- Scenarios: {results['summary']['scenario_count']}",
        f"- Graphify hits: {results['summary']['graphify_hits']}",
        f"- Baseline hits: {results['summary']['baseline_hits']}",
        f"- Graphify estimated tokens: {results['summary']['graphify_estimated_tokens']}",
        f"- Baseline estimated tokens: {results['summary']['baseline_estimated_tokens']}",
        f"- Graphify smaller + more relevant wins: {results['summary']['graphify_smaller_and_better_count']}",
        f"- Second non-graph baseline recommended: {results['summary']['second_baseline_recommended']}",
        f"- Baseline decision: {results['summary']['second_baseline_rationale']}",
        "",
        "## Scenario Results",
        "",
        "| Scenario | Graphify Relevant | Baseline Relevant | Graphify Score | Baseline Score | Graphify Tokens | Baseline Tokens |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in results["scenarios"]:
        lines.append(
            f"| {item['id']} | {int(item['graphify']['quality_hit'])} | {int(item['baseline']['quality_hit'])} | "
            f"{item['graphify']['relevance_score']} | {item['baseline']['relevance_score']} | "
            f"{item['graphify']['estimated_tokens']} | {item['baseline']['estimated_tokens']} |"
        )
    lines.extend(
        [
            "",
            "## Guidance",
            "",
            "- Validated pattern: use symptom terms plus mechanism/owner terms (function, workflow, file family) so graph-guided retrieval can exploit communities and one-hop links instead of only file-name overlap.",
            "- Use graph-guided retrieval first for topology and owning-file discovery, then confirm with repo search on the returned files.",
            f"- Baseline decision: {results['summary']['second_baseline_rationale']}",
            "",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    scenarios = load_scenarios(args.scenario_file)
    scenario_results: list[dict[str, Any]] = []

    for scenario in scenarios:
        graphify = graphify_results(args.graph_root, args.repos_root, scenario)
        baseline = baseline_results(args.repos_root, scenario)
        scenario_results.append(
            {
                "id": scenario.id,
                "issue_number": scenario.issue_number,
                "repo": scenario.repo,
                "task_type": scenario.task_type,
                "expected_files": scenario.expected_files,
                "expected_terms": scenario.expected_terms,
                "graphify": graphify,
                "baseline": baseline,
            }
        )

    summary = build_summary(scenario_results)
    results = {
        "date": args.date,
        "summary": summary,
        "scenarios": scenario_results,
    }
    write_outputs(args.output_dir, args.date, results)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
