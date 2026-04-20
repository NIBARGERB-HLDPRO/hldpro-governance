#!/usr/bin/env python3
"""No-secret Remote MCP operator connectivity preflight."""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import subprocess
import sys
import threading
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "som-client"))
from som_client import SomClient, SomClientConfig, SomClientError  # noqa: E402


LABEL = "com.hldpro.remote-mcp-monitor"
LAUNCHD_TEMPLATE = Path("launchd/com.hldpro.remote-mcp-monitor.plist")
LAUNCHD_INSTALL_PATH = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
LIVE_REQUIRED_GROUPS = (
    ("SOM_MCP_URL",),
    ("SOM_MCP_TOKEN", "SOM_REMOTE_MCP_JWT"),
    ("CF_ACCESS_CLIENT_ID",),
    ("CF_ACCESS_CLIENT_SECRET",),
)
MONITOR_REQUIRED_GROUPS = (
    ("SOM_REMOTE_MCP_IDENTITY_EMAIL",),
    ("SOM_REMOTE_MCP_IDENTITY_SUB",),
    ("SOM_REMOTE_MCP_AUDIT_DIR",),
    ("SOM_REMOTE_MCP_AUDIT_HMAC_KEY",),
    ("SOM_REMOTE_MCP_STDIO_PROOF_COMMAND",),
)


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "status": self.status, "detail": self.detail}


class _FixtureMcpHandler(BaseHTTPRequestHandler):
    server_version = "FixtureRemoteMCP/1"

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/mcp":
            self._write_json(404, {"error": "not found"})
            return
        if not self.headers.get("Authorization"):
            self._write_json(401, {"error": "missing auth"})
            return
        try:
            payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            self._write_json(400, {"error": "bad json"})
            return

        params = payload.get("params") if isinstance(payload, dict) else None
        tool = params.get("name") if isinstance(params, dict) else None
        if payload.get("method") != "tools.call" or tool != "som.ping":
            self._write_json(400, {"error": "unsupported tool"})
            return
        self._write_json(200, {"jsonrpc": "2.0", "id": payload.get("id"), "result": {"ok": True, "tool": "som.ping"}})

    def _write_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


@contextlib.contextmanager
def _fixture_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _FixtureMcpHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def _missing_groups(groups: Sequence[tuple[str, ...]]) -> list[str]:
    missing: list[str] = []
    for group in groups:
        if not any(os.environ.get(name) for name in group):
            missing.append(" or ".join(group))
    return missing


def _launchctl_loaded() -> bool:
    try:
        result = subprocess.run(["launchctl", "list"], check=False, capture_output=True, text=True)
    except FileNotFoundError:
        return False
    if result.returncode != 0:
        return False
    return LABEL in result.stdout


def _launchd_checks(root: Path) -> list[Check]:
    checks: list[Check] = []
    template = root / LAUNCHD_TEMPLATE
    if not template.is_file():
        return [Check("launchd-template-present", "fail", f"missing {LAUNCHD_TEMPLATE}")]

    text = template.read_text(encoding="utf-8")
    checks.append(Check("launchd-template-present", "pass", str(LAUNCHD_TEMPLATE)))
    checks.append(
        Check(
            "launchd-template-live-mode",
            "pass" if "<string>live</string>" in text else "fail",
            "template invokes live monitor mode" if "<string>live</string>" in text else "template does not invoke live mode",
        )
    )
    checks.append(
        Check(
            "launchd-installed",
            "pass" if LAUNCHD_INSTALL_PATH.is_file() else "warn",
            "installed in user LaunchAgents" if LAUNCHD_INSTALL_PATH.is_file() else "not installed in user LaunchAgents",
        )
    )
    launchd_loaded = _launchctl_loaded()
    checks.append(
        Check(
            "launchd-loaded",
            "pass" if launchd_loaded else "warn",
            "loaded in launchctl" if launchd_loaded else "not loaded in launchctl",
        )
    )
    return checks


def _call_fixture() -> Check:
    with _fixture_server() as base_url:
        client = SomClient(
            SomClientConfig(
                base_url=base_url,
                bearer_token="fixture-token",
                cf_access_client_id="fixture-client-id",
                cf_access_client_secret="fixture-client-secret",
                max_retries=0,
            )
        )
        result = client.ping()
    return Check(
        "som-ping-request-response",
        "pass" if result.get("ok") is True else "fail",
        "fixture som.ping returned a response" if result.get("ok") is True else "fixture som.ping response was malformed",
    )


def _call_live() -> tuple[Check, list[str]]:
    missing = _missing_groups(LIVE_REQUIRED_GROUPS)
    if missing:
        return Check("som-ping-request-response", "fail", "missing live configuration: " + ", ".join(missing)), missing
    try:
        result = SomClient.from_env().ping()
    except SomClientError as exc:
        return Check("som-ping-request-response", "fail", f"live som.ping failed: {exc.to_dict()['error']}"), []
    return Check(
        "som-ping-request-response",
        "pass" if isinstance(result, dict) else "fail",
        "live som.ping returned a response" if isinstance(result, dict) else "live som.ping response was malformed",
    ), []


def build_payload(mode: str, root: Path) -> tuple[dict[str, Any], int]:
    checks = _launchd_checks(root)
    missing_live = _missing_groups(LIVE_REQUIRED_GROUPS)
    missing_monitor = _missing_groups(MONITOR_REQUIRED_GROUPS)

    if mode == "fixture":
        checks.append(_call_fixture())
        ready = True
        exit_code = 0
    else:
        live_check, missing_from_call = _call_live()
        checks.append(live_check)
        missing_live = missing_from_call or missing_live
        ready = live_check.status == "pass"
        exit_code = 0 if ready else 2 if missing_live else 1

    blocking = [check for check in checks if check.status == "fail"]
    warnings = [check for check in checks if check.status == "warn"]
    if ready and not blocking:
        recommended_action = (
            "Fixture request/response is ready; run live preflight to prove current-machine Remote MCP."
            if mode == "fixture"
            else "Remote MCP request/response is ready."
        )
    else:
        recommended_action = "Configure missing live inputs, install/load launchd if desired, then rerun live preflight."
    payload = {
        "schema_version": 1,
        "mode": mode,
        "ready": ready and not blocking,
        "message_path": "som.ping",
        "checks": [check.to_dict() for check in checks],
        "missing_live_config": missing_live,
        "missing_monitor_config": missing_monitor,
        "warnings": [check.name for check in warnings],
        "recommended_action": recommended_action,
    }
    return payload, exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="No-secret Remote MCP operator connectivity preflight.")
    parser.add_argument("--mode", choices=("fixture", "live"), default="live")
    parser.add_argument("--json-output", type=Path, help="Optional path to write JSON output.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    payload, exit_code = build_payload(args.mode, Path.cwd())
    rendered = json.dumps(payload, indent=2) + "\n"
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
