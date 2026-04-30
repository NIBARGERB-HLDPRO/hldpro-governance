#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import io
import sys
from pathlib import Path

import assert_execution_scope
import check_execution_environment


def _discover_selected_scope(
    root: Path, branch: str, scopes_dir: Path
) -> tuple[tuple[Path, object] | None, list[str], list[str]]:
    issue_number = assert_execution_scope._branch_issue_number(branch)
    if issue_number is None:
        return None, [], [f"branch is not issue-backed: {branch}"]

    candidates, warnings = check_execution_environment._discover_scope_candidates(
        root, branch, issue_number, scopes_dir
    )
    selected, selection_failure = check_execution_environment._select_scope(candidates)
    if selection_failure:
        return None, warnings, [selection_failure]
    return selected, warnings, []


def _run_scope_check(
    root: Path, scope_path: Path, changed_files_file: Path | None
) -> tuple[int, list[str], list[str]]:
    try:
        scope = assert_execution_scope._load_scope(scope_path)
    except (OSError, ValueError) as exc:
        return 2, [], [f"scope load failed: {exc}"]
    failures, warnings = assert_execution_scope.check_scope(
        scope,
        root,
        changed_files_file=changed_files_file,
        require_lane_claim=True,
    )
    if failures:
        return 1, warnings, failures
    return 0, warnings, []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Replay the active implementation-capable execution scope from local governance hooks."
    )
    parser.add_argument("--root", default=".", help="Repo root containing raw/execution-scopes.")
    parser.add_argument("--branch", default="", help="Branch name override for tests.")
    parser.add_argument(
        "--changed-files-file",
        default="",
        help="Optional newline-delimited file of changed repo-relative paths.",
    )
    parser.add_argument("--scopes-dir", default="raw/execution-scopes", help="Execution scopes directory.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    changed_files_file = Path(args.changed_files_file).resolve() if args.changed_files_file else None

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        branch = args.branch or assert_execution_scope._current_branch(root)
    if not branch:
        print("FAIL governance hook execution scope: could not determine current branch", file=sys.stderr)
        return 1

    selected, warnings, failures = _discover_selected_scope(root, branch, (root / args.scopes_dir).resolve())
    for warning in warnings:
        print(f"WARN {warning}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1

    assert selected is not None
    scope_path, scope = selected
    if getattr(scope, "execution_mode", "planning_only") == "planning_only":
        print(
            "PASS governance hook execution scope: matched planning-only scope "
            f"{scope_path.relative_to(root).as_posix()}; no implementation replay required"
        )
        return 0

    code, scope_warnings, scope_failures = _run_scope_check(root, scope_path, changed_files_file)
    for warning in scope_warnings:
        print(f"WARN {warning}")
    if scope_failures:
        for failure in scope_failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return code

    print(
        "PASS governance hook execution scope: validated implementation-capable scope "
        f"{scope_path.relative_to(root).as_posix()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
