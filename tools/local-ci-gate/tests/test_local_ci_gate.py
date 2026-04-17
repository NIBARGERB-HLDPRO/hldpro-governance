from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import local_ci_gate as gate


BIN = Path(__file__).resolve().parents[1] / "bin" / "hldpro-local-ci"


class TestLocalCiGate(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init"], cwd=self.root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.root, check=True, capture_output=True, text=True)

        (self.root / "tracked.txt").write_text("tracked\n", encoding="utf-8")
        subprocess.run(["git", "add", "tracked.txt"], cwd=self.root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "commit", "-m", "seed"], cwd=self.root, check=True, capture_output=True, text=True)

        self.profile_path = self.root / "profile.yml"
        self.profile_path.write_text(
            """
profile:
  name: test-profile
  description: Test profile
  report_root: local-reports
  changed_files:
    base_ref: HEAD
    head_ref: HEAD
    include_untracked: true
  checks:
    - id: blocker
      title: Blocker check
      severity: blocker
      scope: always
      command:
        - python3
        - -c
        - "import sys; sys.exit(1)"
    - id: advisory
      title: Advisory check
      severity: advisory
      scope: changed
      paths:
        - tools/local-ci-gate/
      command:
        - python3
        - -c
        - "import sys; sys.exit(1)"
""".strip()
            + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_resolves_changed_files_from_git_and_writes_report(self) -> None:
        (self.root / "tools" / "local-ci-gate").mkdir(parents=True, exist_ok=True)
        (self.root / "tools" / "local-ci-gate" / "note.txt").write_text("x\n", encoding="utf-8")

        changed = gate.resolve_changed_files(self.root, base_ref="HEAD", head_ref="HEAD", include_untracked=True)
        self.assertIn("tools/local-ci-gate/note.txt", changed.files)
        self.assertEqual(changed.source, "git")

        profile = gate.load_profile(self.profile_path)
        report = gate.run_checks(self.root, profile, changed, dry_run=True)

        self.assertEqual(report.verdict, "planned")
        self.assertIn("scope=subset", report.summary)
        self.assertIn("CI remains authoritative", report.summary)
        self.assertTrue(report.report_dir.exists())
        self.assertTrue(list(report.report_dir.glob("*.json")))
        self.assertTrue(list(report.report_dir.glob("*.txt")))

    def test_blocker_and_advisory_statuses_are_distinct(self) -> None:
        changed = gate.resolve_changed_files(
            self.root,
            explicit_files=["tools/local-ci-gate/example.py"],
            include_untracked=True,
        )
        profile = gate.load_profile(self.profile_path)
        report = gate.run_checks(self.root, profile, changed, dry_run=False)

        blocker = next(result for result in report.results if result.check.id == "blocker")
        advisory = next(result for result in report.results if result.check.id == "advisory")

        self.assertEqual(blocker.status, "blocker_failed")
        self.assertEqual(advisory.status, "advisory_failed")
        self.assertEqual(report.verdict, "blocker")
        self.assertEqual(gate._check_exit_code(report), 1)

    def test_noop_profile_supports_dry_run_without_side_effects(self) -> None:
        noop = self.root / "noop.yml"
        noop.write_text(
            """
profile:
  name: noop
  description: No-op profile
  report_root: local-reports
  checks: []
""".strip()
            + "\n",
            encoding="utf-8",
        )
        profile = gate.load_profile(noop)
        changed = gate.resolve_changed_files(self.root, explicit_files=["docs/readme.md"], include_untracked=False)
        report = gate.run_checks(self.root, profile, changed, dry_run=True)

        self.assertEqual(profile.name, "noop")
        self.assertEqual(report.verdict, "pass")
        self.assertIn("CI remains authoritative", report.summary)

    def test_cli_prints_authoritative_note(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(BIN),
                "--repo-root",
                str(self.root),
                "--profile-file",
                str(self.profile_path),
                "--changed-file",
                "tools/local-ci-gate/example.py",
                "--dry-run",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("CI remains authoritative", result.stdout)
        self.assertIn("Verdict: PLANNED", result.stdout)

    def test_cli_accepts_managed_shim_run_invocation(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(BIN),
                "run",
                "--repo-root",
                str(self.root),
                "--governance-root",
                str(self.root),
                "--governance-ref",
                "abc123",
                "--shim-path",
                str(self.root / ".hldpro/local-ci.sh"),
                "--profile-file",
                str(self.profile_path),
                "--changed-file",
                "docs/readme.md",
                "--dry-run",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("CI remains authoritative", result.stdout)
        self.assertIn("Verdict: PLANNED", result.stdout)

    def test_report_json_is_machine_readable(self) -> None:
        changed = gate.resolve_changed_files(self.root, explicit_files=["tools/local-ci-gate/example.py"], include_untracked=False)
        profile = gate.load_profile(self.profile_path)
        report = gate.run_checks(self.root, profile, changed, dry_run=True, report_dir=self.root / "reports")
        payload = sorted(report.report_dir.glob("*.json"))[-1].read_text(encoding="utf-8")
        data = json.loads(payload)

        self.assertEqual(data["profile"]["name"], "test-profile")
        self.assertEqual(data["verdict"], "planned")
        self.assertEqual(data["changed_files"]["files"], ["tools/local-ci-gate/example.py"])

    def test_changed_files_file_accepts_null_separated_entries(self) -> None:
        changed_files = self.root / "changed-files.txt"
        changed_files.write_text("scripts/example.py\0tools/local-ci-gate/example.py\0", encoding="utf-8")

        changed = gate.resolve_changed_files(self.root, changed_files_file=changed_files)

        self.assertEqual(changed.source, f"file:{changed_files}")
        self.assertEqual(changed.files, ("scripts/example.py", "tools/local-ci-gate/example.py"))


if __name__ == "__main__":
    unittest.main()
