#!/usr/bin/env python3
"""Compare graphify-guided retrieval with baseline repo search on repeatable scenarios."""

from __future__ import annotations

import argparse
import json
import math
import re
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
    scenarios = []
    for raw in payload.get("scenarios", []):
        scenarios.append(Scenario(**raw))
    return scenarios


def load_graph_nodes(graph_root: Path, graph_key: str) -> list[dict[str, Any]]:
    graph_path = graph_root / ("graph.json" if graph_key == "hldpro-governance" else f"{graph_key}/graph.json")
    payload = json.loads(graph_path.read_text())
    return payload.get("nodes", [])


def score_text(text: str, tokens: list[str]) -> int:
    lowered = text.casefold()
    return sum(1 for token in tokens if token in lowered)


def graphify_results(graph_root: Path, scenario: Scenario) -> dict[str, Any]:
    nodes = load_graph_nodes(graph_root, scenario.graph_key)
    tokens = normalize_tokens([scenario.prompt] + scenario.query_terms + scenario.expected_terms)
    scored: list[tuple[int, str]] = []
    snippets: list[str] = []
    for node in nodes:
        source_file = str(node.get("source_file", "") or "")
        label = str(node.get("label", "") or "")
        text = " ".join([label, source_file])
        score = score_text(text, tokens)
        if score <= 0 or not source_file:
            continue
        scored.append((score, source_file))
        snippets.append(text)
    scored.sort(key=lambda item: (-item[0], item[1]))
    top_files: list[str] = []
    for _, source_file in scored:
        if source_file not in top_files:
            top_files.append(source_file)
        if len(top_files) == 5:
            break
    success = any(expected in top_files for expected in scenario.expected_files)
    return {
        "strategy": "graphify",
        "top_files": top_files,
        "quality_hit": success,
        "retrieval_count": len(top_files),
        "estimated_tokens": estimate_tokens("\n".join(snippets[:25])),
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
    scored: list[tuple[int, str, str]] = []
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
    snippets: list[str] = []
    for _, rel, snippet in scored:
        if rel not in top_files:
            top_files.append(rel)
            snippets.append(snippet)
        if len(top_files) == 5:
            break
    success = any(expected in top_files for expected in scenario.expected_files)
    return {
        "strategy": "repo-search",
        "top_files": top_files,
        "quality_hit": success,
        "retrieval_count": len(top_files),
        "estimated_tokens": estimate_tokens("\n".join(snippets)),
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
        "",
        "## Scenario Results",
        "",
        "| Scenario | Graphify Hit | Baseline Hit | Graphify Tokens | Baseline Tokens |",
        "|---|---:|---:|---:|---:|",
    ]
    for item in results["scenarios"]:
        lines.append(
            f"| {item['id']} | {int(item['graphify']['quality_hit'])} | {int(item['baseline']['quality_hit'])} | "
            f"{item['graphify']['estimated_tokens']} | {item['baseline']['estimated_tokens']} |"
        )
    md_path.write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    scenarios = load_scenarios(args.scenario_file)
    scenario_results: list[dict[str, Any]] = []
    graphify_hits = 0
    baseline_hits = 0
    graphify_tokens = 0
    baseline_tokens = 0

    for scenario in scenarios:
        graphify = graphify_results(args.graph_root, scenario)
        baseline = baseline_results(args.repos_root, scenario)
        graphify_hits += int(graphify["quality_hit"])
        baseline_hits += int(baseline["quality_hit"])
        graphify_tokens += graphify["estimated_tokens"]
        baseline_tokens += baseline["estimated_tokens"]
        scenario_results.append(
            {
                "id": scenario.id,
                "issue_number": scenario.issue_number,
                "repo": scenario.repo,
                "task_type": scenario.task_type,
                "expected_files": scenario.expected_files,
                "graphify": graphify,
                "baseline": baseline,
            }
        )

    results = {
        "date": args.date,
        "summary": {
            "scenario_count": len(scenarios),
            "graphify_hits": graphify_hits,
            "baseline_hits": baseline_hits,
            "graphify_estimated_tokens": graphify_tokens,
            "baseline_estimated_tokens": baseline_tokens,
        },
        "scenarios": scenario_results,
    }
    write_outputs(args.output_dir, args.date, results)
    print(json.dumps(results["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
