#!/usr/bin/env python3
"""
SoM Stage 4 packet validator.
Enforces governance rules from STANDARDS.md §Society of Minds (SoT).
"""
import re
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Repo root relative to this file: scripts/packet/ -> repo root
_REPO_ROOT = Path(__file__).parent.parent.parent

PII_PATTERNS_PATH = _REPO_ROOT / "scripts" / "lam" / "pii-patterns.yml"

# Models whose tier-1 planning capability is below the governance floor.
# claude-sonnet-* and above are fine; haiku-* variants are not.
WEAK_TIER1_MODELS = {
    "claude-haiku-4-5",
    "claude-haiku-4-5-20251001",
    "claude-haiku-3",
    "claude-haiku-3-20240307",
}

# Codex/OpenAI models below the codex-spark floor.
# gpt-5.x and codex-spark-* are fine.
WEAK_CODEX_MODELS = {
    "gpt-4-turbo",
    "gpt-4o-mini",
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-0613",
}

# Roles that are allowed to produce PII-tagged artifacts.
_LAM_ROLES = {"worker-lam", "critic-lam"}

# Maximum chain depth for self-approval / parent-chain walks.
_MAX_CHAIN_DEPTH = 20


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_packet(path: Path) -> Optional[Dict[str, Any]]:
    """Load a YAML packet; return None if missing or malformed."""
    try:
        return yaml.safe_load(path.read_text())
    except Exception:
        return None


def _find_packet_file(packets_dir: Path, packet_id: str) -> Optional[Path]:
    """Locate a packet file by ID (supports YYYY-MM-DD-<id>.yml naming)."""
    for f in packets_dir.glob(f"*-{packet_id}.yml"):
        return f
    direct = packets_dir / f"{packet_id}.yml"
    if direct.exists():
        return direct
    return None


def _resolve_chain(packet: Dict[str, Any], packets_dir: Path) -> List[Dict[str, Any]]:
    """Walk parent_packet_id links backwards; return ordered list [packet, parent, ...].

    Stops on missing file, cycle, or _MAX_CHAIN_DEPTH exceeded.
    """
    chain: List[Dict[str, Any]] = [packet]
    visited: set = {packet.get("packet_id")}

    current = packet
    for _ in range(_MAX_CHAIN_DEPTH - 1):
        parent_id = current.get("parent_packet_id")
        if not parent_id or parent_id in visited:
            break
        parent_file = _find_packet_file(packets_dir, parent_id)
        if parent_file is None:
            break
        parent = _load_packet(parent_file)
        if parent is None:
            break
        visited.add(parent_id)
        chain.append(parent)
        current = parent

    return chain


def load_pii_patterns() -> List[re.Pattern]:
    """Load and compile PII patterns from pii-patterns.yml."""
    if not PII_PATTERNS_PATH.exists():
        return []
    try:
        data = yaml.safe_load(PII_PATTERNS_PATH.read_text())
        return [
            re.compile(p, re.IGNORECASE)
            for p in (data or {}).get("patterns", [])
        ]
    except Exception:
        return []


# Compiled once at module load.
_COMPILED_PII_PATTERNS = load_pii_patterns()


# ---------------------------------------------------------------------------
# Individual validators
# ---------------------------------------------------------------------------

def validate_dual_planner(
    packet: Dict[str, Any],
    packets_dir: Optional[Path] = None,
) -> Tuple[bool, Optional[str]]:
    """Enforce cross-family independence for tier-1 dual-planner packets.

    When prior.tier == 1 AND parent_packet_id is present, the parent planner
    must come from a different model_family than the current planner.
    """
    prior = packet.get("prior", {})
    if prior.get("tier") != 1:
        return True, None

    parent_id = packet.get("parent_packet_id")
    if not parent_id:
        return True, None

    if packets_dir is None:
        packets_dir = _REPO_ROOT / "raw" / "packets"

    parent_file = _find_packet_file(packets_dir, str(parent_id))
    if parent_file is None:
        return (
            True,
            f"parent packet {parent_id} not found — assumed pre-bootstrap; cross-family check skipped",
        )

    parent = _load_packet(parent_file)
    if parent is None:
        return True, f"parent packet {parent_id} unreadable — cross-family check skipped"

    current_family = prior.get("model_family")
    parent_family = parent.get("prior", {}).get("model_family")

    if current_family and parent_family and current_family == parent_family:
        return (
            False,
            f"cross-family independence violated: parent and current planner share model_family {current_family}",
        )

    return True, None


