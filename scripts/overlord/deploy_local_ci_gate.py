#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path


GOVERNANCE_ROOT = Path(__file__).resolve().parents[2]
MANAGED_MARKER = "# hldpro-governance local-ci gate managed"
ALLOWED_SHIM_RELATIVE_PATHS = {
    ".hldpro/local-ci.sh",
    ".governance/local-ci.sh",
}
DEFAULT_SHIM_PATH = ".hldpro/local-ci.sh"
DEFAULT_PROFILE = "hldpro-governance"
DEFAULT_GOVERNANCE_REF = "HEAD"


class DeployError(RuntimeError):
    pass


@dataclass(frozen=True)
class DeployPlan:
    governance_root: Path
    governance_ref: str
    target_repo: Path
    profile: str
    shim_path: Path
    governance_source: Path
    runner_path: Path
    existing_shim_state: str

    def planned_write_set(self, backup_existing: bool) -> list[str]:
        writes: list[str] = []
        if self.existing_shim_state == "unmanaged" and backup_existing:
            writes.append(str(self.shim_path.with_name(f"{self.shim_path.name}.pre-local-ci-gate")))
        writes.append(str(self.shim_path))
        return writes

    def to_json(self, *, backup_existing: bool, include_body: bool = False) -> dict[str, object]:
        payload: dict[str, object] = {
            "governance_root": str(self.governance_root),
            "governance_ref": self.governance_ref,
            "governance_source": str(self.governance_source),
            "profile": self.profile,
            "target_repo": str(self.target_repo),
            "shim_path": str(self.shim_path),
            "existing_shim_state": self.existing_shim_state,
            "managed_marker": MANAGED_MARKER,
            "planned_write_set": self.planned_write_set(backup_existing=backup_existing),
        }
        if include_body:
            payload["shim_body"] = managed_shim_body(self)
        return payload


def _fail(message: str) -> None:
    raise DeployError(message)


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _existing_shim_state(path: Path) -> str:
    if not path.exists():
        return "missing"
    if path.is_dir():
        _fail(f"shim path is a directory, not a file: {path}")
    current = path.read_text(encoding="utf-8", errors="replace")
    return "managed" if MANAGED_MARKER in current else "unmanaged"


