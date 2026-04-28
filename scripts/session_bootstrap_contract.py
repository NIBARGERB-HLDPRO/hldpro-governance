#!/usr/bin/env python3
"""Canonical governance session-start bootstrap contract."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_DOCS = [
    "CODEX.md",
    "CLAUDE.md",
    "docs/PROGRESS.md",
    "docs/FAIL_FAST_LOG.md",
    "STANDARDS.md",
    "docs/EXTERNAL_SERVICES_RUNBOOK.md",
]
SENTINEL_VERSION = 1


@dataclass(frozen=True)
class RunbookPaths:
    codex_binary: str | None
    codex_config: str | None
    claude_auth: str | None
    bootstrap_command: str | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--emit-hook-note", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--sentinel-path", type=Path, default=None)
    return parser.parse_args()


def resolve_repo_root(explicit: Path | None) -> Path:
    if explicit:
        return explicit.resolve()
    script_root = Path(__file__).resolve().parents[1]
    git_root = run_git_root(script_root)
    return git_root or script_root


def run_git_root(cwd: Path) -> Path | None:
    result = subprocess.run(
        ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


def sentinel_path(repo_root: Path, explicit: Path | None) -> Path:
    if explicit:
        return explicit
    session_key = (
        os.environ.get("CLAUDE_SESSION_ID")
        or os.environ.get("CODEX_SESSION_ID")
        or str(os.getppid())
    )
    return Path("/tmp") / f"hldpro-session-bootstrap-{repo_root.name}-{session_key}.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_som_excerpt(standards_text: str) -> str:
    match = re.search(
        r"## Society of Minds — Model Routing Charter .*?(?=\n## |\Z)",
        standards_text,
        re.S,
    )
    if not match:
        return "MISSING: Society of Minds section not found in STANDARDS.md"
    excerpt = match.group(0).strip().splitlines()
    return "\n".join(excerpt[:18])


def extract_runbook_paths(runbook_text: str) -> RunbookPaths:
    def capture(pattern: str) -> str | None:
        match = re.search(pattern, runbook_text, re.M)
        return match.group(1).strip() if match else None

    bootstrap_match = re.search(
        r"^(bash\s+~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env\.sh\s+<repo>)$",
        runbook_text,
        re.M,
    )

    return RunbookPaths(
        codex_binary=capture(r"^- Binary:\s*(.+)$"),
        codex_config=capture(r"^- Config:\s*(.+)$"),
        claude_auth=capture(r"^- `CLAUDE_CODE_OAUTH_TOKEN` in (.+)$"),
        bootstrap_command=bootstrap_match.group(1).strip() if bootstrap_match else None,
    )


def codex_backlog_status(repo_root: Path) -> dict[str, object]:
    home = Path.home()
    backlog_dir = home / "Developer" / "hldpro" / ".codex-ingestion" / repo_root.name
    pending = sorted(backlog_dir.glob("backlog-*.md"))
    return {
        "directory": str(backlog_dir),
        "pending_count": len(pending),
        "pending_files": [p.name for p in pending[:10]],
    }


def build_report(repo_root: Path) -> dict[str, object]:
    doc_state: dict[str, dict[str, object]] = {}
    loaded = {}
    for rel_path in REQUIRED_DOCS:
        path = repo_root / rel_path
        exists = path.exists()
        doc_state[rel_path] = {"exists": exists, "path": str(path)}
        if exists:
            loaded[rel_path] = read_text(path)

    standards_text = loaded.get("STANDARDS.md", "")
    runbook_text = loaded.get("docs/EXTERNAL_SERVICES_RUNBOOK.md", "")
    runbook_paths = extract_runbook_paths(runbook_text) if runbook_text else RunbookPaths(None, None, None, None)
    backlog = codex_backlog_status(repo_root)
    current_branch = git_branch(repo_root)

    sentinel = {
        "schema_version": SENTINEL_VERSION,
        "repo_root": str(repo_root),
        "repo_name": repo_root.name,
        "current_branch": current_branch,
        "loaded_or_surfaced": {
            "codex_contract": doc_state["CODEX.md"]["exists"],
            "claude_contract": doc_state["CLAUDE.md"]["exists"],
            "progress_doc": doc_state["docs/PROGRESS.md"]["exists"],
            "fail_fast_log": doc_state["docs/FAIL_FAST_LOG.md"]["exists"],
            "standards_som": doc_state["STANDARDS.md"]["exists"] and "## Society of Minds" in standards_text,
            "external_services_runbook": doc_state["docs/EXTERNAL_SERVICES_RUNBOOK.md"]["exists"],
        },
        "runbook_paths": {
            "codex_binary": runbook_paths.codex_binary,
            "codex_config": runbook_paths.codex_config,
            "claude_auth": runbook_paths.claude_auth,
            "bootstrap_command": runbook_paths.bootstrap_command,
        },
        "codex_backlog": backlog,
        "warnings": [
            f"missing:{rel_path}"
            for rel_path, state in doc_state.items()
            if not state["exists"]
        ],
    }

    return {
        "doc_state": doc_state,
        "standards_excerpt": extract_som_excerpt(standards_text) if standards_text else None,
        "runbook_paths": runbook_paths,
        "backlog": backlog,
        "sentinel": sentinel,
    }


def git_branch(repo_root: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "branch", "--show-current"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    branch = result.stdout.strip()
    return branch or None


def write_sentinel(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def format_hook_note(report: dict[str, object], sentinel_file: Path) -> str:
    sentinel = report["sentinel"]
    runbook_paths: RunbookPaths = report["runbook_paths"]
    backlog = report["backlog"]
    warnings = sentinel["warnings"]
    warning_block = "\n".join(f"- WARNING: {warning}" for warning in warnings) or "- WARNING: none"

    return "\n".join(
        [
            "=== SESSION BOOTSTRAP CONTRACT (hldpro-governance) ===",
            "",
            f"sentinel: {sentinel_file}",
            f"branch: {sentinel['current_branch'] or '(unknown)'}",
            "",
            "supervisor_contract:",
            "- Codex is orchestrator/supervisor only.",
            "- Use the waterfall: plan -> alternate-family review -> integrated handoff -> worker -> QA -> deterministic gate.",
            "- Do not improvise CLI/auth/bootstrap paths; use the external-services runbook.",
            "",
            "required_reads:",
            *[f"- {path}" for path in REQUIRED_DOCS],
            "",
            "approved_runbook_paths:",
            f"- codex_binary: {runbook_paths.codex_binary or 'MISSING'}",
            f"- codex_config: {runbook_paths.codex_config or 'MISSING'}",
            f"- claude_auth: {runbook_paths.claude_auth or 'MISSING'}",
            f"- bootstrap_command: {runbook_paths.bootstrap_command or 'MISSING'}",
            "",
            "codex_backlog:",
            f"- directory: {backlog['directory']}",
            f"- pending_count: {backlog['pending_count']}",
            *[f"- pending_file: {name}" for name in backlog["pending_files"]],
            "",
            "warnings:",
            warning_block,
            "",
            "--- STANDARDS.md §Society of Minds (excerpt) ---",
            str(report["standards_excerpt"] or "MISSING"),
            "",
            "=== END SESSION BOOTSTRAP CONTRACT ===",
        ]
    )


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root(args.repo_root)
    report = build_report(repo_root)
    sentinel_file = sentinel_path(repo_root, args.sentinel_path)
    write_sentinel(sentinel_file, report["sentinel"])

    if args.json:
        json.dump(
            {
                "sentinel_path": str(sentinel_file),
                **report["sentinel"],
            },
            sys.stdout,
            indent=2,
            sort_keys=True,
        )
        sys.stdout.write("\n")
        return 0

    if args.emit_hook_note:
        print(format_hook_note(report, sentinel_file))
        return 0

    print(str(sentinel_file))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
