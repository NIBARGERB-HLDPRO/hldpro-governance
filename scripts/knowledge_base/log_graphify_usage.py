#!/usr/bin/env python3
"""Append graphify usage events to tracked JSONL logs."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("metrics/graphify-usage/events"))
    parser.add_argument("--repo", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--experiment-id")
    parser.add_argument("--session-id")
    parser.add_argument("--task-type", required=True)
    parser.add_argument("--strategy", choices=["graphify", "repo-search", "hybrid"], required=True)
    parser.add_argument("--prompt")
    parser.add_argument("--query-term", action="append", default=[])
    parser.add_argument("--top-candidate", action="append", default=[])
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--estimated-tokens", type=int, required=True)
    parser.add_argument("--notes", default="")
    return parser.parse_args()


def build_event(
    *,
    repo: str,
    task_id: str,
    task_type: str,
    strategy: str,
    artifacts: list[str],
    estimated_tokens: int,
    notes: str = "",
    experiment_id: str | None = None,
    session_id: str | None = None,
    prompt: str | None = None,
    query_terms: list[str] | None = None,
    top_candidates: list[str] | None = None,
) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    event: dict[str, Any] = {
        "timestamp": timestamp,
        "repo": repo,
        "task_id": task_id,
        "task_type": task_type,
        "strategy": strategy,
        "artifacts": artifacts or ["unspecified"],
        "notes": notes,
        "estimated_tokens": estimated_tokens,
    }
    if experiment_id:
        event["experiment_id"] = experiment_id
    if session_id:
        event["session_id"] = session_id
    if prompt:
        event["prompt"] = prompt
    if query_terms:
        event["query_terms"] = query_terms
    if top_candidates:
        event["top_candidates"] = top_candidates
    return event


def append_event(output_dir: Path, event: dict[str, Any]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    event_path = output_dir / f"{str(event['timestamp'])[:10]}.jsonl"
    with event_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    return event_path


def main() -> int:
    args = parse_args()
    event = build_event(
        repo=args.repo,
        task_id=args.task_id,
        task_type=args.task_type,
        strategy=args.strategy,
        artifacts=args.artifact,
        estimated_tokens=args.estimated_tokens,
        notes=args.notes,
        experiment_id=args.experiment_id,
        session_id=args.session_id,
        prompt=args.prompt,
        query_terms=args.query_term,
        top_candidates=args.top_candidate,
    )
    event_path = append_event(args.output_dir, event)
    print(event_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
