#!/usr/bin/env python3
"""Run governed Claude/Codex CLI sessions with timeout evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import selectors
import signal
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


TIMEOUT_EXIT = 124


@dataclass
class AttemptResult:
    event: dict
    returncode: int


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def session_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"cli_{stamp}_{uuid.uuid4().hex[:12]}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def event_paths(event_root: Path, event_id: str) -> tuple[Path, Path, Path]:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    day_dir = event_root / day
    day_dir.mkdir(parents=True, exist_ok=True)
    return day_dir / f"{event_id}.stdout", day_dir / f"{event_id}.stderr", event_root / f"{day}.jsonl"


def append_jsonl(path: Path, event: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, sort_keys=True) + "\n")


def kill_group(proc: subprocess.Popen[bytes], grace_sec: float) -> None:
    try:
        pgid = os.getpgid(proc.pid)
    except ProcessLookupError:
        return

    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return

    deadline = time.monotonic() + grace_sec
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            return
        time.sleep(0.02)

    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        return


def build_command(args: argparse.Namespace, prompt_bytes: bytes) -> tuple[list[str], bytes]:
    if args.command:
        command = list(args.command)
        if command and command[0] == "--":
            command = command[1:]
        if not command:
            raise SystemExit("--command requires at least one command token")
        return command, prompt_bytes

    if args.tool == "claude":
        command = ["claude", "-p", prompt_bytes.decode("utf-8"), "--model", args.model]
        if args.permission_mode:
            command.extend(["--permission-mode", args.permission_mode])
        if args.allowed_tools:
            command.extend(["--allowedTools", args.allowed_tools])
        if args.max_turns is not None:
            command.extend(["--max-turns", str(args.max_turns)])
        if args.max_budget_usd is not None:
            command.extend(["--max-budget-usd", str(args.max_budget_usd)])
        if args.output_format:
            command.extend(["--output-format", args.output_format])
            if args.output_format == "stream-json" and not args.verbose:
                command.append("--verbose")
        if args.verbose:
            command.append("--verbose")
        if args.no_session_persistence:
            command.append("--no-session-persistence")
        return command, b""

    command = ["codex", "exec", "-C", str(args.cwd), "-m", args.model]
    if args.reasoning_effort:
        command.extend(["-c", f"model_reasoning_effort={args.reasoning_effort}"])
    command.extend(
        [
            "--sandbox",
            args.codex_sandbox,
            "--ask-for-approval",
            args.codex_approval,
            "--color",
            "never",
            "--",
            "-",
        ]
    )
    return command, prompt_bytes


def stream_attempt(
    *,
    args: argparse.Namespace,
    prompt_path: Path,
    prompt_bytes: bytes,
    retry_of: str | None,
    retry_count: int,
    stdout_copy: Path | None,
) -> AttemptResult:
    event_id = session_id()
    stdout_path, stderr_path, jsonl_path = event_paths(Path(args.event_root), event_id)
    command, stdin_bytes = build_command(args, prompt_bytes)
    started_at = utcnow()
    last_output_at: str | None = None
    start = time.monotonic()
    last_output = start
    termination_reason: str | None = None
    exit_code: int | None = None
    pid: int | None = None
    pgid: int | None = None

    proc = subprocess.Popen(
        command,
        cwd=args.cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    pid = proc.pid
    try:
        pgid = os.getpgid(proc.pid)
    except ProcessLookupError:
        pgid = None

    if proc.stdin is not None:
        try:
            proc.stdin.write(stdin_bytes)
        except BrokenPipeError:
            pass
        finally:
            proc.stdin.close()

    selector = selectors.DefaultSelector()
    assert proc.stdout is not None
    assert proc.stderr is not None
    selector.register(proc.stdout, selectors.EVENT_READ, "stdout")
    selector.register(proc.stderr, selectors.EVENT_READ, "stderr")

    with stdout_path.open("wb") as stdout_fh, stderr_path.open("wb") as stderr_fh:
        stdout_copy_fh = stdout_copy.open("wb") if stdout_copy else None
        try:
            while True:
                now = time.monotonic()
                if now - start >= args.wall_timeout_sec:
                    termination_reason = "total_timeout"
                    print(
                        f"cli-session-supervisor: total_timeout after {args.wall_timeout_sec}s for {event_id}",
                        file=sys.stderr,
                    )
                    kill_group(proc, args.terminate_grace_sec)
                    exit_code = proc.wait()
                    break
                if now - last_output >= args.silence_timeout_sec:
                    termination_reason = "idle_timeout"
                    print(
                        f"cli-session-supervisor: idle_timeout after {args.silence_timeout_sec}s for {event_id}",
                        file=sys.stderr,
                    )
                    kill_group(proc, args.terminate_grace_sec)
                    exit_code = proc.wait()
                    break

                selected = selector.select(timeout=0.05)
                for key, _ in selected:
                    data = os.read(key.fileobj.fileno(), 4096)
                    if not data:
                        selector.unregister(key.fileobj)
                        continue
                    last_output = time.monotonic()
                    last_output_at = utcnow()
                    if key.data == "stdout":
                        stdout_fh.write(data)
                        stdout_fh.flush()
                        if stdout_copy_fh:
                            stdout_copy_fh.write(data)
                            stdout_copy_fh.flush()
                        sys.stdout.buffer.write(data)
                        sys.stdout.buffer.flush()
                    else:
                        stderr_fh.write(data)
                        stderr_fh.flush()
                        sys.stderr.buffer.write(data)
                        sys.stderr.buffer.flush()

                if proc.poll() is not None and not selector.get_map():
                    exit_code = proc.wait()
                    termination_reason = "succeeded" if exit_code == 0 else "failed_nonzero"
                    break
        finally:
            if stdout_copy_fh:
                stdout_copy_fh.close()

    ended_at = utcnow()
    if termination_reason is None:
        exit_code = proc.poll()
        termination_reason = "succeeded" if exit_code == 0 else "failed_nonzero"

    event = {
        "schema_version": "v1",
        "session_event_id": event_id,
        "tool": args.tool,
        "role": args.role,
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "cwd": str(Path(args.cwd).resolve()),
        "command_argv": command,
        "prompt_path": str(prompt_path.resolve()),
        "prompt_sha256": sha256_bytes(prompt_bytes),
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "started_at": started_at,
        "last_output_at": last_output_at,
        "ended_at": ended_at,
        "pid": pid,
        "pgid": pgid,
        "exit_code": exit_code,
        "termination_reason": termination_reason,
        "wall_timeout_sec": args.wall_timeout_sec,
        "silence_timeout_sec": args.silence_timeout_sec,
        "retry_of": retry_of,
        "retry_count": retry_count,
        "scope_slug": args.scope_slug,
        "scope_reduction_summary": args.scope_reduction_summary if retry_count else None,
        "handoff_package_ref": args.handoff_package_ref,
    }
    append_jsonl(jsonl_path, event)

    if termination_reason in {"idle_timeout", "total_timeout"}:
        return AttemptResult(event=event, returncode=TIMEOUT_EXIT)
    return AttemptResult(event=event, returncode=exit_code or 0)


def parse_args(argv: list[str]) -> argparse.Namespace:
    command = None
    if "--command" in argv:
        command_idx = argv.index("--command")
        command = argv[command_idx + 1 :]
        argv = argv[:command_idx]
        if command and command[0] == "--":
            command = command[1:]

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=["claude", "codex"], required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--reasoning-effort")
    parser.add_argument("--cwd", default=".")
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--retry-prompt-file")
    parser.add_argument("--scope-slug", required=True)
    parser.add_argument("--scope-reduction-summary")
    parser.add_argument("--handoff-package-ref")
    parser.add_argument("--event-root", default="raw/cli-session-events")
    parser.add_argument("--stdout-copy")
    parser.add_argument("--wall-timeout-sec", type=float, default=900.0)
    parser.add_argument("--silence-timeout-sec", type=float, default=120.0)
    parser.add_argument("--terminate-grace-sec", type=float, default=2.0)
    parser.add_argument("--permission-mode")
    parser.add_argument("--allowed-tools")
    parser.add_argument("--max-turns", type=int)
    parser.add_argument("--max-budget-usd", type=float)
    parser.add_argument("--output-format")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--no-session-persistence", action="store_true")
    parser.add_argument("--codex-sandbox", default="workspace-write")
    parser.add_argument("--codex-approval", default="never")
    args = parser.parse_args(argv)
    args.command = command

    if args.retry_prompt_file and not args.scope_reduction_summary:
        parser.error("--retry-prompt-file requires --scope-reduction-summary")
    if args.tool == "codex" and not args.reasoning_effort:
        parser.error("--tool codex requires --reasoning-effort so codex exec emits model_reasoning_effort")
    if args.wall_timeout_sec <= 0 or args.silence_timeout_sec <= 0:
        parser.error("timeouts must be greater than zero")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    prompt_path = Path(args.prompt_file)
    prompt_bytes = prompt_path.read_bytes()
    stdout_copy = Path(args.stdout_copy) if args.stdout_copy else None

    result = stream_attempt(
        args=args,
        prompt_path=prompt_path,
        prompt_bytes=prompt_bytes,
        retry_of=None,
        retry_count=0,
        stdout_copy=stdout_copy,
    )
    if result.returncode == 0:
        return 0

    if (
        result.event["termination_reason"] in {"idle_timeout", "total_timeout"}
        and args.retry_prompt_file
    ):
        retry_prompt_path = Path(args.retry_prompt_file)
        retry_result = stream_attempt(
            args=args,
            prompt_path=retry_prompt_path,
            prompt_bytes=retry_prompt_path.read_bytes(),
            retry_of=result.event["session_event_id"],
            retry_count=1,
            stdout_copy=stdout_copy,
        )
        return retry_result.returncode

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
