#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class HandoffEvidence:
    status: str
    planner_model: str
    implementer_model: str
    accepted_at: datetime
    evidence_paths: tuple[str, ...]
    active_exception_ref: str | None
    active_exception_expires_at: datetime | None


@dataclass(frozen=True)
class ExecutionScope:
    expected_execution_root: str
    expected_branch: str
    allowed_write_paths: tuple[str, ...]
    forbidden_roots: tuple[Path, ...]
    active_parallel_roots: tuple[Path, ...] = ()
    execution_mode: str = "planning_only"
    handoff_evidence: HandoffEvidence | None = None


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def _normalize_repo_path(path: str) -> str:
    while path.startswith("./"):
        path = path[2:]
    return path


def _normalize_repo_relative_file_path(raw_path: str, field_name: str, scope_path: Path) -> str:
    normalized = _normalize_repo_path(raw_path.strip())
    if not normalized:
        raise ValueError(f"{scope_path}: `{field_name}` must be a non-empty repo-relative file path")
    if "\\" in normalized:
        raise ValueError(f"{scope_path}: `{field_name}` must use '/' path separators")
    path_obj = Path(normalized)
    if path_obj.is_absolute():
        raise ValueError(f"{scope_path}: `{field_name}` must be repo-relative (absolute paths are not allowed)")
    if any(part == ".." for part in path_obj.parts):
        raise ValueError(f"{scope_path}: `{field_name}` must not traverse parent directories")
    normalized_path = path_obj.as_posix()
    if normalized_path in {"", "."}:
        raise ValueError(f"{scope_path}: `{field_name}` must point to a repo file path")
    return normalized_path


def _normalize_active_exception_ref(raw_ref: str, scope_path: Path) -> str:
    path_part, has_anchor, anchor = raw_ref.partition("#")
    normalized_path = _normalize_repo_relative_file_path(
        path_part,
        "handoff_evidence.active_exception_ref",
        scope_path,
    )
    if has_anchor and not anchor:
        raise ValueError(f"{scope_path}: `handoff_evidence.active_exception_ref` has an empty '#anchor' suffix")
    if has_anchor:
        return f"{normalized_path}#{anchor}"
    return normalized_path


def _parse_iso8601_timestamp(raw_value: str, field_name: str, path: Path) -> datetime:
    if not isinstance(raw_value, str) or not raw_value:
        raise ValueError(f"{path}: `{field_name}` must be a non-empty string")
    normalized = raw_value
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{path}: `{field_name}` must be a valid ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _load_handoff_evidence(payload: dict[str, object], scope_path: Path) -> HandoffEvidence:
    required = [
        "status",
        "planner_model",
        "implementer_model",
        "accepted_at",
        "evidence_paths",
        "active_exception_ref",
        "active_exception_expires_at",
    ]
    missing = [field for field in required if field not in payload]
    if missing:
        raise ValueError(f"{scope_path}: `handoff_evidence` missing field(s): {', '.join(missing)}")

    status = payload["status"]
    planner_model = payload["planner_model"]
    implementer_model = payload["implementer_model"]
    accepted_at_raw = payload["accepted_at"]
    evidence_paths = payload["evidence_paths"]
    active_exception_ref = payload["active_exception_ref"]
    active_exception_expires_at_raw = payload["active_exception_expires_at"]

    if not isinstance(status, str) or not status:
        raise ValueError(f"{scope_path}: `handoff_evidence.status` must be a non-empty string")
    if not isinstance(planner_model, str) or not planner_model:
        raise ValueError(f"{scope_path}: `handoff_evidence.planner_model` must be a non-empty string")
    if not isinstance(implementer_model, str) or not implementer_model:
        raise ValueError(f"{scope_path}: `handoff_evidence.implementer_model` must be a non-empty string")
    if not isinstance(evidence_paths, list) or not all(isinstance(item, str) and item for item in evidence_paths):
        raise ValueError(f"{scope_path}: `handoff_evidence.evidence_paths` must be an array of non-empty strings")
    if active_exception_ref is not None and (not isinstance(active_exception_ref, str) or not active_exception_ref):
        raise ValueError(f"{scope_path}: `handoff_evidence.active_exception_ref` must be null or a non-empty string")
    if active_exception_expires_at_raw is not None and (
        not isinstance(active_exception_expires_at_raw, str) or not active_exception_expires_at_raw
    ):
        raise ValueError(
            f"{scope_path}: `handoff_evidence.active_exception_expires_at` must be null or a non-empty string"
        )

    accepted_at = _parse_iso8601_timestamp(accepted_at_raw, "handoff_evidence.accepted_at", scope_path)
    active_exception_expires_at = None
    if isinstance(active_exception_expires_at_raw, str):
        active_exception_expires_at = _parse_iso8601_timestamp(
            active_exception_expires_at_raw,
            "handoff_evidence.active_exception_expires_at",
            scope_path,
        )

    normalized_exception_ref = None
    if isinstance(active_exception_ref, str):
        normalized_exception_ref = _normalize_active_exception_ref(active_exception_ref, scope_path)

    return HandoffEvidence(
        status=status,
        planner_model=planner_model,
        implementer_model=implementer_model,
        accepted_at=accepted_at,
        evidence_paths=tuple(_normalize_repo_path(item) for item in evidence_paths),
        active_exception_ref=normalized_exception_ref,
        active_exception_expires_at=active_exception_expires_at,
    )


