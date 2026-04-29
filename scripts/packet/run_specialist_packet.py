#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from hldprosim.engine import SimulationEngine
from hldprosim.personas import PersonaLoader
from hldprosim.providers import CodexCliProvider
from hldprosim.runner import Runner

from scripts.packet.emit import emit_dispatch_packet
from scripts.packet.validate import validate_packet


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "governance-specialist-output.schema.json"


def _repo_ref(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"packet must be a YAML object: {path}")
    return payload


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"schema must be a JSON object: {path}")
    return payload


def _specialist_prompt(event: dict[str, Any], persona: dict[str, Any]) -> tuple[str, str]:
    system = "\n".join(
        [
            f"You are {persona.get('name', persona.get('persona_id', 'specialist'))}.",
            str(persona.get("prompt_context", "")),
            "Accept only the supplied structured packet as scope.",
            "Return only JSON that matches the provided output schema.",
        ]
    ).strip()
    user = json.dumps(event, indent=2, sort_keys=True)
    return system, user


def _resolve_model_settings(
    persona: dict[str, Any],
    model_override: str | None,
    effort_override: str | None,
) -> tuple[str, str]:
    model = model_override or str(persona.get("model_id") or "gpt-5.4")
    effort = effort_override or str(persona.get("reasoning_effort") or "medium")
    return model, effort


def run_specialist_packet(
    *,
    packet_path: Path,
    persona_id: str,
    output_root: Path,
    model: str | None = None,
    effort: str | None = None,
    dry_run: bool = False,
) -> tuple[Path, Path]:
    packet = _load_yaml(packet_path)
    passed, failures = validate_packet(packet)
    if not passed:
        raise ValueError("; ".join(failures))

    output_schema = _load_json(OUTPUT_SCHEMA_PATH)
    Draft202012Validator.check_schema(output_schema)

    loader = PersonaLoader.from_package(local_dir=REPO_ROOT / "sim-personas" / "local")
    persona = loader.load(persona_id)
    model_name, effort_name = _resolve_model_settings(persona, model, effort)
    provider = CodexCliProvider(model=model_name, effort=effort_name)
    engine = SimulationEngine(
        provider=provider,
        persona_loader=loader,
        prompt_template=_specialist_prompt,
        outcome_schema=output_schema,
    )
    runner = Runner(max_workers=1)

    if dry_run:
        outcome = {
            "schema_version": "governance-specialist-output.v1",
            "specialist_role": persona_id,
            "packet_id": str(packet["packet_id"]),
            "issue_number": packet.get("governance", {}).get("issue_number"),
            "verdict": "accepted",
            "summary": "dry-run",
            "artifact_refs": [str(packet_path)],
            "findings": [],
            "validation_commands": packet.get("governance", {}).get("validation_commands", []),
        }
    else:
        outcome = runner.run_n(engine, packet, persona_id, 1)[0]

    errors = sorted(Draft202012Validator(output_schema).iter_errors(outcome), key=lambda err: list(err.path))
    if errors:
        raise ValueError("; ".join(f"output schema: {err.message}" for err in errors))

    output_root.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    result_path = output_root / f"{ts}-{persona_id}-result.json"
    result_path.write_text(json.dumps(outcome, indent=2) + "\n", encoding="utf-8")

    gov = packet.get("governance") or {}
    prior_tier = int(packet["next_tier"])
    next_tier = prior_tier + 1 if prior_tier < 4 else 4
    outbound_packet = emit_dispatch_packet(
        prior_tier=prior_tier,
        prior_role="reviewer",
        prior_model_id=model_name,
        prior_model_family="openai",
        next_tier=next_tier,
        artifacts=[_repo_ref(result_path)],
        issue_number=int(gov["issue_number"]),
        structured_plan_ref=str(gov["structured_plan_ref"]),
        validation_commands=list(gov.get("validation_commands") or []),
        review_artifacts=list(gov.get("review_artifacts") or [_repo_ref(result_path)]),
        pii_mode=str(gov.get("pii_mode") or "none"),
        dispatch_authorized=bool(gov.get("dispatch_authorized", False)),
        execution_scope_ref=gov.get("execution_scope_ref"),
        fallback_log_ref=gov.get("fallback_log_ref"),
        dry_run_authorized=True if dry_run else gov.get("dry_run_authorized"),
        parent_packet_id=str(packet["packet_id"]),
        packets_dir=output_root,
    )
    return result_path, Path(outbound_packet)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a governance specialist against a structured packet.")
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--persona-id", required=True)
    parser.add_argument("--output-root", default=REPO_ROOT / "raw" / "packets" / "outbound", type=Path)
    parser.add_argument("--model")
    parser.add_argument("--effort")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        result_path, outbound_path = run_specialist_packet(
            packet_path=args.packet,
            persona_id=args.persona_id,
            output_root=args.output_root,
            model=args.model,
            effort=args.effort,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"result_path": str(result_path), "outbound_packet": str(outbound_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
