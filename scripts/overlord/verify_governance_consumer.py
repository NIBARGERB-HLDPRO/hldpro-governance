#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


GOVERNANCE_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_MANIFEST = GOVERNANCE_ROOT / "docs" / "governance-tooling-package.json"
DESIRED_STATE = GOVERNANCE_ROOT / "docs" / "governance-consumer-pull-state.json"
DEFAULT_RECORD_PATH = ".hldpro/governance-tooling.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MANAGED_LOCAL_CI_MARKER = "# hldpro-governance local-ci gate managed"


class ConsumerVerifyError(RuntimeError):
    pass


@dataclass(frozen=True)
class ConsumerRecord:
    path: Path
    payload: dict[str, Any]


def _fail(message: str) -> None:
    raise ConsumerVerifyError(message)


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, check=False, capture_output=True, text=True)


def _git_root(path: Path) -> Path:
    result = _run_git(["rev-parse", "--show-toplevel"], path)
    if result.returncode != 0:
        _fail(f"target repo must be inside a git repository: {path}")
    return Path(result.stdout.strip()).resolve(strict=False)


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        _fail(f"could not read {label} {path}: {exc}")
    except json.JSONDecodeError as exc:
        _fail(f"could not parse {label} {path}: {exc}")
    if not isinstance(payload, dict):
        _fail(f"{label} must be a JSON object: {path}")
    return payload


def _consumer_record_relpath(manifest: dict[str, Any]) -> str:
    versioning = manifest.get("versioning")
    if isinstance(versioning, dict):
        raw = versioning.get("consumer_record_path")
        if isinstance(raw, str) and raw:
            return raw
    return DEFAULT_RECORD_PATH


def _required_record_fields(manifest: dict[str, Any]) -> list[str]:
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


def _initial_package_version(manifest: dict[str, Any]) -> str:
    versioning = manifest.get("versioning")
    if isinstance(versioning, dict):
        value = versioning.get("initial_version")
        if isinstance(value, str) and value:
            return value
    return "0.0.0-unknown"


def _profile_desired_state(desired_state: dict[str, Any], profile: str) -> dict[str, Any]:
    profiles = desired_state.get("profiles")
    if not isinstance(profiles, dict):
        return {}
    profile_state = profiles.get(profile)
    return profile_state if isinstance(profile_state, dict) else {}


def _expected_managed_paths(profile_state: dict[str, Any]) -> set[str]:
    raw = profile_state.get("managed_files")
    if isinstance(raw, list) and all(isinstance(item, str) for item in raw):
        return set(raw)
    return {".hldpro/local-ci.sh", ".hldpro/governance-tooling.json"}


def _managed_paths(record: dict[str, Any]) -> set[str]:
    managed_files = record.get("managed_files")
    if not isinstance(managed_files, list):
        return set()
    paths: set[str] = set()
    for item in managed_files:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            paths.add(item["path"])
    return paths


def _managed_file_type(record: dict[str, Any], relpath: str) -> str:
    managed_files = record.get("managed_files")
    if not isinstance(managed_files, list):
        return ""
    for item in managed_files:
        if isinstance(item, dict) and item.get("path") == relpath and isinstance(item.get("type"), str):
            return item["type"]
    return ""


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _load_consumer_record(target_repo: Path, record_relpath: str) -> ConsumerRecord:
    record_path = (target_repo / record_relpath).resolve()
    if not _is_relative_to(record_path, target_repo):
        _fail(f"consumer record path must stay under target repo: {record_relpath}")
    if not record_path.exists():
        _fail(f"consumer record missing: {record_path}")
    return ConsumerRecord(path=record_path, payload=_load_json(record_path, "consumer record"))


