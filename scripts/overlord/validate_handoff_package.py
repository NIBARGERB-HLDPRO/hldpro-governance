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
    "implementation_complete",
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
    "implementation_complete",
    "in_progress",
    "validation_ready",
    "accepted",
    "released",
    "consumed",
}
PACKET_REQUIRED_STATES = {"validation_ready", "accepted", "released", "consumed"}
CLOSEOUT_REQUIRED_STATES = {"accepted", "released", "consumed", "deprecated", "rolled_back", "archived"}
EVIDENCE_REQUIRED_STATES = {
    "implementation_ready",
    "implementation_complete",
    "in_progress",
    "validation_ready",
    "accepted",
}
EVIDENCE_REFS_GATE_CREATED_AT = "2026-04-28T20:45:00Z"
DISPATCH_CONTRACT_GATE_CREATED_AT = "2026-04-29T17:15:00Z"
DISPATCH_WRAPPER_PATH = "scripts/codex-review.sh"
DISPATCH_WRAPPER_IDS = {
    "openai": "claude",
    "anthropic": "codex",
}
FALLBACK_MODEL_ORDER = {
    "openai": [
        "gpt-5.3-codex-spark",
        "gpt-5.4",
    ],
    "anthropic": [
        "claude-sonnet-4-6",
        "claude-opus-4-6",
    ],
}
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
SPECIALIST_OUTPUT_PREFIXES = (
    "docs/codex-reviews/",
    "raw/cross-review/",
    "raw/packets/outbound/",
    "raw/validation/",
)
DISPATCH_OUTPUT_PREFIXES = SPECIALIST_OUTPUT_PREFIXES


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


def _repo_file_exists_with_prefix(root: Path, ref: str, prefixes: tuple[str, ...]) -> bool:
    return _repo_file_exists(root, ref) and any(ref.startswith(prefix) for prefix in prefixes)


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


def _validate_non_empty_ref_array_for_state(
    package_path: Path,
    payload: dict[str, Any],
    field_name: str,
    lifecycle_state: str,
    failures: list[str],
) -> None:
    value = payload.get(field_name)
    if not isinstance(value, list) or not value:
        failures.append(
            f"{package_path}: lifecycle_state {lifecycle_state!r} requires non-empty `{field_name}`"
        )


def _evidence_ref_gate_applies(payload: dict[str, Any]) -> bool:
    created_at = payload.get("created_at")
    if not isinstance(created_at, str) or not created_at:
        return True
    return created_at >= EVIDENCE_REFS_GATE_CREATED_AT


def _dispatch_contract_gate_applies(payload: dict[str, Any]) -> bool:
    created_at = payload.get("created_at")
    if not isinstance(created_at, str) or not created_at:
        return False
    return created_at >= DISPATCH_CONTRACT_GATE_CREATED_AT


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


