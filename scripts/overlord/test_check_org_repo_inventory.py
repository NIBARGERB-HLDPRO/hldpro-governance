#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("check_org_repo_inventory.py")
SPEC = importlib.util.spec_from_file_location("check_org_repo_inventory", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
check_org_repo_inventory = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = check_org_repo_inventory
SPEC.loader.exec_module(check_org_repo_inventory)


class TestOrgRepoInventory(unittest.TestCase):
    def _registry(self, tmpdir: Path, repos: list[str], *, archived: set[str] | None = None) -> Path:
        archived = archived or set()
        payload = {
            "version": 1,
            "organization": "NIBARGERB-HLDPRO",
            "repos_root_env": "HLDPRO_REPOS_ROOT",
            "default_repos_root": "~/Developer/HLDPRO",
            "repositories": [
                {
                    "repo_slug": repo.lower(),
                    "display_name": repo,
                    "repo_dir_name": repo,
                    "github_repo": f"NIBARGERB-HLDPRO/{repo}",
                    "local_path": repo,
                    "ci_checkout_path": "." if repo == "hldpro-governance" else f"repos/{repo}",
                    "graph_output_path": f"graphify-out/{repo.lower()}",
                    "wiki_path": f"wiki/{repo.lower()}",
                    "project_path": f"projects/{repo.lower()}",
                    "governance_tier": "standard",
                    "security_tier": "baseline",
                    "lifecycle_status": "archived" if repo in archived else "active",
                    "governance_status": "exempt" if repo in archived else "governed",
                    "classification": {
                        "owner": "governance",
                        "rationale": f"{repo} fixture classification.",
                        "review_date": "2026-04-18",
                        "issue_refs": [
                            "#310"
                        ],
                    },
                    "description": f"{repo} fixture",
                    "enabled_subsystems": {
                        "graphify": True,
                        "sweep": True,
                        "metrics": True,
                        "memory_integrity": True,
                        "codex_ingestion": True,
                        "compendium": True,
                        "raw_feed_sync": True,
                        "code_governance": True,
                    },
                }
                for repo in repos
            ],
        }
        path = tmpdir / "governed_repos.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def _inventory(self, tmpdir: Path, rows: list[dict[str, object]]) -> Path:
        path = tmpdir / "inventory.json"
        path.write_text(json.dumps(rows), encoding="utf-8")
        return path

    def _repo_row(self, name: str, *, archived: bool = False) -> dict[str, object]:
        return {
            "name": name,
            "isArchived": archived,
            "isPrivate": True,
            "defaultBranchRef": {"name": "main"},
            "url": f"https://github.com/NIBARGERB-HLDPRO/{name}",
            "pushedAt": "2026-04-18T00:00:00Z",
        }

    def _run(self, *args: str) -> tuple[int, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = check_org_repo_inventory.main(list(args))
        return code, stdout.getvalue() + stderr.getvalue()

    def test_exact_active_inventory_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            registry = self._registry(tmpdir, ["hldpro-governance", "knocktracker"])
            inventory = self._inventory(
                tmpdir,
                [self._repo_row("hldpro-governance"), self._repo_row("knocktracker")],
            )

            code, output = self._run("--registry", str(registry), "--inventory-file", str(inventory))

        self.assertEqual(code, 0, output)
        self.assertIn("PASS org inventory matches", output)

    def test_missing_active_repo_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            registry = self._registry(tmpdir, ["hldpro-governance"])
            inventory = self._inventory(
                tmpdir,
                [self._repo_row("hldpro-governance"), self._repo_row("seek-and-ponder")],
            )

            code, output = self._run("--registry", str(registry), "--inventory-file", str(inventory))

        self.assertEqual(code, 1)
        self.assertIn("FAIL org inventory drift detected", output)
        self.assertIn("NIBARGERB-HLDPRO/seek-and-ponder", output)

    def test_warn_only_reports_missing_active_repo_but_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            registry = self._registry(tmpdir, ["hldpro-governance"])
            inventory = self._inventory(
                tmpdir,
                [self._repo_row("hldpro-governance"), self._repo_row("EmailAssistant")],
            )

            code, output = self._run(
                "--registry",
                str(registry),
                "--inventory-file",
                str(inventory),
                "--warn-only",
                "--format",
                "markdown",
            )

        self.assertEqual(code, 0, output)
        self.assertIn("ATTENTION (warn-only)", output)
        self.assertIn("NIBARGERB-HLDPRO/EmailAssistant", output)

    def test_stale_registry_repo_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            registry = self._registry(tmpdir, ["hldpro-governance", "missing-repo"])
            inventory = self._inventory(tmpdir, [self._repo_row("hldpro-governance")])

            code, output = self._run("--registry", str(registry), "--inventory-file", str(inventory))

        self.assertEqual(code, 1)
        self.assertIn("Registry repos missing from live org inventory", output)
        self.assertIn("NIBARGERB-HLDPRO/missing-repo", output)

    def test_archived_unregistered_repo_is_notice_not_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            registry = self._registry(tmpdir, ["hldpro-governance"])
            inventory = self._inventory(
                tmpdir,
                [self._repo_row("hldpro-governance"), self._repo_row("old-repo", archived=True)],
            )

            code, output = self._run("--registry", str(registry), "--inventory-file", str(inventory))

        self.assertEqual(code, 0, output)
        self.assertIn("Archived repos absent from registry", output)
        self.assertIn("NIBARGERB-HLDPRO/old-repo", output)

    def test_archived_registry_repo_fails_without_archived_lifecycle_classification(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            registry = self._registry(tmpdir, ["hldpro-governance", "old-repo"])
            inventory = self._inventory(
                tmpdir,
                [self._repo_row("hldpro-governance"), self._repo_row("old-repo", archived=True)],
            )

            code, output = self._run("--registry", str(registry), "--inventory-file", str(inventory))

        self.assertEqual(code, 1)
        self.assertIn("Archived repos still present in registry", output)
        self.assertIn("NIBARGERB-HLDPRO/old-repo", output)

    def test_archived_registry_repo_passes_with_archived_lifecycle_classification(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmpdir:
            tmpdir = Path(raw_tmpdir)
            registry = self._registry(tmpdir, ["hldpro-governance", "old-repo"], archived={"old-repo"})
            inventory = self._inventory(
                tmpdir,
                [self._repo_row("hldpro-governance"), self._repo_row("old-repo", archived=True)],
            )

            code, output = self._run("--registry", str(registry), "--inventory-file", str(inventory))

        self.assertEqual(code, 0, output)
        self.assertIn("PASS org inventory matches", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
