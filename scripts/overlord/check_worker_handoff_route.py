#!/usr/bin/env python3
"""Validate that a new code-file write is covered by Worker handoff evidence."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

import assert_execution_scope


WORKER_ROLES = {
    "worker",
    "implementer",
    "claude-sonnet-worker",
    "sonnet-worker",
    "local-qwen-worker",
    "qwen-worker",
    "worker-specialist",
}

CODE_EXTENSIONS = {".sh", ".py", ".mjs", ".js", ".ts", ".tsx", ".go", ".rb", ".rs"}


def _normalize_repo_path(path: str) -> str:
    return assert_execution_scope._normalize_repo_path(path.strip())


def _actionable_next_step(issue_number: int | None, target_path: str) -> str:
    issue_token = f"issue-{issue_number}" if issue_number else "issue-<n>"
    return (
        "Next: create/update "
        f"raw/execution-scopes/<date>-{issue_token}-worker-implementation.json and "
        f"raw/handoffs/<date>-{issue_token}-<scope>.json; include "
        f"{target_path!r} in allowed_write_paths; set execution_mode to implementation_ready; "
        "set handoff_evidence.status to accepted; then rerun from the approved Worker lane."
    )


def _result(decision: str, reason: str, missing_evidence: list[str] | None = None) -> dict[str, object]:
    return {
        "decision": decision,
        "reason": reason,
        "missing_evidence": missing_evidence or [],
    }


def _find_scope(repo_root: Path, issue_number: int) -> tuple[Path | None, list[str]]:
    scope_dir = repo_root / "raw" / "execution-scopes"
    if not scope_dir.is_dir():
        return None, ["execution scope directory"]
    matches = sorted(scope_dir.glob(f"*issue-{issue_number}*implementation*.json"))
    if len(matches) == 1:
        return matches[0], []
    if not matches:
        return None, ["issue-specific implementation execution scope"]
    return None, ["single issue-specific implementation execution scope"]


def check_route(repo_root: Path, target_path: str, branch_name: str, role: str) -> dict[str, object]:
    repo_root = repo_root.resolve(strict=False)
    normalized_target = _normalize_repo_path(target_path)
    issue_number = assert_execution_scope._branch_issue_number(branch_name)
    role_normalized = role.strip().lower() or "planner"

    if not normalized_target:
        return _result("block", "Worker handoff route missing target path.", ["target path"])

    if Path(normalized_target).suffix not in CODE_EXTENSIONS:
        return _result("allow", "Target path is not a governed code-file extension.")

    if issue_number is None:
        return _result(
            "block",
            "BLOCKED: New code-file writes require an issue branch before Worker handoff can be verified. "
            + _actionable_next_step(None, normalized_target),
            ["issue branch"],
        )

    if role_normalized not in WORKER_ROLES:
        return _result(
            "block",
            "BLOCKED: New code file must be authored by an approved Worker, not the planning/orchestration lane. "
            + _actionable_next_step(issue_number, normalized_target),
            ["approved Worker lane"],
        )

    scope_path, missing = _find_scope(repo_root, issue_number)
    if scope_path is None:
        return _result(
            "block",
            "BLOCKED: Worker lane is missing issue-backed implementation scope evidence. "
            + _actionable_next_step(issue_number, normalized_target),
            missing,
        )

    try:
        scope = assert_execution_scope._load_scope(scope_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return _result("block", f"BLOCKED: Worker handoff scope is invalid: {exc}", ["valid execution scope"])

    missing_evidence: list[str] = []
    if not assert_execution_scope._path_allowed(normalized_target, scope.allowed_write_paths):
        missing_evidence.append("target path in allowed_write_paths")
    if scope.handoff_evidence is None:
        missing_evidence.append("accepted Worker handoff evidence")
    elif scope.handoff_evidence.status.lower() != "accepted":
        missing_evidence.append("handoff_evidence.status accepted")

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as changed_file:
        changed_file.write(normalized_target + "\n")
        changed_file_path = Path(changed_file.name)
    try:
        failures, warnings = assert_execution_scope.check_scope(
            scope,
            repo_root,
            changed_files_file=changed_file_path,
            require_lane_claim=True,
        )
    finally:
        changed_file_path.unlink(missing_ok=True)

    if failures:
        reason = (
            "BLOCKED: Worker handoff evidence does not authorize this new code-file write. "
            + _actionable_next_step(issue_number, normalized_target)
            + "\n\n"
            + "\n".join(f"FAIL {failure}" for failure in failures)
        )
        return _result("block", reason, missing_evidence or ["valid Worker handoff evidence"])

    reason = "ALLOW: approved Worker handoff evidence covers this target path."
    if warnings:
        reason += "\n" + "\n".join(f"WARN {warning}" for warning in warnings)
    return _result("allow", reason)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--target-path", required=True)
    parser.add_argument("--branch-name")
    parser.add_argument("--role", default=os.environ.get("HLDPRO_LANE_ROLE") or os.environ.get("SOM_LANE_ROLE") or "planner")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = Path(args.repo_root)
    branch_name = args.branch_name
    if not branch_name:
        branch_name = assert_execution_scope._current_branch(repo_root) or ""

    result = check_route(repo_root, args.target_path, branch_name, args.role)
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(result["reason"])
    return 0 if result["decision"] == "allow" else 1


if __name__ == "__main__":
    raise SystemExit(main())
