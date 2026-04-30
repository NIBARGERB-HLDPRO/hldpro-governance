import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "session_bootstrap_contract.py"
HOOK_SCRIPT = ROOT / "hooks" / "pre-session-context.sh"
CHECK_EXECUTION_ENV_SCRIPT = ROOT / "scripts" / "overlord" / "check_execution_environment.py"
ASSERT_EXECUTION_SCOPE_SCRIPT = ROOT / "scripts" / "overlord" / "assert_execution_scope.py"


def make_repo(tmp_path: Path, branch: str = "issue-test", repo_name: str = "repo") -> Path:
    repo = tmp_path / repo_name
    (repo / "docs").mkdir(parents=True)
    (repo / "scripts").mkdir()
    (repo / "scripts" / "overlord").mkdir(parents=True)
    (repo / "hooks").mkdir()
    (repo / "CODEX.md").write_text("codex contract\n", encoding="utf-8")
    (repo / "CLAUDE.md").write_text("claude contract\n", encoding="utf-8")
    (repo / "docs" / "PROGRESS.md").write_text("progress\n", encoding="utf-8")
    (repo / "docs" / "FAIL_FAST_LOG.md").write_text("fail fast\n", encoding="utf-8")
    (repo / "STANDARDS.md").write_text(
        textwrap.dedent(
            """
            # Standards

            ## Society of Minds — Model Routing Charter (2026-04-14)
            line 1
            line 2

            ## Another Section
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    (repo / "docs" / "EXTERNAL_SERVICES_RUNBOOK.md").write_text(
        textwrap.dedent(
            """
            # Runbook
            - Binary: ~/.nvm/versions/node/v24.14.1/bin/codex
            - Config: ~/.codex/config.toml

            ## Claude
            - `CLAUDE_CODE_OAUTH_TOKEN` in repo-level `.env` (NOT committed)

            ```bash
            bash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh <repo>
            ```
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", branch], cwd=repo, check=True, capture_output=True)
    return repo


def add_startup_scope_bundle(repo: Path, issue_number: int, branch: str) -> None:
    (repo / "hooks" / "pre-session-context.sh").write_text(HOOK_SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
    (repo / "scripts" / "session_bootstrap_contract.py").write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
    (
        repo / "scripts" / "overlord" / "check_execution_environment.py"
    ).write_text(CHECK_EXECUTION_ENV_SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
    (
        repo / "scripts" / "overlord" / "assert_execution_scope.py"
    ).write_text(ASSERT_EXECUTION_SCOPE_SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")

    (repo / "raw" / "execution-scopes").mkdir(parents=True, exist_ok=True)
    (repo / "raw" / "handoffs").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "codex-reviews").mkdir(parents=True, exist_ok=True)

    (repo / "docs" / "codex-reviews" / "2026-04-30-issue-617-claude.md").write_text("review\n", encoding="utf-8")
    (repo / "docs" / "plans" / "issue-617-plan.json").write_text(
        json.dumps(
            {
                "specialist_reviews": [
                    {"reviewer": "startup-scope research specialist", "status": "mixed"},
                    {"reviewer": "startup-scope QA specialist", "status": "mixed"},
                ],
                "alternate_model_review": {"required": True, "status": "accepted"},
                "execution_handoff": {
                    "next_role": "codex-orchestrator",
                    "next_execution_step": "begin bounded startup implementation",
                    "qa_gate_required": True,
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (repo / "raw" / "execution-scopes" / "2026-04-30-issue-617-implementation.json").write_text(
        json.dumps(
            {
                "expected_execution_root": ".",
                "expected_branch": branch,
                "execution_mode": "implementation_ready",
                "allowed_write_paths": [
                    "raw/",
                    "docs/",
                    "hooks/pre-session-context.sh",
                    "scripts/session_bootstrap_contract.py",
                    "scripts/overlord/assert_execution_scope.py",
                    "scripts/overlord/check_execution_environment.py",
                    "CLAUDE.md",
                    "CODEX.md",
                    "STANDARDS.md"
                ],
                "forbidden_roots": [],
                "lane_claim": {
                    "issue_number": issue_number,
                    "claim_ref": f"https://example.invalid/issues/{issue_number}",
                    "claimed_by": "codex",
                    "claimed_at": "2026-04-30T03:05:00Z",
                },
                "handoff_evidence": {
                    "status": "accepted",
                    "planner_model": "gpt-5.4",
                    "implementer_model": "gpt-5.4",
                    "accepted_at": "2026-04-30T03:35:00Z",
                    "evidence_paths": ["docs/plans/issue-617-plan.json"],
                    "active_exception_ref": "docs/codex-reviews/2026-04-30-issue-617-claude.md",
                    "active_exception_expires_at": "2026-05-01T03:35:00Z",
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (repo / "raw" / "handoffs" / "2026-04-30-issue-617.json").write_text(
        json.dumps(
            {
                "execution_scope_ref": "raw/execution-scopes/2026-04-30-issue-617-implementation.json",
                "structured_plan_ref": "docs/plans/issue-617-plan.json",
                "to_role": "codex-orchestrator",
                "created_at": "2026-04-30T03:35:00Z",
            }
        )
        + "\n",
        encoding="utf-8",
    )


def run_contract(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )


class SessionBootstrapContractTests(unittest.TestCase):
    def test_emit_hook_note_writes_sentinel_and_surfaces_runbook_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            repo = make_repo(tmp_path)
            sentinel = tmp_path / "sentinel.json"

            result = run_contract(repo, "--emit-hook-note", "--sentinel-path", str(sentinel))

            self.assertEqual(result.returncode, 0)
            self.assertIn("Codex is orchestrator/supervisor only.", result.stdout)
            self.assertIn(
                "bootstrap_command: bash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh <repo>",
                result.stdout,
            )
            payload = json.loads(sentinel.read_text(encoding="utf-8"))
            self.assertTrue(payload["loaded_or_surfaced"]["codex_contract"])
            self.assertTrue(payload["loaded_or_surfaced"]["external_services_runbook"])
            self.assertTrue(payload["loaded_or_surfaced"]["standards_som"])
            self.assertEqual(
                payload["runbook_paths"]["codex_binary"],
                "~/.nvm/versions/node/v24.14.1/bin/codex",
            )

    def test_missing_required_file_is_recorded_as_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            repo = make_repo(tmp_path)
            (repo / "CODEX.md").unlink()
            sentinel = tmp_path / "sentinel.json"

            result = run_contract(repo, "--json", "--sentinel-path", str(sentinel))

            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["loaded_or_surfaced"]["codex_contract"])
            self.assertIn("missing:CODEX.md", payload["warnings"])
            sentinel_payload = json.loads(sentinel.read_text(encoding="utf-8"))
            self.assertEqual(sentinel_payload["warnings"], payload["warnings"])

    def test_pre_session_hook_appends_startup_execution_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            branch = "issue-617-hook-test-20260430"
            repo = make_repo(tmp_path, branch=branch, repo_name="hldpro-governance")
            add_startup_scope_bundle(repo, issue_number=617, branch=branch)
            session_id = f"issue-617-hook-test-{tmp_path.name}"

            result = subprocess.run(
                ["bash", str(repo / "hooks" / "pre-session-context.sh")],
                cwd=repo / "docs",
                text=True,
                capture_output=True,
                check=False,
                env={
                    **os.environ,
                    "CLAUDE_CWD": str(repo / "docs"),
                    "CLAUDE_SESSION_ID": session_id,
                    "PYTHONDONTWRITEBYTECODE": "1",
                },
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("=== SESSION BOOTSTRAP CONTRACT (hldpro-governance) ===", result.stdout)
            self.assertIn("PASS startup execution context", result.stdout)
            self.assertIn("scope_path: raw/execution-scopes/2026-04-30-issue-617-implementation.json", result.stdout)
            self.assertIn("required_specialists: startup-scope research specialist, startup-scope QA specialist, alternate_model_review, qa_gate_required", result.stdout)


if __name__ == "__main__":
    unittest.main()