def validate_no_self_approval(
    packet: Dict[str, Any],
    packets_dir: Optional[Path] = None,
) -> Tuple[bool, Optional[str]]:
    """Refuse if any consecutive pair in the parent chain shares model_id across different roles."""
    if packets_dir is None:
        packets_dir = _REPO_ROOT / "raw" / "packets"

    chain = _resolve_chain(packet, packets_dir)

    for i in range(len(chain) - 1):
        current_p = chain[i]
        parent_p = chain[i + 1]
        c_prior = current_p.get("prior", {})
        p_prior = parent_p.get("prior", {})
        c_model = c_prior.get("model_id")
        p_model = p_prior.get("model_id")
        c_role = c_prior.get("role")
        p_role = p_prior.get("role")
        if (
            c_model
            and p_model
            and c_model == p_model
            and c_role != p_role
        ):
            return (
                False,
                f"self-approval detected: model {c_model} appears as both {p_role} and {c_role} in consecutive chain positions",
            )

    return True, None


def validate_planning_floor(packet: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Refuse tier-1 packets whose model is below the planning floor."""
    prior = packet.get("prior", {})
    if prior.get("tier") != 1:
        return True, None

    model_id = prior.get("model_id", "")
    if model_id in WEAK_TIER1_MODELS or model_id in WEAK_CODEX_MODELS:
        return (
            False,
            f"planning floor violation: model {model_id} is below the tier-1 planning floor (STANDARDS.md §SoM)",
        )

    return True, None


def validate_pii_floor(packet: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Refuse if PII artifacts appear outside LAM-role packets, or if the pattern file is absent."""
    if not PII_PATTERNS_PATH.exists():
        return (
            False,
            "PII floor unenforceable: scripts/lam/pii-patterns.yml not found in repo — validator cannot determine if artifacts contain PII",
        )

    patterns = _COMPILED_PII_PATTERNS
    if not patterns:
        return (
            False,
            "PII floor unenforceable: scripts/lam/pii-patterns.yml loaded but contains no patterns",
        )

    prior = packet.get("prior", {})
    role = prior.get("role", "")
    artifacts = packet.get("artifacts", [])

    for artifact in artifacts:
        artifact_str = str(artifact)
        for pat in patterns:
            if pat.search(artifact_str):
                if role not in _LAM_ROLES:
                    return (
                        False,
                        f"PII artifact detected in non-LAM packet: artifact '{artifact_str}' matches PII pattern; role '{role}' is not in {_LAM_ROLES}",
                    )
                break  # artifact matched but role is LAM — ok, check next artifact

    return True, None


# ---------------------------------------------------------------------------
# Top-level validate_packet
# ---------------------------------------------------------------------------

def validate_packet(
    packet: Dict[str, Any],
    packets_dir: Optional[Path] = None,
) -> Tuple[bool, List[str]]:
    """Run all validators against a packet dict.

    Returns (all_passed, list_of_failure_reasons).
    """
    if packets_dir is None:
        packets_dir = _REPO_ROOT / "raw" / "packets"

    failures: List[str] = []

    checks = [
        ("dual_planner", validate_dual_planner(packet, packets_dir)),
        ("no_self_approval", validate_no_self_approval(packet, packets_dir)),
        ("planning_floor", validate_planning_floor(packet)),
        ("pii_floor", validate_pii_floor(packet)),
    ]

    for name, (passed, reason) in checks:
        if not passed:
            failures.append(f"[{name}] {reason}")

    return (len(failures) == 0, failures)
