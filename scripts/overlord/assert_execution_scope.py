#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExecutionScope:
    expected_execution_root: Path
    expected_branch: str
    allowed_write_paths: tuple[str, ...]
    forbidden_roots: tuple[Path, ...]


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def _normalize_repo_path(path: str) -> str:
    while path.startswith("./"):
        path = path[2:]
    return path


def _load_scope(path: Path) -> ExecutionScope:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: top-level JSON must be an object")

    required = [
        "expected_execution_root",
        "expected_branch",
        "allowed_write_paths",
        "forbidden_roots",
    ]
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"{path}: missing required field(s): {', '.join(missing)}")

    expected_execution_root = payload["expected_execution_root"]
    expected_branch = payload["expected_branch"]
    allowed_write_paths = payload["allowed_write_paths"]
    forbidden_roots = payload["forbidden_roots"]

    if not isinstance(expected_execution_root, str) or not expected_execution_root:
        raise ValueError(f"{path}: `expected_execution_root` must be a non-empty string")
    if not isinstance(expected_branch, str) or not expected_branch:
        raise ValueError(f"{path}: `expected_branch` must be a non-empty string")
    if not isinstance(allowed_write_paths, list) or not all(isinstance(item, str) and item for item in allowed_write_paths):
        raise ValueError(f"{path}: `allowed_write_paths` must be an array of non-empty strings")
    if not isinstance(forbidden_roots, list) or not all(isinstance(item, str) and item for item in forbidden_roots):
        raise ValueError(f"{path}: `forbidden_roots` must be an array of non-empty strings")

    return ExecutionScope(
        expected_execution_root=Path(expected_execution_root).expanduser().resolve(strict=False),
        expected_branch=expected_branch,
        allowed_write_paths=tuple(_normalize_repo_path(item) for item in allowed_write_paths),
        forbidden_roots=tuple(Path(item).expanduser().resolve(strict=False) for item in forbidden_roots),
    )


def _git_root(cwd: Path) -> Path | None:
    result = _run_git(["rev-parse", "--show-toplevel"], cwd)
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve(strict=False)


def _current_branch(cwd: Path) -> str | None:
    result = _run_git(["branch", "--show-current"], cwd)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _changed_paths(cwd: Path) -> list[str] | None:
    result = _run_git(["status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd)
    if result.returncode != 0:
        return None

    fields = result.stdout.split("\0")
    if fields and fields[-1] == "":
        fields.pop()

    paths: list[str] = []
    index = 0
    while index < len(fields):
        entry = fields[index]
        if len(entry) < 4:
            index += 1
            continue

        status = entry[:2]
        paths.append(_normalize_repo_path(entry[3:]))
        if status[0] in {"R", "C"} or status[1] in {"R", "C"}:
            index += 1
            if index < len(fields):
                paths.append(_normalize_repo_path(fields[index]))
        index += 1

    return sorted(set(paths))


def _path_allowed(path: str, allowed_write_paths: tuple[str, ...]) -> bool:
    return any(path == allowed or (allowed.endswith("/") and path.startswith(allowed)) for allowed in allowed_write_paths)


def _format_path(path: Path) -> str:
    return str(path)


def check_scope(scope: ExecutionScope, cwd: Path) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []

    actual_root = _git_root(cwd)
    if actual_root is None:
        failures.append(f"{cwd}: not inside a git repository")
        return failures, warnings
    if actual_root != scope.expected_execution_root:
        failures.append(
            "execution root mismatch: "
            f"expected {_format_path(scope.expected_execution_root)}, got {_format_path(actual_root)}"
        )

    actual_branch = _current_branch(cwd)
    if actual_branch is None:
        failures.append(f"{actual_root}: could not determine current branch")
    elif actual_branch != scope.expected_branch:
        failures.append(f"branch mismatch: expected {scope.expected_branch}, got {actual_branch or '<detached HEAD>'}")

    changed_paths = _changed_paths(actual_root)
    if changed_paths is None:
        failures.append(f"{actual_root}: could not read git status")
    else:
        out_of_scope = [path for path in changed_paths if not _path_allowed(path, scope.allowed_write_paths)]
        if out_of_scope:
            failures.append(
                "changed paths outside allowed_write_paths: "
                + ", ".join(out_of_scope)
                + " (allowed: "
                + ", ".join(scope.allowed_write_paths)
                + ")"
            )

    for forbidden_root in scope.forbidden_roots:
        if not forbidden_root.exists():
            warnings.append(f"forbidden root missing, skipped: {_format_path(forbidden_root)}")
            continue

        forbidden_git_root = _git_root(forbidden_root)
        if forbidden_git_root is None:
            warnings.append(f"forbidden root is not a git repository, skipped: {_format_path(forbidden_root)}")
            continue

        forbidden_changes = _changed_paths(forbidden_git_root)
        if forbidden_changes is None:
            failures.append(f"forbidden root status unreadable: {_format_path(forbidden_git_root)}")
        elif forbidden_changes:
            failures.append(
                "forbidden root is dirty: "
                f"{_format_path(forbidden_git_root)} has changed paths: "
                + ", ".join(forbidden_changes)
            )

    return failures, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Assert the current checkout matches a declared execution scope.")
    parser.add_argument("--scope", required=True, help="Path to execution scope JSON.")
    args = parser.parse_args(argv)

    try:
        scope = _load_scope(Path(args.scope))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL could not load scope: {exc}", file=sys.stderr)
        return 2

    failures, warnings = check_scope(scope, Path.cwd())
    for warning in warnings:
        print(f"WARN {warning}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    print("PASS execution scope matches declared root, branch, write paths, and forbidden roots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
