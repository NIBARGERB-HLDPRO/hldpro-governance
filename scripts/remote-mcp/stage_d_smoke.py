#!/usr/bin/env python3
"""
Stage D remote smoke and security proof runner for hldpro-governance#109/#364.

The default mode targets a live Remote MCP Bridge and requires environment
configuration. `--fixture` starts a local in-process bridge-shaped HTTP server
so the proof harness itself remains CI-testable without live Cloudflare secrets.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple

import verify_audit


DEFAULT_TIMEOUT_SEC = 8.0
DEFAULT_PROOF_PATH = "/mcp/call"
ZERO_HASH = "0" * 64


@dataclass
class ProofResult:
    name: str
    status: str
    detail: str

    def to_dict(self) -> Dict[str, str]:
        return {"name": self.name, "status": self.status, "detail": self.detail}


@dataclass
class StageDConfig:
    base_url: str
    proof_path: str
    token: str
    identity_email: str
    identity_sub: str
    cf_access_client_id: str
    cf_access_client_secret: str
    audit_dir: Optional[Path]
    audit_hmac_key: Optional[str]
    timeout_sec: float
    require_audit: bool
    stdio_proof_command: Optional[str]

    @classmethod
    def from_env(cls, args: argparse.Namespace) -> "StageDConfig":
        base_url = args.url or os.environ.get("SOM_MCP_URL", "")
        token = args.token or os.environ.get("SOM_MCP_TOKEN", "") or os.environ.get("SOM_REMOTE_MCP_JWT", "")
        audit_dir_raw = args.audit_dir or os.environ.get("SOM_REMOTE_MCP_AUDIT_DIR")
        return cls(
            base_url=base_url.rstrip("/"),
            proof_path=args.path or os.environ.get("SOM_REMOTE_MCP_PROOF_PATH", DEFAULT_PROOF_PATH),
            token=token,
            identity_email=args.identity_email or os.environ.get("SOM_REMOTE_MCP_IDENTITY_EMAIL", ""),
            identity_sub=args.identity_sub or os.environ.get("SOM_REMOTE_MCP_IDENTITY_SUB", ""),
            cf_access_client_id=os.environ.get("CF_ACCESS_CLIENT_ID", ""),
            cf_access_client_secret=os.environ.get("CF_ACCESS_CLIENT_SECRET", ""),
            audit_dir=Path(audit_dir_raw) if audit_dir_raw else None,
            audit_hmac_key=args.audit_hmac_key or os.environ.get("SOM_REMOTE_MCP_AUDIT_HMAC_KEY"),
            timeout_sec=args.timeout_sec,
            require_audit=True,
            stdio_proof_command=args.stdio_proof_command or os.environ.get("SOM_REMOTE_MCP_STDIO_PROOF_COMMAND"),
        )

    def validate_live(self) -> list[str]:
        missing = []
        for label, value in [
            ("SOM_MCP_URL", self.base_url),
            ("SOM_MCP_TOKEN or SOM_REMOTE_MCP_JWT", self.token),
            ("SOM_REMOTE_MCP_IDENTITY_EMAIL", self.identity_email),
            ("SOM_REMOTE_MCP_IDENTITY_SUB", self.identity_sub),
        ]:
            if not value:
                missing.append(label)
        if self.require_audit and self.audit_dir is None:
            missing.append("SOM_REMOTE_MCP_AUDIT_DIR or --audit-dir")
        if self.require_audit and not self.audit_hmac_key:
            missing.append("SOM_REMOTE_MCP_AUDIT_HMAC_KEY or --audit-hmac-key")
        if self.stdio_proof_command is None:
            missing.append("SOM_REMOTE_MCP_STDIO_PROOF_COMMAND or --stdio-proof-command")
        return missing


def _safe_json_response(error: urllib.error.HTTPError) -> Dict[str, Any]:
    try:
        raw = error.read()
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return {}


def _request(
    config: StageDConfig,
    *,
    tool: str,
    arguments: Dict[str, Any],
    auth: bool = True,
    body_extra: Optional[Dict[str, Any]] = None,
    headers_extra: Optional[Dict[str, str]] = None,
) -> Tuple[int, Dict[str, Any]]:
    body = {"tool": tool, "arguments": arguments}
    if body_extra:
        body.update(body_extra)

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if auth:
        headers["Authorization"] = f"Bearer {config.token}"
        headers["Cf-Access-Jwt-Assertion"] = config.token
        headers["Cf-Access-Authenticated-User-Email"] = config.identity_email
        headers["Cf-Access-Authenticated-User-Id"] = config.identity_sub
        if config.cf_access_client_id and config.cf_access_client_secret:
            headers["Cf-Access-Client-Id"] = config.cf_access_client_id
            headers["Cf-Access-Client-Secret"] = config.cf_access_client_secret
    if headers_extra:
        headers.update(headers_extra)

    request = urllib.request.Request(
        url=f"{config.base_url}{config.proof_path}",
        data=json.dumps(body, separators=(",", ":")).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.timeout_sec) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return response.status, payload
    except urllib.error.HTTPError as error:
        return error.code, _safe_json_response(error)


def _expect(name: str, condition: bool, detail: str) -> ProofResult:
    return ProofResult(name=name, status="pass" if condition else "fail", detail=detail)


def _verify_audit_valid(config: StageDConfig) -> ProofResult:
    if config.audit_dir is None:
        return ProofResult("audit-valid", "fail", "audit directory is not configured")
    success, errors = verify_audit.verify_audit_dir(
        config.audit_dir,
        hmac_key=config.audit_hmac_key,
        require_hmac_key=config.audit_hmac_key is not None,
    )
    return _expect("audit-valid", success, "; ".join(errors) or "valid audit chain")


def _verify_audit_tamper_fails(config: StageDConfig) -> ProofResult:
    if config.audit_dir is None or not config.audit_dir.exists():
        return ProofResult("audit-tamper-negative", "fail", "audit directory is absent")
    with tempfile.TemporaryDirectory() as tmpdir:
        copied = Path(tmpdir) / "remote-mcp-audit"
        shutil.copytree(config.audit_dir, copied)
        jsonl_files = sorted(copied.glob("*.jsonl"))
        if not jsonl_files:
            return ProofResult("audit-tamper-negative", "fail", "no audit jsonl files to tamper")
        first = jsonl_files[0]
        rows = [json.loads(line) for line in first.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not rows:
            return ProofResult("audit-tamper-negative", "fail", "audit jsonl file is empty")
        rows[0]["seq"] = 999999
        first.write_text("\n".join(json.dumps(row, separators=(",", ":")) for row in rows) + "\n", encoding="utf-8")
        success, errors = verify_audit.verify_audit_dir(
            copied,
            hmac_key=config.audit_hmac_key,
            require_hmac_key=config.audit_hmac_key is not None,
        )
        return _expect(
            "audit-tamper-negative",
            not success,
            "; ".join(errors) or "tamper rejected",
        )


def _run_stdio_proof(config: StageDConfig) -> ProofResult:
    if not config.stdio_proof_command:
        return ProofResult("stdio-after-tunnel-stop", "fail", "stdio proof command is not configured")
    code = os.system(config.stdio_proof_command)
    return _expect(
        "stdio-after-tunnel-stop",
        code == 0,
        f"command exited with {code}",
    )


def run_stage_d(config: StageDConfig) -> list[ProofResult]:
    results: list[ProofResult] = []

    status, payload = _request(config, tool="som.ping", arguments={})
    results.append(_expect("authenticated-ping", status == 200, f"status={status} body_keys={sorted(payload.keys())}"))

    status, _ = _request(config, tool="som.ping", arguments={}, auth=False)
    results.append(_expect("anonymous-rejected", status in {400, 401, 403}, f"status={status}"))

    status, _ = _request(
        config,
        tool="som.ping",
        arguments={},
        body_extra={"origin": "local"},
        headers_extra={"Origin": "local"},
    )
    results.append(_expect("origin-spoof-non-authoritative", status in {400, 401, 403}, f"status={status}"))

    status, _ = _request(
        config,
        tool="som.handoff",
        arguments={"packet": {"prompt": "patient SSN 123-45-6789"}},
    )
    results.append(_expect("pii-handoff-rejected", status in {400, 401, 403}, f"status={status}"))

    status, _ = _request(config, tool="lam.scrub_pii", arguments={"text": "ssn 123-45-6789"})
    results.append(_expect("scrub-pii-remote-rejected", status in {400, 401, 403, 404}, f"status={status}"))

    if config.require_audit or (config.audit_dir is not None and config.audit_dir.exists()):
        results.append(_verify_audit_valid(config))
        results.append(_verify_audit_tamper_fails(config))
    else:
        results.append(ProofResult("audit-valid", "skip", "audit directory not configured"))
        results.append(ProofResult("audit-tamper-negative", "skip", "audit directory not configured"))

    if config.stdio_proof_command:
        results.append(_run_stdio_proof(config))
    else:
        results.append(ProofResult("stdio-after-tunnel-stop", "skip", "stdio proof command not configured"))

    return results


def _write_fixture_entry(
    audit_dir: Path,
    *,
    seq: int,
    prev_hash: str,
    principal: str,
    session_jti: str,
    tool: str,
    arguments: Dict[str, Any],
    status: str,
    reject_reason: str,
    hmac_key: str,
) -> str:
    log_path = audit_dir / "2026-04-19.jsonl"
    entry = {
        "ts": "2026-04-19T00:00:00.000Z",
        "seq": seq,
        "prev_hash": prev_hash,
        "principal": principal,
        "session_jti": session_jti,
        "tool": tool,
        "args_hmac": verify_audit.compute_entry_hmac({"tool": tool, "arguments": arguments}, hmac_key),
        "status": status,
        "reject_reason": reject_reason,
        "latency_ms": 1,
        "entry_hmac": "",
    }
    entry["entry_hmac"] = verify_audit.compute_entry_hmac(entry, hmac_key)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, separators=(",", ":")) + "\n")

    rows = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    manifest = {
        "first_hash": verify_audit.compute_entry_hash(rows[0]),
        "last_hash": verify_audit.compute_entry_hash(rows[-1]),
        "entry_count": len(rows),
        "sha256_of_file": verify_audit.compute_sha256(log_path.read_bytes()),
    }
    log_path.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, separators=(",", ":")),
        encoding="utf-8",
    )
    return verify_audit.compute_entry_hash(entry)


def _build_fixture_server(audit_dir: Path, hmac_key: str) -> ThreadingHTTPServer:
    audit_dir.mkdir(parents=True, exist_ok=True)
    state = {"seq": 0, "prev_hash": ZERO_HASH}

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            tool = payload.get("tool", "")
            authed = bool(
                self.headers.get("Cf-Access-Authenticated-User-Email")
                and self.headers.get("Cf-Access-Authenticated-User-Id")
                and self.headers.get("Cf-Access-Jwt-Assertion")
            )
            status = 200
            body: Dict[str, Any] = {"status": "ok", "result": [{"type": "json", "json": {"ok": True}}]}
            reject_reason = ""
            if not authed:
                status = 401
                reject_reason = "missing_identity"
            elif payload.get("origin") or self.headers.get("Origin") == "local":
                status = 400
                reject_reason = "caller_origin_override_rejected"
            elif tool == "lam.scrub_pii":
                status = 400
                reject_reason = "remote_tool_forbidden"
            elif "123-45-6789" in json.dumps(payload):
                status = 400
                reject_reason = "pii_detected"
            if reject_reason:
                body = {"status": "rejected", "reason": reject_reason}
            state["prev_hash"] = _write_fixture_entry(
                audit_dir,
                seq=state["seq"],
                prev_hash=state["prev_hash"],
                principal=self.headers.get("Cf-Access-Authenticated-User-Id", "unauthenticated"),
                session_jti="fixture-jti",
                tool=tool or "unknown",
                arguments=payload.get("arguments", {}),
                status="ok" if status == 200 else "rejected",
                reject_reason=reject_reason,
                hmac_key=hmac_key,
            )
            state["seq"] += 1
            encoded = json.dumps(body, separators=(",", ":")).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def log_message(self, format: str, *args: Any) -> None:
            return

    return ThreadingHTTPServer(("127.0.0.1", 0), Handler)


def run_fixture(args: argparse.Namespace) -> tuple[list[ProofResult], Path]:
    tmpdir = tempfile.TemporaryDirectory()
    # Keep the directory alive by attaching it to the returned path object owner.
    audit_dir = Path(tmpdir.name) / "remote-mcp-audit"
    hmac_key = "fixture-audit-key"
    server = _build_fixture_server(audit_dir, hmac_key)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        config = StageDConfig(
            base_url=f"http://127.0.0.1:{server.server_port}",
            proof_path=DEFAULT_PROOF_PATH,
            token="fixture-token",
            identity_email="operator@example.invalid",
            identity_sub="fixture-user",
            cf_access_client_id="",
            cf_access_client_secret="",
            audit_dir=audit_dir,
            audit_hmac_key=hmac_key,
            timeout_sec=args.timeout_sec,
            require_audit=True,
            stdio_proof_command=None,
        )
        results = run_stage_d(config)
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()
    # Materialize copied evidence for callers before temp cleanup.
    evidence_dir = Path(args.fixture_evidence_dir) if args.fixture_evidence_dir else Path.cwd() / "raw" / "remote-mcp-stage-d-fixture"
    if evidence_dir.exists():
        shutil.rmtree(evidence_dir)
    shutil.copytree(audit_dir, evidence_dir)
    tmpdir.cleanup()
    return results, evidence_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Remote MCP Stage D proof checks.")
    parser.add_argument("--url", help="Remote MCP bridge base URL. Defaults to SOM_MCP_URL.")
    parser.add_argument("--path", help=f"Remote MCP call path. Defaults to {DEFAULT_PROOF_PATH}.")
    parser.add_argument("--token", help="Inner bridge token. Defaults to SOM_MCP_TOKEN or SOM_REMOTE_MCP_JWT.")
    parser.add_argument("--identity-email", help="Expected authenticated email header for direct bridge tests.")
    parser.add_argument("--identity-sub", help="Expected authenticated subject header for direct bridge tests.")
    parser.add_argument("--audit-dir", help="Directory containing copied remote audit JSONL files.")
    parser.add_argument("--audit-hmac-key", help="HMAC key for strict audit verification.")
    parser.add_argument("--stdio-proof-command", help="Command proving local stdio MCP still works after tunnel stop.")
    parser.add_argument("--timeout-sec", type=float, default=DEFAULT_TIMEOUT_SEC)
    parser.add_argument("--fixture", action="store_true", help="Run against a local in-process fixture server.")
    parser.add_argument("--fixture-evidence-dir", help="Directory to receive fixture audit evidence.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable result JSON.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    if args.fixture:
        results, evidence_dir = run_fixture(args)
        evidence_note = str(evidence_dir)
    else:
        config = StageDConfig.from_env(args)
        missing = config.validate_live()
        if missing:
            print("missing required live proof configuration: " + ", ".join(missing), file=sys.stderr)
            return 2
        results = run_stage_d(config)
        evidence_note = str(config.audit_dir) if config.audit_dir else ""

    if args.json:
        print(json.dumps({"results": [result.to_dict() for result in results], "evidence_dir": evidence_note}, indent=2))
    else:
        for result in results:
            print(f"{result.status.upper()} {result.name}: {result.detail}")
        if evidence_note:
            print(f"EVIDENCE {evidence_note}")

    return 0 if all(result.status in {"pass", "skip"} for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