def _load_scope(path: Path) -> ExecutionScope:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: top-level JSON must be an object")

    required = [
        "expected_execution_root",
        "expected_branch",
        "allowed_write_paths",
        "forbidden_roots",
    ]
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"{path}: missing required field(s): {', '.join(missing)}")

    expected_execution_root = payload["expected_execution_root"]
    expected_branch = payload["expected_branch"]
    allowed_write_paths = payload["allowed_write_paths"]
    forbidden_roots = payload["forbidden_roots"]
    active_parallel_roots = payload.get("active_parallel_roots", [])
    execution_mode = payload.get("execution_mode", "planning_only")
    handoff_evidence_payload = payload.get("handoff_evidence")

    if not isinstance(expected_execution_root, str) or not expected_execution_root:
        raise ValueError(f"{path}: `expected_execution_root` must be a non-empty string")
    if not isinstance(expected_branch, str) or not expected_branch:
        raise ValueError(f"{path}: `expected_branch` must be a non-empty string")
    if not isinstance(allowed_write_paths, list) or not all(isinstance(item, str) and item for item in allowed_write_paths):
        raise ValueError(f"{path}: `allowed_write_paths` must be an array of non-empty strings")
    if not isinstance(forbidden_roots, list) or not all(isinstance(item, str) and item for item in forbidden_roots):
        raise ValueError(f"{path}: `forbidden_roots` must be an array of non-empty strings")
    if not isinstance(active_parallel_roots, list):
        raise ValueError(f"{path}: `active_parallel_roots` must be an array when provided")
    if not isinstance(execution_mode, str) or not execution_mode:
        raise ValueError(f"{path}: `execution_mode` must be a non-empty string when provided")
    if handoff_evidence_payload is not None and not isinstance(handoff_evidence_payload, dict):
        raise ValueError(f"{path}: `handoff_evidence` must be an object when provided")

    normalized_forbidden_roots = tuple(Path(item).expanduser().resolve(strict=False) for item in forbidden_roots)
    normalized_active_roots: list[Path] = []
    for index, item in enumerate(active_parallel_roots, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"{path}: `active_parallel_roots[{index}]` must be an object")
        active_path = item.get("path")
        reason = item.get("reason")
        if not isinstance(active_path, str) or not active_path:
            raise ValueError(f"{path}: `active_parallel_roots[{index}].path` must be a non-empty string")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"{path}: `active_parallel_roots[{index}].reason` must be a non-empty string")
        normalized_active = Path(active_path).expanduser().resolve(strict=False)
        if normalized_active not in normalized_forbidden_roots:
            raise ValueError(
                f"{path}: `active_parallel_roots[{index}].path` must also appear in `forbidden_roots`: "
                f"{normalized_active}"
            )
        if normalized_active not in normalized_active_roots:
            normalized_active_roots.append(normalized_active)

    handoff_evidence = None
    if isinstance(handoff_evidence_payload, dict):
        handoff_evidence = _load_handoff_evidence(handoff_evidence_payload, path)

    return ExecutionScope(
        expected_execution_root=expected_execution_root,
        expected_branch=expected_branch,
        allowed_write_paths=tuple(_normalize_repo_path(item) for item in allowed_write_paths),
        forbidden_roots=normalized_forbidden_roots,
        active_parallel_roots=tuple(normalized_active_roots),
        execution_mode=execution_mode,
        handoff_evidence=handoff_evidence,
    )


