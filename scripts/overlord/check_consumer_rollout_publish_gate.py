#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


TITLE_RE = re.compile(r"^\[Issue #\d+\]\s+.+")
REQUIRED_PR_SECTIONS = [
    "## Summary",
    "## Acceptance Criteria Status",
    "## Validation",
    "## Blockers and Dependencies",
]
RUNNER_TRIGGER_RE = re.compile(r"^(\.github/workflows/|\.github/actionlint\.yaml|scripts/ci/|scripts/runner/)")


class PublishGateError(RuntimeError):
    pass


def _fail(message: str) -> None:
    raise PublishGateError(message)


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, check=False, capture_output=True, text=True)


def _git_root(path: Path) -> Path:
    result = _run_git(["rev-parse", "--show-toplevel"], path)
    if result.returncode != 0:
        _fail(f"target repo must be inside a git repository: {path}")
    return Path(result.stdout.strip()).resolve(strict=False)


def _changed_files(target_repo: Path, base_ref: str) -> list[str]:
    refs = _run_git(["diff", "--name-only", f"{base_ref}...HEAD"], target_repo)
    if refs.returncode != 0:
        detail = refs.stderr.strip() or refs.stdout.strip() or "git diff failed"
        _fail(f"could not compute changed files against {base_ref}: {detail}")
    staged = _run_git(["diff", "--name-only", "--cached"], target_repo)
    if staged.returncode != 0:
        detail = staged.stderr.strip() or staged.stdout.strip() or "git diff --cached failed"
        _fail(f"could not compute staged changed files: {detail}")
    working = _run_git(["diff", "--name-only"], target_repo)
    if working.returncode != 0:
        detail = working.stderr.strip() or working.stdout.strip() or "git diff failed"
        _fail(f"could not compute working-tree changed files: {detail}")
    untracked = _run_git(["ls-files", "--others", "--exclude-standard"], target_repo)
    if untracked.returncode != 0:
        detail = untracked.stderr.strip() or untracked.stdout.strip() or "git ls-files failed"
        _fail(f"could not compute untracked changed files: {detail}")
    changed: set[str] = set()
    for output in (refs.stdout, staged.stdout, working.stdout, untracked.stdout):
        changed.update(line.strip() for line in output.splitlines() if line.strip())
    return sorted(changed)


def _package_has_file_index_check(target_repo: Path) -> bool:
    package_json = target_repo / "package.json"
    if not package_json.is_file():
        return False
    try:
        payload = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    scripts = payload.get("scripts")
    return isinstance(scripts, dict) and isinstance(scripts.get("file-index:check"), str)


def _run_file_index_check(target_repo: Path) -> str | None:
    if not (target_repo / "docs" / "file-index.txt").is_file():
        return None
    if not _package_has_file_index_check(target_repo):
        return None
    proc = subprocess.run(
        ["npm", "run", "file-index:check"],
        cwd=target_repo,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return None
    return (proc.stdout + proc.stderr).strip()


def check_publish_gate(args: argparse.Namespace) -> dict[str, Any]:
    target_repo = _git_root(Path(args.target_repo).resolve())
    changed_files = _changed_files(target_repo, args.base_ref)
    failures: list[str] = []
    warnings: list[str] = []

    if not TITLE_RE.fullmatch(args.pr_title.strip()):
        failures.append("PR title must match: [Issue #<number>] <scope summary>.")

    try:
        body = Path(args.pr_body_file).read_text(encoding="utf-8")
    except OSError as exc:
        _fail(f"could not read PR body file {args.pr_body_file}: {exc}")
    missing_sections = [section for section in REQUIRED_PR_SECTIONS if section not in body]
    if missing_sections:
        failures.append(f"PR body is missing required sections: {', '.join(missing_sections)}")

    if any(RUNNER_TRIGGER_RE.match(path) for path in changed_files):
        if "docs/sprint/runner-status.md" not in changed_files:
            failures.append(
                "CI/runner files changed, but docs/sprint/runner-status.md was not updated."
            )

    file_index_failure = _run_file_index_check(target_repo)
    if file_index_failure:
        failures.append(f"file-index check failed:\n{file_index_failure}")
    elif (target_repo / "docs" / "file-index.txt").is_file() and not _package_has_file_index_check(target_repo):
        warnings.append("docs/file-index.txt exists but package.json lacks file-index:check; skipped")

    return {
        "status": "passed" if not failures else "failed",
        "target_repo": str(target_repo),
        "base_ref": args.base_ref,
        "changed_files": changed_files,
        "failures": failures,
        "warnings": warnings,
    }


def print_json(payload: Any) -> None:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check consumer rollout publish gates before PR creation.")
    parser.add_argument("--target-repo", default=".", help="Consumer repo checkout root")
    parser.add_argument("--base-ref", default="origin/main", help="Base ref for changed-file diff")
    parser.add_argument("--pr-title", required=True, help="Proposed PR title")
    parser.add_argument("--pr-body-file", required=True, help="Path to the proposed PR body markdown file")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        payload = check_publish_gate(args)
        print_json(payload)
        return 0 if payload["status"] == "passed" else 1
    except PublishGateError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
