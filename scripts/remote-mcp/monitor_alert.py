#!/usr/bin/env python3
"""Payload-safe alert/report formatter for Remote MCP monitor results."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Sequence


DENY_PATTERNS = (
    ("raw-ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("bearer-token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{10,}", re.IGNORECASE)),
    ("cloudflare-access-token", re.compile(r"\bCF-Access\b", re.IGNORECASE)),
    ("jwt-fragment", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}", re.IGNORECASE)),
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _contains_sensitive(text: str) -> list[str]:
    return [label for label, pattern in DENY_PATTERNS if pattern.search(text)]


def _safe_text(value: Any, *, fallback: str = "not provided") -> tuple[str, list[str]]:
    text = str(value if value is not None else fallback)
    findings = _contains_sensitive(text)
    if findings:
        return "[redacted-sensitive-detail]", findings
    return text, []


def _load_payload(path: Optional[Path]) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8") if path else sys.stdin.read()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"monitor payload is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("monitor payload must be a JSON object")
    return payload


def build_alert(payload: dict[str, Any], *, generated_at: Optional[str] = None) -> dict[str, Any]:
    mode, mode_findings = _safe_text(payload.get("mode"), fallback="unknown")
    evidence_dir, evidence_findings = _safe_text(payload.get("evidence_dir"), fallback="")
    raw_results = payload.get("results")
    if not isinstance(raw_results, list):
        raise ValueError("monitor payload must include results array")

    checks: list[dict[str, str]] = []
    sensitive_findings: list[str] = []
    sensitive_findings.extend(f"mode:{label}" for label in mode_findings)
    sensitive_findings.extend(f"evidence_dir:{label}" for label in evidence_findings)

    for index, item in enumerate(raw_results):
        if not isinstance(item, dict):
            raise ValueError(f"results[{index}] must be an object")
        name, name_findings = _safe_text(item.get("name"), fallback=f"check-{index}")
        status, status_findings = _safe_text(item.get("status"), fallback="unknown")
        detail, detail_findings = _safe_text(item.get("detail"), fallback="")
        sensitive_findings.extend(f"{name}:name:{label}" for label in name_findings)
        sensitive_findings.extend(f"{name}:status:{label}" for label in status_findings)
        sensitive_findings.extend(f"{name}:detail:{label}" for label in detail_findings)
        checks.append({"name": name, "status": status, "detail": detail})

    failed = [check for check in checks if check["status"] == "fail"]
    unknown = [check for check in checks if check["status"] not in {"pass", "skip", "fail"}]
    skipped = [check for check in checks if check["status"] == "skip"]
    health = "degraded" if failed or unknown or sensitive_findings else "healthy"
    recommended_action = (
        "Restrict or disable Remote MCP exposure until failed checks pass and evidence is payload-safe."
        if health == "degraded"
        else "No action required."
    )

    return {
        "schema_version": 1,
        "generated_at": generated_at or _now(),
        "service": "remote-mcp",
        "monitor": "live_health_monitor",
        "mode": mode,
        "health": health,
        "summary": {
            "total": len(checks),
            "passed": len([check for check in checks if check["status"] == "pass"]),
            "failed": len(failed),
            "skipped": len(skipped),
            "unknown": len(unknown),
            "sensitive_findings": len(sensitive_findings),
        },
        "failed_checks": failed,
        "unknown_checks": unknown,
        "sensitive_findings": sensitive_findings,
        "evidence_dir": evidence_dir,
        "recommended_action": recommended_action,
    }


def render_markdown(alert: dict[str, Any]) -> str:
    lines = [
        "# Remote MCP Monitor Alert",
        "",
        f"Generated: {alert['generated_at']}",
        f"Health: {alert['health'].upper()}",
        f"Mode: {alert['mode']}",
        f"Evidence: {alert['evidence_dir'] or 'not recorded'}",
        "",
        "## Summary",
        "",
        f"- total checks: {alert['summary']['total']}",
        f"- passed: {alert['summary']['passed']}",
        f"- failed: {alert['summary']['failed']}",
        f"- skipped: {alert['summary']['skipped']}",
        f"- unknown: {alert['summary']['unknown']}",
        f"- sensitive findings: {alert['summary']['sensitive_findings']}",
        "",
        "## Action",
        "",
        alert["recommended_action"],
    ]
    if alert["failed_checks"]:
        lines.extend(["", "## Failed Checks", ""])
        for check in alert["failed_checks"]:
            lines.append(f"- {check['name']}: {check['detail']}")
    if alert["sensitive_findings"]:
        lines.extend(["", "## Sensitive Material", ""])
        lines.append("Sensitive detail was redacted from the alert output.")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a payload-safe Remote MCP monitor alert.")
    parser.add_argument("--input", type=Path, help="Monitor JSON input. Defaults to stdin.")
    parser.add_argument("--json-output", type=Path, help="Write alert JSON to this path.")
    parser.add_argument("--markdown-output", type=Path, help="Write alert Markdown to this path.")
    parser.add_argument("--fail-on-degraded", action="store_true", help="Exit 1 when alert health is degraded.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        alert = build_alert(_load_payload(args.input))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(alert, indent=2) + "\n", encoding="utf-8")
    else:
        print(json.dumps(alert, indent=2))

    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown(alert), encoding="utf-8")

    return 1 if args.fail_on_degraded and alert["health"] != "healthy" else 0


if __name__ == "__main__":
    raise SystemExit(main())
