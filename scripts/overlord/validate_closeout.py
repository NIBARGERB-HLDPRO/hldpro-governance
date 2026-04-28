#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from validate_handoff_package import validate_package
except ImportError:  # pragma: no cover - supports direct execution from unusual cwd.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from validate_handoff_package import validate_package


REPO_PATH_PATTERN = re.compile(
    r"(?P<path>"
    r"(?:docs/plans/|raw/(?:closeouts|cross-review|execution-scopes|handoffs|packets|validation)/|"
    r"cache/local-ci-gate/reports/|\.github/|hooks/|scripts/)"
    r"[A-Za-z0-9._/@()+=:-]+(?:/[A-Za-z0-9._/@()+=:-]+)*"
    r")"
)
ISSUE_REF_PATTERN = re.compile(r"(?:^|[\s([])(?:#\d+|https://github\.com/[^/\s]+/[^/\s]+/issues/\d+)(?:$|[\s).,\]])")
PLACEHOLDER_PATTERN = re.compile(r"_{4,}|\[[^\]]+\]")
ACCEPTED_LIFECYCLE_PATTERN = re.compile(r"handoff lifecycle\s*:\s*(?:accepted|released)\b", re.IGNORECASE)

REQUIRED_SECTIONS = {
    "Issue Links",
    "Review And Gate Identity",
    "Execution Scope / Write Boundary",
    "Validation Commands",
    "Residual Risks / Follow-Up",
}
REQUIRED_REF_CLASSES = {
    "structured plan": "docs/plans/",
    "execution scope": "raw/execution-scopes/",
    "handoff package": "raw/handoffs/",
    "validation artifact": "raw/validation/",
}


def _repo_rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def _extract_repo_refs(text: str) -> list[str]:
    refs: list[str] = []
    seen: set[str] = set()
    for match in REPO_PATH_PATTERN.finditer(text):
        ref = match.group("path").rstrip("`.,)")
        if ref not in seen:
            refs.append(ref)
            seen.add(ref)
    return refs


def _load_json(path: Path, failures: list[str]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"{path}: could not parse JSON: {exc}")
        return None


def _execution_scope_refs(refs: list[str]) -> list[str]:
    return [ref for ref in refs if ref.startswith("raw/execution-scopes/")]


def _validate_residuals(closeout_path: Path, sections: dict[str, str], failures: list[str]) -> None:
    residuals = sections.get("Residual Risks / Follow-Up", "").strip()
    if not residuals:
        failures.append(f"{closeout_path}: `Residual Risks / Follow-Up` must be explicitly none or issue-backed")
        return
    if PLACEHOLDER_PATTERN.search(residuals):
        failures.append(f"{closeout_path}: `Residual Risks / Follow-Up` still contains placeholder text")
        return
    lowered_lines = [line.strip().lower() for line in residuals.splitlines() if line.strip()]
    if any(line in {"none", "none."} or line.startswith("none.") for line in lowered_lines):
        return
    if not ISSUE_REF_PATTERN.search(residuals):
        failures.append(f"{closeout_path}: residual risks/follow-ups must cite a GitHub issue or state `None.`")


def _validate_refs(
    root: Path,
    closeout_path: Path,
    refs: list[str],
    sections: dict[str, str],
    failures: list[str],
) -> None:
    for label, prefix in REQUIRED_REF_CLASSES.items():
        if not any(ref.startswith(prefix) for ref in refs):
            failures.append(f"{closeout_path}: missing required {label} reference with prefix `{prefix}`")
    review_section = sections.get("Review And Gate Identity", "")
    implementation_only = "implementation only" in review_section.lower()
    if not any(ref.startswith("raw/cross-review/") for ref in refs) and not implementation_only:
        failures.append(f"{closeout_path}: missing review artifact reference with prefix `raw/cross-review/`")
    has_gate_artifact = any(ref.startswith("cache/local-ci-gate/reports/") for ref in refs)
    has_gate_command_result = "command result" in review_section.lower()
    if not has_gate_artifact and not has_gate_command_result:
        failures.append(
            f"{closeout_path}: missing gate artifact reference with prefix `cache/local-ci-gate/reports/` "
            "or explicit gate command result"
        )
    for ref in refs:
        path = root / ref
        if not path.exists():
            failures.append(f"{closeout_path}: referenced artifact does not exist: {ref}")


def _validate_handoff_refs(root: Path, closeout_path: Path, refs: list[str], text: str, failures: list[str]) -> None:
    handoff_refs = [ref for ref in refs if ref.startswith("raw/handoffs/")]
    if not handoff_refs:
        return
    closeout_ref = _repo_rel(closeout_path, root)
    lifecycle_recorded = bool(ACCEPTED_LIFECYCLE_PATTERN.search(text))
    for ref in handoff_refs:
        package_path = root / ref
        if not package_path.is_file():
            continue
        if not lifecycle_recorded:
            failures.append(
                f"{closeout_path}: handoff package {ref} requires `Handoff lifecycle: accepted` "
                "or `Handoff lifecycle: released` in the closeout"
            )
        failures.extend(validate_package(root, package_path))
        payload = _load_json(package_path, failures)
        if not isinstance(payload, dict):
            continue
        lifecycle_state = payload.get("lifecycle_state")
        if lifecycle_state in {"accepted", "released"}:
            if payload.get("closeout_ref") != closeout_ref:
                failures.append(
                    f"{closeout_path}: handoff package {ref} lifecycle is {lifecycle_state!r} "
                    f"but closeout_ref is not {closeout_ref!r}"
                )
            continue


def resolve_closeout_execution_mode(root: Path, closeout_path: Path) -> str | None:
    if not closeout_path.is_absolute():
        closeout_path = root / closeout_path
    if not closeout_path.is_file():
        return None

    refs = _extract_repo_refs(closeout_path.read_text(encoding="utf-8"))
    scope_refs = _execution_scope_refs(refs)
    if len(scope_refs) != 1:
        return None

    failures: list[str] = []
    payload = _load_json(root / scope_refs[0], failures)
    if failures or not isinstance(payload, dict):
        return None

    execution_mode = payload.get("execution_mode")
    if isinstance(execution_mode, str) and execution_mode:
        return execution_mode
    return "planning_only"


def validate_closeout(root: Path, closeout_path: Path) -> list[str]:
    failures: list[str] = []
    if not closeout_path.is_absolute():
        closeout_path = root / closeout_path
    if not closeout_path.is_file():
        return [f"{closeout_path}: closeout file does not exist"]

    text = closeout_path.read_text(encoding="utf-8")
    sections = _sections(text)
    for section in sorted(REQUIRED_SECTIONS):
        content = sections.get(section)
        if not content:
            failures.append(f"{closeout_path}: missing required section `## {section}`")
        elif PLACEHOLDER_PATTERN.search(content):
            failures.append(f"{closeout_path}: section `## {section}` still contains placeholder text")

    refs = _extract_repo_refs(text)
    _validate_refs(root, closeout_path, refs, sections, failures)
    _validate_residuals(closeout_path, sections, failures)
    _validate_handoff_refs(root, closeout_path, refs, text, failures)
    return failures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Stage 6 closeout evidence before graph/wiki refresh.")
    parser.add_argument("closeout", help="Repo-relative or absolute closeout markdown path")
    parser.add_argument("--root", default=".", help="Repository root")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).resolve()
    failures = validate_closeout(root, Path(args.closeout))
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print(f"PASS closeout evidence validated: {args.closeout}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
