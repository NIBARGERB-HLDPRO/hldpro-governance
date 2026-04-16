#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


REPO_SLUGS = (
    "ai-integration-services",
    "HealthcarePlatform",
    "local-ai-machine",
    "knocktracker",
    "hldpro-governance",
)

MEMORY_ROOT_PREFIX = Path.home() / ".claude/projects"
POINTER_RE = re.compile(r"^\s*-\s*\[[^\]]+\]\(([^)]+\.md)\)(?:\s*[—-].*)?$")
FRONTMATTER_RE = re.compile(r"^([^:]+)\s*:\s*(.*)$")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def memory_dir_for_repo(repo_slug: str) -> Path:
    return MEMORY_ROOT_PREFIX / f"-Users-bennibarger-Developer-HLDPRO-{repo_slug}" / "memory"


def load_memory_lines(memory_path: Path) -> list[str]:
    return memory_path.read_text(encoding="utf-8").splitlines()


def check_memory_exists(repo_slug: str) -> tuple[Path, list[str]]:
    memory_dir = memory_dir_for_repo(repo_slug)
    memory_md = memory_dir / "MEMORY.md"
    if not memory_md.exists():
        return memory_md, [f"{memory_md} missing"]
    return memory_md, []


def parse_pointer_filenames(memory_lines: list[str]) -> tuple[list[str], list[str]]:
    pointers: list[str] = []
    issues: list[str] = []
    for idx, line in enumerate(memory_lines, start=1):
        match = POINTER_RE.match(line)
        if not match:
            continue
        pointer = match.group(1).strip()
        if not pointer:
            issues.append(f"line {idx}: empty markdown link target")
            continue
        pointers.append(pointer)
    return pointers, issues


def validate_frontmatter(path: Path, repo_slug: str, file_name: str) -> list[str]:
    issues: list[str] = []
    try:
        content = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [f"{repo_slug}: cannot read referenced memory file '{file_name}': {exc}"]

    if not content or content[0].strip() != "---":
        return [f"{repo_slug}: {file_name} missing YAML frontmatter"]

    try:
        end_idx = content[1:].index("---")
    except ValueError:
        return [f"{repo_slug}: {file_name} frontmatter missing closing '---'"]

    frontmatter_lines = content[1 : 1 + end_idx]
    fields: dict[str, str] = {}
    for raw in frontmatter_lines:
        match = FRONTMATTER_RE.match(raw)
        if not match:
            continue
        key = match.group(1).strip()
        value = match.group(2).strip().strip('"\'')
        fields[key] = value

    for required in ("name", "description", "type"):
        if required not in fields or not fields[required]:
            issues.append(f"{repo_slug}: {file_name} missing frontmatter field '{required}'")
    return issues


def inspect_repo(repo_slug: str) -> tuple[bool, list[str], int]:
    memory_md, issues = check_memory_exists(repo_slug)
    if issues:
        return False, issues, 0

    memory_lines = load_memory_lines(memory_md)
    line_count = len(memory_lines)
    if line_count > 200:
        issues.append(f"MEMORY.md has {line_count} lines (must be under 200)")

    pointers, pointer_issues = parse_pointer_filenames(memory_lines)
    issues.extend(pointer_issues)
    entries = len(pointers)

    duplicates = [name for name, count in Counter(Path(p).name for p in pointers).items() if count > 1]
    for duplicate in sorted(duplicates):
        issues.append(f"duplicate pointer in MEMORY.md: {duplicate}")

    memory_directory = memory_dir_for_repo(repo_slug)
    for pointer in pointers:
        target = (memory_directory / pointer).resolve()
        if not target.exists():
            issues.append(f"pointer '{pointer}' does not resolve to a file in {memory_directory}")
            continue
        if not str(target).startswith(str(memory_directory)):
            issues.append(f"pointer '{pointer}' resolves outside memory directory")
            continue
        issues.extend(validate_frontmatter(target, repo_slug, pointer))

    return (len(issues) == 0), issues, entries


def main() -> None:
    all_pass = True
    for repo_slug in REPO_SLUGS:
        passed, issues, entries = inspect_repo(repo_slug)
        status = "PASS" if passed else "FAIL"
        print(f"{repo_slug}: {status} ({entries} entries, {len(issues)} issues)")
        if issues:
            all_pass = False
            for issue in issues:
                print(f"- {issue}")

    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
