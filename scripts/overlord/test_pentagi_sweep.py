from __future__ import annotations

import json
import subprocess
from pathlib import Path

from pentagi_sweep import main


def _registry(tmp_path: Path) -> Path:
    payload = {
        "version": 1,
        "repositories": [
            {
                "repo_slug": "ais",
                "display_name": "AIS",
                "repo_dir_name": "ai-integration-services",
                "github_repo": "NIBARGERB-HLDPRO/ai-integration-services",
                "local_path": "ai-integration-services",
                "ci_checkout_path": "repos/ai-integration-services",
                "graph_output_path": "graphify-out/ai-integration-services",
                "wiki_path": "wiki/ai-integration-services",
                "project_path": "projects/ai-integration-services",
                "governance_tier": "full",
                "security_tier": "full-pentagi",
                "lifecycle_status": "active",
                "governance_status": "governed",
                "classification": {},
                "description": "test",
                "enabled_subsystems": {
                    "sweep": True,
                    "graphify": False,
                    "metrics": False,
                    "memory_integrity": False,
                    "codex_ingestion": False,
                    "compendium": False,
                    "raw_feed_sync": False,
                    "code_governance": False,
                },
            },
            {
                "repo_slug": "kt",
                "display_name": "KT",
                "repo_dir_name": "knocktracker",
                "github_repo": "NIBARGERB-HLDPRO/knocktracker",
                "local_path": "knocktracker",
                "ci_checkout_path": "repos/knocktracker",
                "graph_output_path": "graphify-out/knocktracker",
                "wiki_path": "wiki/knocktracker",
                "project_path": "projects/knocktracker",
                "governance_tier": "standard",
                "security_tier": "baseline",
                "lifecycle_status": "active",
                "governance_status": "governed",
                "classification": {},
                "description": "test",
                "enabled_subsystems": {
                    "sweep": True,
                    "graphify": False,
                    "metrics": False,
                    "memory_integrity": False,
                    "codex_ingestion": False,
                    "compendium": False,
                    "raw_feed_sync": False,
                    "code_governance": False,
                },
            },
        ],
    }
    path = tmp_path / "registry.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _repo(root: Path) -> Path:
    repo = root / "repos" / "ai-integration-services"
    (repo / "docs" / "security-reports").mkdir(parents=True)
    subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    return repo


def _track(repo: Path, *paths: Path) -> None:
    subprocess.run(["git", "add", *(str(path.relative_to(repo)) for path in paths)], cwd=repo, check=True)


def _run(tmp_path: Path, monkeypatch, *extra: str) -> dict:
    output = tmp_path / "pentagi.json"
    argv = [
        "pentagi_sweep.py",
        "--registry",
        str(_registry(tmp_path)),
        "--repos-root",
        str(tmp_path),
        "--date",
        "2026-04-19",
        "--output-json",
        str(output),
    ]
    argv.extend(extra)
    monkeypatch.setattr("sys.argv", argv)
    assert main() == 0
    return json.loads(output.read_text(encoding="utf-8"))


def test_missing_report_skips_with_missing_token(tmp_path, monkeypatch):
    _repo(tmp_path)
    monkeypatch.delenv("PENTAGI_API_TOKEN", raising=False)

    payload = _run(tmp_path, monkeypatch)

    assert len(payload["statuses"]) == 1
    status = payload["statuses"][0]
    assert status["freshness"] == "missing"
    assert status["trigger_status"] == "SKIPPED"
    assert status["detail"] == "missing PENTAGI_API_TOKEN"
    assert status["status_label"] == "SKIPPED: missing PENTAGI_API_TOKEN"


def test_stale_report_skips_with_missing_token(tmp_path, monkeypatch):
    repo = _repo(tmp_path)
    report = repo / "docs" / "security-reports" / "pentagi-2026-03-01-baseline.md"
    report.write_text("old", encoding="utf-8")
    _track(repo, report)
    monkeypatch.delenv("PENTAGI_API_TOKEN", raising=False)

    status = _run(tmp_path, monkeypatch)["statuses"][0]

    assert status["freshness"] == "stale"
    assert status["age_days"] == 49
    assert status["trigger_status"] == "SKIPPED"
    assert status["detail"] == "missing PENTAGI_API_TOKEN"


