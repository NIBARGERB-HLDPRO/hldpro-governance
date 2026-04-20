#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover - dependency bootstrap
    yaml = None
    YAML_IMPORT_ERROR = exc
else:
    YAML_IMPORT_ERROR = None


TOOL_ROOT = Path(__file__).resolve().parent
DEFAULT_PROFILE_NAME = "hldpro-governance"
DEFAULT_PROFILE_PATH = TOOL_ROOT / "profiles" / f"{DEFAULT_PROFILE_NAME}.yml"
DEFAULT_REPORT_ROOT = Path("cache") / "local-ci-gate" / "reports"
AUTHORITATIVE_NOTE = "CI remains authoritative; this local gate only filters preventable failures before push."


class GateError(RuntimeError):
    pass


@dataclass(frozen=True)
class ChangedFiles:
    source: str
    files: tuple[str, ...]
    base_ref: str | None = None
    head_ref: str | None = None


@dataclass(frozen=True)
class CheckSpec:
    id: str
    title: str
    severity: str
    command: tuple[str, ...]
    scope: str = "always"
    paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class Profile:
    name: str
    description: str
    report_root: Path
    requires_dependencies: tuple[str, ...]
    changed_files_base_ref: str | None
    changed_files_head_ref: str | None
    include_untracked: bool
    checks: tuple[CheckSpec, ...]


@dataclass(frozen=True)
class CheckResult:
    check: CheckSpec
    status: str
    matched_changed_files: tuple[str, ...]
    returncode: int | None = None
    stdout: str = ""
    stderr: str = ""
    reason: str = ""
    command: tuple[str, ...] = ()


@dataclass(frozen=True)
class RunReport:
    profile: Profile
    repo_root: Path
    dry_run: bool
    changed_files: ChangedFiles
    results: tuple[CheckResult, ...]
    run_mode: str
    verdict: str
    summary: str
    report_dir: Path
    governance_root: str = ""
    governance_ref: str = ""
    shim_path: str = ""
    argv: tuple[str, ...] = ()
    cwd: str = ""
    runner_path: str = ""


def _load_yaml(path: Path) -> Any:
    if yaml is None:
        raise GateError(f"PyYAML is required to load profiles: {YAML_IMPORT_ERROR}")
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise GateError(f"could not read profile {path}: {exc}") from exc
    except Exception as exc:
        raise GateError(f"could not parse profile {path}: {exc}") from exc


def _normalize_path(value: str) -> str:
    while value.startswith("./"):
        value = value[2:]
    return value


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, check=False, capture_output=True, text=True)


