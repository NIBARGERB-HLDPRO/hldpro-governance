#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("read_only_observer.py")
SPEC = importlib.util.spec_from_file_location("read_only_observer", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
read_only_observer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = read_only_observer
SPEC.loader.exec_module(read_only_observer)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _copy_fixture(source: Path, target: Path) -> None:
    if source.is_dir():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


class TestReadOnlyObserver(unittest.TestCase):
    def _fixture(self, tmpdir: Path) -> Path:
        fixture = tmpdir / "repo"
        for relative in [
            "docs/governed_repos.json",
            "docs/ORG_GOVERNANCE_COMPENDIUM.md",
            "OVERLORD_BACKLOG.md",
            "raw/closeouts",
            "raw/github-issues",
            "graphify-out/hldpro-governance/GRAPH_REPORT.md",
            "wiki/hldpro/index.md",
            "scripts/overlord/validate_structured_agent_cycle_plan.py",
        ]:
            _copy_fixture(REPO_ROOT / relative, fixture / relative)
        return fixture

    def test_check_only_does_not_write_reports_or_packets(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmpdir = Path(raw)
            fixture = self._fixture(tmpdir)
            report_root = tmpdir / "reports"

            reports = read_only_observer.build_reports(fixture, report_root)

            self.assertGreaterEqual(len(reports), 1)
            self.assertFalse((report_root / "projects").exists())
            self.assertFalse((fixture / "raw" / "packets").exists())

    def test_writes_only_project_reports(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmpdir = Path(raw)
            fixture = self._fixture(tmpdir)
            report_root = tmpdir / "reports"

            reports = read_only_observer.build_reports(fixture, report_root)
            written = read_only_observer.write_reports(reports, report_root, "test")

            self.assertTrue(written)
            for path in written:
                self.assertTrue(path.is_file())
                self.assertTrue(path.relative_to(report_root).as_posix().startswith("projects/"))
            self.assertFalse((fixture / "raw" / "packets").exists())

            governance_json = report_root / "projects" / "hldpro-governance" / "reports" / "test.json"
            payload = json.loads(governance_json.read_text(encoding="utf-8"))
            self.assertEqual(payload["daemon_readiness"]["packet_enqueue_enabled"], False)
            self.assertEqual(payload["daemon_readiness"]["report_dir_within_projects"], True)
            self.assertIn("source_commit", payload)
            self.assertIn("sha256", payload["artifacts"]["compendium"])

    def test_cli_check_only(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmpdir = Path(raw)
            fixture = self._fixture(tmpdir)
            result = subprocess.run(
                [
                    sys.executable,
                    str(MODULE_PATH),
                    "--repo-root",
                    str(fixture),
                    "--report-root",
                    str(tmpdir / "reports"),
                    "--check-only",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["packet_enqueue_enabled"], False)
        self.assertGreaterEqual(payload["reports"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
