#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


GOVERNANCE_SURFACE_PREFIXES = (
    ".github/scripts/",
    ".github/workflows/",
    "agents/",
    "docs/schemas/",
    "docs/plans/",
    "hooks/",
    "launchd/",
    "raw/closeouts/",
    "raw/cross-review/",
    "raw/execution-scopes/",
    "raw/gate/",
    "raw/handoffs/",
    "raw/model-fallbacks/",
    "raw/operator-context/",
    "raw/packets/",
    "metrics/pilot/",
    "metrics/self-learning/",
    "scripts/knowledge_base/",
    "scripts/lam/",
    "scripts/orchestrator/",
    "scripts/overlord/",
    "scripts/packet/",
    "wiki/",
)
GOVERNANCE_SURFACE_FILES = {
    "CLAUDE.md",
    "README.md",
    "STANDARDS.md",
    "OVERLORD_BACKLOG.md",
    "docs/DATA_DICTIONARY.md",
    "docs/FEATURE_REGISTRY.md",
    "docs/ORG_GOVERNANCE_COMPENDIUM.md",
    "docs/PROGRESS.md",
    "docs/SERVICE_REGISTRY.md",
    "docs/governed_repos.json",
    "docs/graphify_targets.json",
}
IMPLEMENTATION_READY_MODES = {"implementation_ready", "implementation_complete"}
ACCEPTED_REVIEW_STATES = {"accepted", "accepted_with_followup"}
IMPLEMENTATION_READY_REVIEW_GATE_APPROVED_AT = "2026-04-28T19:00:00Z"
ALTERNATE_REVIEW_IDENTITY_GATE_APPROVED_AT = "2026-04-29T16:30:00Z"
SPECIALIST_PACKET_CONTRACT_REVIEWERS = {
    "codex-reviewer",
    "sim-runner",
    "som-worker-triage",
}
ALTERNATE_REVIEW_EXEMPTION_TYPES = {
    "historical_grandfathered",
    "alternate_service_outage",
}
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
DISPATCH_OUTPUT_PREFIXES = (
    "docs/codex-reviews/",
    "raw/cross-review/",
    "raw/packets/outbound/",
    "raw/validation/",
)
PLANNING_EVIDENCE_PREFIXES = (
    "docs/plans/",
    "raw/closeouts/",
    "raw/cross-review/",
    "raw/execution-scopes/",
    "raw/handoffs/",
    "raw/packets/",
    "raw/validation/",
)
PLANNING_EVIDENCE_FILES = {
    "OVERLORD_BACKLOG.md",
    "docs/PROGRESS.md",
}


