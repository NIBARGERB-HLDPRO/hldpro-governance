#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


GOVERNANCE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = GOVERNANCE_ROOT / "docs" / "graphify_targets.json"
MANAGED_MARKER = "# hldpro-governance graphify hook helper managed"
HOOK_NAMES = ("post-commit", "post-checkout")


class HelperError(RuntimeError):
    pass


@dataclass(frozen=True)
class HookPlan:
    repo_slug: str
    target_repo: Path
    governance_root: Path
    source_path: Path
    output_path: Path
    wiki_path: Path
    hook_paths: dict[str, Path]

    def to_json(self) -> dict[str, object]:
        return {
            "repo_slug": self.repo_slug,
            "target_repo": str(self.target_repo),
            "governance_root": str(self.governance_root),
            "source_path": str(self.source_path),
            "output_path": str(self.output_path),
            "wiki_path": str(self.wiki_path),
            "hook_paths": {name: str(path) for name, path in self.hook_paths.items()},
        }


def load_manifest(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise HelperError("manifest root must be an object")
    targets = payload.get("targets")
    if not isinstance(targets, list) or not targets:
        raise HelperError("manifest must contain a non-empty targets array")
    return payload


def target_rows(manifest: dict[str, object]) -> list[dict[str, object]]:
    rows = manifest.get("targets")
    if not isinstance(rows, list):
        raise HelperError("manifest targets must be an array")
    return [row for row in rows if isinstance(row, dict)]


def find_target(rows: list[dict[str, object]], repo_slug: str) -> dict[str, object]:
    for row in rows:
        if row.get("repo_slug") == repo_slug:
            return row
    raise HelperError(f"repo_slug not found in manifest: {repo_slug}")


def infer_repo_slug(rows: list[dict[str, object]], target_repo: Path) -> str:
    names = {target_repo.name, target_repo.resolve().name}
    normalized_names = {name.lower() for name in names}
    for row in rows:
        repo_slug = str(row.get("repo_slug", ""))
        display_name = str(row.get("display_name", ""))
        candidates = {repo_slug.lower(), display_name.lower()}
        if normalized_names & candidates:
            return repo_slug
    raise HelperError(f"unable to infer repo slug from target repo: {target_repo}")


def resolve_under(root: Path, raw_path: object, field: str) -> Path:
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise HelperError(f"manifest target missing {field}")
    path = Path(raw_path)
    if path.is_absolute():
        raise HelperError(f"manifest {field} must be relative to governance root: {raw_path}")
    return (root / path).resolve()


def git_hook_paths(target_repo: Path) -> dict[str, Path]:
    result = subprocess.run(
        ["git", "-C", str(target_repo), "rev-parse", "--git-path", "hooks"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise HelperError(result.stderr.strip() or f"not a git repository: {target_repo}")
    hooks_root = Path(result.stdout.strip())
    if not hooks_root.is_absolute():
        hooks_root = (target_repo / hooks_root).resolve()
    return {name: hooks_root / name for name in HOOK_NAMES}


def build_plan(args: argparse.Namespace) -> HookPlan:
    governance_root = Path(args.governance_root).resolve()
    manifest_path = Path(args.manifest).resolve() if args.manifest else governance_root / "docs" / "graphify_targets.json"
    target_repo = Path(args.target_repo).resolve()
    manifest = load_manifest(manifest_path)
    rows = target_rows(manifest)
    repo_slug = args.repo_slug or infer_repo_slug(rows, target_repo)
    target = find_target(rows, repo_slug)
    return HookPlan(
        repo_slug=repo_slug,
        target_repo=target_repo,
        governance_root=governance_root,
        source_path=resolve_under(governance_root, target.get("source_path"), "source_path"),
        output_path=resolve_under(governance_root, target.get("output_path"), "output_path"),
        wiki_path=resolve_under(governance_root, target.get("wiki_path"), "wiki_path"),
        hook_paths=git_hook_paths(target_repo),
    )


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def preflight_safe_output(plan: HookPlan) -> None:
    if plan.repo_slug != "hldpro-governance" and is_relative_to(plan.output_path, plan.target_repo):
        raise HelperError(f"refusing graphify output under product repo checkout: {plan.output_path}")
    if not is_relative_to(plan.output_path, plan.governance_root):
        raise HelperError(f"refusing graphify output outside governance root: {plan.output_path}")
    if not is_relative_to(plan.wiki_path, plan.governance_root):
        raise HelperError(f"refusing wiki output outside governance root: {plan.wiki_path}")


def build_refresh_command(plan: HookPlan, no_html: bool) -> list[str]:
    command = [
        sys.executable,
        str(plan.governance_root / "scripts" / "knowledge_base" / "build_graph.py"),
        "--source",
        str(plan.source_path),
        "--output",
        str(plan.output_path),
        "--wiki-dir",
        str(plan.wiki_path),
        "--repo-slug",
        plan.repo_slug,
    ]
    if no_html:
        command.append("--no-html")
    return command


def managed_hook_body(governance_root: Path, target_repo: Path, repo_slug: str) -> str:
    helper = governance_root / "scripts" / "knowledge_base" / "graphify_hook_helper.py"
    return f"""#!/usr/bin/env bash
{MANAGED_MARKER}
set -euo pipefail

python3 "{helper}" refresh \\
  --governance-root "{governance_root}" \\
  --target-repo "{target_repo}" \\
  --repo-slug "{repo_slug}" \\
  --no-html
"""


def install_hooks(plan: HookPlan, backup_existing: bool, force: bool) -> None:
    body = managed_hook_body(plan.governance_root, plan.target_repo, plan.repo_slug)
    for name, path in plan.hook_paths.items():
        if path.exists():
            current = path.read_text(encoding="utf-8", errors="replace")
            if MANAGED_MARKER not in current and not (backup_existing or force):
                raise HelperError(f"refusing to overwrite unmanaged hook {path}; use --backup-existing or --force")
            if MANAGED_MARKER not in current and backup_existing:
                backup = path.with_name(f"{path.name}.pre-governance-graphify")
                path.replace(backup)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        path.chmod(0o755)
        print(f"installed {name}: {path}")


def execute_refresh(plan: HookPlan, no_html: bool) -> int:
    preflight_safe_output(plan)
    return subprocess.run(build_refresh_command(plan, no_html=no_html)).returncode


def print_json(data: object) -> None:
    json.dump(data, sys.stdout, indent=2)
    sys.stdout.write("\n")


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--governance-root", default=str(GOVERNANCE_ROOT), help="hldpro-governance checkout root")
    parser.add_argument("--manifest", help="Path to graphify_targets.json; defaults to <governance-root>/docs/graphify_targets.json")
    parser.add_argument("--target-repo", default=".", help="Product/governed repo checkout root")
    parser.add_argument("--repo-slug", help="Manifest repo_slug; inferred from --target-repo when omitted")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install and run governance-managed graphify hooks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve_parser = subparsers.add_parser("resolve", help="Print resolved helper paths as JSON")
    add_common_args(resolve_parser)

    dry_run_parser = subparsers.add_parser("dry-run", help="Resolve paths and print the refresh command without running it")
    add_common_args(dry_run_parser)
    dry_run_parser.add_argument("--no-html", action="store_true", help="Include --no-html in the refresh command")

    refresh_parser = subparsers.add_parser("refresh", help="Run the governance graph builder for the resolved target")
    add_common_args(refresh_parser)
    refresh_parser.add_argument("--no-html", action="store_true", help="Skip graph.html generation")

    install_parser = subparsers.add_parser("install", help="Install managed post-commit and post-checkout hooks")
    add_common_args(install_parser)
    install_parser.add_argument("--backup-existing", action="store_true", help="Rename unmanaged existing hooks before installing")
    install_parser.add_argument("--force", action="store_true", help="Overwrite unmanaged existing hooks without backup")

    args = parser.parse_args()
    try:
        plan = build_plan(args)
        if args.command == "resolve":
            preflight_safe_output(plan)
            print_json(plan.to_json())
            return 0

        if args.command == "dry-run":
            preflight_safe_output(plan)
            payload = plan.to_json()
            payload["refresh_command"] = build_refresh_command(plan, no_html=args.no_html)
            print_json(payload)
            return 0

        if args.command == "refresh":
            return execute_refresh(plan, no_html=args.no_html)

        if args.command == "install":
            preflight_safe_output(plan)
            install_hooks(plan, backup_existing=args.backup_existing, force=args.force)
            return 0

        parser.error(f"unknown command: {args.command}")
        return 2
    except HelperError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
