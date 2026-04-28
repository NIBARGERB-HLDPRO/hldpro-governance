#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import validate_closeout
except ImportError:  # pragma: no cover - supports direct execution from unusual cwd.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import validate_closeout


ISSUE_BRANCH_PATTERN = re.compile(r"(?:^|[-_/])issue-(\d+)(?:[-_/]|$)")

GOVERNANCE_SURFACE_PREFIXES = (
    ".github/",
    "agents/",
    "docs/",
    "hooks/",
    "launchd/",
    "metrics/",
    "raw/",
    "scripts/",
    "tools/local-ci-gate/",
    "wiki/",
)
GOVERNANCE_SURFACE_FILES = {
    "CLAUDE.md",
    "README.md",
    "STANDARDS.md",
    "OVERLORD_BACKLOG.md",
}

PLANNING_ONLY_PREFIXES = (
    "docs/plans/",
    "raw/closeouts/",
    "raw/cross-review/",
    "raw/execution-scopes/",
    "raw/handoffs/",
    "raw/validation/",
)
PLANNING_ONLY_FILES = {
    "OVERLORD_BACKLOG.md",
    "docs/PROGRESS.md",
}


@dataclass(frozen=True)
class CloseoutDecision:
    required: bool
    issue_number: int | None
    closeout_paths: tuple[str, ...]
    reason: str
    failures: tuple[str, ...] = ()


def _normalize(path: str) -> str:
    while path.startswith("./"):
        path = path[2:]
    return path.strip()


def _read_changed_files(path: Path) -> list[str]:
    return [_normalize(line) for line in path.read_text(encoding="utf-8").splitlines() if _normalize(line)]


def _issue_number(branch_name: str) -> int | None:
    match = ISSUE_BRANCH_PATTERN.search(branch_name)
    return int(match.group(1)) if match else None


def _is_governance_surface(path: str) -> bool:
    return path in GOVERNANCE_SURFACE_FILES or path.startswith(GOVERNANCE_SURFACE_PREFIXES)


def _is_planning_only(path: str) -> bool:
    return path in PLANNING_ONLY_FILES or path.startswith(PLANNING_ONLY_PREFIXES)


def _matching_closeouts(changed_files: list[str], issue_number: int) -> tuple[str, ...]:
    token = f"issue-{issue_number}"
    return tuple(
        path
        for path in changed_files
        if path.startswith("raw/closeouts/") and path.endswith(".md") and token in Path(path).name
    )


def evaluate(root: Path, branch_name: str, changed_files: list[str]) -> CloseoutDecision:
    relevant = [path for path in changed_files if _is_governance_surface(path)]
    if not relevant:
        return CloseoutDecision(False, None, (), "no_governance_surface_changes")

    if all(_is_planning_only(path) for path in relevant):
        return CloseoutDecision(False, _issue_number(branch_name), (), "planning_only_changes")

    issue_number = _issue_number(branch_name)
    if issue_number is None:
        return CloseoutDecision(
            True,
            None,
            (),
            "missing_issue_branch",
            ("Stage 6 closeout enforcement requires an issue branch name like issue-<number>-...",),
        )

    closeouts = _matching_closeouts(changed_files, issue_number)
    if not closeouts:
        return CloseoutDecision(
            True,
            issue_number,
            (),
            "missing_stage6_closeout",
            (
                f"Stage 6 closeout required for issue-{issue_number} implementation/governance-surface changes.",
                f"Add raw/closeouts/*issue-{issue_number}*.md and run scripts/overlord/validate_closeout.py.",
            ),
        )
    if len(closeouts) > 1:
        return CloseoutDecision(
            True,
            issue_number,
            closeouts,
            "multiple_stage6_closeouts",
            (f"Multiple Stage 6 closeouts match issue-{issue_number}: {', '.join(closeouts)}",),
        )

    failures = tuple(validate_closeout.validate_closeout(root, Path(closeouts[0])))
    if failures:
        return CloseoutDecision(True, issue_number, closeouts, "invalid_stage6_closeout", failures)

    return CloseoutDecision(True, issue_number, closeouts, "stage6_closeout_valid")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Require Stage 6 closeout evidence for implementation PRs.")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--branch-name", required=True, help="Current branch name")
    parser.add_argument("--changed-files-file", required=True, help="File containing changed paths, one per line")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve(strict=False)
    changed_files = _read_changed_files(Path(args.changed_files_file))
    decision = evaluate(root, args.branch_name, changed_files)

    if decision.failures:
        for failure in decision.failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1

    if decision.required:
        print(f"PASS Stage 6 closeout enforced: {decision.closeout_paths[0]}")
    else:
        print(f"PASS Stage 6 closeout not required: {decision.reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
