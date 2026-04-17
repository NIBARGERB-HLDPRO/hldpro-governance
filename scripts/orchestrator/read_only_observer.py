#!/usr/bin/env python3
"""Read-only governance observer for always-on reporting.

The observer reads existing governance artifacts and writes deterministic reports
under projects/<repo_slug>/reports/. It does not enqueue packets or mutate
governed repositories.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.overlord.governed_repos import GovernedRepo, governed_repos, repos_root

DEFAULT_REPORT_NAME = "latest"
HASH_CHUNK_SIZE = 1024 * 1024


@dataclass(frozen=True)
class ArtifactStatus:
    path: str
    exists: bool
    sha256: str | None
    detail: str


@dataclass(frozen=True)
class RepoReport:
    repo_slug: str
    display_name: str
    generated_at: str
    source_commit: str | None
    health: dict[str, Any]
    stale_knowledge: dict[str, Any]
    planning_gate: dict[str, Any]
    daemon_readiness: dict[str, Any]
    artifacts: dict[str, ArtifactStatus]


def _run_git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, check=False, capture_output=True, text=True)


def _git_commit(path: Path) -> str | None:
    if not path.exists():
        return None
    result = _run_git(path, "rev-parse", "HEAD")
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(HASH_CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _artifact(root: Path, relative_path: str, *, detail: str = "") -> ArtifactStatus:
    path = root / relative_path
    if path.is_file():
        return ArtifactStatus(relative_path, True, _sha256_file(path), detail or "file present")
    if path.is_dir():
        entries = [
            f"{item.relative_to(root).as_posix()}:{_sha256_file(item)}"
            for item in sorted(path.rglob("*"))
            if item.is_file()
        ]
        digest = hashlib.sha256("\n".join(entries).encode("utf-8")).hexdigest()
        return ArtifactStatus(relative_path, True, digest, detail or f"directory present with {len(entries)} files")
    return ArtifactStatus(relative_path, False, None, detail or "missing")


def _count_open_issue_metadata(raw_issue_file: Path) -> int:
    if not raw_issue_file.is_file():
        return 0
    count = 0
    for line in raw_issue_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- #") or stripped.startswith("## #"):
            count += 1
    return count


def _repo_path(repo: GovernedRepo, registry_root: Path) -> Path:
    if repo.repo_slug == "hldpro-governance":
        return registry_root
    return repos_root() / repo.local_path


def _latest_raw_issue_file(registry_root: Path, repo: GovernedRepo) -> Path | None:
    candidates = []
    raw_dir = registry_root / "raw" / "github-issues"
    for token in {repo.display_name, repo.repo_dir_name, repo.repo_slug}:
        candidates.extend(raw_dir.glob(f"*-{token}.md"))
    files = sorted({path for path in candidates if path.is_file()})
    return files[-1] if files else None


def _planning_gate(root: Path, repo: GovernedRepo) -> dict[str, Any]:
    plan_files = sorted((root / "docs" / "plans").glob("*structured-agent-cycle-plan.json"))
    current_issue_plans = [path.name for path in plan_files if "issue-" in path.name]
    return {
        "structured_plan_files": len(plan_files),
        "issue_plan_files": current_issue_plans[-10:],
        "governance_surface_gate": "active" if (root / "scripts/overlord/validate_structured_agent_cycle_plan.py").is_file() else "unknown",
        "code_governance_enabled": repo.enabled("code_governance"),
    }


def _daemon_readiness(repo: GovernedRepo, report_root: Path, launchd_plist: Path) -> dict[str, Any]:
    report_dir = report_root / repo.project_path / "reports"
    return {
        "observer_mode": "read_only",
        "packet_enqueue_enabled": False,
        "report_dir": report_dir.as_posix(),
        "report_dir_within_projects": report_dir.relative_to(report_root).as_posix().startswith("projects/"),
        "launchd_template_present": launchd_plist.is_file(),
        "enabled_subsystems": dict(sorted(repo.enabled_subsystems.items())),
    }


def _repo_report(repo: GovernedRepo, *, registry_root: Path, report_root: Path, generated_at: str) -> RepoReport:
    path = _repo_path(repo, registry_root)
    raw_issue_file = _latest_raw_issue_file(registry_root, repo)

    artifacts = {
        "registry": _artifact(registry_root, "docs/governed_repos.json"),
        "compendium": _artifact(registry_root, "docs/ORG_GOVERNANCE_COMPENDIUM.md"),
        "backlog": _artifact(registry_root, "OVERLORD_BACKLOG.md"),
        "closeouts": _artifact(registry_root, "raw/closeouts", detail="closeout directory fingerprint"),
        "graph_report": _artifact(registry_root, f"{repo.graph_output_path}/GRAPH_REPORT.md"),
        "wiki_index": _artifact(registry_root, f"{repo.wiki_path}/index.md"),
        "raw_issue_feed": _artifact(registry_root, raw_issue_file.relative_to(registry_root).as_posix()) if raw_issue_file else ArtifactStatus("raw/github-issues/<repo>.md", False, None, "metadata feed missing"),
    }
    missing = sorted(name for name, artifact in artifacts.items() if not artifact.exists)
    stale_inputs = sorted(name for name in ("graph_report", "wiki_index", "raw_issue_feed") if not artifacts[name].exists)

    health = {
        "local_path": path.as_posix(),
        "local_path_exists": path.exists(),
        "missing_artifacts": missing,
        "raw_issue_metadata_count": _count_open_issue_metadata(raw_issue_file) if raw_issue_file else 0,
    }
    stale_knowledge = {
        "status": "attention_needed" if stale_inputs else "current_inputs_present",
        "missing_inputs": stale_inputs,
        "graphify_enabled": repo.enabled("graphify"),
        "compendium_enabled": repo.enabled("compendium"),
    }
    return RepoReport(
        repo_slug=repo.repo_slug,
        display_name=repo.display_name,
        generated_at=generated_at,
        source_commit=_git_commit(path),
        health=health,
        stale_knowledge=stale_knowledge,
        planning_gate=_planning_gate(registry_root, repo),
        daemon_readiness=_daemon_readiness(repo, report_root, registry_root / "launchd" / "com.hldpro.governance-observer.plist"),
        artifacts=artifacts,
    )


def _report_to_json(report: RepoReport) -> dict[str, Any]:
    payload = asdict(report)
    payload["artifacts"] = {key: asdict(value) for key, value in report.artifacts.items()}
    return payload


def _write_markdown(path: Path, report: RepoReport) -> None:
    lines = [
        f"# Governance Observer Report — {report.display_name}",
        "",
        f"Generated: {report.generated_at}",
        f"Source commit: `{report.source_commit or 'unavailable'}`",
        f"Observer mode: `{report.daemon_readiness['observer_mode']}`",
        f"Packet enqueue enabled: `{report.daemon_readiness['packet_enqueue_enabled']}`",
        "",
        "## Health",
        "",
        f"- Local path exists: `{report.health['local_path_exists']}`",
        f"- Missing artifacts: `{', '.join(report.health['missing_artifacts']) if report.health['missing_artifacts'] else 'none'}`",
        f"- Raw issue metadata count: `{report.health['raw_issue_metadata_count']}`",
        "",
        "## Stale Knowledge",
        "",
        f"- Status: `{report.stale_knowledge['status']}`",
        f"- Missing inputs: `{', '.join(report.stale_knowledge['missing_inputs']) if report.stale_knowledge['missing_inputs'] else 'none'}`",
        "",
        "## Planning Gate",
        "",
        f"- Structured plan files: `{report.planning_gate['structured_plan_files']}`",
        f"- Governance-surface gate: `{report.planning_gate['governance_surface_gate']}`",
        f"- Code governance enabled for repo: `{report.planning_gate['code_governance_enabled']}`",
        "",
        "## Daemon Readiness",
        "",
        f"- launchd template present: `{report.daemon_readiness['launchd_template_present']}`",
        f"- Report dir: `{report.daemon_readiness['report_dir']}`",
        "",
        "## Artifact Hashes",
        "",
        "| Artifact | Exists | SHA-256 | Detail |",
        "|---|---:|---|---|",
    ]
    for name, artifact in sorted(report.artifacts.items()):
        lines.append(f"| `{name}` | `{artifact.exists}` | `{artifact.sha256 or 'n/a'}` | {artifact.detail} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_reports(reports: list[RepoReport], report_root: Path, report_name: str = DEFAULT_REPORT_NAME) -> list[Path]:
    written: list[Path] = []
    for report in reports:
        report_dir = report_root / "projects" / report.repo_slug / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        json_path = report_dir / f"{report_name}.json"
        markdown_path = report_dir / f"{report_name}.md"
        json_path.write_text(json.dumps(_report_to_json(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        _write_markdown(markdown_path, report)
        written.extend([json_path, markdown_path])
    return written


def build_reports(registry_root: Path, report_root: Path) -> list[RepoReport]:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return [
        _repo_report(repo, registry_root=registry_root, report_root=report_root, generated_at=generated_at)
        for repo in governed_repos(registry_root / "docs" / "governed_repos.json")
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate read-only governance observer reports.")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT, help="Governance repo root.")
    parser.add_argument("--report-root", type=Path, default=REPO_ROOT, help="Root where projects/<repo>/reports is written.")
    parser.add_argument("--report-name", default=DEFAULT_REPORT_NAME, help="Report basename without extension.")
    parser.add_argument("--check-only", action="store_true", help="Build reports and print summary without writing files.")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    report_root = args.report_root.resolve()
    reports = build_reports(repo_root, report_root)
    if args.check_only:
        print(json.dumps({"reports": len(reports), "packet_enqueue_enabled": False}, sort_keys=True))
        return 0

    written = write_reports(reports, report_root, args.report_name)
    print(json.dumps({"reports": len(reports), "written": [path.as_posix() for path in written]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
