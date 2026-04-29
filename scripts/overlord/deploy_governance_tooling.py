#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import deploy_local_ci_gate


GOVERNANCE_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_MANIFEST = GOVERNANCE_ROOT / "docs" / "governance-tooling-package.json"
DESIRED_STATE = GOVERNANCE_ROOT / "docs" / "governance-consumer-pull-state.json"
CONSUMER_RECORD_PATH = ".hldpro/governance-tooling.json"
DEFAULT_PROFILE = "hldpro-governance"
DEFAULT_SHIM_PATH = ".hldpro/local-ci.sh"


class GovernanceDeployError(RuntimeError):
    pass


@dataclass(frozen=True)
class ToolingPlan:
    governance_root: Path
    target_repo: Path
    governance_ref: str
    package_version: str
    profile: str
    shim_path: Path
    record_path: Path
    manifest_path: Path
    dirty_target: bool
    existing_shim_state: str
    existing_record_state: str

    def managed_files(self) -> list[dict[str, object]]:
        desired_state = _load_json(self.governance_root / "docs" / "governance-consumer-pull-state.json", "consumer pull desired state")
        return _managed_file_contract_entries(
            desired_state,
            self.profile,
            self.target_repo,
            self.shim_path,
            self.record_path,
            self.existing_shim_state,
            self.existing_record_state,
        )

    def planned_write_set(self) -> list[str]:
        return [str(self.shim_path), str(self.record_path)]

    def planned_rollback_set(self) -> list[str]:
        return [str(self.shim_path), str(self.record_path)]

    def to_json(self) -> dict[str, object]:
        return {
            "governance_root": str(self.governance_root),
            "target_repo": str(self.target_repo),
            "governance_ref": self.governance_ref,
            "package_version": self.package_version,
            "profile": self.profile,
            "manifest_path": str(self.manifest_path),
            "shim_path": str(self.shim_path),
            "record_path": str(self.record_path),
            "dirty_target": self.dirty_target,
            "existing_shim_state": self.existing_shim_state,
            "existing_record_state": self.existing_record_state,
            "managed_files": self.managed_files(),
            "planned_write_set": self.planned_write_set(),
            "planned_rollback_set": self.planned_rollback_set(),
        }


def _fail(message: str) -> None:
    raise GovernanceDeployError(message)


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, check=False, capture_output=True, text=True)


def _git_root(path: Path) -> Path:
    result = _run_git(["rev-parse", "--show-toplevel"], path)
    if result.returncode != 0:
        _fail(f"target repo must be inside a git repository: {path}")
    return Path(result.stdout.strip()).resolve(strict=False)


def _git_is_dirty(repo: Path) -> bool:
    result = _run_git(["status", "--porcelain=v1", "--untracked-files=all"], repo)
    if result.returncode != 0:
        _fail(f"could not read git status for target repo: {repo}")
    return bool(result.stdout.strip())


def _git_head(root: Path) -> str:
    result = _run_git(["rev-parse", "HEAD"], root)
    if result.returncode != 0:
        return "HEAD"
    return result.stdout.strip()