def _resolve_shim_path(target_repo: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        resolved = candidate.resolve()
    else:
        resolved = (target_repo / candidate).resolve()
    if not _is_relative_to(resolved, target_repo):
        _fail(f"shim path must stay under target repo: {raw_path}")
    relative = resolved.relative_to(target_repo).as_posix()
    if relative not in ALLOWED_SHIM_RELATIVE_PATHS:
        allowed = ", ".join(sorted(ALLOWED_SHIM_RELATIVE_PATHS))
        _fail(f"shim path must be one of {allowed}: {relative}")
    return resolved


def build_plan(args: argparse.Namespace) -> DeployPlan:
    governance_root = Path(args.governance_root).resolve()
    target_repo = Path(args.target_repo).resolve()
    if not governance_root.is_dir():
        _fail(f"governance root must exist and be a directory: {governance_root}")
    if not target_repo.is_dir():
        _fail(f"target repo must exist and be a directory: {target_repo}")

    shim_path = _resolve_shim_path(target_repo, args.shim_path or DEFAULT_SHIM_PATH)
    governance_source = (governance_root / "tools" / "local-ci-gate").resolve()
    runner_path = governance_source / "bin" / "hldpro-local-ci"
    return DeployPlan(
        governance_root=governance_root,
        governance_ref=args.governance_ref or DEFAULT_GOVERNANCE_REF,
        target_repo=target_repo,
        profile=args.profile or DEFAULT_PROFILE,
        shim_path=shim_path,
        governance_source=governance_source,
        runner_path=runner_path,
        existing_shim_state=_existing_shim_state(shim_path),
    )


def managed_shim_body(plan: DeployPlan) -> str:
    return f"""#!/usr/bin/env bash
{MANAGED_MARKER}
set -euo pipefail

EMBEDDED_GOVERNANCE_ROOT="{plan.governance_root}"
GOVERNANCE_ROOT="${{HLDPRO_GOVERNANCE_ROOT:-$EMBEDDED_GOVERNANCE_ROOT}}"
RUNNER_PATH="${{GOVERNANCE_ROOT}}/tools/local-ci-gate/bin/hldpro-local-ci"

exec python3 "${{RUNNER_PATH}}" run \\
  --profile "{plan.profile}" \\
  --governance-root "${{GOVERNANCE_ROOT}}" \\
  --governance-ref "{plan.governance_ref}" \\
  --repo-root "{plan.target_repo}" \\
  --shim-path "{plan.shim_path}"
"""


def _refuse_unmanaged_overwrite(path: Path, backup_existing: bool, force: bool) -> None:
    if not path.exists():
        return
    if _existing_shim_state(path) != "unmanaged":
        return
    if backup_existing or force:
        return
    _fail(f"refusing to overwrite unmanaged shim {path}; use --backup-existing or --force")


def _write_managed_shim(plan: DeployPlan, backup_existing: bool, force: bool) -> None:
    _refuse_unmanaged_overwrite(plan.shim_path, backup_existing=backup_existing, force=force)
    if plan.shim_path.exists() and plan.existing_shim_state == "unmanaged" and backup_existing:
        backup = plan.shim_path.with_name(f"{plan.shim_path.name}.pre-local-ci-gate")
        plan.shim_path.replace(backup)
        print(f"backed up unmanaged shim: {backup}")
    plan.shim_path.parent.mkdir(parents=True, exist_ok=True)
    plan.shim_path.write_text(managed_shim_body(plan), encoding="utf-8")
    plan.shim_path.chmod(0o755)


def print_json(data: object) -> None:
    json.dump(data, sys.stdout, indent=2)
    sys.stdout.write("\n")


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--governance-root", default=str(GOVERNANCE_ROOT), help="hldpro-governance checkout root")
    parser.add_argument("--governance-ref", default=DEFAULT_GOVERNANCE_REF, help="Pinned governance checkout/ref recorded in the shim")
    parser.add_argument("--target-repo", default=".", help="Consumer repo checkout root")
    parser.add_argument("--shim-path", default=DEFAULT_SHIM_PATH, help="Repo-local shim path, under the target repo root")
    parser.add_argument("--profile", default=DEFAULT_PROFILE, help="Local CI gate profile name")


def _common_preview_payload(plan: DeployPlan, backup_existing: bool, include_body: bool) -> dict[str, object]:
    payload = plan.to_json(backup_existing=backup_existing, include_body=include_body)
    payload["command_preview"] = [
        sys.executable,
        str(plan.runner_path),
        "run",
        "--profile",
        plan.profile,
        "--governance-root",
        str(plan.governance_root),
        "--governance-ref",
        plan.governance_ref,
        "--repo-root",
        str(plan.target_repo),
        "--shim-path",
        str(plan.shim_path),
    ]
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install and refresh governance-managed local CI gate shims.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve_parser = subparsers.add_parser("resolve", help="Print resolved shim paths as JSON")
    add_common_args(resolve_parser)
    resolve_parser.add_argument("--backup-existing", action="store_true", help="Preview a backup when an unmanaged shim exists")

    dry_run_parser = subparsers.add_parser("dry-run", help="Print the resolved write set and shim body without writing")
    add_common_args(dry_run_parser)
    dry_run_parser.add_argument("--backup-existing", action="store_true", help="Preview a backup when an unmanaged shim exists")

    install_parser = subparsers.add_parser("install", help="Install a managed shim")
    add_common_args(install_parser)
    install_parser.add_argument("--backup-existing", action="store_true", help="Rename an unmanaged existing shim before installing")
    install_parser.add_argument("--force", action="store_true", help="Overwrite an unmanaged existing shim without backup")

    refresh_parser = subparsers.add_parser("refresh", help="Refresh a managed shim")
    add_common_args(refresh_parser)
    refresh_parser.add_argument("--backup-existing", action="store_true", help="Rename an unmanaged existing shim before refreshing")
    refresh_parser.add_argument("--force", action="store_true", help="Overwrite an unmanaged existing shim without backup")

    args = parser.parse_args(argv)
    try:
        plan = build_plan(args)
        if args.command == "resolve":
            print_json(_common_preview_payload(plan, backup_existing=args.backup_existing, include_body=False))
            return 0
        if args.command == "dry-run":
            print_json(_common_preview_payload(plan, backup_existing=args.backup_existing, include_body=True))
            return 0
        if args.command == "install":
            _write_managed_shim(plan, backup_existing=args.backup_existing, force=args.force)
            print(f"installed managed shim: {plan.shim_path}")
            return 0
        if args.command == "refresh":
            if plan.existing_shim_state == "unmanaged" and not (args.backup_existing or args.force):
                _fail(f"refusing to refresh unmanaged shim {plan.shim_path}; use --backup-existing or --force")
            _write_managed_shim(plan, backup_existing=args.backup_existing, force=args.force)
            print(f"refreshed managed shim: {plan.shim_path}")
            return 0
        parser.error(f"unknown command: {args.command}")
        return 2
    except DeployError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