def _validate_dispatch_contract(
    root: Path,
    package_path: Path,
    payload: dict[str, Any],
    failures: list[str],
) -> None:
    dispatch_contract = payload.get("dispatch_contract")
    if not isinstance(dispatch_contract, dict):
        failures.append(f"{package_path}: `dispatch_contract` must be an object")
        return

    primary_session_family = dispatch_contract.get("primary_session_family")
    if primary_session_family not in {"openai", "anthropic"}:
        failures.append(f"{package_path}: `dispatch_contract.primary_session_family` must be one of ['anthropic', 'openai']")
        return

    expected_wrapper_id = DISPATCH_WRAPPER_IDS[str(primary_session_family)]
    wrapper_path = dispatch_contract.get("wrapper_path")
    if wrapper_path != DISPATCH_WRAPPER_PATH:
        failures.append(f"{package_path}: `dispatch_contract.wrapper_path` must be `{DISPATCH_WRAPPER_PATH}`")
    elif not _repo_file_exists(root, wrapper_path):
        failures.append(f"{package_path}: `dispatch_contract.wrapper_path` does not exist: {wrapper_path}")

    wrapper_id = dispatch_contract.get("wrapper_id")
    if not isinstance(wrapper_id, str) or not wrapper_id.strip():
        failures.append(f"{package_path}: `dispatch_contract.wrapper_id` must be a non-empty string")
    elif wrapper_id != expected_wrapper_id:
        failures.append(
            f"{package_path}: `dispatch_contract.wrapper_id` must be `{expected_wrapper_id}` for primary session family `{primary_session_family}`"
        )

    if dispatch_contract.get("packet_transport_mode") != "file":
        failures.append(f"{package_path}: `dispatch_contract.packet_transport_mode` must be 'file'")

    owned_roles = dispatch_contract.get("owned_roles")
    if not isinstance(owned_roles, list) or not owned_roles:
        failures.append(f"{package_path}: `dispatch_contract.owned_roles` must be a non-empty array")
    else:
        for index, item in enumerate(owned_roles, start=1):
            if not isinstance(item, dict):
                failures.append(f"{package_path}: `dispatch_contract.owned_roles[{index}]` must be an object")
                continue
            role = item.get("role")
            model_family = item.get("model_family")
            if not isinstance(role, str) or not role.strip():
                failures.append(f"{package_path}: `dispatch_contract.owned_roles[{index}].role` must be a non-empty string")
            if model_family not in {"openai", "anthropic"}:
                failures.append(
                    f"{package_path}: `dispatch_contract.owned_roles[{index}].model_family` must be one of ['anthropic', 'openai']"
                )
                continue
            if model_family == primary_session_family:
                failures.append(
                    f"{package_path}: `dispatch_contract.owned_roles[{index}]` cannot be absorbed by the primary session family"
                )

    output_artifact_refs = dispatch_contract.get("output_artifact_refs")
    if not isinstance(output_artifact_refs, list) or not output_artifact_refs:
        failures.append(f"{package_path}: `dispatch_contract.output_artifact_refs` must be a non-empty array")
        return
    for index, item in enumerate(output_artifact_refs, start=1):
        if not isinstance(item, str) or not item.strip():
            failures.append(f"{package_path}: `dispatch_contract.output_artifact_refs[{index}]` must be a non-empty string")
            continue
        normalized = _normalize_repo_path(item, f"dispatch_contract.output_artifact_refs[{index}]", package_path)
        if not _repo_file_exists(root, normalized):
            failures.append(
                f"{package_path}: `dispatch_contract.output_artifact_refs[{index}]` does not exist: {normalized}"
            )
        if not any(normalized.startswith(prefix) for prefix in DISPATCH_OUTPUT_PREFIXES):
            failures.append(
                f"{package_path}: `dispatch_contract.output_artifact_refs[{index}]` must reference a governed output artifact, got {normalized}"
            )

    packet_output_ref = payload.get("packet_output_ref")
    if isinstance(packet_output_ref, str) and packet_output_ref and packet_output_ref not in output_artifact_refs:
        failures.append(f"{package_path}: `packet_output_ref` must be included in `dispatch_contract.output_artifact_refs`")

    fallback_policy = dispatch_contract.get("fallback_policy")
    if not isinstance(fallback_policy, dict):
        failures.append(f"{package_path}: `dispatch_contract.fallback_policy` must be an object")
        return
    if fallback_policy.get("same_family_only") is not True:
        failures.append(f"{package_path}: `dispatch_contract.fallback_policy.same_family_only` must be true")
    ordered_models = fallback_policy.get("ordered_models")
    if not isinstance(ordered_models, list) or not ordered_models:
        failures.append(f"{package_path}: `dispatch_contract.fallback_policy.ordered_models` must be a non-empty array")
        return
    expected_order = FALLBACK_MODEL_ORDER[str(primary_session_family)]
    last_rank = -1
    for index, item in enumerate(ordered_models, start=1):
        if not isinstance(item, dict):
            failures.append(f"{package_path}: `dispatch_contract.fallback_policy.ordered_models[{index}]` must be an object")
            continue
        family = item.get("family")
        model_id = item.get("model_id")
        if family != primary_session_family:
            failures.append(
                f"{package_path}: `dispatch_contract.fallback_policy.ordered_models[{index}].family` must match `{primary_session_family}`"
            )
            continue
        if not isinstance(model_id, str) or not model_id.strip():
            failures.append(
                f"{package_path}: `dispatch_contract.fallback_policy.ordered_models[{index}].model_id` must be a non-empty string"
            )
            continue
        try:
            model_rank = expected_order.index(model_id)
        except ValueError:
            failures.append(
                f"{package_path}: `dispatch_contract.fallback_policy.ordered_models[{index}].model_id` must be an approved model for `{primary_session_family}`"
            )
            continue
        if model_rank <= last_rank:
            failures.append(
                f"{package_path}: `dispatch_contract.fallback_policy.ordered_models[{index}]` must be in strictly increasing quality order"
            )
            continue
        last_rank = model_rank

    owned_families = {
        str(item.get("model_family"))
        for item in owned_roles
        if isinstance(item, dict) and isinstance(item.get("model_family"), str)
    }
    if primary_session_family == "openai" and "anthropic" not in owned_families:
        failures.append(f"{package_path}: `dispatch_contract.owned_roles` must declare opposite-family ownership for `anthropic`")
    if primary_session_family == "anthropic" and "openai" not in owned_families:
        failures.append(f"{package_path}: `dispatch_contract.owned_roles` must declare opposite-family ownership for `openai`")


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


