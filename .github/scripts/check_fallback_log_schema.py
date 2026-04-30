#!/usr/bin/env python3
from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys

import yaml


DEGRADED_FALLBACK_SCOPE = "alternate_model_review"
PLACEHOLDER_VALUES = {"todo", "tbd", "n/a", "na", "placeholder"}
DISALLOWED_DEGRADED_REASONS = {"other", "auto", "no_fallback_required"}
REQUIRED_FIELDS = {"date", "session_id", "tier", "primary_model", "fallback_model", "reason", "caller_script"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def emit(path: str, line: int, msg: str) -> None:
    print(f"::error file={path},line={line}::[check-fallback-log-schema] {msg}")


def is_placeholder(value: object) -> bool:
    return str(value).strip().lower() in PLACEHOLDER_VALUES


def is_non_empty(value: object) -> bool:
    if value is None:
        return False
    return bool(str(value).strip())


def validate_repo_ref(value: object, field_name: str) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return f"{field_name} must be non-empty"
    if is_placeholder(value):
        return f"{field_name} must not use placeholder text"
    path_part, _, _anchor = value.partition("#")
    path_text = path_part.strip()
    if path_text.startswith("/"):
        return f"{field_name} must be repo-relative"
    if "\\" in path_text:
        return f"{field_name} must use '/' path separators"
    path_obj = pathlib.Path(path_text)
    if any(part == ".." for part in path_obj.parts):
        return f"{field_name} must not traverse parent directories"
    if path_text in {"", "."}:
        return f"{field_name} must reference a repo file"
    return None


def validate_block(data: dict[object, object], file: str, start: int) -> bool:
    fail = False
    missing = sorted(REQUIRED_FIELDS - set(data.keys()))
    if missing:
        emit(file, start, f"missing required fields: {', '.join(missing)}")
        fail = True

    date_value = str(data.get("date", ""))
    if not DATE_RE.match(date_value):
        emit(file, start, "date must be YYYY-MM-DD")
        fail = True

    tier = data.get("tier")
    if not isinstance(tier, int) or not (1 <= tier <= 4):
        emit(file, start, "tier must be integer in range 1-4")
        fail = True

    reason = str(data.get("reason", "")).strip()
    if not reason:
        emit(file, start, "reason must be non-empty")
        fail = True
    elif is_placeholder(reason):
        emit(file, start, "reason must not use placeholder text")
        fail = True

    for key in ("primary_model", "fallback_model", "caller_script", "session_id"):
        if not is_non_empty(data.get(key, "")):
            emit(file, start, f"{key} must be non-empty")
            fail = True
        elif is_placeholder(data.get(key, "")):
            emit(file, start, f"{key} must not use placeholder text")
            fail = True

    fallback_scope = data.get("fallback_scope")
    cross_family_unavailable = data.get("cross_family_path_unavailable")
    cross_family_path_ref = data.get("cross_family_path_ref")
    degraded_metadata_present = any(
        field in data for field in ("fallback_scope", "cross_family_path_unavailable", "cross_family_path_ref")
    )

    if fallback_scope is not None and not isinstance(fallback_scope, str):
        emit(file, start, "fallback_scope must be a string when present")
        fail = True
    if cross_family_unavailable is not None and not isinstance(cross_family_unavailable, bool):
        emit(file, start, "cross_family_path_unavailable must be a boolean when present")
        fail = True
    if cross_family_path_ref is not None and not isinstance(cross_family_path_ref, str):
        emit(file, start, "cross_family_path_ref must be a string when present")
        fail = True

    if fallback_scope is None:
        if degraded_metadata_present:
            emit(file, start, "degraded fallback metadata requires fallback_scope: alternate_model_review")
            fail = True
        return fail

    scope_text = str(fallback_scope).strip()
    if scope_text != DEGRADED_FALLBACK_SCOPE:
        emit(file, start, f"fallback_scope must be {DEGRADED_FALLBACK_SCOPE!r} when present")
        fail = True
    if cross_family_unavailable is not True:
        emit(file, start, "alternate_model_review fallback requires cross_family_path_unavailable: true")
        fail = True
    path_ref_error = validate_repo_ref(cross_family_path_ref, "cross_family_path_ref")
    if path_ref_error:
        emit(file, start, path_ref_error)
        fail = True
    if reason.lower() in DISALLOWED_DEGRADED_REASONS:
        emit(file, start, "alternate_model_review fallback reason must be specific, not generic")
        fail = True
    return fail


def validate_file(path: pathlib.Path) -> int:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines or lines[0].strip() != "---":
        emit(path.as_posix(), 1, "file must start with YAML frontmatter block")
        return 1

    fail = False
    i = 0
    while i < len(lines):
        if lines[i].strip() == "":
            i += 1
            continue
        if lines[i].strip() != "---":
            emit(path.as_posix(), i + 1, "expected frontmatter separator")
            return 1
        start = i + 1
        i += 1
        block_lines: list[str] = []
        while i < len(lines) and lines[i].strip() != "---":
            block_lines.append(lines[i])
            i += 1
        if i >= len(lines):
            emit(path.as_posix(), start, "frontmatter block missing closing ---")
            return 1
        i += 1
        block_text = "\n".join(block_lines)
        try:
            data = yaml.safe_load(block_text) or {}
        except Exception as exc:
            emit(path.as_posix(), start, f"invalid YAML frontmatter: {exc}")
            fail = True
            continue
        if not isinstance(data, dict):
            emit(path.as_posix(), start, "frontmatter must be YAML mapping")
            fail = True
            continue
        fail = validate_block(data, path.as_posix(), start) or fail

    return 1 if fail else 0


def main() -> int:
    base_sha = os.environ.get("BASE_SHA", "")
    head_sha = os.environ.get("HEAD_SHA", "")
    if not base_sha or not head_sha:
        print("::warning::[check-fallback-log-schema] Missing pull request context; skipping.")
        return 0

    diff = subprocess.check_output(["git", "diff", "--name-only", f"{base_sha}...{head_sha}"], text=True).splitlines()
    fallback_files = [path for path in diff if path.startswith("raw/model-fallbacks/") and path.endswith(".md")]
    if not fallback_files:
        return 0

    fail = False
    for file in fallback_files:
        fp = pathlib.Path(file)
        if not fp.exists():
            emit(file, 1, "file missing")
            fail = True
            continue
        fail = validate_file(fp) != 0 or fail
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
