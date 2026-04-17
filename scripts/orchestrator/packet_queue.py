#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_QUEUE_ROOT = REPO_ROOT / "raw" / "packets" / "queue"
QUEUE_STATES = ("inbound", "dispatched", "review", "gate", "done", "halted")
ALLOWED_TRANSITIONS = {
    ("inbound", "dispatched"),
    ("inbound", "halted"),
    ("dispatched", "review"),
    ("dispatched", "halted"),
    ("review", "gate"),
    ("review", "halted"),
    ("gate", "done"),
    ("gate", "halted"),
}
LAM_ROLES = {"worker-lam", "critic-lam"}
IMPLEMENTATION_READY_MODES = {"implementation_ready", "implementation_complete"}


def _load_packet_validator():
    validator_path = REPO_ROOT / "scripts" / "packet" / "validate.py"
    spec = importlib.util.spec_from_file_location("som_packet_validate", validator_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load packet validator from {validator_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_PACKET_VALIDATOR = _load_packet_validator()


@dataclass(frozen=True)
class QueueDecision:
    allowed: bool
    status: str
    reason: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_queue(root: Path = DEFAULT_QUEUE_ROOT) -> None:
    for state in QUEUE_STATES:
        (root / state).mkdir(parents=True, exist_ok=True)
    root.mkdir(parents=True, exist_ok=True)


def load_packet(path: Path) -> dict[str, Any]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"failed to read packet YAML: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"packet must be a YAML object: {path}")
    return payload


def atomic_write_packet(packet: dict[str, Any], destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = destination.with_name(f".{destination.name}.{datetime.now(timezone.utc).timestamp()}.tmp")
    tmp_path.write_text(yaml.safe_dump(packet, sort_keys=False), encoding="utf-8")
    tmp_path.replace(destination)
    return destination


def _repo_relative_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        try:
            path.relative_to(repo_root)
        except ValueError as exc:
            raise ValueError(f"path escapes repo root: {value}") from exc
        return path
    return repo_root / path


def _load_plan(repo_root: Path, plan_ref: str) -> dict[str, Any]:
    plan_path = _repo_relative_path(repo_root, plan_ref)
    if not plan_path.exists() or not plan_path.is_file():
        raise ValueError(f"structured plan not found: {plan_ref}")
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"structured plan is not valid JSON: {plan_ref}: {exc}") from exc
    if not isinstance(plan, dict):
        raise ValueError(f"structured plan must be a JSON object: {plan_ref}")
    return plan


def _validate_fallback_ref(repo_root: Path, fallback_ref: str | None) -> None:
    if fallback_ref is None:
        return
    fallback_path = _repo_relative_path(repo_root, fallback_ref)
    fallback_dir = repo_root / "raw" / "model-fallbacks"
    if fallback_path.parent != fallback_dir:
        raise ValueError("fallback_log_ref must resolve under raw/model-fallbacks/")
    if not fallback_path.is_file():
        raise ValueError(f"fallback log not found: {fallback_ref}")


def _validate_execution_scope_ref(repo_root: Path, execution_scope_ref: str | None) -> None:
    if execution_scope_ref is None:
        return
    scope_path = _repo_relative_path(repo_root, execution_scope_ref)
    scope_dir = repo_root / "raw" / "execution-scopes"
    if scope_path.parent != scope_dir:
        raise ValueError("execution_scope_ref must resolve under raw/execution-scopes/")
    if scope_path.suffix != ".json":
        raise ValueError("execution_scope_ref must be a JSON execution-scope artifact")
    if not scope_path.is_file():
        raise ValueError(f"execution scope not found: {execution_scope_ref}")
    try:
        payload = json.loads(scope_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"execution scope is not valid JSON: {execution_scope_ref}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"execution scope must be a JSON object: {execution_scope_ref}")
    required = {"expected_execution_root", "expected_branch", "allowed_write_paths", "forbidden_roots"}
    missing = sorted(required - set(payload))
    if missing:
        raise ValueError(f"execution scope missing required field(s): {', '.join(missing)}")


def _validate_local_refs(repo_root: Path, field_name: str, refs: list[str]) -> None:
    for ref in refs:
        if ref.startswith(("http://", "https://")):
            continue
        ref_path = _repo_relative_path(repo_root, ref)
        if not ref_path.exists():
            raise ValueError(f"{field_name} reference not found: {ref}")


def validate_for_dispatch(
    packet: dict[str, Any],
    packet_path: Path,
    *,
    repo_root: Path = REPO_ROOT,
    dry_run: bool = False,
) -> QueueDecision:
    packets_dir = repo_root / "raw" / "packets"
    schema_ok, schema_failures = _PACKET_VALIDATOR.validate_packet(packet, packets_dir=packets_dir)
    if not schema_ok:
        return QueueDecision(False, "refused", "; ".join(schema_failures))

    governance = packet.get("governance")
    if not isinstance(governance, dict):
        return QueueDecision(False, "refused", "missing governance dispatch metadata")

    try:
        issue_number = governance["issue_number"]
        plan_ref = governance["structured_plan_ref"]
        execution_scope_ref = governance["execution_scope_ref"]
        fallback_ref = governance["fallback_log_ref"]
        validation_commands = governance["validation_commands"]
        review_artifacts = governance["review_artifacts"]
        pii_mode = governance["pii_mode"]
        dispatch_authorized = governance["dispatch_authorized"]
    except KeyError as exc:
        return QueueDecision(False, "refused", f"missing governance field: {exc.args[0]}")

    try:
        _validate_fallback_ref(repo_root, fallback_ref)
        _validate_execution_scope_ref(repo_root, execution_scope_ref)
        _validate_local_refs(repo_root, "review_artifacts", [str(ref) for ref in review_artifacts])
        plan = _load_plan(repo_root, str(plan_ref))
    except ValueError as exc:
        return QueueDecision(False, "refused", str(exc))

    if plan.get("issue_number") != issue_number:
        return QueueDecision(False, "refused", "structured plan issue_number does not match packet issue_number")
    if plan.get("approved") is not True:
        return QueueDecision(False, "refused", "structured plan is not approved")
    handoff = plan.get("execution_handoff")
    if not isinstance(handoff, dict) or handoff.get("execution_mode") not in IMPLEMENTATION_READY_MODES:
        return QueueDecision(False, "refused", "structured plan is not implementation-ready")
    if not validation_commands:
        return QueueDecision(False, "refused", "validation_commands must be non-empty")
    if not review_artifacts:
        return QueueDecision(False, "refused", "review_artifacts must be non-empty")
    if dispatch_authorized is not True and not (dry_run and governance.get("dry_run_authorized") is True):
        return QueueDecision(False, "refused", "dispatch_authorized must be true before dispatch")

    role = packet.get("prior", {}).get("role")
    if pii_mode in {"tagged", "detected", "lam_only"} and role not in LAM_ROLES:
        return QueueDecision(False, "halted", f"PII mode {pii_mode} requires LAM role before dispatch")

    known_failure_context = governance.get("known_failure_context") or []
    for item in known_failure_context:
        if isinstance(item, dict) and item.get("repeat_count", 0) >= 2:
            return QueueDecision(False, "halted", "known failure context repeated; planning-gate escalation required")

    return QueueDecision(True, "ok", f"packet {packet_path.name} is dispatch-ready")


def _audit_path(root: Path) -> Path:
    return root / "audit.jsonl"


def append_audit(root: Path, event: dict[str, Any]) -> None:
    root.mkdir(parents=True, exist_ok=True)
    with _audit_path(root).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def transition_packet(
    packet_path: Path,
    from_state: str,
    to_state: str,
    *,
    queue_root: Path = DEFAULT_QUEUE_ROOT,
    repo_root: Path = REPO_ROOT,
    dry_run: bool = True,
) -> QueueDecision:
    if from_state not in QUEUE_STATES or to_state not in QUEUE_STATES:
        return QueueDecision(False, "refused", "unknown queue state")
    if (from_state, to_state) not in ALLOWED_TRANSITIONS:
        return QueueDecision(False, "refused", f"invalid transition: {from_state}->{to_state}")

    ensure_queue(queue_root)
    source = packet_path
    if not source.is_absolute():
        source = queue_root / from_state / source
    packet_hash = sha256_file(source) if source.exists() else None

    try:
        packet = load_packet(source)
    except ValueError as exc:
        decision = QueueDecision(False, "refused", str(exc))
        _write_transition_audit(queue_root, source, None, from_state, to_state, dry_run, decision, packet_hash)
        return decision

    packet_id = packet.get("packet_id")
    schema_ok, schema_failures = _PACKET_VALIDATOR.validate_packet(packet, packets_dir=repo_root / "raw" / "packets")
    if not schema_ok:
        decision = QueueDecision(False, "refused", "; ".join(schema_failures))
        _write_transition_audit(queue_root, source, None, from_state, to_state, dry_run, decision, packet_hash, packet_id)
        return decision

    if to_state == "dispatched":
        decision = validate_for_dispatch(packet, source, repo_root=repo_root, dry_run=dry_run)
        if not decision.allowed:
            _write_transition_audit(queue_root, source, None, from_state, to_state, dry_run, decision, packet_hash, packet_id)
            return decision

    destination = queue_root / to_state / source.name
    if destination.exists() and source.resolve() != destination.resolve():
        decision = QueueDecision(False, "refused", f"destination already exists: {destination}")
        _write_transition_audit(queue_root, source, destination, from_state, to_state, dry_run, decision, packet_hash, packet_id)
        return decision

    if dry_run:
        decision = QueueDecision(True, "dry_run", f"would move {source} to {destination}")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        tmp_destination = destination.with_name(f".{destination.name}.transition.tmp")
        source.replace(tmp_destination)
        tmp_destination.replace(destination)
        decision = QueueDecision(True, "moved", f"moved {source} to {destination}")

    _write_transition_audit(queue_root, source, destination, from_state, to_state, dry_run, decision, packet_hash, packet_id)
    return decision


def _write_transition_audit(
    queue_root: Path,
    source: Path,
    destination: Path | None,
    from_state: str,
    to_state: str,
    dry_run: bool,
    decision: QueueDecision,
    packet_hash: str | None,
    packet_id: Any = None,
) -> None:
    append_audit(
        queue_root,
        {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "from_state": from_state,
            "to_state": to_state,
            "dry_run": dry_run,
            "allowed": decision.allowed,
            "status": decision.status,
            "reason": decision.reason,
            "source": str(source),
            "destination": str(destination) if destination else None,
            "sha256": packet_hash,
        },
    )


def replay_audit(audit_path: Path) -> dict[str, Any]:
    """Replay audit events into logical latest states.

    `latest_states` includes accepted dry-run transitions because dry-run queue
    rehearsals are part of the governance audit trail. It is not a physical
    filesystem reconciliation report.
    """
    states: dict[str, str] = {}
    events = 0
    refused = 0
    dry_runs = 0
    for line in audit_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        events += 1
        packet_id = event.get("packet_id") or event.get("source")
        if event.get("dry_run"):
            dry_runs += 1
        if event.get("allowed"):
            states[str(packet_id)] = event.get("to_state")
        else:
            refused += 1
    return {
        "events": events,
        "accepted_transitions": len(states),
        "refused_events": refused,
        "dry_run_events": dry_runs,
        "latest_states": states,
    }


def _run_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage the governance packet queue")
    parser.add_argument("--queue-root", type=Path, default=DEFAULT_QUEUE_ROOT)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Create queue state directories")

    transition = subparsers.add_parser("transition", help="Validate and transition a packet")
    transition.add_argument("--packet", type=Path, required=True)
    transition.add_argument("--from-state", choices=QUEUE_STATES, required=True)
    transition.add_argument("--to-state", choices=QUEUE_STATES, required=True)
    transition.add_argument("--dry-run", action="store_true", help="Preview the transition; this is the default")
    transition.add_argument("--apply", action="store_true", help="Move the packet file after validation")

    replay = subparsers.add_parser("replay", help="Replay audit log into latest packet states")
    replay.add_argument("--audit", type=Path)

    args = parser.parse_args(argv)
    if args.command == "init":
        ensure_queue(args.queue_root)
        print(json.dumps({"status": "ok", "queue_root": str(args.queue_root), "states": list(QUEUE_STATES)}))
        return 0
    if args.command == "transition":
        decision = transition_packet(
            args.packet,
            args.from_state,
            args.to_state,
            queue_root=args.queue_root,
            repo_root=args.repo_root,
            dry_run=not args.apply,
        )
        print(json.dumps({"allowed": decision.allowed, "status": decision.status, "reason": decision.reason}, sort_keys=True))
        return 0 if decision.allowed else 1
    if args.command == "replay":
        audit_path = args.audit or _audit_path(args.queue_root)
        print(json.dumps(replay_audit(audit_path), sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(_run_cli())
