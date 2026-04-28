import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "session_bootstrap_contract.py"


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "scripts").mkdir()
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
    subprocess.run(["git", "checkout", "-b", "issue-test"], cwd=repo, check=True, capture_output=True)
    return repo


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


if __name__ == "__main__":
    unittest.main()
