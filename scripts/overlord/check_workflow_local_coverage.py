#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


INVENTORY_PATH = Path("docs/workflow-local-coverage-inventory.json")
WORKFLOW_ROOT = Path(".github/workflows")
ALLOWED_COVERAGE_TYPES = {"local_command", "workflow_contract", "script_dry_run", "github_only"}
LOCAL_FIRST_TYPES = {"local_command", "workflow_contract", "script_dry_run"}


def _normalize_path(value: str) -> str:
    while value.startswith("./"):
        value = value[2:]
    return value


def _load_inventory(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _actual_workflows(root: Path) -> set[str]:
    workflow_root = root / WORKFLOW_ROOT
    return {
        path.relative_to(root).as_posix()
        for path in workflow_root.glob("*.yml")
        if path.is_file()
    }


def _command_file_candidates(command: list[Any]) -> list[str]:
    candidates: list[str] = []
    for token in command[1:]:
        if not isinstance(token, str):
            continue
        if token.startswith("-") or token in {".", "|"}:
            continue
        normalized = _normalize_path(token)
        if normalized.startswith((".github/", "scripts/", "tools/", "docs/", "raw/")):
            candidates.append(normalized)
    return candidates


def _validate_coverage(
    root: Path,
    workflow_path: str,
    entry: dict[str, Any],
    failures: list[str],
) -> None:
    coverage = entry.get("coverage")
    if not isinstance(coverage, list) or not coverage:
        failures.append(f"{workflow_path}: `coverage` must be a non-empty array")
        return

    has_local_first = False
    has_github_only = False
    for index, item in enumerate(coverage, start=1):
        prefix = f"{workflow_path}: coverage[{index}]"
        if not isinstance(item, dict):
            failures.append(f"{prefix} must be an object")
            continue
        coverage_type = item.get("type")
        if coverage_type not in ALLOWED_COVERAGE_TYPES:
            failures.append(f"{prefix}.type must be one of {sorted(ALLOWED_COVERAGE_TYPES)}")
            continue
        if coverage_type in LOCAL_FIRST_TYPES:
            has_local_first = True
            command = item.get("command")
            if not isinstance(command, list) or not command or not all(isinstance(part, str) and part for part in command):
                failures.append(f"{prefix}.command must be a non-empty string array for {coverage_type}")
                continue
            for candidate in _command_file_candidates(command):
                if not (root / candidate).exists():
                    failures.append(f"{prefix}.command references missing repo path: {candidate}")
        if coverage_type == "github_only":
            has_github_only = True
            rationale = item.get("rationale")
            if not isinstance(rationale, str) or len(rationale.strip()) < 20:
                failures.append(f"{prefix}.rationale must explain the GitHub-only exemption")

    risk = entry.get("risk")
    if not isinstance(risk, str) or not risk:
        failures.append(f"{workflow_path}: `risk` must be a non-empty string")
    if risk != "github-only-side-effecting" and risk != "github-only-scheduled-operational" and not has_local_first:
        failures.append(f"{workflow_path}: non-GitHub-only workflows require local, contract, or script/dry-run coverage")
    if risk.startswith("github-only") and not has_github_only:
        failures.append(f"{workflow_path}: GitHub-only workflows require an explicit github_only coverage entry")


def _validate_required_snippets(root: Path, workflow_path: str, entry: dict[str, Any], failures: list[str]) -> None:
    snippets = entry.get("required_snippets", [])
    if not isinstance(snippets, list) or not snippets:
        failures.append(f"{workflow_path}: `required_snippets` must be a non-empty array")
        return
    if not all(isinstance(snippet, str) and snippet for snippet in snippets):
        failures.append(f"{workflow_path}: `required_snippets` must contain non-empty strings")
        return

    workflow_text = (root / workflow_path).read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in workflow_text:
            failures.append(f"{workflow_path}: required snippet not found: {snippet}")


def check_inventory(root: Path, inventory_path: Path = INVENTORY_PATH) -> list[str]:
    root = root.resolve()
    failures: list[str] = []
    inventory_file = root / inventory_path
    if not inventory_file.is_file():
        return [f"missing workflow coverage inventory: {inventory_path}"]

    try:
        inventory = _load_inventory(inventory_file)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"could not load workflow coverage inventory: {exc}"]

    workflows = inventory.get("workflows")
    if not isinstance(workflows, list):
        return [f"{inventory_path}: `workflows` must be an array"]

    actual = _actual_workflows(root)
    seen: set[str] = set()
    for index, entry in enumerate(workflows, start=1):
        if not isinstance(entry, dict):
            failures.append(f"{inventory_path}: workflows[{index}] must be an object")
            continue
        raw_path = entry.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            failures.append(f"{inventory_path}: workflows[{index}].path must be a non-empty string")
            continue
        workflow_path = _normalize_path(raw_path)
        if workflow_path in seen:
            failures.append(f"{workflow_path}: duplicate workflow inventory entry")
            continue
        seen.add(workflow_path)
        if workflow_path not in actual:
            failures.append(f"{workflow_path}: inventory references missing workflow file")
            continue
        _validate_coverage(root, workflow_path, entry, failures)
        _validate_required_snippets(root, workflow_path, entry, failures)
        rationale = entry.get("rationale")
        if not isinstance(rationale, str) or len(rationale.strip()) < 20:
            failures.append(f"{workflow_path}: `rationale` must explain coverage classification")

    missing = sorted(actual - seen)
    unexpected = sorted(seen - actual)
    if missing:
        failures.append("workflow files missing inventory entries: " + ", ".join(missing))
    if unexpected:
        failures.append("inventory entries without workflow files: " + ", ".join(unexpected))

    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate local-first coverage inventory for GitHub workflows.")
    parser.add_argument("--root", default=".", help="Repository root to validate")
    parser.add_argument("--inventory", default=str(INVENTORY_PATH), help="Inventory path relative to root")
    args = parser.parse_args(argv)

    failures = check_inventory(Path(args.root), Path(args.inventory))
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("PASS workflow local coverage inventory")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
