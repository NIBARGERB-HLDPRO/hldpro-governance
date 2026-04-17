#!/usr/bin/env python3
"""Shared helpers for the governed repository registry."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = REPO_ROOT / "docs" / "governed_repos.json"


@dataclass(frozen=True)
class GovernedRepo:
    repo_slug: str
    display_name: str
    repo_dir_name: str
    github_repo: str
    local_path: str
    ci_checkout_path: str
    graph_output_path: str
    wiki_path: str
    project_path: str
    governance_tier: str
    security_tier: str
    description: str
    enabled_subsystems: dict[str, bool]

    def enabled(self, subsystem: str) -> bool:
        return bool(self.enabled_subsystems.get(subsystem))


def _expand_home(raw: str) -> Path:
    if raw.startswith("~/"):
        return Path.home() / raw[2:]
    return Path(raw)


def load_registry(path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("governed repo registry root must be an object")
    return payload


def governed_repos(path: Path = DEFAULT_REGISTRY) -> list[GovernedRepo]:
    payload = load_registry(path)
    rows = payload.get("repositories")
    if not isinstance(rows, list):
        raise ValueError("governed repo registry must contain repositories[]")
    repos: list[GovernedRepo] = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("repository entry must be an object")
        repos.append(
            GovernedRepo(
                repo_slug=str(row["repo_slug"]),
                display_name=str(row["display_name"]),
                repo_dir_name=str(row["repo_dir_name"]),
                github_repo=str(row["github_repo"]),
                local_path=str(row["local_path"]),
                ci_checkout_path=str(row["ci_checkout_path"]),
                graph_output_path=str(row["graph_output_path"]),
                wiki_path=str(row["wiki_path"]),
                project_path=str(row["project_path"]),
                governance_tier=str(row["governance_tier"]),
                security_tier=str(row["security_tier"]),
                description=str(row["description"]),
                enabled_subsystems={str(k): bool(v) for k, v in dict(row["enabled_subsystems"]).items()},
            )
        )
    return repos


def repos_enabled_for(subsystem: str, path: Path = DEFAULT_REGISTRY) -> list[GovernedRepo]:
    return [repo for repo in governed_repos(path) if repo.enabled(subsystem)]


def repo_names_enabled_for(subsystem: str, path: Path = DEFAULT_REGISTRY) -> list[str]:
    return [repo.repo_dir_name for repo in repos_enabled_for(subsystem, path)]


def repos_root(path: Path = DEFAULT_REGISTRY) -> Path:
    payload = load_registry(path)
    env_name = str(payload.get("repos_root_env") or "HLDPRO_REPOS_ROOT")
    if os.environ.get(env_name):
        return Path(os.environ[env_name])
    return _expand_home(str(payload.get("default_repos_root") or "~/Developer/HLDPRO"))
