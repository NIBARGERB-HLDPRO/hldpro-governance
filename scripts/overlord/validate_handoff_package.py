#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "schema_version",
    "handoff_id",
    "issue_number",
    "parent_epic_number",
    "lifecycle_state",
    "from_role",
    "to_role",
    "structured_plan_ref",
    "execution_scope_ref",
    "packet_ref",
    "package_manifest_ref",
    "acceptance_criteria",
    "validation_commands",
    "review_artifact_refs",
    "gate_artifact_refs",
    "artifact_refs",
    "audit_refs",
    "closeout_ref",
    "blocked_on",
    "handoff_decision",
    "created_at",
}

VALID_LIFECYCLE_STATES = {
    "draft",
    "planned",
    "implementation_ready",
    "in_progress",
    "validation_ready",
    "accepted",
    "released",
    "consumed",
    "deprecated",
    "rolled_back",
    "archived",
}

VALID_DECISIONS = {"draft", "accepted", "rejected", "blocked"}
HANDOFF_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
SCOPE_REQUIRED_STATES = {
    "implementation_ready",
    "in_progress",
    "validation_ready",
    "accepted",
    "released",
    "consumed",
}
PACKET_REQUIRED_STATES = {"validation_ready", "accepted", "released", "consumed"}
CLOSEOUT_REQUIRED_STATES = {"accepted", "released", "consumed", "deprecated", "rolled_back", "archived"}
CONSUMER_VERIFIER_COMMAND = "verify_governance_consumer.py"
CONSUMER_VERIFIER_ACCEPTANCE_GATE_CREATED_AT = "2026-04-21T22:33:23Z"
CONSUMER_MANAGED_PATH_PREFIXES = (
    ".hldpro/",
    ".governance/",
)
CONSUMER_MANAGED_PATHS = {
    "docs/governance-consumer-pull-state.json",
    "docs/governance-tooling-package.json",
    "scripts/overlord/verify_governance_consumer.py",
    "scripts/overlord/test_verify_governance_consumer.py",
}


def _is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def _normalize_repo_path(raw_path: str, field_name: str, package_path: Path) -> str:
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ValueError(f"{package_path}: `{field_name}` must be a non-empty string")
    normalized = raw_path.strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    path_obj = Path(normalized)
    if path_obj.is_absolute() or "\\" in normalized or any(part == ".." for part in path_obj.parts):
        raise ValueError(f"{package_path}: `{field_name}` must be a safe repo-relative path")
    return path_obj.as_posix()


def _repo_file_exists(root: Path, ref: str) -> bool:
    if _is_url(ref):
        return True
    return (root / ref).is_file()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_json_ref(root: Path, ref: str, field_name: str, package_path: Path, failures: list[str]) -> Any | None:
    if _is_url(ref):
        failures.append(f"{package_path}: `{field_name}` must reference a repo JSON artifact, got URL {ref}")
        return None
    path = root / ref
    if not path.is_file():
        failures.append(f"{package_path}: `{field_name}` does not exist: {ref}")
        return None
    try:
        return _load_json(path)
    except (json.JSONDecodeError, OSError) as exc:
        failures.append(f"{package_path}: `{field_name}` could not be parsed as JSON: {ref}: {exc}")
        return None


def _validate_ref_array(
    root: Path,
    package_path: Path,
    payload: dict[str, Any],
    field_name: str,
    failures: list[str],
) -> None:
    value = payload.get(field_name)
    if not isinstance(value, list):
        failures.append(f"{package_path}: `{field_name}` must be an array")
        return
    for index, item in enumerate(value, start=1):
        try:
            ref = _normalize_repo_path(item, f"{field_name}[{index}]", package_path) if not _is_url(str(item)) else item
        except ValueError as exc:
            failures.append(str(exc))
            continue
        if not _repo_file_exists(root, ref):
            failures.append(f"{package_path}: `{field_name}[{index}]` does not exist: {ref}")


