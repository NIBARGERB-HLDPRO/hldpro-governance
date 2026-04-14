#!/usr/bin/env python3
"""
Packet emitter: helper to author SoM Stage 4 handoff packets.
Generates YAML packet with UUID and current timestamp.
"""
import sys
import argparse
import yaml
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List


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
) -> str:
    """
    Emit a packet YAML file.
    Returns: path to written file
    """
    packet_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    packet = {
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

    # Determine output directory
    packets_dir = Path(__file__).parent.parent.parent / "raw" / "packets"
    packets_dir.mkdir(parents=True, exist_ok=True)

    # Use YYYY-MM-DD prefix + packet_id
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = packets_dir / f"{date_str}-{packet_id}.yml"

    # Write YAML
    with open(output_path, "w") as f:
        yaml.dump(packet, f, default_flow_style=False, sort_keys=False)

    return str(output_path)


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

    args = parser.parse_args()

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
    )

    print(path)


if __name__ == "__main__":
    main()
