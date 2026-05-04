"""Tests for check_acceptance_audit.py — functional acceptance audit CI gate."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / ".github" / "scripts" / "check_acceptance_audit.py"


def run_check(tmp_path, branch, audit_dir=None, planning_only=False, artifacts=None):
    """Helper: run check_acceptance_audit.py with given args against a temp audit dir."""
    if audit_dir is None:
        audit_dir = tmp_path / "raw" / "acceptance-audits"
    if artifacts:
        audit_dir.mkdir(parents=True, exist_ok=True)
        for name, content in artifacts.items():
            (audit_dir / name).write_text(json.dumps(content))
    cmd = [sys.executable, str(SCRIPT), "--branch", branch, "--audit-dir", str(audit_dir)]
    if planning_only:
        cmd.append("--planning-only")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


def test_pass_artifact_present_and_matching(tmp_path):
    """PASS artifact with matching issue_number and overall_verdict=PASS → exits 0."""
    result = run_check(
        tmp_path,
        branch="issue-659-my-feature",
        artifacts={"2026-05-03-659-audit.json": {"issue_number": 659, "overall_verdict": "PASS"}},
    )
    assert result.returncode == 0
    assert "PASS" in result.stdout or "notice" in result.stdout.lower()


def test_no_audit_dir_exits_1(tmp_path):
    """Non-existent audit dir → exits 1."""
    missing_dir = tmp_path / "nonexistent"
    result = run_check(tmp_path, branch="issue-659-my-feature", audit_dir=missing_dir)
    assert result.returncode == 1
    assert "::error::" in result.stdout


def test_audit_dir_exists_but_no_matching_issue(tmp_path):
    """Audit dir exists but no artifact for the branch issue → exits 1."""
    result = run_check(
        tmp_path,
        branch="issue-999-other-issue",
        artifacts={"2026-05-03-659-audit.json": {"issue_number": 659, "overall_verdict": "PASS"}},
    )
    assert result.returncode == 1
    assert "::error::" in result.stdout


def test_non_issue_branch_exempt(tmp_path):
    """Non-issue branch (e.g. chore/foo) → exits 0 (exempt)."""
    result = run_check(tmp_path, branch="chore/update-deps")
    assert result.returncode == 0
    assert "notice" in result.stdout.lower()


def test_planning_only_flag_exempt(tmp_path):
    """planning_only flag → exits 0 regardless of audit artifacts."""
    result = run_check(tmp_path, branch="issue-659-my-feature", planning_only=True)
    assert result.returncode == 0
    assert "notice" in result.stdout.lower()
