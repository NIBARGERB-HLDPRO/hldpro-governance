#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
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
GOVERNANCE_WORKFLOW_REF_RE = re.compile(
    r"NIBARGERB-HLDPRO/hldpro-governance/(?:\.github/workflows/)?[^\s'\"#]+@(?P<ref>[^\s'\"#]+)"
)


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


def _profile_contract(manifest: dict[str, Any]) -> dict[str, Any]:
    contract = manifest.get("profile_contract")
    return contract if isinstance(contract, dict) else {}


def _manifest_profiles(manifest: dict[str, Any]) -> dict[str, Any]:
    profiles = _profile_contract(manifest).get("required_profiles")
    return profiles if isinstance(profiles, dict) else {}


def _known_profiles(manifest: dict[str, Any], desired_state: dict[str, Any]) -> set[str]:
    profiles: set[str] = set(_manifest_profiles(manifest))
    desired_profiles = desired_state.get("profiles")
    if isinstance(desired_profiles, dict):
        profiles.update(str(key) for key in desired_profiles)
    return profiles


def _next_package_version(manifest: dict[str, Any]) -> str:
    versioning = manifest.get("versioning")
    if isinstance(versioning, dict):
        value = versioning.get("next_contract_version")
        if isinstance(value, str):
            return value
    return ""


def _is_v2_record(payload: dict[str, Any], manifest: dict[str, Any]) -> bool:
    return (
        payload.get("package_version") == _next_package_version(manifest)
        or payload.get("schema_version") == 2
        or "profile_constraints" in payload
        or "repo_profile" in payload
        or "local_overrides" in payload
    )


def _profile_required_constraints(manifest: dict[str, Any], profile: str) -> list[str]:
    profile_payload = _manifest_profiles(manifest).get(profile)
    if not isinstance(profile_payload, dict):
        return []
    raw = profile_payload.get("required_constraints")
    if isinstance(raw, list) and all(isinstance(item, str) for item in raw):
        return raw
    return []


def _record_constraints(payload: dict[str, Any]) -> set[str]:
    raw = payload.get("profile_constraints")
    if isinstance(raw, list) and all(isinstance(item, str) for item in raw):
        return set(raw)
    repo_profile = payload.get("repo_profile")
    if isinstance(repo_profile, dict):
        constraints = repo_profile.get("required_constraints")
        if isinstance(constraints, list) and all(isinstance(item, str) for item in constraints):
            return set(constraints)
    return set()


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


def _managed_file_entry(record: dict[str, Any], relpath: str) -> dict[str, Any]:
    managed_files = record.get("managed_files")
    if not isinstance(managed_files, list):
        return {}
    for item in managed_files:
        if isinstance(item, dict) and item.get("path") == relpath:
            return item
    return {}


def _managed_markers(manifest: dict[str, Any]) -> list[str]:
    contract = manifest.get("managed_file_contract")
    if isinstance(contract, dict):
        markers = contract.get("markers")
        if isinstance(markers, list) and all(isinstance(item, str) for item in markers):
            return markers
    return [MANAGED_LOCAL_CI_MARKER, "# hldpro-governance managed", "# Managed by hldpro-governance"]


def _expected_checksum(entry: dict[str, Any]) -> str:
    for key in ("sha256", "content_sha256", "checksum_sha256"):
        value = entry.get(key)
        if isinstance(value, str) and value:
            return value
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


def _override_records(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    failures: list[str] = []
    overrides: list[dict[str, Any]] = []
    for field in ("overrides", "local_overrides"):
        raw = payload.get(field, [])
        if raw in (None, []):
            continue
        if not isinstance(raw, list):
            failures.append(f"{field} must be a list")
            continue
        for index, item in enumerate(raw):
            if not isinstance(item, dict):
                failures.append(f"{field}[{index}] must be an object")
                continue
            overrides.append(item)
            for required in ("issue", "reason", "owner"):
                if not item.get(required):
                    failures.append(f"{field}[{index}] missing required override metadata: {required}")
            if not item.get("review_cadence") and not item.get("expires_at"):
                failures.append(f"{field}[{index}] missing required override metadata: review_cadence or expires_at")
    return overrides, failures


def _workflow_ref_failures(target_repo: Path) -> list[str]:
    workflow_root = target_repo / ".github" / "workflows"
    if not workflow_root.exists():
        return []
    failures: list[str] = []
    for path in sorted(workflow_root.glob("*.y*ml")):
        relpath = path.relative_to(target_repo).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in GOVERNANCE_WORKFLOW_REF_RE.finditer(text):
            ref = match.group("ref").rstrip("/")
            if not SHA_RE.fullmatch(ref):
                failures.append(f"reusable workflow ref must be pinned to an exact governance SHA: {relpath} uses @{ref}")
    return failures


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
) -> tuple[list[str], list[str], list[dict[str, Any]]]:
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
    known_profiles = _known_profiles(manifest, desired_state)
    if profile and known_profiles and profile not in known_profiles:
        failures.append(f"unknown profile: {profile}")

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
        elif _managed_file_type(payload, relpath) not in {"consumer_record", ""}:
            text = candidate.read_text(encoding="utf-8", errors="replace")
            if not any(marker in text for marker in _managed_markers(manifest)):
                failures.append(f"managed file missing marker: {relpath}")
        checksum = _expected_checksum(_managed_file_entry(payload, relpath))
        if checksum:
            actual_checksum = hashlib.sha256(candidate.read_bytes()).hexdigest()
            if actual_checksum != checksum:
                failures.append(f"managed file checksum drift: {relpath}")

    if _is_v2_record(payload, manifest):
        required_constraints = _profile_required_constraints(manifest, profile)
        if required_constraints:
            actual_constraints = _record_constraints(payload)
            missing_constraints = sorted(set(required_constraints) - actual_constraints)
            if missing_constraints:
                failures.append(
                    f"profile constraints missing required constraint(s) for {profile}: {', '.join(missing_constraints)}"
                )
        if profile == "stampede" and payload.get("schema_version") != 2:
            warnings.append("Stampede consumer record uses older bootstrap shape; migration to schema_version 2 is recommended")

    observed_overrides, override_failures = _override_records(payload)
    failures.extend(override_failures)
    failures.extend(_workflow_ref_failures(target_repo))

    central = desired_state.get("centrally_applied_surfaces")
    if isinstance(central, list) and central:
        warnings.append("central GitHub rules/settings are report-only in consumer verification")

    return failures, warnings, observed_overrides


def verify(args: argparse.Namespace) -> dict[str, Any]:
    governance_root = Path(args.governance_root).resolve()
    manifest_path = Path(args.manifest).resolve()
    desired_state_path = Path(args.desired_state).resolve()
    target_repo = _git_root(Path(args.target_repo).resolve())

    manifest = _load_json(manifest_path, "package manifest")
    desired_state = _load_json(desired_state_path, "consumer pull desired state")
    record_relpath = args.record_path or _consumer_record_relpath(manifest)
    record = _load_consumer_record(target_repo, record_relpath)
    failures, warnings, observed_overrides = _validate_record(
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
        "observed_overrides": observed_overrides,
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
