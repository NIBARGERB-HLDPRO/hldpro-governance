#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import assert_execution_scope


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _repo_relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _discover_scope_candidates(root: Path, branch: str, issue_number: int, scopes_dir: Path) -> tuple[list[tuple[Path, Any]], list[str]]:
    warnings: list[str] = []
    candidates: list[tuple[Path, Any]] = []
    if not scopes_dir.is_dir():
        warnings.append(f"scopes directory missing: {_repo_relative(root, scopes_dir)}")
        return candidates, warnings

    for scope_path in sorted(scopes_dir.glob("*.json")):
        try:
            scope = assert_execution_scope._load_scope(scope_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            warnings.append(f"skipped unreadable scope {scope_path.name}: {exc}")
            continue
        if scope.expected_branch != branch:
            continue
        if scope.lane_claim is None or scope.lane_claim.issue_number != issue_number:
            continue
        candidates.append((scope_path, scope))
    return candidates, warnings


def _select_scope(candidates: list[tuple[Path, Any]]) -> tuple[tuple[Path, Any] | None, str | None]:
    if not candidates:
        return None, "no claimed execution scope matched the current issue branch"

    implementation_ready = [
        item for item in candidates if getattr(item[1], "execution_mode", "planning_only") != "planning_only"
    ]
    if len(implementation_ready) == 1:
        return implementation_ready[0], None
    if len(implementation_ready) > 1:
        names = ", ".join(path.name for path, _ in implementation_ready)
        return None, f"multiple implementation-capable claimed scopes matched the current branch: {names}"
    if len(candidates) == 1:
        return candidates[0], None

    names = ", ".join(path.name for path, _ in candidates)
    return None, f"multiple planning-only claimed scopes matched the current branch: {names}"


def _linked_handoff(root: Path, scope_ref: str) -> dict[str, Any] | None:
    handoffs_dir = root / "raw" / "handoffs"
    matches: list[tuple[str, Path, dict[str, Any]]] = []
    if not handoffs_dir.is_dir():
        return None
    for handoff_path in sorted(handoffs_dir.glob("*.json")):
        payload = _load_json(handoff_path)
        if not payload:
            continue
        if payload.get("execution_scope_ref") == scope_ref:
            created_at = str(payload.get("created_at") or "")
            matches.append((created_at, handoff_path, payload))
    if not matches:
        return None
    matches.sort(key=lambda item: (item[0], item[1].name), reverse=True)
    return matches[0][2]


def _required_specialist_signals(plan_payload: dict[str, Any]) -> list[str]:
    signals: list[str] = []
    specialist_reviews = plan_payload.get("specialist_reviews")
    if isinstance(specialist_reviews, list):
        for review in specialist_reviews:
            if not isinstance(review, dict):
                continue
            reviewer = review.get("reviewer")
            if isinstance(reviewer, str) and reviewer.strip():
                signals.append(reviewer.strip())

    alternate_review = plan_payload.get("alternate_model_review")
    if isinstance(alternate_review, dict) and alternate_review.get("required") is True:
        signals.append("alternate_model_review")

    execution_handoff = plan_payload.get("execution_handoff")
    if isinstance(execution_handoff, dict) and execution_handoff.get("qa_gate_required") is True:
        signals.append("qa_gate_required")

    return signals


def _startup_summary(root: Path, scope_path: Path, scope: Any) -> tuple[dict[str, Any], int]:
    scope_ref = _repo_relative(root, scope_path)
    branch = assert_execution_scope._current_branch(root)
    issue_number = scope.lane_claim.issue_number if scope.lane_claim else None

    failures, warnings = assert_execution_scope.check_scope(
        scope,
        root,
        require_lane_claim=True,
    )

    handoff_payload = _linked_handoff(root, scope_ref)
    plan_payload = None
    if handoff_payload and isinstance(handoff_payload.get("structured_plan_ref"), str):
        plan_payload = _load_json(root / str(handoff_payload["structured_plan_ref"]))

    next_role = None
    next_execution_step = None
    required_specialists: list[str] = []
    if isinstance(plan_payload, dict):
        execution_handoff = plan_payload.get("execution_handoff")
        if isinstance(execution_handoff, dict):
            next_role = execution_handoff.get("next_role")
            next_execution_step = execution_handoff.get("next_execution_step")
        required_specialists = _required_specialist_signals(plan_payload)

    if not next_role and handoff_payload:
        to_role = handoff_payload.get("to_role")
        if isinstance(to_role, str) and to_role.strip():
            next_role = to_role.strip()

    payload = {
        "status": "pass" if not failures else "blocked",
        "scope_path": scope_ref,
        "issue_number": issue_number,
        "execution_mode": scope.execution_mode,
        "next_role": next_role,
        "next_execution_step": next_execution_step,
        "required_specialists": required_specialists,
        "warnings": warnings,
        "failures": failures,
        "handoff_ref": None if not handoff_payload else _repo_relative(
            root, root / str(handoff_payload.get("execution_scope_ref", scope_ref))
        ),
        "branch": branch,
    }
    return payload, 0 if not failures else 1


def _emit_startup_human(payload: dict[str, Any]) -> None:
    status = payload["status"]
    if status == "pass":
        print("PASS startup execution context")
    else:
        print("BLOCKED startup execution context")
    print(f"branch: {payload.get('branch') or '(unknown)'}")
    print(f"scope_path: {payload.get('scope_path') or '(none)'}")
    print(f"issue_number: {payload.get('issue_number') or '(unknown)'}")
    print(f"execution_mode: {payload.get('execution_mode') or '(unknown)'}")
    if payload.get("next_role"):
        print(f"next_role: {payload['next_role']}")
    if payload.get("next_execution_step"):
        print(f"next_execution_step: {payload['next_execution_step']}")
    specialists = payload.get("required_specialists") or []
    if specialists:
        print("required_specialists: " + ", ".join(str(item) for item in specialists))
    warnings = payload.get("warnings") or []
    for warning in warnings:
        print(f"WARN {warning}")
    failures = payload.get("failures") or []
    for failure in failures:
        print(f"FAIL {failure}")


def _run_startup_preflight(scopes_dir_arg: str, emit_json: bool) -> int:
    root = Path.cwd()
    branch = assert_execution_scope._current_branch(root)
    if not branch:
        payload = {
            "status": "blocked",
            "scope_path": None,
            "issue_number": None,
            "execution_mode": None,
            "next_role": None,
            "next_execution_step": None,
            "required_specialists": [],
            "warnings": [],
            "failures": ["could not determine current branch"],
            "branch": None,
        }
        if emit_json:
            json.dump(payload, sys.stdout, indent=2, sort_keys=True)
            sys.stdout.write("\n")
        else:
            _emit_startup_human(payload)
        return 1

    issue_number = assert_execution_scope._branch_issue_number(branch)
    if issue_number is None:
        payload = {
            "status": "blocked",
            "scope_path": None,
            "issue_number": None,
            "execution_mode": None,
            "next_role": None,
            "next_execution_step": None,
            "required_specialists": [],
            "warnings": [],
            "failures": [f"branch is not issue-backed: {branch}"],
            "branch": branch,
        }
        if emit_json:
            json.dump(payload, sys.stdout, indent=2, sort_keys=True)
            sys.stdout.write("\n")
        else:
            _emit_startup_human(payload)
        return 1

    scopes_dir = (root / scopes_dir_arg).resolve()
    candidates, warnings = _discover_scope_candidates(root, branch, issue_number, scopes_dir)
    selected, selection_failure = _select_scope(candidates)
    if selection_failure:
        payload = {
            "status": "blocked",
            "scope_path": None,
            "issue_number": issue_number,
            "execution_mode": None,
            "next_role": None,
            "next_execution_step": None,
            "required_specialists": [],
            "warnings": warnings,
            "failures": [selection_failure],
            "branch": branch,
        }
        if emit_json:
            json.dump(payload, sys.stdout, indent=2, sort_keys=True)
            sys.stdout.write("\n")
        else:
            _emit_startup_human(payload)
        return 1

    assert selected is not None
    payload, exit_code = _startup_summary(root, selected[0], selected[1])
    payload["warnings"] = warnings + list(payload.get("warnings") or [])
    payload["branch"] = branch

    if emit_json:
        json.dump(payload, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        _emit_startup_human(payload)
    return exit_code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preflight the current execution environment against a scope file.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--scope", help="Path to execution scope JSON.")
    mode.add_argument(
        "--startup-preflight",
        action="store_true",
        help="Discover the active execution scope for the current issue branch and summarize startup execution context.",
    )
    parser.add_argument("--changed-files-file", help="Optional file containing changed paths to validate.")
    parser.add_argument("--require-lane-claim", action="store_true", help="Require the scope lane_claim to match the current issue branch.")
    parser.add_argument("--scopes-dir", default="raw/execution-scopes", help="Scope directory used by --startup-preflight.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output for startup preflight mode.")
    args = parser.parse_args(argv)

    if args.startup_preflight:
        return _run_startup_preflight(args.scopes_dir, args.json)

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