def _validate_acceptance_criteria(
    root: Path,
    package_path: Path,
    payload: dict[str, Any],
    failures: list[str],
) -> None:
    criteria = payload.get("acceptance_criteria")
    if not isinstance(criteria, list) or not criteria:
        failures.append(f"{package_path}: `acceptance_criteria` must be a non-empty array")
        return
    seen_ids: set[str] = set()
    for index, criterion in enumerate(criteria, start=1):
        if not isinstance(criterion, dict):
            failures.append(f"{package_path}: `acceptance_criteria[{index}]` must be an object")
            continue
        criterion_id = criterion.get("id")
        if not isinstance(criterion_id, str) or not criterion_id:
            failures.append(f"{package_path}: `acceptance_criteria[{index}].id` must be a non-empty string")
        elif criterion_id in seen_ids:
            failures.append(f"{package_path}: duplicate acceptance criterion id `{criterion_id}`")
        else:
            seen_ids.add(criterion_id)
        if not isinstance(criterion.get("statement"), str) or not criterion.get("statement"):
            failures.append(f"{package_path}: `acceptance_criteria[{index}].statement` must be non-empty")
        refs = criterion.get("verification_refs")
        if not isinstance(refs, list):
            failures.append(f"{package_path}: `acceptance_criteria[{index}].verification_refs` must be an array")
            continue
        for ref_index, item in enumerate(refs, start=1):
            ref = str(item)
            if _is_url(ref):
                continue
            try:
                normalized = _normalize_repo_path(ref, f"acceptance_criteria[{index}].verification_refs[{ref_index}]", package_path)
            except ValueError as exc:
                failures.append(str(exc))
                continue
            if not _repo_file_exists(root, normalized):
                failures.append(
                    f"{package_path}: `acceptance_criteria[{index}].verification_refs[{ref_index}]` does not exist: {normalized}"
                )


def _consumer_managed_paths(scope_payload: dict[str, Any]) -> list[str]:
    allowed_write_paths = scope_payload.get("allowed_write_paths")
    if not isinstance(allowed_write_paths, list):
        return []
    managed: list[str] = []
    for item in allowed_write_paths:
        if not isinstance(item, str):
            continue
        normalized = item.strip()
        while normalized.startswith("./"):
            normalized = normalized[2:]
        if normalized in CONSUMER_MANAGED_PATHS or normalized.startswith(CONSUMER_MANAGED_PATH_PREFIXES):
            managed.append(normalized)
    return sorted(set(managed))


