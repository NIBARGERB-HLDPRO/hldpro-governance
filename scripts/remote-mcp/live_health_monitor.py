#!/usr/bin/env python3
"""
Recurring Remote MCP live health and audit monitor.

The monitor composes the Stage D proof runner so scheduled checks exercise the
same authenticated smoke, negative security, strict audit, and tamper-negative
paths used for the final live proof. In unconfigured CI it runs fixture mode so
the harness stays continuously tested without requiring production secrets.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional, Sequence

import stage_d_smoke


LIVE_MARKER_ENVS = (
    "SOM_MCP_URL",
    "SOM_MCP_TOKEN",
    "SOM_REMOTE_MCP_JWT",
    "SOM_REMOTE_MCP_AUDIT_DIR",
    "SOM_REMOTE_MCP_STDIO_PROOF_COMMAND",
    "CF_ACCESS_CLIENT_ID",
    "CF_ACCESS_CLIENT_SECRET",
)

EVIDENCE_DENY_PATTERNS = (
    ("raw-ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("bearer-token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE)),
    ("cloudflare-access-token", re.compile(r"\bCF-Access\b", re.IGNORECASE)),
    ("jwt-fragment", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}", re.IGNORECASE)),
)


def _env_has_live_markers() -> bool:
    return any(os.environ.get(name) for name in LIVE_MARKER_ENVS)


def _scan_evidence_dir(evidence_dir: Path) -> stage_d_smoke.ProofResult:
    if not evidence_dir.exists():
        return stage_d_smoke.ProofResult(
            "evidence-safety-scan",
            "fail",
            f"evidence directory does not exist: {evidence_dir}",
        )
    if not evidence_dir.is_dir():
        return stage_d_smoke.ProofResult(
            "evidence-safety-scan",
            "fail",
            f"evidence path is not a directory: {evidence_dir}",
        )

    findings: list[str] = []
    for path in sorted(evidence_dir.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"{path.name}: non-utf8 evidence file")
            continue
        for label, pattern in EVIDENCE_DENY_PATTERNS:
            if pattern.search(text):
                findings.append(f"{path.name}: {label}")

    if findings:
        return stage_d_smoke.ProofResult(
            "evidence-safety-scan",
            "fail",
            "; ".join(findings),
        )
    return stage_d_smoke.ProofResult(
        "evidence-safety-scan",
        "pass",
        "no raw PII, bearer tokens, Cloudflare Access tokens, or JWT fragments found",
    )


def _stage_d_args(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        url=args.url,
        path=args.path,
        token=args.token,
        identity_email=args.identity_email,
        identity_sub=args.identity_sub,
        audit_dir=args.audit_dir,
        audit_hmac_key=args.audit_hmac_key,
        stdio_proof_command=args.stdio_proof_command,
        timeout_sec=args.timeout_sec,
        fixture=True,
        fixture_evidence_dir=args.fixture_evidence_dir,
        json=args.json,
    )


def _run_fixture(args: argparse.Namespace) -> tuple[list[stage_d_smoke.ProofResult], str]:
    results, evidence_dir = stage_d_smoke.run_fixture(_stage_d_args(args))
    results.append(_scan_evidence_dir(evidence_dir))
    return results, str(evidence_dir)


def _run_live(args: argparse.Namespace) -> tuple[list[stage_d_smoke.ProofResult], str]:
    config = stage_d_smoke.StageDConfig.from_env(_stage_d_args(args))
    missing = config.validate_live()
    if missing:
        raise ValueError("missing required live monitor configuration: " + ", ".join(missing))
    results = stage_d_smoke.run_stage_d(config)
    if config.audit_dir is None:
        results.append(stage_d_smoke.ProofResult("evidence-safety-scan", "fail", "audit directory is not configured"))
        return results, ""
    results.append(_scan_evidence_dir(config.audit_dir))
    return results, str(config.audit_dir)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the recurring Remote MCP health monitor.")
    parser.add_argument(
        "--mode",
        choices=("auto", "fixture", "live"),
        default=os.environ.get("SOM_REMOTE_MCP_MONITOR_MODE", "auto"),
        help="Monitor mode. auto uses live when live env markers are present; otherwise fixture.",
    )
    parser.add_argument("--url", help="Remote MCP bridge base URL. Defaults to SOM_MCP_URL.")
    parser.add_argument("--path", help=f"Remote MCP call path. Defaults to {stage_d_smoke.DEFAULT_PROOF_PATH}.")
    parser.add_argument("--token", help="Inner bridge token. Defaults to SOM_MCP_TOKEN or SOM_REMOTE_MCP_JWT.")
    parser.add_argument("--identity-email", help="Expected authenticated email header for direct bridge tests.")
    parser.add_argument("--identity-sub", help="Expected authenticated subject header for direct bridge tests.")
    parser.add_argument("--audit-dir", help="Directory containing copied remote audit JSONL files.")
    parser.add_argument("--audit-hmac-key", help="HMAC key for strict audit verification.")
    parser.add_argument("--stdio-proof-command", help="Command proving local stdio MCP still works after tunnel stop.")
    parser.add_argument("--timeout-sec", type=float, default=stage_d_smoke.DEFAULT_TIMEOUT_SEC)
    parser.add_argument("--fixture-evidence-dir", help="Directory to receive fixture audit evidence.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable result JSON.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    mode = args.mode
    if mode == "auto":
        mode = "live" if _env_has_live_markers() else "fixture"

    try:
        if mode == "live":
            results, evidence_dir = _run_live(args)
        else:
            results, evidence_dir = _run_fixture(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    payload = {
        "mode": mode,
        "results": [result.to_dict() for result in results],
        "evidence_dir": evidence_dir,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for result in results:
            print(f"{result.status.upper()} {result.name}: {result.detail}")
        if evidence_dir:
            print(f"EVIDENCE {evidence_dir}")

    return 0 if all(result.status in {"pass", "skip"} for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
