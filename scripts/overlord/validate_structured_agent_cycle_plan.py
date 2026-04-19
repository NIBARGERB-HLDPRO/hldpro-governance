#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


GOVERNANCE_SURFACE_PREFIXES = (
    ".github/scripts/",
    ".github/workflows/",
    "agents/",
    "docs/schemas/",
    "docs/plans/",
    "hooks/",
    "launchd/",
    "raw/closeouts/",
    "raw/cross-review/",
    "raw/execution-scopes/",
    "raw/gate/",
    "raw/model-fallbacks/",
    "raw/operator-context/",
    "raw/packets/",
    "metrics/pilot/",
    "metrics/self-learning/",
    "scripts/knowledge_base/",
    "scripts/lam/",
    "scripts/orchestrator/",
    "scripts/overlord/",
    "scripts/packet/",
    "wiki/",
)
GOVERNANCE_SURFACE_FILES = {
    "CLAUDE.md",
    "README.md",
    "STANDARDS.md",
    "OVERLORD_BACKLOG.md",
    "docs/DATA_DICTIONARY.md",
    "docs/FEATURE_REGISTRY.md",
    "docs/ORG_GOVERNANCE_COMPENDIUM.md",
    "docs/PROGRESS.md",
    "docs/SERVICE_REGISTRY.md",
    "docs/governed_repos.json",
    "docs/graphify_targets.json",
}
IMPLEMENTATION_READY_MODES = {"implementation_ready", "implementation_complete"}
ACCEPTED_REVIEW_STATES = {"accepted", "accepted_with_followup"}


def _display_path(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def _load_json_safe(path: Path, root: Path, failures: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        failures.append(f"{_display_path(path, root)}: could not parse JSON: {exc}")
        return None


def _find_plan_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*structured-agent-cycle-plan.json"))


def _require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def _branch_issue_number(branch_name: str) -> int | None:
    match = re.search(r"(?:^|/)issue-(\d+)(?:[-_/]|$)", branch_name)
    return int(match.group(1)) if match else None


def _is_governance_surface(path: str) -> bool:
    normalized = path
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized in GOVERNANCE_SURFACE_FILES or any(
        normalized.startswith(prefix) for prefix in GOVERNANCE_SURFACE_PREFIXES
    )


def _read_changed_files(path: Path | None) -> list[str]:
    if path is None:
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _matching_plan_payloads(
    loaded_plans: list[tuple[Path, object | None]],
    root: Path,
    issue_number: int | None,
) -> list[tuple[Path, object]]:
    if issue_number is None:
        return []
    matches: list[tuple[Path, object]] = []
    for file_path, payload in loaded_plans:
        if isinstance(payload, dict) and payload.get("issue_number") == issue_number:
            matches.append((file_path.relative_to(root), payload))
    return matches


def _matching_execution_scopes(root: Path, issue_number: int | None, mode: str) -> list[Path]:
    if issue_number is None:
        return []
    scope_root = root / "raw" / "execution-scopes"
    if not scope_root.is_dir():
        return []
    return sorted(scope_root.glob(f"*issue-{issue_number}*{mode}*.json"))


def _validate_planner_boundary_scope_presence(
    root: Path,
    branch_name: str,
    changed_files: list[str],
    failures: list[str],
) -> None:
    boundary_changes = [path for path in changed_files if _is_governance_surface(path)]
    if not boundary_changes:
        return

    issue_number = _branch_issue_number(branch_name)
    if issue_number is None:
        failures.append(
            "planner-boundary changes require a branch name containing `issue-<number>` so execution-scope evidence can be resolved; changed paths: "
            + ", ".join(boundary_changes)
        )
        return

    implementation_scopes = _matching_execution_scopes(root, issue_number, "implementation")
    planning_scopes = _matching_execution_scopes(root, issue_number, "planning")
    if len(implementation_scopes) > 1:
        failures.append(f"multiple implementation execution scopes match issue #{issue_number}")
    if len(planning_scopes) > 1:
        failures.append(f"multiple planning execution scopes match issue #{issue_number}")
    if not implementation_scopes and not planning_scopes:
        failures.append(
            f"planner-boundary changes require an issue-specific execution scope for issue #{issue_number}; "
            f"expected raw/execution-scopes/*issue-{issue_number}*implementation*.json or *issue-{issue_number}*planning*.json; "
            "changed paths: " + ", ".join(boundary_changes)
        )


def _validate_implementation_ready_plan(path: Path, payload: object, failures: list[str]) -> None:
    if not isinstance(payload, dict):
        failures.append(f"{path}: implementation gate plan must be a JSON object")
        return
    _require(payload.get("approved") is True, f"{path}: governance-surface plan must have `approved: true`", failures)
    handoff = payload.get("execution_handoff")
    if not isinstance(handoff, dict):
        failures.append(f"{path}: governance-surface plan must include `execution_handoff`")
    else:
        mode = handoff.get("execution_mode")
        _require(
            mode in IMPLEMENTATION_READY_MODES,
            f"{path}: governance-surface plan execution_mode must be one of {sorted(IMPLEMENTATION_READY_MODES)}, got {mode!r}",
            failures,
        )
    review = payload.get("alternate_model_review")
    if isinstance(review, dict) and review.get("required") is True:
        status = review.get("status")
        _require(
            status in ACCEPTED_REVIEW_STATES,
            f"{path}: required alternate_model_review must be accepted before governance-surface implementation, got {status!r}",
            failures,
        )


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
    parser.add_argument("--changed-files-file", type=Path, help="Optional newline-delimited changed file list for governance-surface enforcement.")
    parser.add_argument("--enforce-governance-surface", action="store_true", help="Require an approved issue-specific plan when governance-surface files changed.")
    parser.add_argument("--enforce-planner-boundary-scope", action="store_true", help="Require issue-specific execution-scope evidence when planner-boundary files changed.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    files = _find_plan_files(root)
    failures: list[str] = []
    loaded_plans = [(file_path, _load_json_safe(file_path, root, failures)) for file_path in files]

    if args.require_if_issue_branch:
        branch = args.branch_name
        branch_requires_plan = branch.startswith("issue-") or branch.startswith("riskfix/")
        if branch_requires_plan and not files:
            failures.append(f"{branch}: requires at least one `*structured-agent-cycle-plan.json` file before execution.")

    changed_files = _read_changed_files(args.changed_files_file)
    governance_surface_changes = [path for path in changed_files if _is_governance_surface(path)]
    if args.enforce_governance_surface and governance_surface_changes:
        issue_number = _branch_issue_number(args.branch_name)
        if issue_number is None:
            failures.append(
                "governance-surface changes require a branch name containing `issue-<number>` and a matching canonical structured plan; changed paths: "
                + ", ".join(governance_surface_changes)
            )
        matches = _matching_plan_payloads(loaded_plans, root, issue_number)
        if not matches:
            issue_label = f"issue #{issue_number}" if issue_number is not None else "this branch"
            failures.append(
                f"governance-surface changes require a canonical structured plan for {issue_label}; changed paths: "
                + ", ".join(governance_surface_changes)
            )
        for rel_path, payload in matches:
            _validate_implementation_ready_plan(rel_path, payload, failures)

    if args.enforce_planner_boundary_scope:
        _validate_planner_boundary_scope_presence(root, args.branch_name, changed_files, failures)

    for file_path, payload in loaded_plans:
        if payload is not None:
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