def _repo_root(cwd: Path) -> Path:
    result = _git(cwd, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        raise GateError(result.stderr.strip() or f"{cwd}: not inside a git repository")
    return Path(result.stdout.strip()).resolve()


def _current_branch(repo_root: Path) -> str:
    result = _git(repo_root, "branch", "--show-current")
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _changed_files_from_git(repo_root: Path, base_ref: str | None, head_ref: str | None, include_untracked: bool) -> list[str]:
    files: set[str] = set()

    if base_ref:
        diff_args = ["diff", "--name-only", "--diff-filter=ACMR"]
        if head_ref:
            diff_args.append(f"{base_ref}...{head_ref}")
        else:
            diff_args.append(f"{base_ref}...HEAD")
        result = _git(repo_root, *diff_args)
        if result.returncode != 0:
            raise GateError(result.stderr.strip() or f"could not resolve changed files from {base_ref}")
        files.update(_normalize_path(line) for line in result.stdout.splitlines() if line.strip())

    unstaged = _git(repo_root, "diff", "--name-only", "--diff-filter=ACMR")
    if unstaged.returncode != 0:
        raise GateError(unstaged.stderr.strip() or "could not resolve unstaged changed files")
    files.update(_normalize_path(line) for line in unstaged.stdout.splitlines() if line.strip())

    staged = _git(repo_root, "diff", "--cached", "--name-only", "--diff-filter=ACMR")
    if staged.returncode != 0:
        raise GateError(staged.stderr.strip() or "could not resolve staged changed files")
    files.update(_normalize_path(line) for line in staged.stdout.splitlines() if line.strip())

    if include_untracked:
        untracked = _git(repo_root, "ls-files", "--others", "--exclude-standard")
        if untracked.returncode != 0:
            raise GateError(untracked.stderr.strip() or "could not resolve untracked files")
        files.update(_normalize_path(line) for line in untracked.stdout.splitlines() if line.strip())

    return sorted(files)


def _read_changed_files_file(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    if "\0" in raw:
        entries = raw.split("\0")
    else:
        entries = raw.splitlines()
    return sorted({_normalize_path(entry.strip()) for entry in entries if entry.strip()})


def resolve_changed_files(
    repo_root: Path,
    *,
    explicit_files: list[str] | None = None,
    changed_files_file: Path | None = None,
    base_ref: str | None = None,
    head_ref: str | None = None,
    include_untracked: bool = True,
) -> ChangedFiles:
    if changed_files_file is not None:
        return ChangedFiles(
            source=f"file:{changed_files_file}",
            files=tuple(_read_changed_files_file(changed_files_file)),
            base_ref=base_ref,
            head_ref=head_ref,
        )

    if explicit_files is not None:
        return ChangedFiles(
            source="explicit-args",
            files=tuple(sorted({_normalize_path(item.strip()) for item in explicit_files if item.strip()})),
            base_ref=base_ref,
            head_ref=head_ref,
        )

    files = _changed_files_from_git(repo_root, base_ref, head_ref, include_untracked)
    return ChangedFiles(
        source="git",
        files=tuple(files),
        base_ref=base_ref,
        head_ref=head_ref,
    )


def _is_glob(pattern: str) -> bool:
    return any(token in pattern for token in "*?[]")


def _path_matches(path: str, pattern: str) -> bool:
    normalized_path = _normalize_path(path)
    normalized_pattern = _normalize_path(pattern)
    if not normalized_pattern:
        return False
    if normalized_pattern == "*":
        return True
    if _is_glob(normalized_pattern):
        return fnmatch.fnmatch(normalized_path, normalized_pattern)
    if normalized_pattern.endswith("/"):
        return normalized_path.startswith(normalized_pattern)
    return normalized_path == normalized_pattern or normalized_path.startswith(f"{normalized_pattern}/")


def _check_matches_changed_files(check: CheckSpec, changed_files: tuple[str, ...]) -> tuple[str, ...]:
    if check.scope == "always" or not check.paths:
        return changed_files
    matches = []
    for changed in changed_files:
        if any(_path_matches(changed, pattern) for pattern in check.paths):
            matches.append(changed)
    return tuple(sorted(set(matches)))


def _load_checks(items: Any, path: Path) -> tuple[CheckSpec, ...]:
    if not isinstance(items, list):
        raise GateError(f"{path}: `checks` must be a list")
    checks: list[CheckSpec] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise GateError(f"{path}: checks[{index}] must be a mapping")
        missing = [key for key in ("id", "title", "severity", "command") if key not in item]
        if missing:
            raise GateError(f"{path}: checks[{index}] missing field(s): {', '.join(missing)}")
        check_id = item["id"]
        title = item["title"]
        severity = item["severity"]
        command = item["command"]
        scope = item.get("scope", "always")
        paths = item.get("paths", [])
        if not isinstance(check_id, str) or not check_id:
            raise GateError(f"{path}: checks[{index}].id must be a non-empty string")
        if check_id in seen_ids:
            raise GateError(f"{path}: duplicate check id: {check_id}")
        seen_ids.add(check_id)
        if not isinstance(title, str) or not title:
            raise GateError(f"{path}: checks[{index}].title must be a non-empty string")
        if severity not in {"blocker", "advisory"}:
            raise GateError(f"{path}: checks[{index}].severity must be blocker or advisory")
        if scope not in {"always", "changed"}:
            raise GateError(f"{path}: checks[{index}].scope must be always or changed")
        if not isinstance(command, list) or not command or not all(isinstance(arg, str) and arg for arg in command):
            raise GateError(f"{path}: checks[{index}].command must be a non-empty list of strings")
        if not isinstance(paths, list) or not all(isinstance(arg, str) and arg for arg in paths):
            raise GateError(f"{path}: checks[{index}].paths must be a list of non-empty strings")
        checks.append(
            CheckSpec(
                id=check_id,
                title=title,
                severity=severity,
                command=tuple(command),
                scope=scope,
                paths=tuple(paths),
            )
        )
    return tuple(checks)


def _load_requires_dependencies(profile: dict[str, Any], path: Path) -> tuple[str, ...]:
    raw = profile.get("requires_dependencies", [])
    if not isinstance(raw, list) or not all(isinstance(item, str) and item for item in raw):
        raise GateError(f"{path}: profile.requires_dependencies must be a list of non-empty strings when provided")
    if len(raw) != len(set(raw)):
        raise GateError(f"{path}: profile.requires_dependencies must not contain duplicates")
    return tuple(raw)


def load_profile(path: Path) -> Profile:
    payload = _load_yaml(path)
    if not isinstance(payload, dict):
        raise GateError(f"{path}: profile root must be a mapping")
    profile = payload.get("profile", payload)
    if not isinstance(profile, dict):
        raise GateError(f"{path}: `profile` must be a mapping")
    missing = [key for key in ("name", "description", "checks") if key not in profile]
    if missing:
        raise GateError(f"{path}: profile missing field(s): {', '.join(missing)}")

    name = profile["name"]
    description = profile["description"]
    report_root_raw = profile.get("report_root", "reports")
    changed_files = profile.get("changed_files", {})
    if not isinstance(name, str) or not name:
        raise GateError(f"{path}: profile.name must be a non-empty string")
    if not isinstance(description, str) or not description:
        raise GateError(f"{path}: profile.description must be a non-empty string")
    if not isinstance(report_root_raw, str) or not report_root_raw:
        raise GateError(f"{path}: profile.report_root must be a non-empty string")
    if not isinstance(changed_files, dict):
        raise GateError(f"{path}: profile.changed_files must be a mapping when provided")

    base_ref = changed_files.get("base_ref")
    head_ref = changed_files.get("head_ref")
    include_untracked = changed_files.get("include_untracked", True)
    if base_ref is not None and (not isinstance(base_ref, str) or not base_ref):
        raise GateError(f"{path}: profile.changed_files.base_ref must be a non-empty string when provided")
    if head_ref is not None and (not isinstance(head_ref, str) or not head_ref):
        raise GateError(f"{path}: profile.changed_files.head_ref must be a non-empty string when provided")
    if not isinstance(include_untracked, bool):
        raise GateError(f"{path}: profile.changed_files.include_untracked must be a boolean when provided")

    return Profile(
        name=name,
        description=description,
        report_root=Path(report_root_raw),
        requires_dependencies=_load_requires_dependencies(profile, path),
        changed_files_base_ref=base_ref,
        changed_files_head_ref=head_ref,
        include_untracked=include_untracked,
        checks=_load_checks(profile["checks"], path),
    )


def _format_command(command: tuple[str, ...], context: dict[str, str]) -> tuple[str, ...]:
    return tuple(part.format_map(context) for part in command)


def _branch_issue_number(branch_name: str) -> str:
    match = re.search(r"(?:^|/)issue-(\d+)(?:[-_/]|$)", branch_name)
    return match.group(1) if match else ""


def _scope_lane_claim_issue(path: Path) -> str:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GateError(f"could not read execution scope {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise GateError(f"{path}: execution scope must be a JSON object")
    lane_claim = payload.get("lane_claim")
    if not isinstance(lane_claim, dict):
        return ""
    issue_number = lane_claim.get("issue_number")
    if not isinstance(issue_number, int) or issue_number <= 0:
        raise GateError(f"{path}: lane_claim.issue_number must be a positive integer")
    return str(issue_number)


def _resolve_execution_scope(repo_root: Path, branch_name: str) -> str:
    issue_number = _branch_issue_number(branch_name)
    if not issue_number:
        return ""
    scope_root = repo_root / "raw" / "execution-scopes"
    implementation_matches = sorted(scope_root.glob(f"*issue-{issue_number}*implementation*.json"))
    planning_matches = sorted(scope_root.glob(f"*issue-{issue_number}*planning*.json"))
    matches = implementation_matches or planning_matches
    if len(matches) > 1:
        raise GateError(f"multiple execution scopes match issue-{issue_number}: {', '.join(str(item) for item in matches)}")
    if not matches:
        return ""
    claimed_matches = [path for path in matches if _scope_lane_claim_issue(path) == issue_number]
    if len(claimed_matches) > 1:
        raise GateError(
            f"multiple claimed execution scopes match issue-{issue_number}: "
            + ", ".join(str(item) for item in claimed_matches)
        )
    if not claimed_matches:
        raise GateError(
            f"execution scope for issue-{issue_number} must include lane_claim.issue_number={issue_number}"
        )
    return claimed_matches[0].relative_to(repo_root).as_posix()


def _command_context(
    repo_root: Path,
    profile: Profile,
    changed_files: ChangedFiles,
    report_dir: Path,
) -> dict[str, str]:
    branch_name = _current_branch(repo_root)
    return {
        "repo_root": str(repo_root),
        "tool_root": str(TOOL_ROOT),
        "report_dir": str(report_dir),
        "changed_files_file": str(report_dir / "changed-files.txt"),
        "changed_files_csv": ",".join(changed_files.files),
        "changed_files_count": str(len(changed_files.files)),
        "changed_files_source": changed_files.source,
        "profile_name": profile.name,
        "branch_name": branch_name,
        "execution_scope": _resolve_execution_scope(repo_root, branch_name),
        "base_ref": changed_files.base_ref or profile.changed_files_base_ref or "",
        "head_ref": changed_files.head_ref or profile.changed_files_head_ref or "HEAD",
    }


def _exec_command(command: tuple[str, ...], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)


def run_checks(
    repo_root: Path,
    profile: Profile,
    changed_files: ChangedFiles,
    *,
    dry_run: bool,
    report_dir: Path | None = None,
    governance_root: str = "",
    governance_ref: str = "",
    shim_path: str = "",
    argv: tuple[str, ...] = (),
    cwd: str = "",
    runner_path: str = "",
) -> RunReport:
    output_dir = report_dir or _default_report_dir(repo_root, profile, changed_files)
    output_dir.mkdir(parents=True, exist_ok=True)
    changed_files_path = output_dir / "changed-files.txt"
    changed_files_path.write_text("\n".join(changed_files.files) + ("\n" if changed_files.files else ""), encoding="utf-8")

    context = _command_context(repo_root, profile, changed_files, output_dir)
    results: list[CheckResult] = []
    for check in profile.checks:
        matched = _check_matches_changed_files(check, changed_files.files)
        if check.scope == "changed" and not matched:
            results.append(
                CheckResult(
                    check=check,
                    status="skipped",
                    matched_changed_files=(),
                    reason="no changed files matched this check",
                    command=_format_command(check.command, context),
                )
            )
            continue

        command = _format_command(check.command, context)
        if dry_run:
            results.append(
                CheckResult(
                    check=check,
                    status="planned",
                    matched_changed_files=matched,
                    reason="dry-run",
                    command=command,
                )
            )
            continue

        completed = _exec_command(command, repo_root)
        status = "passed" if completed.returncode == 0 else f"{check.severity}_failed"
        results.append(
            CheckResult(
                check=check,
                status=status,
                matched_changed_files=matched,
                returncode=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
                reason="" if completed.returncode == 0 else "command exited non-zero",
                command=command,
            )
        )

    verdict = _summarize_verdict(results, dry_run=dry_run)
    run_mode = "dry-run" if dry_run else "run"
    summary = _build_summary(profile, changed_files, results, verdict, dry_run)
    report = RunReport(
        profile=profile,
        repo_root=repo_root,
        dry_run=dry_run,
        changed_files=changed_files,
        results=tuple(results),
        run_mode=run_mode,
        verdict=verdict,
        summary=summary,
        report_dir=output_dir,
        governance_root=governance_root,
        governance_ref=governance_ref,
        shim_path=shim_path,
        argv=argv,
        cwd=cwd,
        runner_path=runner_path,
    )
    _write_report(report)
    return report


def _summarize_verdict(results: list[CheckResult], *, dry_run: bool) -> str:
    if dry_run:
        if any(result.status == "planned" for result in results):
            return "planned"
        if any(result.status == "skipped" for result in results):
            return "subset"
        return "pass"
    blocker_failures = [result for result in results if result.status == "blocker_failed"]
    advisory_failures = [result for result in results if result.status == "advisory_failed"]
    if blocker_failures:
        return "blocker"
    if advisory_failures:
        return "advisory"
    return "pass"


def _build_summary(profile: Profile, changed_files: ChangedFiles, results: list[CheckResult], verdict: str, dry_run: bool) -> str:
    total = len(results)
    blockers = sum(1 for result in results if result.status == "blocker_failed")
    advisories = sum(1 for result in results if result.status == "advisory_failed")
    skipped = sum(1 for result in results if result.status == "skipped")
    planned = sum(1 for result in results if result.status == "planned")
    mode = "dry-run" if dry_run else "live"
    run_scope = "subset" if skipped or planned else "full-scope"
    return (
        f"profile={profile.name} changed_files={len(changed_files.files)} source={changed_files.source} "
        f"mode={mode} scope={run_scope} total_checks={total} blockers={blockers} advisories={advisories} "
        f"skipped={skipped} planned={planned} verdict={verdict}. {AUTHORITATIVE_NOTE}"
    )


def _report_path(report_dir: Path, suffix: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return report_dir / f"local-ci-{timestamp}{suffix}"


def _write_report(report: RunReport) -> None:
    payload = {
        "profile": {
            "name": report.profile.name,
            "description": report.profile.description,
            "report_root": str(report.profile.report_root),
            "requires_dependencies": list(report.profile.requires_dependencies),
            "changed_files_base_ref": report.profile.changed_files_base_ref,
            "changed_files_head_ref": report.profile.changed_files_head_ref,
            "include_untracked": report.profile.include_untracked,
            "checks": [
                {
                    "id": check.id,
                    "title": check.title,
                    "severity": check.severity,
                    "scope": check.scope,
                    "paths": list(check.paths),
                }
                for check in report.profile.checks
            ],
        },
        "repo_root": str(report.repo_root),
        "invocation": {
            "governance_root": report.governance_root,
            "governance_ref": report.governance_ref,
            "shim_path": report.shim_path,
            "argv": list(report.argv),
            "cwd": report.cwd,
            "runner_path": report.runner_path,
        },
        "dry_run": report.dry_run,
        "changed_files": {
            "source": report.changed_files.source,
            "base_ref": report.changed_files.base_ref,
            "head_ref": report.changed_files.head_ref,
            "files": list(report.changed_files.files),
        },
        "verdict": report.verdict,
        "summary": report.summary,
        "results": [
            {
                "id": result.check.id,
                "title": result.check.title,
                "severity": result.check.severity,
                "scope": result.check.scope,
                "paths": list(result.check.paths),
                "status": result.status,
                "matched_changed_files": list(result.matched_changed_files),
                "returncode": result.returncode,
                "command": list(result.command),
                "stdout": result.stdout,
                "stderr": result.stderr,
                "reason": result.reason,
            }
            for result in report.results
        ],
    }

    report_json = _report_path(report.report_dir, ".json")
    report_txt = _report_path(report.report_dir, ".txt")
    report_json.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    report_txt.write_text(render_report(report), encoding="utf-8")


def render_report(report: RunReport) -> str:
    lines = [
        f"Local CI Gate profile: {report.profile.name}",
        f"Repo root: {report.repo_root}",
        f"Mode: {'dry-run' if report.dry_run else 'run'}",
        f"Changed files ({len(report.changed_files.files)}, source={report.changed_files.source}):",
    ]
    if report.governance_root or report.governance_ref or report.shim_path:
        lines.append("Invocation:")
        lines.append(f"  governance_root: {report.governance_root or '<unset>'}")
        lines.append(f"  governance_ref: {report.governance_ref or '<unset>'}")
        lines.append(f"  shim_path: {report.shim_path or '<unset>'}")
        lines.append(f"  cwd: {report.cwd or '<unset>'}")
        lines.append(f"  runner_path: {report.runner_path or '<unset>'}")
    if report.changed_files.files:
        lines.extend(f"  - {item}" for item in report.changed_files.files)
    else:
        lines.append("  - <none>")
    lines.append(f"Verdict: {report.verdict.upper()}")
    lines.append(AUTHORITATIVE_NOTE)
    lines.append("Checks:")
    for result in report.results:
        lines.append(f"  - [{result.check.severity}] {result.check.id}: {result.status}")
        if result.status == "planned":
            lines.append(f"    command: {' '.join(result.command)}")
        elif result.status == "skipped":
            lines.append(f"    reason: {result.reason}")
        else:
            lines.append(f"    command: {' '.join(result.command)}")
            lines.append(f"    returncode: {result.returncode}")
    lines.append(f"Summary: {report.summary}")
    return "\n".join(lines) + "\n"


def _default_report_dir(repo_root: Path, profile: Profile, changed_files: ChangedFiles) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = f"{profile.name}-{changed_files.source.replace(':', '-')}"
    base = profile.report_root if profile.report_root.is_absolute() else (repo_root / profile.report_root)
    return (base / f"{timestamp}-{suffix}").resolve()


def _print_report(report: RunReport) -> None:
    print(render_report(report), end="")


def _check_exit_code(report: RunReport) -> int:
    if report.verdict == "blocker":
        return 1
    return 0


def _resolve_profile_path(args: argparse.Namespace) -> Path:
    if args.profile_file:
        return Path(args.profile_file).expanduser().resolve()
    if args.profile and ("/" in args.profile or args.profile.endswith((".yml", ".yaml"))):
        return Path(args.profile).expanduser().resolve()
    return (TOOL_ROOT / "profiles" / f"{args.profile or DEFAULT_PROFILE_NAME}.yml").resolve()


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the governance-owned local CI gate runner.",
        epilog=f"{AUTHORITATIVE_NOTE} Reports are local-only and should use a gitignored report directory.",
    )
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect")
    parser.add_argument("--governance-root", help="Governance checkout path recorded by a managed shim")
    parser.add_argument("--governance-ref", help="Governance ref recorded by a managed shim")
    parser.add_argument("--shim-path", help="Managed shim path that invoked this runner")
    parser.add_argument("--profile", default=DEFAULT_PROFILE_NAME, help="Profile name or profile file path")
    parser.add_argument("--profile-file", help="Explicit profile file path")
    parser.add_argument("--report-dir", help="Override the local report output directory")
    parser.add_argument("--changed-files-file", type=Path, help="Read changed files from a file instead of git")
    parser.add_argument("--changed-file", action="append", dest="changed_files", help="Explicit changed file path; may be repeated")
    parser.add_argument("--base-ref", help="Base ref for changed-file resolution")
    parser.add_argument("--head-ref", help="Head ref for changed-file resolution")
    parser.add_argument("--dry-run", action="store_true", help="Plan checks without executing them")
    parser.add_argument("--json", action="store_true", help="Print the final report JSON to stdout")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    if effective_argv and effective_argv[0] == "run":
        effective_argv = effective_argv[1:]
    args = parser.parse_args(effective_argv)

    try:
        repo_root = _repo_root(Path(args.repo_root).resolve())
        profile_path = _resolve_profile_path(args)
        profile = load_profile(profile_path)
        changed_files = resolve_changed_files(
            repo_root,
            explicit_files=args.changed_files,
            changed_files_file=args.changed_files_file,
            base_ref=args.base_ref or profile.changed_files_base_ref,
            head_ref=args.head_ref or profile.changed_files_head_ref,
            include_untracked=profile.include_untracked,
        )
        report_dir = Path(args.report_dir).expanduser().resolve() if args.report_dir else None
        report = run_checks(
            repo_root,
            profile,
            changed_files,
            dry_run=args.dry_run,
            report_dir=report_dir,
            governance_root=args.governance_root or "",
            governance_ref=args.governance_ref or "",
            shim_path=args.shim_path or "",
            argv=tuple(effective_argv),
            cwd=os.getcwd(),
            runner_path=str(Path(sys.argv[0]).resolve()),
        )

        _print_report(report)
        if args.json:
            print(json.dumps(
                {
                    "profile": profile.name,
                    "verdict": report.verdict,
                    "summary": report.summary,
                    "changed_files": list(changed_files.files),
                    "report_dir": str(report.report_dir),
                    "invocation": {
                        "governance_root": report.governance_root,
                        "governance_ref": report.governance_ref,
                        "shim_path": report.shim_path,
                        "argv": list(report.argv),
                        "cwd": report.cwd,
                        "runner_path": report.runner_path,
                    },
                },
                indent=2,
            ))
        return _check_exit_code(report)
    except GateError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
