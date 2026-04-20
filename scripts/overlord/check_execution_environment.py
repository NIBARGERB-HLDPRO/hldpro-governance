#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import assert_execution_scope


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preflight the current execution environment against a scope file.")
    parser.add_argument("--scope", required=True, help="Path to execution scope JSON.")
    parser.add_argument("--changed-files-file", help="Optional file containing changed paths to validate.")
    parser.add_argument("--require-lane-claim", action="store_true", help="Require the scope lane_claim to match the current issue branch.")
    args = parser.parse_args(argv)

    scope_path = Path(args.scope)
    try:
        scope = assert_execution_scope._load_scope(scope_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL execution environment scope load failed: {exc}", file=sys.stderr)
        return 2

    changed_files_file = Path(args.changed_files_file).expanduser() if args.changed_files_file else None
    failures, warnings = assert_execution_scope.check_scope(
        scope,
        Path.cwd(),
        changed_files_file=changed_files_file,
        require_lane_claim=args.require_lane_claim,
    )

    for warning in warnings:
        print(f"WARN {warning}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    active_count = len(scope.active_parallel_roots)
    print(
        "PASS execution environment matches scope "
        f"(active_parallel_roots={active_count}, warnings={len(warnings)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
