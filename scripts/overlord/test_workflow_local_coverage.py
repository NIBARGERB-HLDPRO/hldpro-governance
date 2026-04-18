#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import check_workflow_local_coverage as coverage


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _inventory(entries: list[dict]) -> dict:
    return {
        "schema_version": 1,
        "updated_at": "2026-04-18",
        "principle": "CI remains authoritative.",
        "coverage_types": ["local_command", "workflow_contract", "script_dry_run", "github_only"],
        "workflows": entries,
    }


def _entry(path: str, *, coverage_items: list[dict] | None = None, snippets: list[str] | None = None) -> dict:
    return {
        "path": path,
        "risk": "deterministic",
        "coverage": coverage_items
        if coverage_items is not None
        else [{"type": "local_command", "command": ["python3", "scripts/check.py"]}],
        "required_snippets": snippets if snippets is not None else ["python3 scripts/check.py"],
        "rationale": "Deterministic workflow covered by a local command.",
    }


class TestWorkflowLocalCoverage(unittest.TestCase):
    def test_repository_inventory_passes(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]

        self.assertEqual(coverage.check_inventory(repo_root), [])

    def test_rejects_workflow_missing_from_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write(root / ".github/workflows/known.yml", "name: known\nrun: python3 scripts/check.py\n")
            _write(root / ".github/workflows/missing.yml", "name: missing\n")
            _write(root / "scripts/check.py", "")
            _write(root / coverage.INVENTORY_PATH, json.dumps(_inventory([_entry(".github/workflows/known.yml")])))

            failures = coverage.check_inventory(root)

        self.assertIn(
            "workflow files missing inventory entries: .github/workflows/missing.yml",
            failures,
        )

    def test_rejects_inventory_entry_without_workflow_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write(root / ".github/workflows/known.yml", "name: known\nrun: python3 scripts/check.py\n")
            _write(root / "scripts/check.py", "")
            entries = [_entry(".github/workflows/known.yml"), _entry(".github/workflows/ghost.yml")]
            _write(root / coverage.INVENTORY_PATH, json.dumps(_inventory(entries)))

            failures = coverage.check_inventory(root)

        self.assertIn(".github/workflows/ghost.yml: inventory references missing workflow file", failures)

    def test_rejects_deterministic_workflow_without_local_first_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write(root / ".github/workflows/known.yml", "name: known\nrun: echo remote\n")
            entry = _entry(
                ".github/workflows/known.yml",
                coverage_items=[{"type": "github_only", "rationale": "Only runs on GitHub for testing purposes."}],
                snippets=["echo remote"],
            )
            _write(root / coverage.INVENTORY_PATH, json.dumps(_inventory([entry])))

            failures = coverage.check_inventory(root)

        self.assertIn(
            ".github/workflows/known.yml: non-GitHub-only workflows require local, contract, or script/dry-run coverage",
            failures,
        )

    def test_rejects_missing_command_path(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write(root / ".github/workflows/known.yml", "name: known\nrun: python3 scripts/missing.py\n")
            entry = _entry(
                ".github/workflows/known.yml",
                coverage_items=[{"type": "local_command", "command": ["python3", "scripts/missing.py"]}],
                snippets=["python3 scripts/missing.py"],
            )
            _write(root / coverage.INVENTORY_PATH, json.dumps(_inventory([entry])))

            failures = coverage.check_inventory(root)

        self.assertIn(
            ".github/workflows/known.yml: coverage[1].command references missing repo path: scripts/missing.py",
            failures,
        )

    def test_rejects_missing_required_snippet(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write(root / ".github/workflows/known.yml", "name: known\nrun: python3 scripts/check.py\n")
            _write(root / "scripts/check.py", "")
            entry = _entry(".github/workflows/known.yml", snippets=["bash scripts/check.sh"])
            _write(root / coverage.INVENTORY_PATH, json.dumps(_inventory([entry])))

            failures = coverage.check_inventory(root)

        self.assertIn(
            ".github/workflows/known.yml: required snippet not found: bash scripts/check.sh",
            failures,
        )

    def test_accepts_github_only_with_rationale(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write(root / ".github/workflows/scheduled.yml", "name: scheduled\nrun: git push\n")
            entry = {
                "path": ".github/workflows/scheduled.yml",
                "risk": "github-only-side-effecting",
                "coverage": [
                    {
                        "type": "github_only",
                        "rationale": "Scheduled job pushes commits and must not be replayed locally.",
                    }
                ],
                "required_snippets": ["git push"],
                "rationale": "Scheduled side-effecting job has explicit GitHub-only coverage rationale.",
            }
            _write(root / coverage.INVENTORY_PATH, json.dumps(_inventory([entry])))

            failures = coverage.check_inventory(root)

        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
