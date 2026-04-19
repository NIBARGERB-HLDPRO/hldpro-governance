#!/usr/bin/env python3
"""Deterministic PentAGI freshness and trigger status for overlord sweep."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from governed_repos import DEFAULT_REGISTRY, GovernedRepo, governed_repos


DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")
DEFAULT_RUNNER = Path("scripts/pentagi-run.sh")
FRESH_DAYS = 30


@dataclass
class PentagiStatus:
    repo: str
    display_name: str
    security_tier: str
    repo_path: str
    source_kind: str
    commit: str
    latest_report: str | None
    latest_report_date: str | None
    age_days: int | None
    freshness: str
    trigger_status: str
    status_label: str
    detail: str
    expected_runner: str


def _parse_date(raw: str) -> date | None:
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        return None


def _report_date(path: Path) -> date | None:
    match = DATE_RE.search(path.name)
    if not match:
        return None
    return _parse_date(match.group(1))


def _git_commit(repo_path: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo_path), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _git_tracked_paths(repo_path: Path, pattern: str) -> list[Path] | None:
    try:
        subprocess.check_output(
            ["git", "-C", str(repo_path), "rev-parse", "--is-inside-work-tree"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    try:
        raw = subprocess.check_output(
            ["git", "-C", str(repo_path), "ls-files", "-z", "--", pattern],
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return []

    return [repo_path / item.decode("utf-8") for item in raw.split(b"\0") if item]


def _git_path_is_tracked(repo_path: Path, relpath: Path) -> bool | None:
    tracked = _git_tracked_paths(repo_path, str(relpath))
    if tracked is None:
        return None
    return bool(tracked)


def _candidate_paths(repos_root: Path, repo: GovernedRepo) -> list[tuple[str, Path]]:
    return [
        ("ci_checkout_path", repos_root / repo.ci_checkout_path),
        ("repo_dir_name", repos_root / repo.repo_dir_name),
        ("local_path", repos_root / repo.local_path),
    ]


def resolve_repo_path(repos_root: Path, repo: GovernedRepo) -> tuple[str, Path]:
    for source_kind, path in _candidate_paths(repos_root, repo):
        if path.exists():
            return source_kind, path
    source_kind, path = _candidate_paths(repos_root, repo)[0]
    return source_kind, path


def latest_pentagi_report(repo_path: Path) -> tuple[Path | None, date | None]:
    report_dir = repo_path / "docs" / "security-reports"
    tracked = _git_tracked_paths(repo_path, "docs/security-reports/pentagi-*")
    paths = tracked if tracked is not None else list(report_dir.glob("pentagi-*"))
    candidates: list[tuple[date, Path]] = []
    for path in paths:
        if not path.is_file():
            continue
        parsed = _report_date(path)
        if parsed is not None:
            candidates.append((parsed, path))
    if not candidates:
        return None, None
    latest_date, latest_path = max(candidates, key=lambda item: (item[0], item[1].name))
    return latest_path, latest_date


def pentagi_repos(registry_path: Path) -> list[GovernedRepo]:
    return [
        repo
        for repo in governed_repos(registry_path)
        if repo.enabled("sweep") and "pentagi" in repo.security_tier.lower()
    ]


def evaluate_repo(
    repo: GovernedRepo,
    *,
    repos_root: Path,
    today: date,
    token_present: bool,
    execute: bool,
    runner_relpath: Path = DEFAULT_RUNNER,
) -> PentagiStatus:
    source_kind, repo_path = resolve_repo_path(repos_root, repo)
    expected_runner = repo_path / runner_relpath
    latest_report, latest_date = latest_pentagi_report(repo_path)
    commit = _git_commit(repo_path) if repo_path.exists() else "missing"

    age_days: int | None = None
    freshness = "missing"
    if latest_date is not None:
        age_days = (today - latest_date).days
        freshness = "fresh" if age_days <= FRESH_DAYS else "stale"

    if not repo_path.exists():
        trigger_status = "SKIPPED"
        detail = f"missing audited repo path: {repo_path}"
    elif freshness == "fresh":
        trigger_status = "NOT_NEEDED"
        detail = "fresh PentAGI report is within 30 days"
    elif not token_present:
        trigger_status = "SKIPPED"
        detail = "missing PENTAGI_API_TOKEN"
    elif not expected_runner.is_file() or _git_path_is_tracked(repo_path, runner_relpath) is False:
        trigger_status = "SKIPPED"
        detail = f"missing PentAGI runner: {runner_relpath}"
    elif not execute:
        trigger_status = "WOULD_RUN"
        detail = f"would run {runner_relpath} baseline"
    else:
        completed = subprocess.run(
            ["bash", str(runner_relpath), "baseline"],
            cwd=repo_path,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if completed.returncode == 0:
            trigger_status = "TRIGGERED"
            detail = f"runner completed: {runner_relpath} baseline"
        else:
            trigger_status = "FAILED"
            output = " ".join(completed.stdout.split())[:240]
            detail = f"runner failed ({completed.returncode}): {output}"

    status_label = trigger_status
    if trigger_status in {"SKIPPED", "FAILED"}:
        status_label = f"{trigger_status}: {detail}"

    return PentagiStatus(
        repo=repo.repo_dir_name,
        display_name=repo.display_name,
        security_tier=repo.security_tier,
        repo_path=str(repo_path),
        source_kind=source_kind,
        commit=commit,
        latest_report=str(latest_report.relative_to(repo_path)) if latest_report else None,
        latest_report_date=latest_date.isoformat() if latest_date else None,
        age_days=age_days,
        freshness=freshness,
        trigger_status=trigger_status,
        status_label=status_label,
        detail=detail,
        expected_runner=str(runner_relpath),
    )


def build_payload(statuses: list[PentagiStatus], *, repos_root: Path, today: date, execute: bool) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "generated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "date": today.isoformat(),
        "repos_root": str(repos_root),
        "execute": execute,
        "freshness_window_days": FRESH_DAYS,
        "statuses": [asdict(status) for status in statuses],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "| Repo | Source | Commit | Latest Report | Age | Freshness | Trigger Status | Detail |",
        "|---|---|---|---|---:|---|---|---|",
    ]
    for row in payload["statuses"]:
        commit = row["commit"]
        if commit not in ("unknown", "missing"):
            commit = commit[:7]
        latest = row["latest_report_date"] or "none"
        age = "N/A" if row["age_days"] is None else str(row["age_days"])
        detail = str(row["detail"]).replace("|", "\\|")
        lines.append(
            f"| {row['display_name']} | {row['source_kind']} | {commit} | {latest} | "
            f"{age} | {row['freshness']} | {row['status_label']} | {detail} |"
        )
    lines.append("")
    lines.append(f"Source root: `{payload['repos_root']}`")
    lines.append("Dashboard consumers must use this payload for PentAGI freshness; untracked canonical checkout reports do not count for sweep freshness.")
    return "\n".join(lines) + "\n"


def write_optional(path: str | None, content: str) -> None:
    if not path:
        return
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repos-root", default="repos", help="Audited checkout root used by sweep.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="Governed repo registry path.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Sweep date in YYYY-MM-DD.")
    parser.add_argument("--output-json", help="Optional JSON output path.")
    parser.add_argument("--output-md", help="Optional Markdown output path.")
    parser.add_argument("--execute", action="store_true", help="Run repo-local PentAGI runner when stale/missing and prerequisites exist.")
    parser.add_argument("--runner", default=str(DEFAULT_RUNNER), help="Repo-relative PentAGI runner path.")
    args = parser.parse_args()

    today = _parse_date(args.date)
    if today is None:
        parser.error("--date must be YYYY-MM-DD")

    repos_root = Path(args.repos_root)
    registry_path = Path(args.registry)
    token_present = bool(os.environ.get("PENTAGI_API_TOKEN"))
    runner_relpath = Path(args.runner)

    statuses = [
        evaluate_repo(
            repo,
            repos_root=repos_root,
            today=today,
            token_present=token_present,
            execute=args.execute,
            runner_relpath=runner_relpath,
        )
        for repo in pentagi_repos(registry_path)
    ]
    payload = build_payload(statuses, repos_root=repos_root, today=today, execute=args.execute)
    json_text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    md_text = render_markdown(payload)

    write_optional(args.output_json, json_text)
    write_optional(args.output_md, md_text)
    if not args.output_json and not args.output_md:
        print(md_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