def _validate_record(
    *,
    target_repo: Path,
    record: ConsumerRecord,
    manifest: dict[str, Any],
    desired_state: dict[str, Any],
    expected_profile: str | None,
    expected_governance_ref: str | None,
    expected_package_version: str | None,
    allow_non_sha_ref: bool,
) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    payload = record.payload

    for field in _required_record_fields(manifest):
        if field not in payload:
            failures.append(f"consumer record missing field: {field}")

    governance_repo = payload.get("governance_repo")
    expected_owner = manifest.get("package_owner_repo")
    if expected_owner and governance_repo != expected_owner:
        failures.append(f"governance_repo mismatch: expected {expected_owner}, got {governance_repo}")

    profile = payload.get("profile")
    if not isinstance(profile, str) or not profile:
        failures.append("profile must be a non-empty string")
        profile = expected_profile or ""
    if expected_profile and profile != expected_profile:
        failures.append(f"profile mismatch: expected {expected_profile}, got {profile}")

    package_version = payload.get("package_version")
    expected_version = expected_package_version or _initial_package_version(manifest)
    if package_version != expected_version:
        failures.append(f"package_version mismatch: expected {expected_version}, got {package_version}")

    governance_ref = payload.get("governance_ref")
    if not isinstance(governance_ref, str) or not governance_ref:
        failures.append("governance_ref must be a non-empty string")
    else:
        if expected_governance_ref and governance_ref != expected_governance_ref:
            failures.append(f"governance_ref mismatch: expected {expected_governance_ref}, got {governance_ref}")
        if not allow_non_sha_ref and not SHA_RE.fullmatch(governance_ref):
            failures.append("governance_ref must be an exact 40-character lowercase git SHA")

    consumer_repo = payload.get("consumer_repo")
    if isinstance(consumer_repo, str) and Path(consumer_repo).resolve(strict=False) != target_repo:
        warnings.append(f"consumer_repo path differs from target repo: {consumer_repo}")

    profile_state = _profile_desired_state(desired_state, profile)
    expected_paths = _expected_managed_paths(profile_state)
    actual_paths = _managed_paths(payload)
    missing_paths = sorted(expected_paths - actual_paths)
    if missing_paths:
        failures.append(f"managed_files missing expected path(s): {', '.join(missing_paths)}")

    for relpath in sorted(actual_paths):
        candidate = (target_repo / relpath).resolve()
        if not _is_relative_to(candidate, target_repo):
            failures.append(f"managed file path escapes target repo: {relpath}")
            continue
        if not candidate.exists():
            failures.append(f"managed file missing on disk: {relpath}")
            continue
        if _managed_file_type(payload, relpath) == "local_ci_shim":
            text = candidate.read_text(encoding="utf-8", errors="replace")
            if MANAGED_LOCAL_CI_MARKER not in text:
                failures.append(f"managed local CI shim missing marker: {relpath}")
            if isinstance(governance_ref, str) and governance_ref and governance_ref not in text:
                failures.append(f"managed local CI shim does not reference governance_ref: {relpath}")

    central = desired_state.get("centrally_applied_surfaces")
    if isinstance(central, list) and central:
        warnings.append("central GitHub rules/settings are report-only in consumer verification")

    return failures, warnings


def verify(args: argparse.Namespace) -> dict[str, Any]:
    governance_root = Path(args.governance_root).resolve()
    manifest_path = Path(args.manifest).resolve()
    desired_state_path = Path(args.desired_state).resolve()
    target_repo = _git_root(Path(args.target_repo).resolve())

    manifest = _load_json(manifest_path, "package manifest")
    desired_state = _load_json(desired_state_path, "consumer pull desired state")
    record_relpath = args.record_path or _consumer_record_relpath(manifest)
    record = _load_consumer_record(target_repo, record_relpath)
    failures, warnings = _validate_record(
        target_repo=target_repo,
        record=record,
        manifest=manifest,
        desired_state=desired_state,
        expected_profile=args.profile or None,
        expected_governance_ref=args.governance_ref or None,
        expected_package_version=args.package_version or None,
        allow_non_sha_ref=args.allow_non_sha_ref,
    )
    return {
        "status": "passed" if not failures else "failed",
        "target_repo": str(target_repo),
        "governance_root": str(governance_root),
        "manifest_path": str(manifest_path),
        "desired_state_path": str(desired_state_path),
        "record_path": str(record.path),
        "profile": record.payload.get("profile"),
        "governance_ref": record.payload.get("governance_ref"),
        "package_version": record.payload.get("package_version"),
        "failures": failures,
        "warnings": warnings,
    }


def print_json(payload: Any) -> None:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify a downstream repo consumes pinned HLDPRO governance tooling.")
    parser.add_argument("--governance-root", default=str(GOVERNANCE_ROOT), help="hldpro-governance checkout root")
    parser.add_argument("--manifest", default=str(PACKAGE_MANIFEST), help="Governance package manifest")
    parser.add_argument("--desired-state", default=str(DESIRED_STATE), help="Consumer-pull desired-state contract")
    parser.add_argument("--target-repo", default=".", help="Consumer repo checkout root")
    parser.add_argument("--record-path", default="", help="Repo-relative consumer record path")
    parser.add_argument("--profile", default="", help="Expected consumer profile")
    parser.add_argument("--governance-ref", default="", help="Expected exact governance git SHA")
    parser.add_argument("--package-version", default="", help="Expected package version")
    parser.add_argument("--allow-non-sha-ref", action="store_true", help="Allow non-SHA governance refs for fixture-only checks")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        payload = verify(args)
        print_json(payload)
        return 0 if payload["status"] == "passed" else 1
    except ConsumerVerifyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
