#!/usr/bin/env python3
"""Append graphify usage events to tracked JSONL logs."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("metrics/graphify-usage/events"))
    parser.add_argument("--repo", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--task-type", required=True)
    parser.add_argument("--strategy", choices=["graphify", "repo-search", "hybrid"], required=True)
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--estimated-tokens", type=int, required=True)
    parser.add_argument("--notes", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    event = {
      "timestamp": timestamp,
      "repo": args.repo,
      "task_id": args.task_id,
      "task_type": args.task_type,
      "strategy": args.strategy,
      "artifacts": args.artifact or ["unspecified"],
      "notes": args.notes,
      "estimated_tokens": args.estimated_tokens,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    event_path = args.output_dir / f"{timestamp[:10]}.jsonl"
    with event_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    print(event_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
