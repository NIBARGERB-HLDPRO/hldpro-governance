#!/usr/bin/env python3
"""Validate registry-dependent governance surfaces.

Some consumers can read docs/governed_repos.json directly at runtime. GitHub
Actions checkout steps cannot be generated dynamically, so this validator keeps
those explicit workflow surfaces aligned with registry subsystem flags.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.overlord.governed_repos import governed_repos, repo_names_enabled_for


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def repos_for_static_checkout() -> list[tuple[str, str, str]]:
    rows = []
    for repo in governed_repos():
        if repo.repo_slug == "hldpro-governance":
            continue
        if repo.enabled("sweep"):
            rows.append((repo.repo_slug, repo.github_repo, repo.ci_checkout_path))
    return rows


def validate_static_checkout_workflow(path: str) -> None:
    workflow = read_text(path)
    for repo_slug, github_repo, checkout_path in repos_for_static_checkout():
        check(
            f"repository: {github_repo}" in workflow,
            f"{path} missing checkout repository for sweep-enabled {repo_slug}: {github_repo}",
        )
        check(
            f"path: {checkout_path}" in workflow,
            f"{path} missing checkout path for sweep-enabled {repo_slug}: {checkout_path}",
        )


def validate_runtime_registry_consumers() -> None:
    raw_feed = read_text(".github/workflows/raw-feed-sync.yml")
    check(
        "validate_governed_repos.py --print-subsystem raw_feed_sync" in raw_feed,
        "raw-feed-sync.yml must derive repo selection from raw_feed_sync subsystem flags",
    )

    sweep = read_text(".github/workflows/overlord-sweep.yml")
    for subsystem in ("sweep", "code_governance"):
        check(
            f"validate_governed_repos.py --print-subsystem {subsystem}" in sweep,
            f"overlord-sweep.yml must derive {subsystem} selection from registry",
        )
    check(
        "build_effectiveness_metrics.py" in sweep and "--repos-root repos" in sweep,
        "overlord-sweep.yml must build metrics through registry-aware build_effectiveness_metrics.py",
    )
    check(
        "graphify_targets.py list --scheduled --format tsv" in sweep,
        "overlord-sweep.yml must derive graphify refreshes from graphify target manifest",
    )
    check(
        "build_org_governance_compendium.py" in sweep,
        "overlord-sweep.yml must build compendium through registry-aware generator",
    )
    check(
        "memory_integrity.py" in sweep,
        "overlord-sweep.yml must run registry-aware memory integrity validation",
    )

    local_graphify = read_text("scripts/knowledge_base/prepare_local_graphify_repos.sh")
    check(
        "graphify_targets.py\" list --scheduled --format tsv" in local_graphify,
        "prepare_local_graphify_repos.sh must derive local links from graphify target manifest",
    )


def validate_docs_surfaces() -> None:
    readme = read_text("README.md")
    standards = read_text("STANDARDS.md")
    check("docs/governed_repos.json" in readme, "README.md must point to governed_repos.json")
    check("all 5 repos" not in readme, "README.md contains stale fixed repo count: all 5 repos")
    check(
        "docs/governed_repos.json" in standards and "executable source of truth" in standards,
        "STANDARDS.md repo registry section must identify governed_repos.json as source of truth",
    )
    for repo in governed_repos():
        check(
            repo.display_name in standards or repo.repo_dir_name in standards,
            f"STANDARDS.md repo registry summary missing {repo.repo_slug}",
        )


def validate_subsystem_expectations() -> None:
    for subsystem in (
        "sweep",
        "metrics",
        "raw_feed_sync",
        "codex_ingestion",
        "memory_integrity",
        "compendium",
        "code_governance",
    ):
        names = repo_names_enabled_for(subsystem)
        check(
            len(names) == len(set(names)),
            f"{subsystem} registry selection contains duplicate repo names: {names}",
        )


def main() -> int:
    validate_static_checkout_workflow(".github/workflows/overlord-sweep.yml")
    validate_static_checkout_workflow(".github/workflows/overlord-nightly-cleanup.yml")
    validate_runtime_registry_consumers()
    validate_docs_surfaces()
    validate_subsystem_expectations()
    print("PASS registry-dependent governance surfaces are reconciled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
