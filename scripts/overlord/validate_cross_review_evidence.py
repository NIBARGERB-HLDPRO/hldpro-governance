#!/usr/bin/env python3
"""Validate cross-review evidence for a PR diff.

This module extracts the "newly-added cross-review file" detection logic from
require-cross-review.yml so that it can be unit-tested without running a GitHub
Actions runner.

Public interface
----------------
detect_cross_review_violations(diff_files, planning_only=False) -> list[str]
    Return a list of violation strings (empty = no violations).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Sequence


# ---------------------------------------------------------------------------
# Trigger detection
# ---------------------------------------------------------------------------

CROSS_REVIEW_TRIGGER_PATTERNS: list[str] = [
    r"^STANDARDS\.md$",
    r"^docs/.*/[^/]*charter[^/]*\.md$",
    r"^docs/[^/]*charter[^/]*\.md$",
    r"^agents/[^/]+\.md$",
    r"^hooks/[^/]+\.sh$",
    r"^\.github/workflows/check-[^/]+\.yml$",
    r"^scripts/cross-review/",
    r"^AGENT_REGISTRY\.md$",
]

_TRIGGER_RE = re.compile("|".join(CROSS_REVIEW_TRIGGER_PATTERNS))


def _is_cross_review_trigger(path: str) -> bool:
    """Return True if *path* should trigger cross-review enforcement."""
    return bool(_TRIGGER_RE.search(path))


def _cross_review_files(diff_files: Sequence[str]) -> list[str]:
    """Return paths that are cross-review artifacts (raw/cross-review/*.md)."""
    return [
        p for p in diff_files
        if re.match(r"^raw/cross-review/.*\.md$", p)
    ]


def _trusted_base_violation(diff_files: Sequence[str], planning_only: bool) -> str | None:
    """Return an error string if newly-introduced cross-review evidence must be rejected.

    The rule (G3.3/G3.6): a PR author may NOT introduce a ``raw/cross-review/``
    file in the same PR that requires it, unless ``PLANNING_ONLY=true`` is set by
    the *caller* (not the author).
    """
    if planning_only:
        return None

    new_evidence = _cross_review_files(diff_files)
    if new_evidence:
        return (
            "PR introduces raw/cross-review/ evidence in the same diff that "
            "requires it, without PLANNING_ONLY=true. "
            f"Offending files: {new_evidence}"
        )
    return None


# ---------------------------------------------------------------------------
# Main validation function
# ---------------------------------------------------------------------------

def detect_cross_review_violations(
    diff_files: Sequence[str],
    *,
    planning_only: bool = False,
    base_sha: str = "",
    head_sha: str = "",
) -> list[str]:
    """Validate cross-review evidence for a set of changed files.

    Parameters
    ----------
    diff_files:
        Paths returned by ``git diff --name-only BASE...HEAD``.
    planning_only:
        If True, trusted-base evidence restriction is relaxed (caller-set only).
    base_sha, head_sha:
        If either is empty the gate must fail closed (G3.2).

    Returns
    -------
    List of human-readable violation strings; empty = pass.
    """
    violations: list[str] = []

    # G3.2 — fail closed on missing context
    if not base_sha or not head_sha:
        violations.append(
            "[require-cross-review] Missing pull request context (BASE_SHA or HEAD_SHA empty); "
            "gate must fail closed. Provide a proper PR base/head SHA."
        )
        return violations

    # Determine if cross-review is even triggered
    triggered = any(_is_cross_review_trigger(p) for p in diff_files)
    if not triggered:
        return []

    # Check that at least one cross-review artifact exists in the diff
    evidence = _cross_review_files(diff_files)
    if not evidence:
        violations.append(
            "[require-cross-review] Cross-review trigger hit but no raw/cross-review/*.md "
            "artifact found in PR diff."
        )
        return violations

    # G3.3/G3.6 — trusted-base evidence rule
    tb_violation = _trusted_base_violation(diff_files, planning_only)
    if tb_violation:
        violations.append(tb_violation)

    return violations


# ---------------------------------------------------------------------------
# CLI entry point (for use from shell)
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Validate cross-review evidence")
    parser.add_argument("--diff-files", required=True, help="Newline-separated list of changed files")
    parser.add_argument("--planning-only", action="store_true", default=False)
    parser.add_argument("--base-sha", default=os.environ.get("BASE_SHA", ""))
    parser.add_argument("--head-sha", default=os.environ.get("HEAD_SHA", ""))
    args = parser.parse_args(argv)

    diff_files = [f for f in args.diff_files.splitlines() if f.strip()]
    violations = detect_cross_review_violations(
        diff_files,
        planning_only=args.planning_only,
        base_sha=args.base_sha,
        head_sha=args.head_sha,
    )

    for v in violations:
        print(f"::error::{v}", file=sys.stderr)

    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