def test_missing_runner_is_explicit_when_token_exists(tmp_path, monkeypatch):
    _repo(tmp_path)
    monkeypatch.setenv("PENTAGI_API_TOKEN", "token")

    status = _run(tmp_path, monkeypatch)["statuses"][0]

    assert status["trigger_status"] == "SKIPPED"
    assert status["detail"] == "missing PentAGI runner: scripts/pentagi-run.sh"
    assert status["status_label"] == "SKIPPED: missing PentAGI runner: scripts/pentagi-run.sh"


def test_fresh_report_does_not_trigger(tmp_path, monkeypatch):
    repo = _repo(tmp_path)
    report = repo / "docs" / "security-reports" / "pentagi-2026-04-10-baseline.md"
    report.write_text("fresh", encoding="utf-8")
    _track(repo, report)
    monkeypatch.setenv("PENTAGI_API_TOKEN", "token")

    status = _run(tmp_path, monkeypatch)["statuses"][0]

    assert status["freshness"] == "fresh"
    assert status["age_days"] == 9
    assert status["trigger_status"] == "NOT_NEEDED"


def test_runner_would_run_without_execute(tmp_path, monkeypatch):
    repo = _repo(tmp_path)
    runner = repo / "scripts" / "pentagi-run.sh"
    runner.parent.mkdir()
    runner.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
    _track(repo, runner)
    monkeypatch.setenv("PENTAGI_API_TOKEN", "token")

    status = _run(tmp_path, monkeypatch)["statuses"][0]

    assert status["trigger_status"] == "WOULD_RUN"
    assert status["detail"] == "would run scripts/pentagi-run.sh baseline"


def test_untracked_fresh_report_does_not_count_for_audited_ref(tmp_path, monkeypatch):
    repo = _repo(tmp_path)
    (repo / "docs" / "security-reports" / "pentagi-2026-04-10-baseline.md").write_text("untracked", encoding="utf-8")
    monkeypatch.delenv("PENTAGI_API_TOKEN", raising=False)

    status = _run(tmp_path, monkeypatch)["statuses"][0]

    assert status["freshness"] == "missing"
    assert status["latest_report"] is None
    assert status["trigger_status"] == "SKIPPED"
    assert status["status_label"] == "SKIPPED: missing PENTAGI_API_TOKEN"


def test_execute_runs_tracked_runner(tmp_path, monkeypatch):
    repo = _repo(tmp_path)
    runner = repo / "scripts" / "pentagi-run.sh"
    runner.parent.mkdir()
    runner.write_text("#!/usr/bin/env bash\necho triggered\n", encoding="utf-8")
    _track(repo, runner)
    monkeypatch.setenv("PENTAGI_API_TOKEN", "token")

    status = _run(tmp_path, monkeypatch, "--execute")["statuses"][0]

    assert status["trigger_status"] == "TRIGGERED"
    assert status["detail"] == "runner completed: scripts/pentagi-run.sh baseline"


def test_markdown_records_same_source_root_for_dashboard_consumers(tmp_path, monkeypatch):
    _repo(tmp_path)
    output = tmp_path / "pentagi.md"
    monkeypatch.delenv("PENTAGI_API_TOKEN", raising=False)
    monkeypatch.setattr(
        "sys.argv",
        [
            "pentagi_sweep.py",
            "--registry",
            str(_registry(tmp_path)),
            "--repos-root",
            str(tmp_path),
            "--date",
            "2026-04-19",
            "--output-md",
            str(output),
        ],
    )

    assert main() == 0
    text = output.read_text(encoding="utf-8")
    assert f"Source root: `{tmp_path}`" in text
    assert "Dashboard consumers must use this payload" in text
