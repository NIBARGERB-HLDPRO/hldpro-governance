"""Tests for fail-closed behaviour when BASE_SHA is empty (AC3).

These tests assert that the gate logic in governance-check.yml,
require-cross-review.yml, and check-arch-tier.yml returns exit 1 when
BASE_SHA is empty — simulating push events or stale-ref conditions where
no PR context is available.

Strategy
--------
* For the Python-extracted logic (validate_cross_review_evidence), test the
  function directly.
* For the bash gates embedded in YAML workflows, parse the real workflow YAML
  with PyYAML, extract the run: block from the step that performs the
  BASE_SHA context check, strip GitHub Actions template expressions
  (${{ ... }}) so the script is executable in subprocess, then run with an
  empty BASE_SHA/HEAD_SHA environment and assert returncode == 1.
"""
from __future__ import annotations

import importlib.util
import os
import re
import subprocess
from pathlib import Path

import pytest
import yaml


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"


def _load_validate_module():
    module_path = REPO_ROOT / "scripts" / "overlord" / "validate_cross_review_evidence.py"
    if not module_path.exists():
        pytest.skip(f"Module not found at {module_path}")
    spec = importlib.util.spec_from_file_location("validate_cross_review_evidence", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _strip_gha_templates(script: str, env_passthrough: bool = False) -> str:
    """Replace GitHub Actions ${{ expr }} template expressions.

    When ``env_passthrough`` is False (default — empty-context scenario):
      Replace every ${{ expr }} with empty string, replicating GitHub Actions
      runtime behavior when no PR context or inputs are present. Used for the
      fail-closed (exit 1) tests.

    When ``env_passthrough`` is True (valid-context scenario):
      Instead of substituting an empty string, drop the entire shell assignment
      line that contains a ${{ }} expression (e.g.  ``BASE_SHA="${{ ... }}"``).
      The caller is expected to supply BASE_SHA / HEAD_SHA / GITHUB_WORKSPACE
      via the subprocess env dict. Lines that purely call helper scripts or
      perform git operations are preserved intact.
    """
    if not env_passthrough:
        return re.sub(r"\$\{\{[^}]*\}\}", "", script)
    # Drop any line whose only non-whitespace content (after the '=') is a GHA
    # expression — those are SHA-assignment lines we replace with env injection.
    result_lines = []
    for line in script.splitlines(keepends=True):
        # Match: optional leading whitespace, VAR="${{ ... }}" or VAR=${{ ... }}
        if re.match(r'^\s*\w+=\s*"\s*\$\{\{[^}]*\}\}\s*"\s*$', line):
            continue
        if re.match(r'^\s*\w+=\s*\$\{\{[^}]*\}\}\s*$', line):
            continue
        result_lines.append(line)
    return "".join(result_lines)


def _extract_step_run(workflow_path: Path, step_name_substring: str) -> str:
    """Parse a workflow YAML and return the run: block from the named step.

    Raises pytest.skip if the file or step is not found.
    """
    if not workflow_path.exists():
        pytest.skip(f"Workflow not found: {workflow_path}")
    with workflow_path.open(encoding="utf-8") as fh:
        wf = yaml.safe_load(fh)
    for job in wf.get("jobs", {}).values():
        for step in job.get("steps", []):
            name = step.get("name", "")
            if step_name_substring.lower() in name.lower():
                run = step.get("run", "")
                if run:
                    return run
    pytest.skip(
        f"Step containing {step_name_substring!r} not found in {workflow_path.name}"
    )


def _run_bash_snippet(script: str, env_overrides: dict) -> subprocess.CompletedProcess:
    """Run a bash snippet and return the completed process."""
    env = {"PATH": os.environ["PATH"], **env_overrides}
    return subprocess.run(
        ["bash", "-c", script],
        env=env,
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def vcre():
    return _load_validate_module()


# ---------------------------------------------------------------------------
# Tests: Python-level fail-closed (via validate_cross_review_evidence)
# ---------------------------------------------------------------------------

class TestFailClosedPythonLevel:

    """validate_cross_review_evidence must return violations when BASE_SHA is empty."""

    def test_empty_base_sha_is_violation(self, vcre):
        """detect_cross_review_violations must fail closed on empty BASE_SHA."""
        violations = vcre.detect_cross_review_violations(
            ["STANDARDS.md"],
            planning_only=False,
            base_sha="",
            head_sha="abc123",
        )
        assert violations, "Expected violation on empty BASE_SHA"
        assert any("BASE_SHA" in v or "context" in v.lower() for v in violations), violations

    def test_empty_head_sha_is_violation(self, vcre):
        """detect_cross_review_violations must fail closed on empty HEAD_SHA."""
        violations = vcre.detect_cross_review_violations(
            ["STANDARDS.md"],
            planning_only=False,
            base_sha="abc123",
            head_sha="",
        )
        assert violations, "Expected violation on empty HEAD_SHA"

    def test_both_empty_sha_is_violation(self, vcre):
        """detect_cross_review_violations must fail closed when both SHAs are empty."""
        violations = vcre.detect_cross_review_violations(
            [],
            planning_only=False,
            base_sha="",
            head_sha="",
        )
        assert violations, "Expected violation on both SHAs empty"

    def test_valid_sha_with_no_trigger_passes(self, vcre):
        """With valid SHAs and no trigger, no violations expected."""
        violations = vcre.detect_cross_review_violations(
            ["docs/PROGRESS.md"],
            planning_only=False,
            base_sha="aaa111",
            head_sha="bbb222",
        )
        assert not violations, f"Expected no violation; got: {violations}"


# ---------------------------------------------------------------------------
# Tests: Bash-level fail-closed (extracted from real workflow YAML)
# ---------------------------------------------------------------------------

class TestFailClosedBashLevel:
    """Real workflow bash gates must exit 1 when BASE_SHA/HEAD_SHA is missing.

    Each test extracts the run: block from the actual workflow YAML via PyYAML,
    strips GitHub Actions ${{ }} template expressions (which resolve to empty
    string when inputs are absent), then executes the script in subprocess with
    BASE_SHA="" and HEAD_SHA="" to verify the gate fails closed.
    """

    def test_require_cross_review_exits_1_on_empty_base_sha(self):
        """require-cross-review.yml gate exits 1 when BASE_SHA is empty.

        Extracts the real run: block from the step named
        'Require cross-review artifact' and executes it with empty context.
        GITHUB_WORKSPACE is provided as empty string so the script's
        directory-existence checks don't fail on an unbound variable error
        before the BASE_SHA gate is reached.
        """
        wf_path = WORKFLOWS_DIR / "require-cross-review.yml"
        raw_script = _extract_step_run(wf_path, "Require cross-review artifact")
        script = _strip_gha_templates(raw_script)
        result = _run_bash_snippet(
            script, {"BASE_SHA": "", "HEAD_SHA": "", "GITHUB_WORKSPACE": ""}
        )
        assert result.returncode == 1, (
            f"Expected exit 1 when BASE_SHA empty; got {result.returncode}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
        combined = result.stdout + result.stderr
        assert "::error::" in combined, (
            f"Expected ::error:: annotation in output; got: {combined!r}"
        )

    def test_require_cross_review_passes_with_valid_context(self):
        """require-cross-review.yml gate exits 0 when valid SHAs are provided.

        Uses HEAD as both BASE and HEAD to produce an empty diff (no files
        touched), which the gate treats as a pass.  SHA-assignment lines that
        contain ${{ }} expressions are dropped (env_passthrough=True) so that
        the subprocess env variables BASE_SHA/HEAD_SHA are used directly.
        """
        head = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
            text=True,
        ).strip()
        wf_path = WORKFLOWS_DIR / "require-cross-review.yml"
        raw_script = _extract_step_run(wf_path, "Require cross-review artifact")
        script = _strip_gha_templates(raw_script, env_passthrough=True)
        env = {
            "BASE_SHA": head,
            "HEAD_SHA": head,
            "PATH": os.environ["PATH"],
            "GITHUB_WORKSPACE": str(REPO_ROOT),
            "PLANNING_ONLY": "false",
        }
        result = subprocess.run(
            ["bash", "-c", script],
            env=env,
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, (
            f"Expected exit 0 with valid context; got {result.returncode}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )

    def test_check_arch_tier_exits_1_on_empty_base_sha(self):
        """check-arch-tier.yml gate exits 1 when BASE_SHA is empty.

        Extracts the real run: block from the step named
        'Enforce architecture/standards tier evidence' and executes it
        with empty BASE_SHA and HEAD_SHA.
        """
        wf_path = WORKFLOWS_DIR / "check-arch-tier.yml"
        raw_script = _extract_step_run(wf_path, "Enforce architecture/standards tier evidence")
        script = _strip_gha_templates(raw_script)
        result = _run_bash_snippet(script, {"BASE_SHA": "", "HEAD_SHA": ""})
        assert result.returncode == 1, (
            f"Expected exit 1; got {result.returncode}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
        combined = result.stdout + result.stderr
        assert "::error::" in combined, (
            f"Expected ::error:: annotation in output; got: {combined!r}"
        )

    def test_check_arch_tier_passes_with_valid_context(self):
        """check-arch-tier.yml gate exits 0 when valid SHAs are provided.

        Uses HEAD for both SHAs so the diff is empty and the gate skips.
        """
        head = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
            text=True,
        ).strip()
        wf_path = WORKFLOWS_DIR / "check-arch-tier.yml"
        raw_script = _extract_step_run(wf_path, "Enforce architecture/standards tier evidence")
        script = _strip_gha_templates(raw_script)
        env = {
            "BASE_SHA": head,
            "HEAD_SHA": head,
            "PATH": os.environ["PATH"],
        }
        result = subprocess.run(
            ["bash", "-c", script],
            env=env,
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, (
            f"Expected exit 0; got {result.returncode}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )

    def test_governance_check_inline_cross_review_exits_1_on_empty_base_sha(self):
        """governance-check.yml inline require-cross-review gate exits 1 when BASE_SHA is empty.

        governance-check.yml embeds its own copy of the cross-review context
        check in the step 'Require cross-review artifact'. This test extracts
        that real step run: block and verifies it fails closed.
        """
        wf_path = WORKFLOWS_DIR / "governance-check.yml"
        raw_script = _extract_step_run(wf_path, "Require cross-review artifact")
        script = _strip_gha_templates(raw_script)
        result = _run_bash_snippet(script, {"BASE_SHA": "", "HEAD_SHA": ""})
        assert result.returncode == 1, (
            f"Expected exit 1 when BASE_SHA empty; got {result.returncode}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
        combined = result.stdout + result.stderr
        assert "::error::" in combined, (
            f"Expected ::error:: annotation in output; got: {combined!r}"
        )

    def test_governance_check_inline_cross_review_passes_with_valid_context(self):
        """governance-check.yml inline cross-review gate exits 0 when valid SHAs given.

        Uses HEAD for both SHAs so the diff is empty and the step exits 0.
        SHA-assignment lines containing ${{ }} expressions are dropped
        (env_passthrough=True) so subprocess env vars are used directly.
        """
        head = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
            text=True,
        ).strip()
        wf_path = WORKFLOWS_DIR / "governance-check.yml"
        raw_script = _extract_step_run(wf_path, "Require cross-review artifact")
        script = _strip_gha_templates(raw_script, env_passthrough=True)
        env = {
            "BASE_SHA": head,
            "HEAD_SHA": head,
            "PATH": os.environ["PATH"],
        }
        result = subprocess.run(
            ["bash", "-c", script],
            env=env,
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, (
            f"Expected exit 0 with valid context; got {result.returncode}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )


# ---------------------------------------------------------------------------
# Tests: Workflow file existence (sanity checks)
# ---------------------------------------------------------------------------

class TestWorkflowFilesExist:
    """Assert that the referenced workflow files exist in the repo."""

    @pytest.mark.parametrize("wf_name", [
        "governance-check.yml",
        "require-cross-review.yml",
        "check-arch-tier.yml",
    ])
    def test_workflow_file_exists(self, wf_name: str):
        wf_path = WORKFLOWS_DIR / wf_name
        assert wf_path.exists(), f"Workflow file not found: {wf_path}"

    @pytest.mark.parametrize("wf_name", [
        "governance-check.yml",
        "require-cross-review.yml",
        "check-arch-tier.yml",
    ])
    def test_workflow_has_workflow_call_trigger(self, wf_name: str):
        wf_path = WORKFLOWS_DIR / wf_name
        if not wf_path.exists():
            pytest.skip(f"{wf_name} not found")
        content = wf_path.read_text(encoding="utf-8")
        assert "workflow_call" in content, f"{wf_name} must declare workflow_call trigger"

    @pytest.mark.parametrize("wf_name,step_fragment", [
        ("require-cross-review.yml", "Require cross-review artifact"),
        ("check-arch-tier.yml", "Enforce architecture/standards tier evidence"),
        ("governance-check.yml", "Require cross-review artifact"),
    ])
    def test_workflow_has_fail_closed_step(self, wf_name: str, step_fragment: str):
        """Each workflow must contain a step whose run: block exits 1 on empty BASE_SHA."""
        wf_path = WORKFLOWS_DIR / wf_name
        if not wf_path.exists():
            pytest.skip(f"{wf_name} not found")
        run_block = _extract_step_run(wf_path, step_fragment)
        assert "exit 1" in run_block, (
            f"Step '{step_fragment}' in {wf_name} must contain 'exit 1' for fail-closed gate"
        )
        assert "BASE_SHA" in run_block or "base_sha" in run_block, (
            f"Step '{step_fragment}' in {wf_name} must reference BASE_SHA"
        )