def _agent_registry_has_agent(root: Path, agent_id: str) -> bool:
    registry = root / "AGENT_REGISTRY.md"
    return registry.is_file() and f"| {agent_id} |" in registry.read_text(encoding="utf-8")


def _agent_surface_exists(root: Path, agent_id: str) -> bool:
    return any(
        (root / relpath).is_file()
        for relpath in (
            f"agents/{agent_id}.md",
            f"docs/agents/{agent_id}.md",
        )
    )


def _validate_specialist_agent_contract(
    root: Path,
    package_path: Path,
    payload: dict[str, Any],
    failures: list[str],
) -> None:
    specialist_agent = payload.get("specialist_agent")
    packet_transport = payload.get("packet_transport")
    packet_output_ref = payload.get("packet_output_ref")
    availability_ref = payload.get("availability_ref")
    packet_ref = payload.get("packet_ref")
    package_manifest_ref = payload.get("package_manifest_ref")

    if specialist_agent is None and packet_transport is None and packet_output_ref is None and availability_ref is None:
        return

    if not isinstance(specialist_agent, str) or not specialist_agent.strip():
        failures.append(f"{package_path}: `specialist_agent` must be a non-empty string when specialist packet contract fields are present")
        return
    agent_id = specialist_agent.strip()
    if packet_transport != "file":
        failures.append(f"{package_path}: `packet_transport` must be 'file' for specialist-agent handoffs")
    if not isinstance(packet_ref, str) or not _repo_file_exists_with_prefix(root, packet_ref, ("raw/packets/",)):
        failures.append(f"{package_path}: specialist-agent handoffs require `packet_ref` under `raw/packets/`")
    if not isinstance(packet_output_ref, str) or not _repo_file_exists_with_prefix(root, packet_output_ref, SPECIALIST_OUTPUT_PREFIXES):
        failures.append(
            f"{package_path}: `packet_output_ref` must exist under one of {list(SPECIALIST_OUTPUT_PREFIXES)}"
        )
    valid_availability_ref = availability_ref in {
        "AGENT_REGISTRY.md",
        f"agents/{agent_id}.md",
        f"docs/agents/{agent_id}.md",
    }
    if not isinstance(availability_ref, str) or not valid_availability_ref or not _repo_file_exists(root, availability_ref):
        failures.append(
            f"{package_path}: `availability_ref` must be AGENT_REGISTRY.md or an agent definition for `{agent_id}`"
        )
    if not (_agent_registry_has_agent(root, agent_id) or _agent_surface_exists(root, agent_id)):
        failures.append(f"{package_path}: `specialist_agent` does not resolve to a tracked specialist agent: {agent_id}")

    if agent_id == "sim-runner":
        if not isinstance(package_manifest_ref, str) or not package_manifest_ref.strip():
            failures.append(f"{package_path}: sim-runner specialist handoffs require non-null `package_manifest_ref`")
            return
        manifest_payload = _read_json_ref(root, package_manifest_ref, "package_manifest_ref", package_path, failures)
        if not isinstance(manifest_payload, dict):
            return
        if manifest_payload.get("package") != "hldpro-sim":
            failures.append(f"{package_path}: `package_manifest_ref` must reference hldpro-sim package state for sim-runner")
        managed_personas = manifest_payload.get("managed_personas")
        personas = managed_personas.get("personas") if isinstance(managed_personas, dict) else None
        if not isinstance(personas, list) or not personas:
            failures.append(f"{package_path}: sim-runner package state must expose non-empty managed personas")
        if isinstance(packet_output_ref, str) and not packet_output_ref.startswith("raw/packets/outbound/"):
            failures.append(f"{package_path}: sim-runner `packet_output_ref` must resolve under `raw/packets/outbound/`")


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

    if lifecycle_state in EVIDENCE_REQUIRED_STATES and _evidence_ref_gate_applies(payload):
        for field_name in ("review_artifact_refs", "gate_artifact_refs"):
            _validate_non_empty_ref_array_for_state(package_path, payload, field_name, lifecycle_state, failures)

    _validate_acceptance_criteria(root, package_path, payload, failures)
    if _dispatch_contract_gate_applies(payload) or payload.get("dispatch_contract") is not None:
        if payload.get("dispatch_contract") is None:
            failures.append(
                f"{package_path}: handoffs created on or after {DISPATCH_CONTRACT_GATE_CREATED_AT} require `dispatch_contract`"
            )
        else:
            _validate_dispatch_contract(root, package_path, payload, failures)
    _validate_specialist_agent_contract(root, package_path, payload, failures)
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