def _load_manifest(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _fail(f"could not load package manifest {path}: {exc}")
    if not isinstance(payload, dict):
        _fail(f"package manifest must be a JSON object: {path}")
    return payload


def _load_json(path: Path, label: str) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _fail(f"could not load {label} {path}: {exc}")
    if not isinstance(payload, dict):
        _fail(f"{label} must be a JSON object: {path}")
    return payload


def _consumer_record_relpath(manifest: dict[str, object]) -> str:
    versioning = manifest.get("versioning")
    if isinstance(versioning, dict):
        raw = versioning.get("consumer_record_path")
        if isinstance(raw, str) and raw:
            return raw
    return CONSUMER_RECORD_PATH


def _profile_desired_state(desired_state: dict[str, object], profile: str) -> dict[str, object]:
    profiles = desired_state.get("profiles")
    if not isinstance(profiles, dict):
        return {}
    state = profiles.get(profile)
    return state if isinstance(state, dict) else {}


def _package_version(
    manifest: dict[str, object],
    desired_state: dict[str, object],
    profile: str,
    override: str | None,
) -> str:
    if override:
        return override
    profile_state = _profile_desired_state(desired_state, profile)
    profile_version = profile_state.get("package_version")
    if isinstance(profile_version, str) and profile_version:
        return profile_version
    versioning = manifest.get("versioning")
    if isinstance(versioning, dict):
        raw = versioning.get("initial_version")
        if isinstance(raw, str) and raw:
            return raw
    return "0.0.0-unknown"


def _managed_file_contract_entries(
    desired_state: dict[str, object],
    profile: str,
    target_repo: Path,
    shim_path: Path,
    record_path: Path,
    existing_shim_state: str,
    existing_record_state: str,
) -> list[dict[str, object]]:
    profile_state = _profile_desired_state(desired_state, profile)
    raw = profile_state.get("managed_files")
    if not isinstance(raw, list):
        raw = [".hldpro/local-ci.sh", ".hldpro/governance-tooling.json"]
    shim_rel = shim_path.relative_to(target_repo).as_posix()
    record_rel = record_path.relative_to(target_repo).as_posix()
    entries: list[dict[str, object]] = []
    for item in raw:
        if isinstance(item, str):
            relpath = item
            entry: dict[str, object] = {"path": relpath}
        elif isinstance(item, dict) and isinstance(item.get("path"), str) and item["path"]:
            relpath = item["path"]
            entry = {"path": relpath}
            for key in ("type", "required_strings", "required_pre_tool_use_matchers", "required_post_tool_use_matchers"):
                value = item.get(key)
                if isinstance(value, str):
                    entry[key] = value
                elif isinstance(value, list) and all(isinstance(member, str) for member in value):
                    entry[key] = list(value)
        else:
            continue
        if relpath == shim_rel:
            entry["type"] = "local_ci_shim"
            entry["state"] = existing_shim_state
        elif relpath == record_rel:
            entry["type"] = "consumer_record"
            entry["state"] = existing_record_state
        else:
            entry["state"] = "present" if (target_repo / relpath).exists() else "missing"
        entries.append(entry)
    return entries


def _profile_constraints(desired_state: dict[str, object], profile: str) -> list[str]:
    profile_state = _profile_desired_state(desired_state, profile)
    raw = profile_state.get("profile_constraints")
    if isinstance(raw, list) and all(isinstance(item, str) for item in raw):
        return list(raw)
    return []


def _record_state(path: Path) -> str:
    if not path.exists():
        return "missing"
    if path.is_dir():
        _fail(f"consumer record path is a directory, not a file: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "unmanaged"
    if isinstance(payload, dict) and payload.get("schema_version") == 1 and payload.get("governance_repo"):
        return "managed"
    return "unmanaged"


def _ensure_relative_to(path: Path, root: Path, label: str) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        _fail(f"{label} must stay under target repo: {path}")


def _build_local_ci_plan(plan: ToolingPlan) -> deploy_local_ci_gate.DeployPlan:
    namespace = argparse.Namespace(
        governance_root=str(plan.governance_root),
        governance_ref=plan.governance_ref,
        target_repo=str(plan.target_repo),
        shim_path=plan.shim_path.relative_to(plan.target_repo).as_posix(),
        profile=plan.profile,
    )
    return deploy_local_ci_gate.build_plan(namespace)


def build_plan(args: argparse.Namespace) -> ToolingPlan:
    governance_root = Path(args.governance_root).resolve()
    if not governance_root.is_dir():
        _fail(f"governance root must exist and be a directory: {governance_root}")
    manifest_path = Path(args.manifest).resolve() if args.manifest else governance_root / "docs" / "governance-tooling-package.json"
    manifest = _load_manifest(manifest_path)
    desired_state = _load_json(governance_root / "docs" / "governance-consumer-pull-state.json", "consumer pull desired state")

    target_repo = _git_root(Path(args.target_repo).resolve())
    governance_ref = args.governance_ref or _git_head(governance_root)
    profile = args.profile or DEFAULT_PROFILE
    package_version = _package_version(manifest, desired_state, profile, args.package_version)

    shim_path = deploy_local_ci_gate._resolve_shim_path(target_repo, args.shim_path or DEFAULT_SHIM_PATH)
    record_path = (target_repo / _consumer_record_relpath(manifest)).resolve()
    _ensure_relative_to(record_path, target_repo, "consumer record path")

    return ToolingPlan(
        governance_root=governance_root,
        target_repo=target_repo,
        governance_ref=governance_ref,
        package_version=package_version,
        profile=profile,
        shim_path=shim_path,
        record_path=record_path,
        manifest_path=manifest_path,
        dirty_target=_git_is_dirty(target_repo),
        existing_shim_state=deploy_local_ci_gate._existing_shim_state(shim_path),
        existing_record_state=_record_state(record_path),
    )


def _refuse_dirty(plan: ToolingPlan, allow_dirty_target: bool) -> None:
    if plan.dirty_target and not allow_dirty_target:
        _fail(f"refusing to modify dirty target repo: {plan.target_repo}; commit/stash changes or pass --allow-dirty-target")


def _refuse_unmanaged_record(plan: ToolingPlan, force: bool) -> None:
    if plan.existing_record_state == "unmanaged" and not force:
        _fail(f"refusing to overwrite unmanaged consumer record {plan.record_path}; use --force")


def _consumer_record(plan: ToolingPlan) -> dict[str, object]:
    desired_state = _load_json(plan.governance_root / "docs" / "governance-consumer-pull-state.json", "consumer pull desired state")
    profile_constraints = _profile_constraints(desired_state, plan.profile)
    schema_version = 2 if plan.package_version == "0.3.0-hard-gated-som" or profile_constraints else 1
    record = {
        "schema_version": schema_version,
        "consumer_repo": str(plan.target_repo),
        "governance_repo": "NIBARGERB-HLDPRO/hldpro-governance",
        "governance_root": str(plan.governance_root),
        "governance_ref": plan.governance_ref,
        "package_version": plan.package_version,
        "deployed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "managed_files": plan.managed_files(),
        "profile": plan.profile,
        "local_verification": [
            {
                "command": f"{plan.shim_path.relative_to(plan.target_repo).as_posix()}",
                "status": "pending"
            }
        ],
        "github_verification": [
            {
                "check": "consumer repo GitHub Actions",
                "status": "pending"
            }
        ],
        "overrides": [],
    }
    if profile_constraints:
        record["profile_constraints"] = profile_constraints
    return record


def apply(plan: ToolingPlan, *, allow_dirty_target: bool, force: bool) -> dict[str, object]:
    _refuse_dirty(plan, allow_dirty_target)
    _refuse_unmanaged_record(plan, force)
    local_ci_plan = _build_local_ci_plan(plan)
    deploy_local_ci_gate._write_managed_shim(local_ci_plan, backup_existing=False, force=force)
    plan.record_path.parent.mkdir(parents=True, exist_ok=True)
    plan.record_path.write_text(json.dumps(_consumer_record(plan), indent=2) + "\n", encoding="utf-8")
    return {"status": "applied", **plan.to_json()}


def verify(plan: ToolingPlan) -> dict[str, object]:
    failures: list[str] = []
    if plan.existing_shim_state != "managed":
        failures.append(f"managed shim missing or unmanaged: {plan.shim_path}")
    else:
        expected_shim = deploy_local_ci_gate.managed_shim_body(_build_local_ci_plan(plan))
        actual_shim = plan.shim_path.read_text(encoding="utf-8")
        if actual_shim != expected_shim:
            failures.append(f"managed shim content mismatch for requested ref/profile/root: {plan.shim_path}")
    if plan.existing_record_state != "managed":
        failures.append(f"consumer record missing or unmanaged: {plan.record_path}")
    else:
        record = json.loads(plan.record_path.read_text(encoding="utf-8"))
        for field in _required_record_fields(plan.manifest_path):
            if field not in record:
                failures.append(f"consumer record missing field: {field}")
        if record.get("governance_ref") != plan.governance_ref:
            failures.append(
                f"consumer record governance_ref mismatch: expected {plan.governance_ref}, got {record.get('governance_ref')}"
            )
        if record.get("package_version") != plan.package_version:
            failures.append(
                f"consumer record package_version mismatch: expected {plan.package_version}, got {record.get('package_version')}"
            )
    if failures:
        return {"status": "failed", "failures": failures, **plan.to_json()}
    return {"status": "verified", "failures": [], **plan.to_json()}


def _required_record_fields(manifest_path: Path) -> list[str]:
    manifest = _load_manifest(manifest_path)
    contract = manifest.get("consumer_record_contract")
    if isinstance(contract, dict):
        fields = contract.get("required_fields")
        if isinstance(fields, list) and all(isinstance(item, str) for item in fields):
            return fields
    return [
        "schema_version",
        "consumer_repo",
        "governance_repo",
        "governance_ref",
        "package_version",
        "deployed_at",
        "managed_files",
        "profile",
        "local_verification",
        "github_verification",
        "overrides",
    ]


def rollback(plan: ToolingPlan, *, allow_dirty_target: bool, force: bool) -> dict[str, object]:
    _refuse_dirty(plan, allow_dirty_target)
    removal_checks = [
        (
            plan.shim_path,
            deploy_local_ci_gate._existing_shim_state(plan.shim_path) if plan.shim_path.exists() else "missing",
            "shim",
        ),
        (
            plan.record_path,
            _record_state(plan.record_path) if plan.record_path.exists() else "missing",
            "consumer record",
        ),
    ]
    for path, state, label in removal_checks:
        if path.exists() and state != "managed" and not force:
            _fail(f"refusing to remove unmanaged {label} {path}; use --force")

    removed: list[str] = []
    if plan.shim_path.exists():
        plan.shim_path.unlink()
        removed.append(str(plan.shim_path))
    if plan.record_path.exists():
        plan.record_path.unlink()
        removed.append(str(plan.record_path))
    return {"status": "rolled_back", "removed": removed, **plan.to_json()}


def print_json(payload: object) -> None:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--governance-root", default=str(GOVERNANCE_ROOT), help="hldpro-governance checkout root")
    parser.add_argument("--manifest", default=str(PACKAGE_MANIFEST), help="Governance tooling package manifest")
    parser.add_argument("--target-repo", default=".", help="Consumer repo checkout root")
    parser.add_argument("--governance-ref", default="", help="Pinned governance git SHA/ref")
    parser.add_argument("--package-version", default="", help="Package version to record")
    parser.add_argument("--profile", default=DEFAULT_PROFILE, help="Local CI Gate profile to deploy")
    parser.add_argument("--shim-path", default=DEFAULT_SHIM_PATH, help="Managed Local CI shim path")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deploy pinned HLDPRO governance tooling into a consumer repo.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    dry_run_parser = subparsers.add_parser("dry-run", help="Print deploy plan without writing files")
    add_common_args(dry_run_parser)

    apply_parser = subparsers.add_parser("apply", help="Apply managed governance tooling files")
    add_common_args(apply_parser)
    apply_parser.add_argument("--allow-dirty-target", action="store_true", help="Allow writes when target repo is dirty")
    apply_parser.add_argument("--force", action="store_true", help="Overwrite unmanaged managed paths")

    verify_parser = subparsers.add_parser("verify", help="Verify deployed managed governance tooling files")
    add_common_args(verify_parser)

    rollback_parser = subparsers.add_parser("rollback", help="Remove managed governance tooling files")
    add_common_args(rollback_parser)
    rollback_parser.add_argument("--allow-dirty-target", action="store_true", help="Allow rollback when target repo is dirty")
    rollback_parser.add_argument("--force", action="store_true", help="Remove unmanaged managed paths")

    args = parser.parse_args(argv)
    try:
        plan = build_plan(args)
        if args.command == "dry-run":
            print_json({"status": "planned", **plan.to_json()})
            return 0
        if args.command == "apply":
            print_json(apply(plan, allow_dirty_target=args.allow_dirty_target, force=args.force))
            return 0
        if args.command == "verify":
            payload = verify(plan)
            print_json(payload)
            return 0 if payload["status"] == "verified" else 1
        if args.command == "rollback":
            print_json(rollback(plan, allow_dirty_target=args.allow_dirty_target, force=args.force))
            return 0
        parser.error(f"unknown command: {args.command}")
        return 2
    except GovernanceDeployError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except deploy_local_ci_gate.DeployError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