def _display_path(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def _load_json_safe(path: Path, root: Path, failures: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        failures.append(f"{_display_path(path, root)}: could not parse JSON: {exc}")
        return None


def _find_plan_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*structured-agent-cycle-plan.json"))


def _require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def _branch_issue_number(branch_name: str) -> int | None:
    match = re.search(r"(?:^|/)issue-(\d+)(?:[-_/]|$)", branch_name)
    return int(match.group(1)) if match else None


def _is_governance_surface(path: str) -> bool:
    normalized = path
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized in GOVERNANCE_SURFACE_FILES or any(
        normalized.startswith(prefix) for prefix in GOVERNANCE_SURFACE_PREFIXES
    )


def _read_changed_files(path: Path | None) -> list[str]:
    if path is None:
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _is_planning_evidence_surface(path: str) -> bool:
    normalized = path
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized in PLANNING_EVIDENCE_FILES or any(
        normalized.startswith(prefix) for prefix in PLANNING_EVIDENCE_PREFIXES
    )


def _matching_plan_payloads(
    loaded_plans: list[tuple[Path, object | None]],
    root: Path,
    issue_number: int | None,
) -> list[tuple[Path, object]]:
    if issue_number is None:
        return []
    matches: list[tuple[Path, object]] = []
    for file_path, payload in loaded_plans:
        if isinstance(payload, dict) and payload.get("issue_number") == issue_number:
            matches.append((file_path.relative_to(root), payload))
    return matches


def _matching_execution_scopes(root: Path, issue_number: int | None, mode: str) -> list[Path]:
    if issue_number is None:
        return []
    scope_root = root / "raw" / "execution-scopes"
    if not scope_root.is_dir():
        return []
    return sorted(scope_root.glob(f"*issue-{issue_number}*{mode}*.json"))


def _require_identity(
    value: object,
    path: Path,
    field_name: str,
    failures: list[str],
) -> dict[str, str] | None:
    if not isinstance(value, dict):
        failures.append(f"{path}: `{field_name}` must be an object")
        return None
    required_keys = ("role", "model_id", "model_family")
    for key in required_keys:
        raw = value.get(key)
        if not isinstance(raw, str) or not raw.strip():
            failures.append(f"{path}: `{field_name}.{key}` must be a non-empty string")
            return None
    return {
        "role": str(value["role"]).strip(),
        "model_id": str(value["model_id"]).strip(),
        "model_family": str(value["model_family"]).strip(),
    }


def _require_repo_ref_array(
    value: object,
    path: Path,
    field_name: str,
    failures: list[str],
    *,
    allow_empty: bool,
    required_prefix: str | None = None,
) -> list[str]:
    if not isinstance(value, list):
        failures.append(f"{path}: `{field_name}` must be an array")
        return []
    refs = [item for item in value if isinstance(item, str) and item.strip()]
    if len(refs) != len(value):
        failures.append(f"{path}: `{field_name}` entries must be non-empty strings")
        return []
    if not allow_empty and not refs:
        failures.append(f"{path}: requires non-empty `{field_name}`")
        return []
    if required_prefix is not None:
        invalid = [ref for ref in refs if not ref.startswith(required_prefix)]
        if invalid:
            failures.append(
                f"{path}: `{field_name}` must reference `{required_prefix}...`, got {', '.join(invalid)}"
            )
    return refs


def _repo_ref_exists(root: Path, ref: str) -> bool:
    normalized = ref.strip()
    if not normalized or normalized.startswith("/"):
        return False
    return (root / normalized).is_file()


def _repo_ref_exists_with_prefix(root: Path, ref: str, prefixes: tuple[str, ...]) -> bool:
    normalized = ref.strip()
    return _repo_ref_exists(root, normalized) and any(normalized.startswith(prefix) for prefix in prefixes)


def _agent_registry_has_agent(root: Path, agent_id: str) -> bool:
    registry_path = root / "AGENT_REGISTRY.md"
    if not registry_path.is_file():
        return False
    needle = f"| {agent_id} |"
    return needle in registry_path.read_text(encoding="utf-8")


def _agent_surface_exists(root: Path, agent_id: str) -> bool:
    return any(
        (root / relpath).is_file()
        for relpath in (
            f"agents/{agent_id}.md",
            f"docs/agents/{agent_id}.md",
        )
    )


def _specialist_packet_contract_required(review: dict[str, object]) -> bool:
    packet_contract = review.get("packet_contract")
    if isinstance(packet_contract, dict):
        return True
    reviewer = review.get("reviewer")
    return isinstance(reviewer, str) and reviewer.strip() in SPECIALIST_PACKET_CONTRACT_REVIEWERS


def _validate_specialist_packet_contract(
    root: Path,
    path: Path,
    field_name: str,
    packet_contract: object,
    failures: list[str],
) -> None:
    if not isinstance(packet_contract, dict):
        failures.append(f"{path}: `{field_name}` must be an object")
        return
    required_keys = ("agent_id", "packet_ref", "packet_transport", "response_ref", "availability_ref")
    for key in required_keys:
        raw = packet_contract.get(key)
        if not isinstance(raw, str) or not raw.strip():
            failures.append(f"{path}: `{field_name}.{key}` must be a non-empty string")
    if failures and any(message.startswith(f"{path}: `{field_name}.") for message in failures):
        return

    agent_id = str(packet_contract["agent_id"]).strip()
    packet_ref = str(packet_contract["packet_ref"]).strip()
    packet_transport = str(packet_contract["packet_transport"]).strip()
    response_ref = str(packet_contract["response_ref"]).strip()
    availability_ref = str(packet_contract["availability_ref"]).strip()
    package_manifest_ref = packet_contract.get("package_manifest_ref")

    if packet_transport != "file":
        failures.append(f"{path}: `{field_name}.packet_transport` must be 'file'")
    if not _repo_ref_exists_with_prefix(root, packet_ref, ("raw/packets/",)):
        failures.append(f"{path}: `{field_name}.packet_ref` must exist under `raw/packets/`: {packet_ref}")
    response_prefixes = ("docs/codex-reviews/", "raw/cross-review/", "raw/packets/outbound/", "raw/validation/")
    if not _repo_ref_exists_with_prefix(root, response_ref, response_prefixes):
        failures.append(
            f"{path}: `{field_name}.response_ref` must exist under one of {list(response_prefixes)}: {response_ref}"
        )
    valid_availability_ref = availability_ref in {
        "AGENT_REGISTRY.md",
        f"agents/{agent_id}.md",
        f"docs/agents/{agent_id}.md",
    }
    if not valid_availability_ref or not _repo_ref_exists(root, availability_ref):
        failures.append(
            f"{path}: `{field_name}.availability_ref` must be AGENT_REGISTRY.md or an agent definition for `{agent_id}`"
        )
    if not (_agent_registry_has_agent(root, agent_id) or _agent_surface_exists(root, agent_id)):
        failures.append(f"{path}: `{field_name}.agent_id` does not resolve to a tracked specialist agent: {agent_id}")

    if agent_id == "sim-runner":
        if not isinstance(package_manifest_ref, str) or not package_manifest_ref.strip():
            failures.append(f"{path}: `{field_name}.package_manifest_ref` is required for sim-runner")
            return
        if not _repo_ref_exists(root, package_manifest_ref):
            failures.append(f"{path}: `{field_name}.package_manifest_ref` does not exist: {package_manifest_ref}")
            return
        manifest_payload = _load_json_safe(root / package_manifest_ref, root, failures)
        if not isinstance(manifest_payload, dict):
            return
        if manifest_payload.get("package") != "hldpro-sim":
            failures.append(f"{path}: `{field_name}.package_manifest_ref` must reference hldpro-sim package state")
        managed_personas = manifest_payload.get("managed_personas")
        personas = managed_personas.get("personas") if isinstance(managed_personas, dict) else None
        if not isinstance(personas, list) or not personas:
            failures.append(
                f"{path}: `{field_name}.package_manifest_ref` must expose non-empty managed personas for sim-runner"
            )
        if not response_ref.startswith("raw/packets/outbound/"):
            failures.append(
                f"{path}: `{field_name}.response_ref` for sim-runner must resolve under `raw/packets/outbound/`"
            )
    elif package_manifest_ref is not None and not (
        isinstance(package_manifest_ref, str) and package_manifest_ref.strip() and _repo_ref_exists(root, package_manifest_ref)
    ):
        failures.append(
            f"{path}: `{field_name}.package_manifest_ref` must be null or an existing repo-relative path"
        )


def _validate_dispatch_contract(
    root: Path,
    path: Path,
    payload: dict[str, object],
    plan_author: dict[str, str] | None,
    failures: list[str],
) -> None:
    dispatch_contract = payload.get("dispatch_contract")
    if not isinstance(dispatch_contract, dict):
        failures.append(f"{path}: active issue-branch plans require a non-null `dispatch_contract`")
        return

    primary_session_family = dispatch_contract.get("primary_session_family")
    if primary_session_family not in {"openai", "anthropic"}:
        failures.append(
            f"{path}: `dispatch_contract.primary_session_family` must be one of ['anthropic', 'openai']"
        )
        return
    if plan_author is not None and primary_session_family != plan_author["model_family"]:
        failures.append(
            f"{path}: `dispatch_contract.primary_session_family` must match `plan_author.model_family`"
        )
    expected_wrapper_id = DISPATCH_WRAPPER_IDS[str(primary_session_family)]
    wrapper_path = dispatch_contract.get("wrapper_path")
    if wrapper_path != DISPATCH_WRAPPER_PATH:
        failures.append(
            f"{path}: `dispatch_contract.wrapper_path` must be `{DISPATCH_WRAPPER_PATH}`"
        )
    elif not _repo_ref_exists(root, wrapper_path):
        failures.append(f"{path}: `dispatch_contract.wrapper_path` does not exist: {wrapper_path}")

    wrapper_id = dispatch_contract.get("wrapper_id")
    if not isinstance(wrapper_id, str) or not wrapper_id.strip():
        failures.append(f"{path}: `dispatch_contract.wrapper_id` must be a non-empty string")
    elif wrapper_id != expected_wrapper_id:
        failures.append(
            f"{path}: `dispatch_contract.wrapper_id` must be `{expected_wrapper_id}` for primary session family `{primary_session_family}`"
        )

    packet_transport_mode = dispatch_contract.get("packet_transport_mode")
    if packet_transport_mode != "file":
        failures.append(f"{path}: `dispatch_contract.packet_transport_mode` must be 'file'")

    owned_roles = dispatch_contract.get("owned_roles")
    if not isinstance(owned_roles, list) or not owned_roles:
        failures.append(f"{path}: `dispatch_contract.owned_roles` must be a non-empty array")
    else:
        owned_families: set[str] = set()
        for index, item in enumerate(owned_roles, start=1):
            if not isinstance(item, dict):
                failures.append(f"{path}: `dispatch_contract.owned_roles[{index}]` must be an object")
                continue
            role = item.get("role")
            model_family = item.get("model_family")
            if not isinstance(role, str) or not role.strip():
                failures.append(f"{path}: `dispatch_contract.owned_roles[{index}].role` must be a non-empty string")
            if model_family not in {"openai", "anthropic"}:
                failures.append(
                    f"{path}: `dispatch_contract.owned_roles[{index}].model_family` must be one of ['anthropic', 'openai']"
                )
                continue
            if model_family == primary_session_family:
                failures.append(
                    f"{path}: `dispatch_contract.owned_roles[{index}]` cannot be absorbed by the primary session family"
                )
            owned_families.add(str(model_family))

        accepted_families: set[str] = set()
        specialist_reviews = payload.get("specialist_reviews")
        if isinstance(specialist_reviews, list):
            for review_index, review in enumerate(specialist_reviews, start=1):
                if isinstance(review, dict) and review.get("status") in ACCEPTED_REVIEW_STATES:
                    reviewer_family = review.get("reviewer_model_family")
                    if isinstance(reviewer_family, str) and reviewer_family:
                        accepted_families.add(reviewer_family)
                        if reviewer_family == primary_session_family:
                            failures.append(
                                f"{path}: accepted specialist_reviews reviewer family cannot match the primary session family"
                            )
        alternate_review = payload.get("alternate_model_review")
        if isinstance(alternate_review, dict) and alternate_review.get("status") in ACCEPTED_REVIEW_STATES:
            reviewer_family = alternate_review.get("reviewer_model_family")
            if isinstance(reviewer_family, str) and reviewer_family:
                accepted_families.add(reviewer_family)
                if reviewer_family == primary_session_family:
                    failures.append(
                        f"{path}: accepted alternate_model_review family cannot match the primary session family"
                    )

        owned_families = {
            str(item.get("model_family"))
            for item in owned_roles
            if isinstance(item, dict) and isinstance(item.get("model_family"), str)
        }
        for accepted_family in accepted_families:
            if accepted_family not in owned_families:
                failures.append(
                    f"{path}: `dispatch_contract.owned_roles` must declare opposite-family ownership for `{accepted_family}`"
                )

    output_artifact_refs = _require_repo_ref_array(
        dispatch_contract.get("output_artifact_refs"),
        path,
        "dispatch_contract.output_artifact_refs",
        failures,
        allow_empty=False,
    )
    for ref in output_artifact_refs:
        if not _repo_ref_exists(root, ref):
            failures.append(f"{path}: `dispatch_contract.output_artifact_refs` entry does not exist: {ref}")
        if not any(ref.startswith(prefix) for prefix in DISPATCH_OUTPUT_PREFIXES):
            failures.append(
                f"{path}: `dispatch_contract.output_artifact_refs` must reference a governed output artifact, got {ref}"
            )

    fallback_policy = dispatch_contract.get("fallback_policy")
    if not isinstance(fallback_policy, dict):
        failures.append(f"{path}: `dispatch_contract.fallback_policy` must be an object")
        return
    if fallback_policy.get("same_family_only") is not True:
        failures.append(f"{path}: `dispatch_contract.fallback_policy.same_family_only` must be true")
    ordered_models = fallback_policy.get("ordered_models")
    if not isinstance(ordered_models, list) or not ordered_models:
        failures.append(f"{path}: `dispatch_contract.fallback_policy.ordered_models` must be a non-empty array")
        return
    expected_order = FALLBACK_MODEL_ORDER[str(primary_session_family)]
    last_rank = -1
    for index, item in enumerate(ordered_models, start=1):
        if not isinstance(item, dict):
            failures.append(f"{path}: `dispatch_contract.fallback_policy.ordered_models[{index}]` must be an object")
            continue
        family = item.get("family")
        model_id = item.get("model_id")
        if family != primary_session_family:
            failures.append(
                f"{path}: `dispatch_contract.fallback_policy.ordered_models[{index}].family` must match `{primary_session_family}`"
            )
            continue
        if not isinstance(model_id, str) or not model_id.strip():
            failures.append(
                f"{path}: `dispatch_contract.fallback_policy.ordered_models[{index}].model_id` must be a non-empty string"
            )
            continue
        try:
            model_rank = expected_order.index(model_id)
        except ValueError:
            failures.append(
                f"{path}: `dispatch_contract.fallback_policy.ordered_models[{index}].model_id` must be an approved model for `{primary_session_family}`"
            )
            continue
        if model_rank <= last_rank:
            failures.append(
                f"{path}: `dispatch_contract.fallback_policy.ordered_models[{index}]` must be in strictly increasing quality order"
            )
            continue
        last_rank = model_rank


def _validate_alternate_review_exemption(path: Path, review: dict[str, object], failures: list[str]) -> None:
    exemption = review.get("exemption")
    if not isinstance(exemption, dict):
        failures.append(f"{path}: `alternate_model_review.exemption` must be present when `required` is false")
        return
    exemption_type = exemption.get("exemption_type")
    if exemption_type not in ALTERNATE_REVIEW_EXEMPTION_TYPES:
        failures.append(
            f"{path}: `alternate_model_review.exemption.exemption_type` must be one of {sorted(ALTERNATE_REVIEW_EXEMPTION_TYPES)}"
        )
    granted_by = exemption.get("granted_by")
    if not isinstance(granted_by, str) or not granted_by.strip():
        failures.append(f"{path}: `alternate_model_review.exemption.granted_by` must be a non-empty string")
    expires_at = exemption.get("expires_at")
    if not isinstance(expires_at, str) or not expires_at.strip():
        failures.append(f"{path}: `alternate_model_review.exemption.expires_at` must be a non-empty RFC3339 timestamp")
    rationale = exemption.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        failures.append(f"{path}: `alternate_model_review.exemption.rationale` must be a non-empty string")
    status = review.get("status")
    if exemption_type == "alternate_service_outage" and status != "unavailable":
        failures.append(
            f"{path}: `alternate_model_review.status` must be 'unavailable' when exemption_type is 'alternate_service_outage'"
        )
    if exemption_type == "historical_grandfathered" and status != "not_requested":
        failures.append(
            f"{path}: `alternate_model_review.status` must be 'not_requested' when exemption_type is 'historical_grandfathered'"
        )


def _alternate_review_identity_gate_applies(payload: dict[str, object]) -> bool:
    approved_at = payload.get("approved_at")
    if not isinstance(approved_at, str) or not approved_at:
        return True
    return approved_at >= ALTERNATE_REVIEW_IDENTITY_GATE_APPROVED_AT


def _validate_alternate_review_identity(
    root: Path,
    path: Path,
    payload: dict[str, object],
    plan_author: dict[str, str] | None,
    alternate_review: dict[str, object],
    failures: list[str],
) -> None:
    if not _alternate_review_identity_gate_applies(payload):
        return
    if alternate_review.get("status") not in ACCEPTED_REVIEW_STATES:
        return
    reviewer_model_id = alternate_review.get("reviewer_model_id")
    reviewer_model_family = alternate_review.get("reviewer_model_family")
    if not isinstance(reviewer_model_id, str) or not reviewer_model_id.strip():
        failures.append(f"{path}: accepted `alternate_model_review` must include non-empty `reviewer_model_id`")
        return
    if not isinstance(reviewer_model_family, str) or not reviewer_model_family.strip():
        failures.append(f"{path}: accepted `alternate_model_review` must include non-empty `reviewer_model_family`")
        return
    if plan_author is None:
        return
    if reviewer_model_family == plan_author["model_family"]:
        failures.append(
            f"{path}: accepted `alternate_model_review` must use an alternate model family from `plan_author`"
        )
    if (
        reviewer_model_id == plan_author["model_id"]
        and reviewer_model_family == plan_author["model_family"]
    ):
        failures.append(
            f"{path}: accepted `alternate_model_review` cannot use the same model identity as `plan_author`"
        )


def _validate_active_issue_branch_contract(
    root: Path, path: Path, payload: dict[str, object], failures: list[str]
) -> None:
    plan_author = _require_identity(payload.get("plan_author"), path, "plan_author", failures)

    specialist_reviews = payload.get("specialist_reviews")
    accepted_specialist_reviews = 0
    if isinstance(specialist_reviews, list):
        for index, review in enumerate(specialist_reviews, start=1):
            if not isinstance(review, dict):
                continue
            if review.get("status") not in ACCEPTED_REVIEW_STATES:
                continue
            accepted_specialist_reviews += 1
            identity = _require_identity(
                {
                    "role": review.get("role"),
                    "model_id": review.get("reviewer_model_id"),
                    "model_family": review.get("reviewer_model_family"),
                },
                path,
                f"specialist_reviews[{index}] reviewer identity",
                failures,
            )
            if plan_author and identity:
                if (
                    identity["model_id"] == plan_author["model_id"]
                    and identity["model_family"] == plan_author["model_family"]
                ):
                    failures.append(
                        f"{path}: specialist_reviews[{index}] cannot self-approve with the same model identity as `plan_author`"
                    )
            if _specialist_packet_contract_required(review):
                _validate_specialist_packet_contract(
                    root,
                    path,
                    f"specialist_reviews[{index}].packet_contract",
                    review.get("packet_contract"),
                    failures,
                )

    alternate_review = payload.get("alternate_model_review")
    if isinstance(alternate_review, dict) and alternate_review.get("required") is False:
        _validate_alternate_review_exemption(path, alternate_review, failures)
    if isinstance(alternate_review, dict):
        _validate_alternate_review_identity(root, path, payload, plan_author, alternate_review, failures)

    execution_handoff = payload.get("execution_handoff")
    if not isinstance(execution_handoff, dict):
        return
    _validate_dispatch_contract(root, path, payload, plan_author, failures)
    handoff_ref = execution_handoff.get("handoff_package_ref")
    if not isinstance(handoff_ref, str) or not handoff_ref.strip():
        failures.append(f"{path}: active issue-branch plans require a non-null `execution_handoff.handoff_package_ref`")
    elif not _repo_ref_exists(root, handoff_ref):
        failures.append(f"{path}: `execution_handoff.handoff_package_ref` does not exist: {handoff_ref}")

    accepted_alternate_review = (
        isinstance(alternate_review, dict) and alternate_review.get("status") in ACCEPTED_REVIEW_STATES
    )
    mode = execution_handoff.get("execution_mode")
    review_refs_required = accepted_specialist_reviews > 0 or accepted_alternate_review or mode in IMPLEMENTATION_READY_MODES
    review_refs = _require_repo_ref_array(
        execution_handoff.get("review_artifact_refs"),
        path,
        "execution_handoff.review_artifact_refs",
        failures,
        allow_empty=not review_refs_required,
        required_prefix="raw/cross-review/",
    )
    if review_refs_required:
        for ref in review_refs:
            if not _repo_ref_exists(root, ref):
                failures.append(f"{path}: `execution_handoff.review_artifact_refs` entry does not exist: {ref}")


def _validate_planner_boundary_scope_presence(
    root: Path,
    branch_name: str,
    changed_files: list[str],
    failures: list[str],
) -> None:
    boundary_changes = [path for path in changed_files if _is_governance_surface(path)]
    if not boundary_changes:
        return

    issue_number = _branch_issue_number(branch_name)
    if issue_number is None:
        failures.append(
            "planner-boundary changes require a branch name containing `issue-<number>` so execution-scope evidence can be resolved; changed paths: "
            + ", ".join(boundary_changes)
        )
        return

    implementation_scopes = _matching_execution_scopes(root, issue_number, "implementation")
    planning_scopes = _matching_execution_scopes(root, issue_number, "planning")
    if len(implementation_scopes) > 1:
        failures.append(f"multiple implementation execution scopes match issue #{issue_number}")
    if len(planning_scopes) > 1:
        failures.append(f"multiple planning execution scopes match issue #{issue_number}")
    if not implementation_scopes and not planning_scopes:
        failures.append(
            f"planner-boundary changes require an issue-specific execution scope for issue #{issue_number}; "
            f"expected raw/execution-scopes/*issue-{issue_number}*implementation*.json or *issue-{issue_number}*planning*.json; "
            "changed paths: " + ", ".join(boundary_changes)
        )


def _validate_implementation_ready_plan(path: Path, payload: object, failures: list[str]) -> None:
    if not isinstance(payload, dict):
        failures.append(f"{path}: implementation gate plan must be a JSON object")
        return
    _require(payload.get("approved") is True, f"{path}: governance-surface plan must have `approved: true`", failures)
    handoff = payload.get("execution_handoff")
    if not isinstance(handoff, dict):
        failures.append(f"{path}: governance-surface plan must include `execution_handoff`")
    else:
        mode = handoff.get("execution_mode")
        _require(
            mode in IMPLEMENTATION_READY_MODES,
            f"{path}: governance-surface plan execution_mode must be one of {sorted(IMPLEMENTATION_READY_MODES)}, got {mode!r}",
            failures,
        )
    _validate_implementation_ready_alternate_review(path, payload, failures, scope="governance-surface")


def _validate_planning_evidence_plan(path: Path, payload: object, failures: list[str]) -> None:
    if not isinstance(payload, dict):
        failures.append(f"{path}: planning-evidence gate plan must be a JSON object")
        return
    _require(payload.get("approved") is True, f"{path}: planning-evidence plan must have `approved: true`", failures)
    handoff = payload.get("execution_handoff")
    if not isinstance(handoff, dict):
        failures.append(f"{path}: planning-evidence plan must include `execution_handoff`")
    else:
        mode = handoff.get("execution_mode")
        _require(
            mode in {"planning_only"} | IMPLEMENTATION_READY_MODES,
            f"{path}: planning-evidence plan execution_mode must be one of {sorted({'planning_only'} | IMPLEMENTATION_READY_MODES)}, got {mode!r}",
            failures,
        )
    review = payload.get("alternate_model_review")
    if isinstance(review, dict) and review.get("required") is True:
        status = review.get("status")
        _require(
            status in ACCEPTED_REVIEW_STATES,
            f"{path}: planning-evidence plan requires accepted alternate_model_review before closeout, got {status!r}",
            failures,
        )


def _validate_implementation_ready_alternate_review(
    path: Path,
    payload: dict[str, object],
    failures: list[str],
    *,
    scope: str,
) -> None:
    execution_handoff = payload.get("execution_handoff")
    if not isinstance(execution_handoff, dict):
        return
    mode = execution_handoff.get("execution_mode")
    if mode not in IMPLEMENTATION_READY_MODES:
        return
    approved_at = payload.get("approved_at")
    if isinstance(approved_at, str) and approved_at and approved_at < IMPLEMENTATION_READY_REVIEW_GATE_APPROVED_AT:
        return

    review = payload.get("alternate_model_review")
    if not isinstance(review, dict):
        failures.append(f"{path}: implementation-ready plan must include `alternate_model_review`")
        return

    _require(
        review.get("required") is True,
        f"{path}: implementation-ready plan must set `alternate_model_review.required` to true before {scope} execution",
        failures,
    )
    status = review.get("status")
    _require(
        status in ACCEPTED_REVIEW_STATES,
        f"{path}: implementation-ready plan requires accepted alternate_model_review before {scope} execution, got {status!r}",
        failures,
    )


def _validate_file(path: Path, payload: object, failures: list[str]) -> None:
    if not isinstance(payload, dict):
        failures.append(f"{path}: top-level JSON must be an object")
        return

    required = [
        "session_id",
        "issue_number",
        "objective",
        "tier",
        "scope_boundary",
        "out_of_scope",
        "research_summary",
        "research_artifacts",
        "sprints",
        "specialist_reviews",
        "alternate_model_review",
        "execution_handoff",
        "material_deviation_rules",
        "approved",
        "approved_by",
        "approved_at",
    ]
    for key in required:
        _require(key in payload, f"{path}: missing required field `{key}`", failures)

    if failures:
        return

    _require(isinstance(payload["issue_number"], int) and payload["issue_number"] > 0, f"{path}: `issue_number` must be a positive integer", failures)
    _require(isinstance(payload["tier"], int) and 1 <= payload["tier"] <= 3, f"{path}: `tier` must be 1, 2, or 3", failures)
    _require(isinstance(payload["scope_boundary"], list) and len(payload["scope_boundary"]) > 0, f"{path}: `scope_boundary` must be a non-empty array", failures)
    _require(isinstance(payload["out_of_scope"], list) and len(payload["out_of_scope"]) > 0, f"{path}: `out_of_scope` must be a non-empty array", failures)
    _require(isinstance(payload["research_artifacts"], list) and len(payload["research_artifacts"]) > 0, f"{path}: `research_artifacts` must be a non-empty array", failures)
    _require(isinstance(payload["material_deviation_rules"], list) and len(payload["material_deviation_rules"]) > 0, f"{path}: `material_deviation_rules` must be a non-empty array", failures)
    _require(isinstance(payload["approved_by"], list) and len(payload["approved_by"]) > 0, f"{path}: `approved_by` must be a non-empty array", failures)

    sprints = payload["sprints"]
    _require(isinstance(sprints, list) and len(sprints) > 0, f"{path}: `sprints` must be a non-empty array", failures)
    if isinstance(sprints, list):
        for index, sprint in enumerate(sprints, start=1):
            prefix = f"{path}: sprint[{index}]"
            _require(isinstance(sprint, dict), f"{prefix} must be an object", failures)
            if not isinstance(sprint, dict):
                continue
            for key in ["name", "goal", "tasks", "acceptance_criteria", "file_paths"]:
                _require(key in sprint, f"{prefix} missing `{key}`", failures)
            _require(isinstance(sprint.get("tasks"), list) and len(sprint.get("tasks", [])) > 0, f"{prefix} `tasks` must be a non-empty array", failures)
            _require(isinstance(sprint.get("acceptance_criteria"), list) and len(sprint.get("acceptance_criteria", [])) > 0, f"{prefix} `acceptance_criteria` must be a non-empty array", failures)
            _require(isinstance(sprint.get("file_paths"), list) and len(sprint.get("file_paths", [])) > 0, f"{prefix} `file_paths` must be a non-empty array", failures)

    specialist_reviews = payload["specialist_reviews"]
    _require(isinstance(specialist_reviews, list) and len(specialist_reviews) > 0, f"{path}: `specialist_reviews` must be a non-empty array", failures)
    if isinstance(specialist_reviews, list):
        for index, review in enumerate(specialist_reviews, start=1):
            prefix = f"{path}: specialist_reviews[{index}]"
            _require(isinstance(review, dict), f"{prefix} must be an object", failures)
            if not isinstance(review, dict):
                continue
            for key in ["reviewer", "role", "focus", "status", "summary", "evidence"]:
                _require(key in review, f"{prefix} missing `{key}`", failures)
            _require(isinstance(review.get("evidence"), list) and len(review.get("evidence", [])) > 0, f"{prefix} `evidence` must be a non-empty array", failures)
            if "packet_contract" in review:
                _require(isinstance(review.get("packet_contract"), dict), f"{prefix} `packet_contract` must be an object", failures)

    alternate_review = payload["alternate_model_review"]
    _require(isinstance(alternate_review, dict), f"{path}: `alternate_model_review` must be an object", failures)
    if isinstance(alternate_review, dict):
        for key in ["required", "reviewer", "model_family", "status", "summary", "evidence"]:
            _require(key in alternate_review, f"{path}: `alternate_model_review` missing `{key}`", failures)
        _require(isinstance(alternate_review.get("evidence"), list) and len(alternate_review.get("evidence", [])) > 0, f"{path}: `alternate_model_review.evidence` must be a non-empty array", failures)

    execution_handoff = payload["execution_handoff"]
    _require(isinstance(execution_handoff, dict), f"{path}: `execution_handoff` must be an object", failures)
    if isinstance(execution_handoff, dict):
        for key in ["session_agent", "execution_mode", "approved_scope_summary", "next_execution_step", "blocked_on"]:
            _require(key in execution_handoff, f"{path}: `execution_handoff` missing `{key}`", failures)
        _require(isinstance(execution_handoff.get("blocked_on"), list), f"{path}: `execution_handoff.blocked_on` must be an array", failures)

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate structured agent cycle plan files.")
    parser.add_argument("--root", default=".", help="Repo root to scan.")
    parser.add_argument("--require-if-issue-branch", action="store_true", help="Fail if on an issue/riskfix branch and no structured plan file exists.")
    parser.add_argument("--branch-name", default="", help="Optional branch name for enforcement decisions.")
    parser.add_argument("--changed-files-file", type=Path, help="Optional newline-delimited changed file list for governance-surface enforcement.")
    parser.add_argument("--enforce-governance-surface", action="store_true", help="Require an approved issue-specific plan when governance-surface files changed.")
    parser.add_argument("--enforce-planner-boundary-scope", action="store_true", help="Require issue-specific execution-scope evidence when planner-boundary files changed.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    files = _find_plan_files(root)
    failures: list[str] = []
    loaded_plans = [(file_path, _load_json_safe(file_path, root, failures)) for file_path in files]

    if args.require_if_issue_branch:
        branch = args.branch_name
        issue_number = _branch_issue_number(branch)
        branch_requires_plan = issue_number is not None or branch.startswith("riskfix/")
        if branch_requires_plan and not files:
            failures.append(f"{branch}: requires at least one `*structured-agent-cycle-plan.json` file before execution.")
        elif issue_number is not None and not _matching_plan_payloads(loaded_plans, root, issue_number):
            failures.append(
                f"{branch}: requires a canonical structured plan for issue #{issue_number} before execution."
            )

    changed_files = _read_changed_files(args.changed_files_file)
    governance_surface_changes = [path for path in changed_files if _is_governance_surface(path)]
    active_issue_number = _branch_issue_number(args.branch_name)
    governance_validated_paths: set[Path] = set()
    if args.enforce_governance_surface and governance_surface_changes:
        planning_evidence_only = all(_is_planning_evidence_surface(path) for path in governance_surface_changes)
        if active_issue_number is None:
            failures.append(
                "governance-surface changes require a branch name containing `issue-<number>` and a matching canonical structured plan; changed paths: "
                + ", ".join(governance_surface_changes)
            )
        matches = _matching_plan_payloads(loaded_plans, root, active_issue_number)
        if not matches:
            issue_label = f"issue #{active_issue_number}" if active_issue_number is not None else "this branch"
            failures.append(
                f"governance-surface changes require a canonical structured plan for {issue_label}; changed paths: "
                + ", ".join(governance_surface_changes)
            )
        for rel_path, payload in matches:
            if planning_evidence_only:
                _validate_planning_evidence_plan(rel_path, payload, failures)
            else:
                _validate_implementation_ready_plan(rel_path, payload, failures)
            governance_validated_paths.add(rel_path)

    if args.enforce_planner_boundary_scope:
        _validate_planner_boundary_scope_presence(root, args.branch_name, changed_files, failures)

    if active_issue_number is not None:
        matches = _matching_plan_payloads(loaded_plans, root, active_issue_number)
        for rel_path, payload in matches:
            if rel_path in governance_validated_paths:
                continue
            _validate_implementation_ready_alternate_review(rel_path, payload, failures, scope="implementation")
            if isinstance(payload, dict):
                _validate_active_issue_branch_contract(root, rel_path, payload, failures)

    for file_path, payload in loaded_plans:
        if payload is not None:
            _validate_file(file_path.relative_to(root), payload, failures)

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    if files:
        print(f"PASS validated {len(files)} structured agent cycle plan file(s)")
    else:
        print("PASS no structured agent cycle plan files found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
