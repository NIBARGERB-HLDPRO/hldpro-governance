#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_SCAN_PATHS = (
    "STANDARDS.md",
    "docs/ENV_REGISTRY.md",
    "docs/EXTERNAL_SERVICES_RUNBOOK.md",
    "docs/runbooks/",
    "raw/validation/",
    "scripts/pages-deploy/",
    "scripts/remote-mcp/",
)

FIXTURE_ONLY_PATHS = {
    "scripts/overlord/test_validate_provisioning_evidence.py",
}

SAFE_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".jsonl",
    ".yml",
    ".yaml",
    ".sh",
    ".py",
}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    category: str


@dataclass(frozen=True)
class Rule:
    category: str
    pattern: re.Pattern[str]


RULES = (
    Rule(
        "authorization-header",
        re.compile(r"\bAuthorization\s*:\s*(?:Bearer|Basic|sso-key)\s+(?!\$|\$\{)[^\s`'\"<>]+", re.IGNORECASE),
    ),
    Rule(
        "jwt-fragment",
        re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\b"),
    ),
    Rule(
        "token-like-string",
        re.compile(
            r"\b(?:sk_live|sk_test|sk-ant|ghp|github_pat|xox[baprs]|SG|pk_live|rk_live|AKIA|ASIA)"
            r"[-_A-Za-z0-9]{12,}\b"
        ),
    ),
    Rule(
        "signed-url",
        re.compile(
            r"https?://[^\s`'\"<>]+[?&](?:X-Amz-Signature|X-Goog-Signature|Signature|sig|signature|access_token|token)=",
            re.IGNORECASE,
        ),
    ),
    Rule(
        "raw-phone-number",
        re.compile(r"(?<![A-Za-z0-9_])\+[1-9]\d{10,14}(?![A-Za-z0-9_])"),
    ),
)

ENV_ASSIGNMENT_RE = re.compile(r"^\s*(?:export\s+)?[A-Z][A-Z0-9_]{2,}\s*=\s*(?!$|<redacted>|REDACTED|\$\{?)[^\s#]+")


def _normalize_repo_path(path: str) -> str:
    while path.startswith("./"):
        path = path[2:]
    return path


def _read_changed_files(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    entries = raw.split("\0") if "\0" in raw else raw.splitlines()
    return [_normalize_repo_path(entry.strip()) for entry in entries if entry.strip()]


def _is_env_file(path: str) -> bool:
    name = Path(path).name
    return name == ".env" or name.startswith(".env.") or name.endswith(".env") or ".env." in name


def _is_scan_candidate(path: Path, rel_path: str) -> bool:
    if rel_path in FIXTURE_ONLY_PATHS:
        return False
    if not path.is_file():
        return False
    if _is_env_file(rel_path):
        return True
    return path.suffix in SAFE_SUFFIXES


def _expand_scan_paths(root: Path, requested: list[str]) -> list[Path]:
    paths: list[Path] = []
    for raw in requested:
        rel = _normalize_repo_path(raw)
        candidate = root / rel
        if candidate.is_dir():
            paths.extend(child for child in candidate.rglob("*") if child.is_file())
        elif candidate.exists():
            paths.append(candidate)
    return sorted(set(paths))


def _default_paths(root: Path) -> list[str]:
    return [path for path in DEFAULT_SCAN_PATHS if (root / path).exists()]


def scan_file(root: Path, path: Path) -> list[Finding]:
    try:
        rel_path = path.relative_to(root).as_posix()
    except ValueError:
        rel_path = path.as_posix()

    if not _is_scan_candidate(path, rel_path):
        return []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return []

    findings: list[Finding] = []
    env_file = _is_env_file(rel_path)
    for line_number, line in enumerate(lines, start=1):
        if env_file and ENV_ASSIGNMENT_RE.search(line):
            findings.append(Finding(rel_path, line_number, "generated-env-file-content"))
        for rule in RULES:
            if rule.pattern.search(line):
                findings.append(Finding(rel_path, line_number, rule.category))
    return findings


def scan_paths(root: Path, requested: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for path in _expand_scan_paths(root, requested):
        findings.extend(scan_file(root, path))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate provisioning evidence does not contain secret-like values.")
    parser.add_argument("paths", nargs="*", help="Repo-relative files or directories to scan.")
    parser.add_argument("--root", default=".", help="Repo root.")
    parser.add_argument("--changed-files-file", type=Path, help="Optional newline or NUL-delimited changed files list.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    requested = [_normalize_repo_path(path) for path in args.paths]
    if args.changed_files_file:
        requested.extend(_read_changed_files(args.changed_files_file))
    if not requested:
        requested = _default_paths(root)

    findings = scan_paths(root, requested)
    if findings:
        for finding in findings:
            print(f"FAIL {finding.path}:{finding.line}: provisioning evidence contains {finding.category}")
        return 1

    print(f"PASS provisioning evidence scan: {len(_expand_scan_paths(root, requested))} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