def _criteria_verification_refs(payload: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    criteria = payload.get("acceptance_criteria")
    if not isinstance(criteria, list):
        return refs
    for criterion in criteria:
        if not isinstance(criterion, dict):
            continue
        raw_refs = criterion.get("verification_refs")
        if isinstance(raw_refs, list):
            refs.extend(str(item) for item in raw_refs if str(item))
    return refs


def _consumer_verifier_acceptance_gate_applies(payload: dict[str, Any]) -> bool:
    created_at = payload.get("created_at")
    if not isinstance(created_at, str) or not created_at:
        return True
    return created_at >= CONSUMER_VERIFIER_ACCEPTANCE_GATE_CREATED_AT


def _validate_consumer_verifier_acceptance(
    package_path: Path,
    payload: dict[str, Any],
    scope_payload: Any | None,
    failures: list[str],
) -> None:
    if payload.get("handoff_decision") != "accepted":
        return
    if not _consumer_verifier_acceptance_gate_applies(payload):
        return
    if not isinstance(scope_payload, dict):
        return
    managed_paths = _consumer_managed_paths(scope_payload)
    if not managed_paths:
        return

    validation_commands = payload.get("validation_commands")
    command_text = "\n".join(item for item in validation_commands if isinstance(item, str)) if isinstance(validation_commands, list) else ""
    if CONSUMER_VERIFIER_COMMAND not in command_text:
        failures.append(
            f"{package_path}: accepted handoff touching consumer-managed path(s) "
            f"{', '.join(managed_paths)} requires a `{CONSUMER_VERIFIER_COMMAND}` validation command"
        )

    evidence_refs = _criteria_verification_refs(payload)
    gate_refs = payload.get("gate_artifact_refs")
    if isinstance(gate_refs, list):
        evidence_refs.extend(item for item in gate_refs if isinstance(item, str))
    evidence_text = "\n".join(evidence_refs)
    if CONSUMER_VERIFIER_COMMAND not in evidence_text and "raw/validation/" not in evidence_text:
        failures.append(
            f"{package_path}: accepted handoff touching consumer-managed path(s) "
            f"{', '.join(managed_paths)} requires verifier evidence refs in acceptance criteria or gate artifacts"
        )


def validate_package(root: Path, package_path: Path) -> list[str]:
    failures: list[str] = []
    try:
        payload = _load_json(package_path)
    except (json.JSONDecodeError, OSError) as exc:
        return [f"{package_path}: could not parse JSON: {exc}"]

    if not isinstance(payload, dict):
        return [f"{package_path}: top-level JSON must be an object"]

    missing = sorted(REQUIRED_FIELDS - set(payload))
    if missing:
        failures.append(f"{package_path}: missing required field(s): {', '.join(missing)}")
        return failures

    if payload.get("schema_version") != "v1":
        failures.append(f"{package_path}: `schema_version` must be 'v1'")

    handoff_id = payload.get("handoff_id")
    if not isinstance(handoff_id, str) or not HANDOFF_ID_PATTERN.fullmatch(handoff_id):
        failures.append(f"{package_path}: `handoff_id` must match ^[a-z0-9][a-z0-9._-]*$")

    issue_number = payload.get("issue_number")
    if not isinstance(issue_number, int) or issue_number <= 0:
        failures.append(f"{package_path}: `issue_number` must be a positive integer")

    lifecycle_state = payload.get("lifecycle_state")
    if lifecycle_state not in VALID_LIFECYCLE_STATES:
        failures.append(f"{package_path}: invalid lifecycle_state {lifecycle_state!r}")

    if payload.get("handoff_decision") not in VALID_DECISIONS:
        failures.append(f"{package_path}: invalid handoff_decision {payload.get('handoff_decision')!r}")

    structured_plan = None
    try:
        structured_plan_ref = _normalize_repo_path(payload["structured_plan_ref"], "structured_plan_ref", package_path)
    except ValueError as exc:
        failures.append(str(exc))
    else:
        structured_plan = _read_json_ref(root, structured_plan_ref, "structured_plan_ref", package_path, failures)
        if isinstance(structured_plan, dict) and isinstance(issue_number, int):
            plan_issue = structured_plan.get("issue_number")
            if plan_issue != issue_number:
                failures.append(
                    f"{package_path}: structured plan issue mismatch: handoff issue {issue_number}, plan issue {plan_issue}"
                )

    execution_scope_ref = payload.get("execution_scope_ref")
    if lifecycle_state in SCOPE_REQUIRED_STATES and not execution_scope_ref:
        failures.append(f"{package_path}: lifecycle_state {lifecycle_state!r} requires `execution_scope_ref`")
    scope_payload: Any | None = None
    if isinstance(execution_scope_ref, str):
        try:
            scope_ref = _normalize_repo_path(execution_scope_ref, "execution_scope_ref", package_path)
        except ValueError as exc:
            failures.append(str(exc))
        else:
            scope_payload = _read_json_ref(root, scope_ref, "execution_scope_ref", package_path, failures)
            if isinstance(scope_payload, dict) and isinstance(issue_number, int):
                lane_claim = scope_payload.get("lane_claim")
                if isinstance(lane_claim, dict) and lane_claim.get("issue_number") != issue_number:
                    failures.append(
                        f"{package_path}: execution scope lane_claim issue mismatch: handoff issue {issue_number}, "
                        f"scope issue {lane_claim.get('issue_number')}"
                    )

    packet_ref = payload.get("packet_ref")
    if lifecycle_state in PACKET_REQUIRED_STATES and not packet_ref:
        failures.append(f"{package_path}: lifecycle_state {lifecycle_state!r} requires `packet_ref`")
    if isinstance(packet_ref, str):
        packet_path = _normalize_repo_path(packet_ref, "packet_ref", package_path)
        if not _repo_file_exists(root, packet_path):
            failures.append(f"{package_path}: `packet_ref` does not exist: {packet_path}")

    closeout_ref = payload.get("closeout_ref")
    if lifecycle_state in CLOSEOUT_REQUIRED_STATES and not closeout_ref:
        failures.append(f"{package_path}: lifecycle_state {lifecycle_state!r} requires `closeout_ref`")
    if isinstance(closeout_ref, str):
        normalized_closeout = _normalize_repo_path(closeout_ref, "closeout_ref", package_path)
        if not _repo_file_exists(root, normalized_closeout):
            failures.append(f"{package_path}: `closeout_ref` does not exist: {normalized_closeout}")

    validation_commands = payload.get("validation_commands")
    if lifecycle_state not in {"draft", "planned"} and (
        not isinstance(validation_commands, list) or not validation_commands
    ):
        failures.append(f"{package_path}: lifecycle_state {lifecycle_state!r} requires non-empty `validation_commands`")

    _validate_acceptance_criteria(root, package_path, payload, failures)
    _validate_consumer_verifier_acceptance(package_path, payload, scope_payload, failures)
    for field_name in ["review_artifact_refs", "gate_artifact_refs", "artifact_refs", "audit_refs"]:
        _validate_ref_array(root, package_path, payload, field_name, failures)

    return failures


def _discover_package_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for rel_root in ["raw/handoffs", "docs/schemas/examples/package-handoff"]:
        directory = root / rel_root
        if directory.is_dir():
            paths.extend(sorted(directory.glob("*.json")))
    return paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate package handoff artifacts.")
    parser.add_argument("paths", nargs="*", help="Specific handoff package JSON files to validate.")
    parser.add_argument("--root", default=".", help="Repository root.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve(strict=False)
    package_files = [Path(path) for path in args.paths] if args.paths else _discover_package_files(root)
    failures: list[str] = []
    for package_file in package_files:
        if not package_file.is_absolute():
            package_file = root / package_file
        failures.extend(validate_package(root, package_file))

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    print(f"PASS validated {len(package_files)} package handoff file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
