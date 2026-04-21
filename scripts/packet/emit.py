#!/usr/bin/env python3
"""
Packet emitter: helper to author SoM Stage 4 handoff packets.
Generates YAML packet with UUID and current timestamp.
"""
import argparse
import yaml
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, Optional, List


def emit_packet(
    prior_tier: int,
    prior_role: str,
    prior_model_id: str,
    prior_model_family: str,
    next_tier: int,
    artifacts: List[str],
    parent_packet_id: Optional[str] = None,
    standards_ref: str = "STANDARDS.md §Society of Minds (SoT)",
    runbook_ref: Optional[str] = None,
    fallback_ladder_ref: Optional[str] = None,
    governance: Optional[Dict[str, Any]] = None,
    packets_dir: Optional[Path] = None,
) -> str:
    """Emit a minimal or dispatch-ready packet YAML file. Returns path to written file."""
    packet_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    packet: Dict[str, Any] = {
        "packet_id": packet_id,
        "prior": {
            "tier": prior_tier,
            "role": prior_role,
            "model_id": prior_model_id,
            "model_family": prior_model_family,
            "timestamp": timestamp,
        },
        "next_tier": next_tier,
        "standards_ref": standards_ref,
    }

    if parent_packet_id:
        packet["parent_packet_id"] = parent_packet_id

    if artifacts:
        packet["artifacts"] = artifacts

    if runbook_ref:
        packet["runbook_ref"] = runbook_ref

    if fallback_ladder_ref:
        packet["fallback_ladder_ref"] = fallback_ladder_ref

    if governance is not None:
        packet["governance"] = governance

    if packets_dir is None:
        packets_dir = Path(__file__).parent.parent.parent / "raw" / "packets"
    packets_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = packets_dir / f"{date_str}-{packet_id}.yml"

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(packet, f, default_flow_style=False, sort_keys=False)

    return str(output_path)


def build_governance(
    issue_number: int,
    structured_plan_ref: str,
    validation_commands: List[str],
    review_artifacts: List[str],
    pii_mode: str = "none",
    dispatch_authorized: bool = False,
    execution_scope_ref: Optional[str] = None,
    fallback_log_ref: Optional[str] = None,
    dry_run_authorized: Optional[bool] = None,
) -> Dict[str, Any]:
    """Build a governance block dict for inclusion in a dispatch-ready packet."""
    gov: Dict[str, Any] = {
        "issue_number": issue_number,
        "structured_plan_ref": structured_plan_ref,
        "execution_scope_ref": execution_scope_ref,
        "validation_commands": validation_commands,
        "review_artifacts": review_artifacts,
        "fallback_log_ref": fallback_log_ref,
        "pii_mode": pii_mode,
        "dispatch_authorized": dispatch_authorized,
    }
    if dry_run_authorized is not None:
        gov["dry_run_authorized"] = dry_run_authorized
    return gov