def _git_root(cwd: Path) -> Path | None:
    result = _run_git(["rev-parse", "--show-toplevel"], cwd)
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve(strict=False)


def _current_branch(cwd: Path) -> str | None:
    result = _run_git(["branch", "--show-current"], cwd)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _changed_paths(cwd: Path) -> list[str] | None:
    result = _run_git(["status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd)
    if result.returncode != 0:
        return None

    fields = result.stdout.split("\0")
    if fields and fields[-1] == "":
        fields.pop()

    paths: list[str] = []
    index = 0
    while index < len(fields):
        entry = fields[index]
        if len(entry) < 4:
            index += 1
            continue

        status = entry[:2]
        paths.append(_normalize_repo_path(entry[3:]))
        if status[0] in {"R", "C"} or status[1] in {"R", "C"}:
            index += 1
            if index < len(fields):
                paths.append(_normalize_repo_path(fields[index]))
        index += 1

    return sorted(set(paths))


def _changed_paths_from_file(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    entries = raw.split("\0") if "\0" in raw else raw.splitlines()
    changed_paths = []
    for entry in entries:
        if not entry:
            continue
        changed_paths.append(_normalize_repo_path(entry))
    return sorted(set(changed_paths))


def _path_allowed(path: str, allowed_write_paths: tuple[str, ...]) -> bool:
    return any(path == allowed or (allowed.endswith("/") and path.startswith(allowed)) for allowed in allowed_write_paths)


def _model_family(model: str) -> str:
    normalized = model.strip().lower().replace("_", "-")
    if "/" in normalized:
        normalized = normalized.rsplit("/", 1)[-1]
    if normalized.startswith("gpt-"):
        parts = [part for part in normalized.split("-") if part]
        if len(parts) >= 2:
            major_line = parts[1].split(".", 1)[0]
            if major_line:
                return f"gpt-{major_line}"
        return "gpt"
    if normalized.startswith("claude"):
        return "claude"
    parts = [part for part in normalized.split("-") if part]
    if not parts:
        return normalized
    if len(parts) >= 2 and any(char.isdigit() for char in parts[1]):
        return f"{parts[0]}-{parts[1]}"
    return parts[0]


def _same_model_or_family(planner_model: str, implementer_model: str) -> bool:
    planner = planner_model.strip().lower()
    implementer = implementer_model.strip().lower()
    return planner == implementer or _model_family(planner) == _model_family(implementer)


def _validate_execution_mode(scope: ExecutionScope, now_utc: datetime) -> list[str]:
    if scope.execution_mode == "planning_only":
        return []

    if scope.handoff_evidence is None:
        return [f"execution_mode {scope.execution_mode!r} requires `handoff_evidence.status` == 'accepted'"]

    handoff = scope.handoff_evidence
    failures: list[str] = []
    if handoff.status.lower() != "accepted":
        failures.append("non-planning execution_mode requires `handoff_evidence.status` == 'accepted'")

    if _same_model_or_family(handoff.planner_model, handoff.implementer_model):
        if not handoff.active_exception_ref:
            failures.append(
                "planner/implementer same model or family requires `handoff_evidence.active_exception_ref`"
            )
        if handoff.active_exception_expires_at is None:
            failures.append(
                "planner/implementer same model or family requires `handoff_evidence.active_exception_expires_at`"
            )
        elif handoff.active_exception_expires_at < now_utc:
            failures.append(
                "planner/implementer same model or family requires non-expired "
                "`handoff_evidence.active_exception_expires_at`"
            )

    return failures


def _format_path(path: Path) -> str:
    return str(path)


def _resolve_expected_execution_root(expected_execution_root: str, actual_root: Path) -> Path:
    if expected_execution_root in {".", "{repo_root}"}:
        return actual_root
    return Path(expected_execution_root).expanduser().resolve(strict=False)


def _validate_active_exception_ref(scope: ExecutionScope, actual_root: Path) -> list[str]:
    handoff = scope.handoff_evidence
    if handoff is None or handoff.active_exception_ref is None:
        return []

    exception_path = handoff.active_exception_ref.split("#", 1)[0]
    repo_file = actual_root / exception_path
    if not repo_file.is_file():
        return [
            "handoff_evidence.active_exception_ref must reference an existing repo file path: "
            f"{exception_path}"
        ]
    return []


def check_scope(
    scope: ExecutionScope,
    cwd: Path,
    *,
    changed_files_file: Path | None = None,
    now_utc: datetime | None = None,
) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []

    if now_utc is None:
        now_utc = datetime.now(timezone.utc)

    actual_root = _git_root(cwd)
    if actual_root is None:
        failures.append(f"{cwd}: not inside a git repository")
        return failures, warnings
    expected_root = _resolve_expected_execution_root(scope.expected_execution_root, actual_root)
    if actual_root != expected_root:
        failures.append(
            "execution root mismatch: "
            f"expected {_format_path(expected_root)}, got {_format_path(actual_root)}"
        )

    actual_branch = _current_branch(cwd)
    if actual_branch is None:
        failures.append(f"{actual_root}: could not determine current branch")
    elif actual_branch != scope.expected_branch:
        failures.append(f"branch mismatch: expected {scope.expected_branch}, got {actual_branch or '<detached HEAD>'}")

    failures.extend(_validate_execution_mode(scope, now_utc))
    failures.extend(_validate_active_exception_ref(scope, actual_root))

    changed_paths: list[str] | None = None
    if changed_files_file is None:
        changed_paths = _changed_paths(actual_root)
        if changed_paths is None:
            failures.append(f"{actual_root}: could not read git status")
    else:
        try:
            changed_paths = _changed_paths_from_file(changed_files_file)
        except OSError as exc:
            failures.append(f"could not read changed files from {_format_path(changed_files_file)}: {exc}")

    if changed_paths is not None:
        out_of_scope = [path for path in changed_paths if not _path_allowed(path, scope.allowed_write_paths)]
        if out_of_scope:
            failures.append(
                "changed paths outside allowed_write_paths: "
                + ", ".join(out_of_scope)
                + " (allowed: "
                + ", ".join(scope.allowed_write_paths)
                + ")"
            )

    for forbidden_root in scope.forbidden_roots:
        if not forbidden_root.exists():
            warnings.append(f"forbidden root missing, skipped: {_format_path(forbidden_root)}")
            continue

        forbidden_git_root = _git_root(forbidden_root)
        if forbidden_git_root is None:
            warnings.append(f"forbidden root is not a git repository, skipped: {_format_path(forbidden_root)}")
            continue

        forbidden_changes = _changed_paths(forbidden_git_root)
        if forbidden_changes is None:
            failures.append(f"forbidden root status unreadable: {_format_path(forbidden_git_root)}")
        elif forbidden_changes:
            message = (
                "forbidden root is dirty: "
                f"{_format_path(forbidden_git_root)} has changed paths: "
                + ", ".join(forbidden_changes)
            )
            if forbidden_git_root in scope.active_parallel_roots:
                warnings.append("active parallel root declared; " + message)
            else:
                failures.append(message)

    return failures, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Assert the current checkout matches a declared execution scope.")
    parser.add_argument("--scope", required=True, help="Path to execution scope JSON.")
    parser.add_argument("--changed-files-file", help="Optional file containing changed paths to validate.")
    args = parser.parse_args(argv)

    try:
        scope = _load_scope(Path(args.scope))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL could not load scope: {exc}", file=sys.stderr)
        return 2

    changed_files_file = Path(args.changed_files_file).expanduser() if args.changed_files_file else None
    failures, warnings = check_scope(scope, Path.cwd(), changed_files_file=changed_files_file)
    for warning in warnings:
        print(f"WARN {warning}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    print("PASS execution scope matches declared root, branch, write paths, and forbidden roots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
