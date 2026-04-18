#!/usr/bin/env python3
"""Compare live GitHub org repositories with the governed repo registry."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.overlord.governed_repos import governed_repos, load_registry


DEFAULT_REGISTRY = REPO_ROOT / "docs" / "governed_repos.json"
GH_REPO_FIELDS = "name,isArchived,isPrivate,defaultBranchRef,description,url,pushedAt"


@dataclass(frozen=True)
class OrgRepo:
    name: str
    full_name: str
    archived: bool
    private: bool
    default_branch: str
    url: str
    pushed_at: str


@dataclass(frozen=True)
class InventoryDrift:
    missing_active_repos: tuple[OrgRepo, ...]
    stale_registry_repos: tuple[str, ...]
    archived_registry_repos: tuple[OrgRepo, ...]
    archived_unregistered_repos: tuple[OrgRepo, ...]

    def has_blocking_drift(self) -> bool:
        return bool(self.missing_active_repos or self.stale_registry_repos or self.archived_registry_repos)


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _inventory_rows_from_payload(payload: object) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict) and isinstance(payload.get("repositories"), list):
        rows = payload["repositories"]
    else:
        raise ValueError("inventory JSON must be a list or an object with repositories[]")
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("inventory repositories must be objects")
    return list(rows)


def _default_branch_name(row: dict[str, Any]) -> str:
    default_branch = row.get("defaultBranchRef")
    if isinstance(default_branch, dict):
        name = default_branch.get("name")
        return str(name) if name else ""
    if isinstance(default_branch, str):
        return default_branch
    return ""


def parse_inventory(payload: object, organization: str) -> list[OrgRepo]:
    repos: list[OrgRepo] = []
    for row in _inventory_rows_from_payload(payload):
        name = str(row.get("name") or "")
        if not name:
            raise ValueError("inventory repository missing name")
        full_name = str(row.get("nameWithOwner") or row.get("fullName") or f"{organization}/{name}")
        repos.append(
            OrgRepo(
                name=name,
                full_name=full_name,
                archived=bool(row.get("isArchived", row.get("archived", False))),
                private=bool(row.get("isPrivate", row.get("private", False))),
                default_branch=_default_branch_name(row),
                url=str(row.get("url") or ""),
                pushed_at=str(row.get("pushedAt") or ""),
            )
        )
    return sorted(repos, key=lambda repo: repo.full_name.lower())


def load_inventory_file(path: Path, organization: str) -> list[OrgRepo]:
    return parse_inventory(_load_json(path), organization)


def load_live_inventory(organization: str, limit: int) -> list[OrgRepo]:
    command = [
        "gh",
        "repo",
        "list",
        organization,
        "--limit",
        str(limit),
        "--json",
        GH_REPO_FIELDS,
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return parse_inventory(json.loads(result.stdout), organization)


def compare_inventory(registry_path: Path, inventory: list[OrgRepo]) -> InventoryDrift:
    registry = load_registry(registry_path)
    organization = str(registry.get("organization") or "")
    registry_full_names = {repo.github_repo for repo in governed_repos(registry_path)}
    live_by_full_name = {repo.full_name: repo for repo in inventory}

    missing_active = tuple(
        repo
        for repo in inventory
        if not repo.archived and repo.full_name not in registry_full_names
    )
    stale_registry = tuple(
        sorted(
            repo_name
            for repo_name in registry_full_names
            if repo_name.startswith(f"{organization}/") and repo_name not in live_by_full_name
        )
    )
    archived_registry = tuple(
        repo
        for repo in inventory
        if repo.archived and repo.full_name in registry_full_names
    )
    archived_unregistered = tuple(
        repo
        for repo in inventory
        if repo.archived and repo.full_name not in registry_full_names
    )
    return InventoryDrift(
        missing_active_repos=missing_active,
        stale_registry_repos=stale_registry,
        archived_registry_repos=archived_registry,
        archived_unregistered_repos=archived_unregistered,
    )


def render_text(drift: InventoryDrift) -> str:
    lines: list[str] = []
    if not drift.has_blocking_drift():
        lines.append("PASS org inventory matches governed repo registry for active repos.")
    else:
        lines.append("FAIL org inventory drift detected.")

    if drift.missing_active_repos:
        lines.append("Missing active repos:")
        for repo in drift.missing_active_repos:
            lines.append(f"- {repo.full_name} default={repo.default_branch or 'unknown'} url={repo.url or 'unknown'}")
    if drift.stale_registry_repos:
        lines.append("Registry repos missing from live org inventory:")
        for repo_name in drift.stale_registry_repos:
            lines.append(f"- {repo_name}")
    if drift.archived_registry_repos:
        lines.append("Archived repos still present in registry:")
        for repo in drift.archived_registry_repos:
            lines.append(f"- {repo.full_name}")
    if drift.archived_unregistered_repos:
        lines.append("Archived repos absent from registry (notice):")
        for repo in drift.archived_unregistered_repos:
            lines.append(f"- {repo.full_name}")

    return "\n".join(lines)


def render_markdown(drift: InventoryDrift, *, warn_only: bool) -> str:
    status = "ATTENTION" if drift.has_blocking_drift() else "CLEAN"
    if warn_only and drift.has_blocking_drift():
        status = "ATTENTION (warn-only)"
    lines = [f"**Status:** {status}", ""]
    lines.append("| Category | Count | Repositories |")
    lines.append("|---|---:|---|")
    lines.append(
        "| Missing active repos | "
        f"{len(drift.missing_active_repos)} | "
        f"{_repo_list(repo.full_name for repo in drift.missing_active_repos)} |"
    )
    lines.append(
        "| Registry repos absent from GitHub | "
        f"{len(drift.stale_registry_repos)} | "
        f"{_repo_list(drift.stale_registry_repos)} |"
    )
    lines.append(
        "| Archived registry repos | "
        f"{len(drift.archived_registry_repos)} | "
        f"{_repo_list(repo.full_name for repo in drift.archived_registry_repos)} |"
    )
    lines.append(
        "| Archived unregistered repos | "
        f"{len(drift.archived_unregistered_repos)} | "
        f"{_repo_list(repo.full_name for repo in drift.archived_unregistered_repos)} |"
    )
    return "\n".join(lines)


def _repo_list(values: Any) -> str:
    items = [str(value) for value in values]
    if not items:
        return "None"
    return ", ".join(items)


def render_json(drift: InventoryDrift) -> str:
    return json.dumps(
        {
            "missing_active_repos": [repo.__dict__ for repo in drift.missing_active_repos],
            "stale_registry_repos": list(drift.stale_registry_repos),
            "archived_registry_repos": [repo.__dict__ for repo in drift.archived_registry_repos],
            "archived_unregistered_repos": [repo.__dict__ for repo in drift.archived_unregistered_repos],
            "blocking_drift": drift.has_blocking_drift(),
        },
        indent=2,
        sort_keys=True,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check live org repo inventory against governed repo registry.")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--inventory-file", type=Path, help="Fixture or captured gh repo list JSON.")
    source.add_argument("--live", action="store_true", help="Read org repo inventory through GitHub CLI.")
    parser.add_argument("--limit", type=int, default=200, help="GitHub repo list limit for --live.")
    parser.add_argument("--format", choices=("text", "markdown", "json"), default="text")
    parser.add_argument("--warn-only", action="store_true", help="Report drift but return success.")
    args = parser.parse_args(argv)

    registry = load_registry(args.registry)
    organization = str(registry.get("organization") or "")
    if not organization:
        print("FAIL registry organization is required", file=sys.stderr)
        return 2

    try:
        inventory = load_live_inventory(organization, args.limit) if args.live else load_inventory_file(args.inventory_file, organization)
        drift = compare_inventory(args.registry, inventory)
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"FAIL unable to load org inventory: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(render_json(drift))
    elif args.format == "markdown":
        print(render_markdown(drift, warn_only=args.warn_only))
    else:
        print(render_text(drift))

    if drift.has_blocking_drift() and not args.warn_only:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