def emit_dispatch_packet(
    prior_tier: int,
    prior_role: str,
    prior_model_id: str,
    prior_model_family: str,
    next_tier: int,
    artifacts: List[str],
    issue_number: int,
    structured_plan_ref: str,
    validation_commands: List[str],
    review_artifacts: List[str],
    pii_mode: str = "none",
    dispatch_authorized: bool = False,
    execution_scope_ref: Optional[str] = None,
    fallback_log_ref: Optional[str] = None,
    dry_run_authorized: Optional[bool] = None,
    parent_packet_id: Optional[str] = None,
    standards_ref: str = "STANDARDS.md §Society of Minds (SoT)",
    runbook_ref: Optional[str] = None,
    fallback_ladder_ref: Optional[str] = None,
    packets_dir: Optional[Path] = None,
) -> str:
    """Emit a dispatch-ready packet that includes a complete governance block."""
    governance = build_governance(
        issue_number=issue_number,
        structured_plan_ref=structured_plan_ref,
        validation_commands=validation_commands,
        review_artifacts=review_artifacts,
        pii_mode=pii_mode,
        dispatch_authorized=dispatch_authorized,
        execution_scope_ref=execution_scope_ref,
        fallback_log_ref=fallback_log_ref,
        dry_run_authorized=dry_run_authorized,
    )
    return emit_packet(
        prior_tier=prior_tier,
        prior_role=prior_role,
        prior_model_id=prior_model_id,
        prior_model_family=prior_model_family,
        next_tier=next_tier,
        artifacts=artifacts,
        parent_packet_id=parent_packet_id,
        standards_ref=standards_ref,
        runbook_ref=runbook_ref,
        fallback_ladder_ref=fallback_ladder_ref,
        governance=governance,
        packets_dir=packets_dir,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Emit a SoM Stage 4 handoff packet"
    )
    parser.add_argument("--prior-tier", type=int, required=True, help="Source tier (1-4)")
    parser.add_argument("--prior-role", required=True, help="Source role")
    parser.add_argument("--prior-model-id", required=True, help="Source model ID")
    parser.add_argument("--prior-model-family", required=True, help="Source model family")
    parser.add_argument("--next-tier", type=int, required=True, help="Destination tier (1-4)")
    parser.add_argument("--parent-packet-id", help="Parent packet UUID (for tier 1)")
    parser.add_argument("--artifact", action="append", default=[], help="Artifact path (repeatable)")
    parser.add_argument("--standards-ref", default="STANDARDS.md §Society of Minds (SoT)", help="Standards reference")
    parser.add_argument("--runbook-ref", help="Runbook reference")
    parser.add_argument("--fallback-ladder-ref", help="Fallback ladder reference")

    # Governance flags (all required together when any is provided)
    gov = parser.add_argument_group("governance (dispatch-ready packets)")
    gov.add_argument("--issue-number", type=int, help="GitHub issue number")
    gov.add_argument("--structured-plan-ref", help="Repo-relative path to structured plan JSON")
    gov.add_argument("--execution-scope-ref", help="Repo-relative path to execution scope JSON, or omit")
    gov.add_argument("--validation-command", action="append", default=[], metavar="CMD", help="Validation command (repeatable)")
    gov.add_argument("--review-artifact", action="append", default=[], metavar="PATH", help="Review artifact path (repeatable)")
    gov.add_argument("--pii-mode", choices=["none", "tagged", "detected", "lam_only"], default="none")
    gov.add_argument("--dispatch-authorized", action="store_true", help="Mark dispatch_authorized=true")
    gov.add_argument("--fallback-log-ref", help="Fallback log path under raw/model-fallbacks")
    gov.add_argument("--dry-run-authorized", action="store_true", help="Mark dry_run_authorized=true")

    args = parser.parse_args()

    governance = None
    governance_inputs = [
        args.issue_number is not None,
        args.structured_plan_ref is not None,
        args.execution_scope_ref is not None,
        bool(args.validation_command),
        bool(args.review_artifact),
        args.fallback_log_ref is not None,
        args.dispatch_authorized,
        args.dry_run_authorized,
        args.pii_mode != "none",
    ]
    if any(governance_inputs):
        if args.issue_number is None:
            parser.error("--issue-number is required when emitting governance metadata")
        if not args.structured_plan_ref:
            parser.error("--structured-plan-ref is required with --issue-number")
        if not args.validation_command:
            parser.error("--validation-command is required with --issue-number")
        if not args.review_artifact:
            parser.error("--review-artifact is required with --issue-number")
        governance = build_governance(
            issue_number=args.issue_number,
            structured_plan_ref=args.structured_plan_ref,
            validation_commands=args.validation_command,
            review_artifacts=args.review_artifact,
            pii_mode=args.pii_mode,
            dispatch_authorized=args.dispatch_authorized,
            execution_scope_ref=args.execution_scope_ref,
            fallback_log_ref=args.fallback_log_ref,
            dry_run_authorized=args.dry_run_authorized,
        )

    path = emit_packet(
        prior_tier=args.prior_tier,
        prior_role=args.prior_role,
        prior_model_id=args.prior_model_id,
        prior_model_family=args.prior_model_family,
        next_tier=args.next_tier,
        artifacts=args.artifact,
        parent_packet_id=args.parent_packet_id,
        standards_ref=args.standards_ref,
        runbook_ref=args.runbook_ref,
        fallback_ladder_ref=args.fallback_ladder_ref,
        governance=governance,
    )

    print(path)


if __name__ == "__main__":
    main()
