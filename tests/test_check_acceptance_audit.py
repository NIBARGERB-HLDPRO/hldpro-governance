import json
import os
import subprocess
from pathlib import Path


SCRIPT_PATH = str(Path(__file__).parent.parent / ".github" / "scripts" / "check_acceptance_audit.py")


def _run_checker(tmp_path: Path, head_ref: str, planning_only: str = "false") -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "HEAD_REF": head_ref, "PLANNING_ONLY": planning_only}
    return subprocess.run(
        ["python3.11", SCRIPT_PATH],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def test_pass_artifact_matching_issue(tmp_path: Path) -> None:
    artifact_dir = tmp_path / "raw" / "acceptance-audits"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_file = artifact_dir / "audit.json"
    artifact_file.write_text(
        json.dumps({"issue_number": 42, "overall_verdict": "PASS"}, indent=2),
        encoding="utf-8",
    )

    result = _run_checker(tmp_path, "issue-42-foo")
    assert result.returncode == 0


def test_pass_artifact_wrong_issue(tmp_path: Path) -> None:
    artifact_dir = tmp_path / "raw" / "acceptance-audits"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_file = artifact_dir / "audit.json"
    artifact_file.write_text(
        json.dumps({"issue_number": 42, "overall_verdict": "PASS"}, indent=2),
        encoding="utf-8",
    )

    result = _run_checker(tmp_path, "issue-99-other")
    assert result.returncode == 1


def test_no_artifact_present(tmp_path: Path) -> None:
    (tmp_path / "raw" / "acceptance-audits").mkdir(parents=True, exist_ok=True)

    result = _run_checker(tmp_path, "issue-42-foo")
    assert result.returncode == 1


def test_non_issue_branch_exempt(tmp_path: Path) -> None:
    result = _run_checker(tmp_path, "main")
    assert result.returncode == 0


def test_planning_only_exempt(tmp_path: Path) -> None:
    result = _run_checker(tmp_path, "issue-42-foo", planning_only="true")
    assert result.returncode == 0


def test_fail_verdict_rejected(tmp_path: Path) -> None:
    artifact_dir = tmp_path / "raw" / "acceptance-audits"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_file = artifact_dir / "audit.json"
    artifact_file.write_text(
        json.dumps({"issue_number": 42, "overall_verdict": "FAIL"}, indent=2),
        encoding="utf-8",
    )

    result = _run_checker(tmp_path, "issue-42-foo")
    assert result.returncode == 1
