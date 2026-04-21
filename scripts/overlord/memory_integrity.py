#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.overlord.governed_repos import DEFAULT_REGISTRY, repo_names_enabled_for

MEMORY_ROOT_PREFIX = Path.home() / ".claude/projects"
POINTER_RE = re.compile(r"^\s*-\s*\[[^\]]+\]\(([^)]+\.md)\)(?:\s*[—-].*)?$")
FRONTMATTER_RE = re.compile(r"^([^:]+)\s*:\s*(.*)$")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


@dataclass(frozen=True)
class MemoryInspection:
    passed: bool
    issues: list[str]
    entries: int
    skipped: bool = False


def memory_dir_for_repo(repo_slug: str, memory_root: Path = MEMORY_ROOT_PREFIX) -> Path:
    return memory_root / f"-Users-bennibarger-Developer-HLDPRO-{repo_slug}" / "memory"


def load_memory_lines(memory_path: Path) -> list[str]:
    return memory_path.read_text(encoding="utf-8").splitlines()


def check_memory_exists(repo_slug: str, memory_root: Path = MEMORY_ROOT_PREFIX) -> tuple[Path, list[str]]:
    memory_dir = memory_dir_for_repo(repo_slug, memory_root)
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


def inspect_repo(
    repo_slug: str,
    *,
    memory_root: Path = MEMORY_ROOT_PREFIX,
    allow_missing: bool = False,
) -> MemoryInspection:
    memory_md, issues = check_memory_exists(repo_slug, memory_root)
    if issues:
        if allow_missing:
            return MemoryInspection(
                passed=True,
                issues=[f"memory source unavailable at {memory_md}; skipped in allow-missing mode"],
                entries=0,
                skipped=True,
            )
        return MemoryInspection(False, issues, 0)

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

    memory_directory = memory_dir_for_repo(repo_slug, memory_root)
    for pointer in pointers:
        target = (memory_directory / pointer).resolve()
        if not target.exists():
            issues.append(f"pointer '{pointer}' does not resolve to a file in {memory_directory}")
            continue
        try:
            target.relative_to(memory_directory.resolve())
        except ValueError:
            issues.append(f"pointer '{pointer}' resolves outside memory directory")
            continue
        issues.extend(validate_frontmatter(target, repo_slug, pointer))

    return MemoryInspection(len(issues) == 0, issues, entries)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit governed Claude MEMORY.md pointer files")
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="Path to governed_repos.json",
    )
    parser.add_argument(
        "--memory-root",
        type=Path,
        default=MEMORY_ROOT_PREFIX,
        help="Root containing Claude project memory directories",
    )
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help=(
            "Treat missing MEMORY.md sources as explicit skips. Use only where operator-home "
            "Claude memory is unavailable, such as GitHub-hosted runners."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    all_pass = True
    for repo_slug in repo_names_enabled_for("memory_integrity", args.registry):
        result = inspect_repo(repo_slug, memory_root=args.memory_root, allow_missing=args.allow_missing)
        status = "SKIP" if result.skipped else "PASS" if result.passed else "FAIL"
        issue_label = "notices" if result.skipped else "issues"
        print(f"{repo_slug}: {status} ({result.entries} entries, {len(result.issues)} {issue_label})")
        if not result.passed:
            all_pass = False
        if result.issues:
            for issue in result.issues:
                print(f"- {issue}")

    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
