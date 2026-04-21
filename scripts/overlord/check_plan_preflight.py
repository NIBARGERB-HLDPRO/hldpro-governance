#!/usr/bin/env python3
"""Read-only plan evidence preflight for governed write intent."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import sys
import time
from pathlib import Path
from typing import Any


GOVERNED_EXTENSIONS = {
    ".go",
    ".js",
    ".mjs",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".ts",
    ".tsx",
    ".yaml",
    ".yml",
}


def is_governed_path(path: str) -> bool:
    suffix = Path(path).suffix.lower()
    return suffix in GOVERNED_EXTENSIONS


def recent_plan(plans_dir: Path, freshness_hours: float) -> Path | None:
    if not plans_dir.is_dir():
        return None
    cutoff = time.time() - freshness_hours * 3600
    candidates = [path for path in plans_dir.glob("*.md") if path.is_file() and path.stat().st_mtime >= cutoff]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def detect_bash_write_target(command: str) -> str:
    if re.search(r"\b(?:python|python3)\b.*(?:open\(|write_text\()", command, re.S):
        return "<python file write>"

    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        tokens = list(lexer)
    except ValueError:
        tokens = command.split()

    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "tee":
            target_index = index + 1
            while target_index < len(tokens) and tokens[target_index].startswith("-"):
                target_index += 1
            if target_index < len(tokens):
                target = tokens[target_index].strip("'\"")
                if target and target not in {"/dev/null", "-"}:
                    return target
        if token in {">", ">>"} and index + 1 < len(tokens):
            target = tokens[index + 1].strip("'\"")
            if target and target not in {"/dev/null", "-", "&"}:
                return target
        index += 1
    return ""


def block_reason(*, target: str, plans_dir: str, freshness_hours: float) -> str:
    return "\n".join(
        [
            "PLAN_GATE_BLOCKED: missing_recent_plan",
            "NEXT_ACTION: create_plan",
            f"TARGET_FILE: {target}",
            f"PLANS_DIR: {plans_dir}",
            f"PLAN_FRESHNESS_HOURS: {freshness_hours:g}",
            "BYPASS_ALLOWED: trivial_single_line_only",
            "DETAIL: Stop code-write attempts. Create or update the active plan first; do not retry through Bash, Python, sed, perl, heredoc, or PLAN_GATE_BYPASS unless the documented trivial single-line criteria are satisfied.",
        ]
    )


def evaluate(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    plans_dir = Path(args.plans_dir)
    if not plans_dir.is_absolute():
        plans_dir = repo_root / plans_dir

    target = args.target_path or ""
    if args.command:
        target = detect_bash_write_target(args.command)

    if args.intent == "read":
        return {"decision": "allow", "reason": "read_only_intent", "target_path": target}
    if not target:
        return {"decision": "allow", "reason": "no_write_target_detected", "target_path": target}
    if target == "<python file write>" or is_governed_path(target):
        governed = True
    else:
        governed = False
    if not governed:
        return {"decision": "allow", "reason": "ungoverned_target", "target_path": target}

    if args.plan_gate_bypass:
        if args.trivial_single_line:
            return {
                "decision": "allow",
                "reason": "trivial_single_line_bypass",
                "target_path": target,
                "bypass_allowed": "trivial_single_line_only",
            }
        return {
            "decision": "block",
            "reason": block_reason(target=target, plans_dir=str(plans_dir), freshness_hours=args.freshness_hours),
            "target_path": target,
            "next_action": "create_plan",
        }

    plan = recent_plan(plans_dir, args.freshness_hours)
    if plan:
        return {
            "decision": "allow",
            "reason": "recent_plan_found",
            "target_path": target,
            "plan_ref": str(plan.relative_to(repo_root) if plan.is_relative_to(repo_root) else plan),
        }

    return {
        "decision": "block",
        "reason": block_reason(target=target, plans_dir=str(plans_dir), freshness_hours=args.freshness_hours),
        "target_path": target,
        "next_action": "create_plan",
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--target-path")
    parser.add_argument("--command")
    parser.add_argument("--intent", choices=["read", "write"], default="write")
    parser.add_argument("--plans-dir", default=".claude/plans")
    parser.add_argument("--freshness-hours", type=float, default=3.0)
    parser.add_argument("--plan-gate-bypass", action="store_true", default=os.environ.get("PLAN_GATE_BYPASS") == "true")
    parser.add_argument("--trivial-single-line", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    payload = evaluate(args)
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        print(payload["reason"])
    return 0 if payload["decision"] == "allow" else 1


if __name__ == "__main__":
    raise SystemExit(main())
