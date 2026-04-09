#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _find_plan_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*structured-agent-cycle-plan.json"))


def _require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def _validate_file(path: Path, payload: object, failures: list[str]) -> None:
    if not isinstance(payload, dict):
        failures.append(f"{path}: top-level JSON must be an object")
        return

    required = [
        "session_id",
        "issue_number",
        "objective",
        "tier",
        "scope_boundary",
        "out_of_scope",
        "research_summary",
        "research_artifacts",
        "sprints",
        "specialist_reviews",
        "alternate_model_review",
        "execution_handoff",
        "material_deviation_rules",
        "approved",
        "approved_by",
        "approved_at",
    ]
    for key in required:
        _require(key in payload, f"{path}: missing required field `{key}`", failures)

    if failures:
        return

    _require(isinstance(payload["issue_number"], int) and payload["issue_number"] > 0, f"{path}: `issue_number` must be a positive integer", failures)
    _require(isinstance(payload["tier"], int) and 1 <= payload["tier"] <= 3, f"{path}: `tier` must be 1, 2, or 3", failures)
    _require(isinstance(payload["scope_boundary"], list) and len(payload["scope_boundary"]) > 0, f"{path}: `scope_boundary` must be a non-empty array", failures)
    _require(isinstance(payload["out_of_scope"], list) and len(payload["out_of_scope"]) > 0, f"{path}: `out_of_scope` must be a non-empty array", failures)
    _require(isinstance(payload["research_artifacts"], list) and len(payload["research_artifacts"]) > 0, f"{path}: `research_artifacts` must be a non-empty array", failures)
    _require(isinstance(payload["material_deviation_rules"], list) and len(payload["material_deviation_rules"]) > 0, f"{path}: `material_deviation_rules` must be a non-empty array", failures)
    _require(isinstance(payload["approved_by"], list) and len(payload["approved_by"]) > 0, f"{path}: `approved_by` must be a non-empty array", failures)

    sprints = payload["sprints"]
    _require(isinstance(sprints, list) and len(sprints) > 0, f"{path}: `sprints` must be a non-empty array", failures)
    if isinstance(sprints, list):
        for index, sprint in enumerate(sprints, start=1):
            prefix = f"{path}: sprint[{index}]"
            _require(isinstance(sprint, dict), f"{prefix} must be an object", failures)
            if not isinstance(sprint, dict):
                continue
            for key in ["name", "goal", "tasks", "acceptance_criteria", "file_paths"]:
                _require(key in sprint, f"{prefix} missing `{key}`", failures)
            _require(isinstance(sprint.get("tasks"), list) and len(sprint.get("tasks", [])) > 0, f"{prefix} `tasks` must be a non-empty array", failures)
            _require(isinstance(sprint.get("acceptance_criteria"), list) and len(sprint.get("acceptance_criteria", [])) > 0, f"{prefix} `acceptance_criteria` must be a non-empty array", failures)
            _require(isinstance(sprint.get("file_paths"), list) and len(sprint.get("file_paths", [])) > 0, f"{prefix} `file_paths` must be a non-empty array", failures)

    specialist_reviews = payload["specialist_reviews"]
    _require(isinstance(specialist_reviews, list) and len(specialist_reviews) > 0, f"{path}: `specialist_reviews` must be a non-empty array", failures)
    if isinstance(specialist_reviews, list):
        for index, review in enumerate(specialist_reviews, start=1):
            prefix = f"{path}: specialist_reviews[{index}]"
            _require(isinstance(review, dict), f"{prefix} must be an object", failures)
            if not isinstance(review, dict):
                continue
            for key in ["reviewer", "role", "focus", "status", "summary", "evidence"]:
                _require(key in review, f"{prefix} missing `{key}`", failures)
            _require(isinstance(review.get("evidence"), list) and len(review.get("evidence", [])) > 0, f"{prefix} `evidence` must be a non-empty array", failures)

    alternate_review = payload["alternate_model_review"]
    _require(isinstance(alternate_review, dict), f"{path}: `alternate_model_review` must be an object", failures)
    if isinstance(alternate_review, dict):
        for key in ["required", "reviewer", "model_family", "status", "summary", "evidence"]:
            _require(key in alternate_review, f"{path}: `alternate_model_review` missing `{key}`", failures)
        _require(isinstance(alternate_review.get("evidence"), list) and len(alternate_review.get("evidence", [])) > 0, f"{path}: `alternate_model_review.evidence` must be a non-empty array", failures)

    execution_handoff = payload["execution_handoff"]
    _require(isinstance(execution_handoff, dict), f"{path}: `execution_handoff` must be an object", failures)
    if isinstance(execution_handoff, dict):
        for key in ["session_agent", "execution_mode", "approved_scope_summary", "next_execution_step", "blocked_on"]:
            _require(key in execution_handoff, f"{path}: `execution_handoff` missing `{key}`", failures)
        _require(isinstance(execution_handoff.get("blocked_on"), list), f"{path}: `execution_handoff.blocked_on` must be an array", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate structured agent cycle plan files.")
    parser.add_argument("--root", default=".", help="Repo root to scan.")
    parser.add_argument("--require-if-issue-branch", action="store_true", help="Fail if on an issue/riskfix branch and no structured plan file exists.")
    parser.add_argument("--branch-name", default="", help="Optional branch name for enforcement decisions.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    files = _find_plan_files(root)
    failures: list[str] = []

    if args.require_if_issue_branch:
        branch = args.branch_name
        branch_requires_plan = branch.startswith("issue-") or branch.startswith("riskfix/")
        if branch_requires_plan and not files:
            failures.append(f"{branch}: requires at least one `*structured-agent-cycle-plan.json` file before execution.")

    for file_path in files:
        payload = _load_json(file_path)
        _validate_file(file_path.relative_to(root), payload, failures)

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    if files:
        print(f"PASS validated {len(files)} structured agent cycle plan file(s)")
    else:
        print("PASS no structured agent cycle plan files found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
