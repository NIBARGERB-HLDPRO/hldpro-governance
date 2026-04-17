#!/usr/bin/env python3
"""Validate the governed repository registry and graphify reconciliation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.overlord.governed_repos import governed_repos, load_registry, repo_names_enabled_for


DEFAULT_REGISTRY = REPO_ROOT / "docs" / "governed_repos.json"
DEFAULT_GRAPHIFY_TARGETS = REPO_ROOT / "docs" / "graphify_targets.json"
REQUIRED_SUBSYSTEMS = {
    "graphify",
    "sweep",
    "metrics",
    "memory_integrity",
    "codex_ingestion",
    "compendium",
    "raw_feed_sync",
    "code_governance",
}
SAFE_RELATIVE_RE = re.compile(r"^[A-Za-z0-9_.@/-]+$")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path} is not valid JSON: {exc}")
    check(isinstance(payload, dict), f"{path} root must be an object")
    return payload


def validate_registry_shape(registry_path: Path) -> None:
    payload = load_registry(registry_path)
    check(isinstance(payload.get("version"), int), "version must be an integer")
    check(isinstance(payload.get("organization"), str) and payload["organization"], "organization is required")
    rows = payload.get("repositories")
    check(isinstance(rows, list) and rows, "repositories must be a non-empty list")

    seen: dict[str, str] = {}
    for repo in governed_repos(registry_path):
        for field_name, value in (
            ("repo_slug", repo.repo_slug),
            ("display_name", repo.display_name),
            ("repo_dir_name", repo.repo_dir_name),
            ("github_repo", repo.github_repo),
            ("local_path", repo.local_path),
            ("ci_checkout_path", repo.ci_checkout_path),
            ("graph_output_path", repo.graph_output_path),
            ("wiki_path", repo.wiki_path),
            ("project_path", repo.project_path),
            ("governance_tier", repo.governance_tier),
            ("security_tier", repo.security_tier),
            ("description", repo.description),
        ):
            check(value, f"{repo.repo_slug}.{field_name} must not be empty")
            check(".." not in value.split("/"), f"{repo.repo_slug}.{field_name} must not contain '..'")
            if field_name.endswith("_path") or field_name in {"local_path", "ci_checkout_path"}:
                check(SAFE_RELATIVE_RE.fullmatch(value) is not None, f"{repo.repo_slug}.{field_name} has unsafe characters: {value}")
        check("/" in repo.github_repo, f"{repo.repo_slug}.github_repo must be owner/name")
        check(repo.graph_output_path.startswith("graphify-out/"), f"{repo.repo_slug}.graph_output_path must stay under graphify-out/")
        check(repo.wiki_path.startswith("wiki/"), f"{repo.repo_slug}.wiki_path must stay under wiki/")
        check(repo.project_path.startswith("projects/"), f"{repo.repo_slug}.project_path must stay under projects/")
        missing_subsystems = REQUIRED_SUBSYSTEMS - set(repo.enabled_subsystems)
        check(not missing_subsystems, f"{repo.repo_slug}.enabled_subsystems missing {sorted(missing_subsystems)}")
        for key, value in repo.enabled_subsystems.items():
            check(isinstance(value, bool), f"{repo.repo_slug}.enabled_subsystems.{key} must be boolean")
        for unique_field, value in (
            ("repo_slug", repo.repo_slug),
            ("repo_dir_name", repo.repo_dir_name),
            ("github_repo", repo.github_repo),
            ("ci_checkout_path", repo.ci_checkout_path),
            ("graph_output_path", repo.graph_output_path),
            ("wiki_path", repo.wiki_path),
            ("project_path", repo.project_path),
        ):
            key = f"{unique_field}:{value}"
            check(key not in seen, f"duplicate {unique_field}: {value} ({seen.get(key)} and {repo.repo_slug})")
            seen[key] = repo.repo_slug


def validate_graphify_reconciliation(registry_path: Path, graphify_targets_path: Path) -> None:
    graphify_targets = load_json(graphify_targets_path)
    rows = graphify_targets.get("targets")
    check(isinstance(rows, list) and rows, "graphify targets must contain targets[]")
    by_slug = {str(row.get("repo_slug")): row for row in rows if isinstance(row, dict)}

    for repo in governed_repos(registry_path):
        if not repo.enabled("graphify"):
            continue
        target = by_slug.get(repo.repo_slug)
        check(target is not None, f"graphify target missing for {repo.repo_slug}")
        expected_source = "." if repo.repo_slug == "hldpro-governance" else repo.ci_checkout_path
        expected = {
            "display_name": repo.display_name,
            "source_path": expected_source,
            "output_path": repo.graph_output_path,
            "wiki_path": repo.wiki_path,
            "scheduled": repo.enabled("graphify"),
        }
        for key, value in expected.items():
            check(target.get(key) == value, f"graphify target {repo.repo_slug}.{key}={target.get(key)!r}, expected {value!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate governed repository registry")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--graphify-targets", type=Path, default=DEFAULT_GRAPHIFY_TARGETS)
    parser.add_argument("--print-subsystem", choices=sorted(REQUIRED_SUBSYSTEMS))
    parser.add_argument("--print-exempt", action="store_true")
    args = parser.parse_args()

    validate_registry_shape(args.registry)
    validate_graphify_reconciliation(args.registry, args.graphify_targets)
    if args.print_subsystem:
        print(" ".join(repo_names_enabled_for(args.print_subsystem, args.registry)))
        return 0
    if args.print_exempt:
        print(" ".join(repo.repo_dir_name for repo in governed_repos(args.registry) if not repo.enabled("code_governance")))
        return 0
    print(f"PASS governed repo registry valid: {args.registry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
