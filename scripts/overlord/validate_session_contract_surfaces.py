#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_FILES = (
    Path("CODEX.md"),
    Path("hooks/pre-session-context.sh"),
    Path(".claude/hooks/pre-session-context.sh"),
    Path(".claude/settings.json"),
)


def _find_hook_command(entries: object, matcher: str | None, needle: str) -> bool:
    if not isinstance(entries, list):
        return False
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if matcher is not None and entry.get("matcher") != matcher:
            continue
        hooks = entry.get("hooks")
        if not isinstance(hooks, list):
            continue
        for hook in hooks:
            if not isinstance(hook, dict):
                continue
            command = hook.get("command")
            if isinstance(command, str) and needle in command:
                return True
    return False


def validate(root: Path) -> list[str]:
    failures: list[str] = []
    missing = [path.as_posix() for path in REQUIRED_FILES if not (root / path).is_file()]
    if missing:
        failures.append(
            "governance session-contract surfaces missing: " + ", ".join(missing)
        )
        return failures

    try:
        payload = json.loads((root / ".claude/settings.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f".claude/settings.json could not be parsed as JSON: {exc}"]

    hooks = payload.get("hooks", {})
    if not isinstance(hooks, dict):
        return [".claude/settings.json must expose a top-level `hooks` object"]

    if not _find_hook_command(
        hooks.get("UserPromptSubmit"),
        None,
        "hooks/pre-session-context.sh",
    ):
        failures.append(
            ".claude/settings.json must expose a UserPromptSubmit command that invokes hooks/pre-session-context.sh"
        )

    if not _find_hook_command(
        hooks.get("PostToolUse"),
        "*",
        "hooks/check-errors.sh",
    ):
        failures.append(
            ".claude/settings.json must expose PostToolUse matcher '*' with a command invoking hooks/check-errors.sh"
        )

    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate tracked governance session-contract surfaces.")
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    failures = validate(root)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print("PASS governance session contract surfaces present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
