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
PROFILES_DIR = Path(__file__).resolve().parents[1] / "profiles"


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
  requires_dependencies:
    - python3
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

    def test_base_ref_changed_files_include_unstaged_tracked_edits(self) -> None:
        (self.root / "tracked.txt").write_text("tracked\nmodified\n", encoding="utf-8")

        changed = gate.resolve_changed_files(self.root, base_ref="HEAD", head_ref="HEAD", include_untracked=False)

        self.assertIn("tracked.txt", changed.files)

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
        report_dir = self.root / "managed-report"
        shim_path = self.root / ".hldpro/local-ci.sh"
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
                str(shim_path),
                "--profile-file",
                str(self.profile_path),
                "--report-dir",
                str(report_dir),
                "--changed-file",
                "docs/readme.md",
                "--dry-run",
                "--json",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("CI remains authoritative", result.stdout)
        self.assertIn("Verdict: PLANNED", result.stdout)
        stdout_payload = json.loads(result.stdout[result.stdout.index('{\n  "profile"') :])
        self.assertEqual(stdout_payload["invocation"]["governance_root"], str(self.root))
        self.assertEqual(stdout_payload["invocation"]["governance_ref"], "abc123")
        self.assertEqual(stdout_payload["invocation"]["shim_path"], str(shim_path))

        report_payload = json.loads(sorted(report_dir.glob("*.json"))[-1].read_text(encoding="utf-8"))
        self.assertEqual(report_payload["repo_root"], str(self.root.resolve()))
        self.assertEqual(report_payload["invocation"]["governance_root"], str(self.root))
        self.assertEqual(report_payload["invocation"]["governance_ref"], "abc123")
        self.assertEqual(report_payload["invocation"]["shim_path"], str(shim_path))
        self.assertIn("--governance-ref", report_payload["invocation"]["argv"])
        self.assertTrue(report_payload["invocation"]["cwd"])
        self.assertTrue(report_payload["invocation"]["runner_path"])

    def test_report_json_is_machine_readable(self) -> None:
        changed = gate.resolve_changed_files(self.root, explicit_files=["tools/local-ci-gate/example.py"], include_untracked=False)
        profile = gate.load_profile(self.profile_path)
        report = gate.run_checks(
            self.root,
            profile,
            changed,
            dry_run=True,
            report_dir=self.root / "reports",
            governance_root="/governance",
            governance_ref="abc123",
            shim_path="/repo/.hldpro/local-ci.sh",
            argv=("--profile", "test-profile"),
            cwd="/repo",
            runner_path="/governance/tools/local-ci-gate/bin/hldpro-local-ci",
        )
        payload = sorted(report.report_dir.glob("*.json"))[-1].read_text(encoding="utf-8")
        data = json.loads(payload)

        self.assertEqual(data["profile"]["name"], "test-profile")
        self.assertEqual(data["profile"]["requires_dependencies"], ["python3"])
        self.assertEqual(data["verdict"], "planned")
        self.assertEqual(data["changed_files"]["files"], ["tools/local-ci-gate/example.py"])
        self.assertEqual(
            data["invocation"],
            {
                "governance_root": "/governance",
                "governance_ref": "abc123",
                "shim_path": "/repo/.hldpro/local-ci.sh",
                "argv": ["--profile", "test-profile"],
                "cwd": "/repo",
                "runner_path": "/governance/tools/local-ci-gate/bin/hldpro-local-ci",
            },
        )

    def test_profile_rejects_duplicate_check_ids(self) -> None:
        duplicate = self.root / "duplicate.yml"
        duplicate.write_text(
            """
profile:
  name: duplicate
  description: Duplicate check ids
  checks:
    - id: same
      title: First
      severity: blocker
      command:
        - python3
        - -c
        - "print('first')"
    - id: same
      title: Second
      severity: blocker
      command:
        - python3
        - -c
        - "print('second')"
""".strip()
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(gate.GateError, "duplicate check id: same"):
            gate.load_profile(duplicate)

    def test_profile_rejects_malformed_dependency_metadata(self) -> None:
        invalid = self.root / "invalid-dependencies.yml"
        invalid.write_text(
            """
profile:
  name: invalid-dependencies
  description: Invalid dependency metadata
  requires_dependencies:
    - npm
    - ""
  checks: []
""".strip()
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(gate.GateError, "requires_dependencies"):
            gate.load_profile(invalid)

    def test_changed_files_file_accepts_null_separated_entries(self) -> None:
        changed_files = self.root / "changed-files.txt"
        changed_files.write_text("scripts/example.py\0tools/local-ci-gate/example.py\0", encoding="utf-8")

        changed = gate.resolve_changed_files(self.root, changed_files_file=changed_files)

        self.assertEqual(changed.source, f"file:{changed_files}")
        self.assertEqual(changed.files, ("scripts/example.py", "tools/local-ci-gate/example.py"))

    def test_bundled_profiles_load(self) -> None:
        profile_paths = sorted(PROFILES_DIR.glob("*.yml"))

        self.assertGreaterEqual(len(profile_paths), 2)
        profiles = [gate.load_profile(path) for path in profile_paths]

        self.assertIn("ai-integration-services", {profile.name for profile in profiles})
        self.assertIn("hldpro-governance", {profile.name for profile in profiles})
        self.assertIn("knocktracker", {profile.name for profile in profiles})
        self.assertIn("local-ai-machine", {profile.name for profile in profiles})
        for profile in profiles:
            self.assertTrue(profile.checks)
            self.assertEqual(profile.report_root, Path("cache/local-ci-gate/reports"))
            self.assertTrue(profile.requires_dependencies)
            check_ids = [check.id for check in profile.checks]
            self.assertEqual(len(check_ids), len(set(check_ids)))

    def test_governance_profile_uses_active_execution_scope_placeholder(self) -> None:
        profile = gate.load_profile(PROFILES_DIR / "hldpro-governance.yml")
        planner_boundary = next(check for check in profile.checks if check.id == "planner-boundary")

        self.assertIn("{execution_scope}", planner_boundary.command)
        self.assertNotIn("issue-253", " ".join(planner_boundary.command))

    def test_governance_profile_runs_handoff_validator_for_handoff_paths(self) -> None:
        profile = gate.load_profile(PROFILES_DIR / "hldpro-governance.yml")
        changed = gate.resolve_changed_files(
            self.root,
            explicit_files=["raw/handoffs/2026-04-21-issue-435-plan-to-implementation.json"],
            include_untracked=False,
        )

        report = gate.run_checks(self.root, profile, changed, dry_run=True, report_dir=self.root / "reports")
        statuses = {result.check.id: result.status for result in report.results}
        handoff = next(result for result in report.results if result.check.id == "handoff-package-integrity")

        self.assertEqual(statuses["handoff-package-integrity"], "planned")
        self.assertIn("scripts/overlord/validate_handoff_package.py", handoff.command)
        self.assertIn("--root", handoff.command)

    def test_governance_profile_skips_handoff_validator_for_unrelated_paths(self) -> None:
        profile = gate.load_profile(PROFILES_DIR / "hldpro-governance.yml")
        changed = gate.resolve_changed_files(
            self.root,
            explicit_files=["docs/runbooks/unrelated.md"],
            include_untracked=False,
        )

        report = gate.run_checks(self.root, profile, changed, dry_run=True, report_dir=self.root / "reports")
        statuses = {result.check.id: result.status for result in report.results}

        self.assertEqual(statuses["handoff-package-integrity"], "skipped")

    def test_governance_profile_runs_provisioning_evidence_validator_for_runbooks(self) -> None:
        profile = gate.load_profile(PROFILES_DIR / "hldpro-governance.yml")
        changed = gate.resolve_changed_files(
            self.root,
            explicit_files=["docs/runbooks/pages-deploy-gate.md"],
            include_untracked=False,
        )

        report = gate.run_checks(self.root, profile, changed, dry_run=True, report_dir=self.root / "reports")
        provisioning = next(result for result in report.results if result.check.id == "provisioning-evidence-safety")

        self.assertEqual(provisioning.status, "planned")
        self.assertIn("scripts/overlord/validate_provisioning_evidence.py", provisioning.command)
        self.assertIn("--changed-files-file", provisioning.command)

    def test_governance_profile_skips_provisioning_evidence_validator_for_unrelated_paths(self) -> None:
        profile = gate.load_profile(PROFILES_DIR / "hldpro-governance.yml")
        changed = gate.resolve_changed_files(
            self.root,
            explicit_files=["docs/plans/issue-999-example.md"],
            include_untracked=False,
        )

        report = gate.run_checks(self.root, profile, changed, dry_run=True, report_dir=self.root / "reports")
        statuses = {result.check.id: result.status for result in report.results}

        self.assertEqual(statuses["provisioning-evidence-safety"], "skipped")

    def test_execution_scope_resolution_prefers_active_issue_implementation_scope(self) -> None:
        scope_dir = self.root / "raw" / "execution-scopes"
        scope_dir.mkdir(parents=True)
        planning = scope_dir / "2026-04-18-issue-275-planning.json"
        implementation = scope_dir / "2026-04-18-issue-275-implementation.json"
        planning.write_text("{}\n", encoding="utf-8")
        implementation.write_text('{"lane_claim": {"issue_number": 275}}\n', encoding="utf-8")

        resolved = gate._resolve_execution_scope(self.root, "feature/issue-275-local-ci-enforcement-remediation")

        self.assertEqual(resolved, "raw/execution-scopes/2026-04-18-issue-275-implementation.json")

    def test_execution_scope_resolution_requires_matching_lane_claim(self) -> None:
        scope_dir = self.root / "raw" / "execution-scopes"
        scope_dir.mkdir(parents=True)
        implementation = scope_dir / "2026-04-18-issue-275-implementation.json"
        implementation.write_text('{"lane_claim": {"issue_number": 276}}\n', encoding="utf-8")

        with self.assertRaises(gate.GateError) as ctx:
            gate._resolve_execution_scope(self.root, "feature/issue-275-local-ci-enforcement-remediation")

        self.assertIn("lane_claim.issue_number=275", str(ctx.exception))

    def test_knocktracker_profile_scopes_heavy_checks_to_matching_files(self) -> None:
        profile = gate.load_profile(PROFILES_DIR / "knocktracker.yml")
        changed = gate.resolve_changed_files(
            self.root,
            explicit_files=["app/(main)/map.web.tsx"],
            include_untracked=False,
        )

        report = gate.run_checks(self.root, profile, changed, dry_run=True, report_dir=self.root / "reports")
        statuses = {result.check.id: result.status for result in report.results}

        self.assertEqual(statuses["brand-verify"], "planned")
        self.assertEqual(statuses["lint"], "planned")
        self.assertEqual(statuses["typecheck"], "planned")
        self.assertEqual(statuses["file-index-check"], "planned")
        self.assertEqual(statuses["routing-tests"], "planned")
        self.assertEqual(statuses["web-build"], "planned")
        self.assertEqual(statuses["track-logic-tests"], "skipped")
        self.assertEqual(statuses["edge-contract-tests"], "skipped")
        self.assertEqual(statuses["manager-dashboard-contract-tests"], "skipped")
        self.assertIn("CI remains authoritative", report.summary)

    def test_ai_integration_services_profile_scopes_app_builds(self) -> None:
        profile = gate.load_profile(PROFILES_DIR / "ai-integration-services.yml")
        changed = gate.resolve_changed_files(
            self.root,
            explicit_files=["apps/marketing/src/App.tsx"],
            include_untracked=False,
        )

        report = gate.run_checks(self.root, profile, changed, dry_run=True, report_dir=self.root / "reports")
        statuses = {result.check.id: result.status for result in report.results}

        self.assertEqual(statuses["typecheck"], "planned")
        self.assertEqual(statuses["marketing-build"], "planned")
        self.assertEqual(statuses["dashboard-build"], "skipped")
        self.assertEqual(statuses["reseller-build"], "skipped")
        self.assertEqual(statuses["pwa-build"], "skipped")
        self.assertEqual(statuses["error-handler-audit"], "skipped")
        self.assertEqual(statuses["preflight-probe"], "skipped")
        self.assertEqual(statuses["playwright-smoke"], "skipped")
        self.assertIn("CI remains authoritative", report.summary)

    def test_local_ai_machine_profile_scopes_contract_checks(self) -> None:
        profile = gate.load_profile(PROFILES_DIR / "local-ai-machine.yml")
        changed = gate.resolve_changed_files(
            self.root,
            explicit_files=["scripts/microvm/boot_run.sh", "src/workflows/runtime_envelope.ts"],
            include_untracked=False,
        )

        report = gate.run_checks(self.root, profile, changed, dry_run=True, report_dir=self.root / "reports")
        statuses = {result.check.id: result.status for result in report.results}

        self.assertEqual(statuses["agents-governance-contract"], "planned")
        self.assertEqual(statuses["env-var-docs-contract"], "planned")
        self.assertEqual(statuses["clean-branch-governance-contract"], "planned")
        self.assertEqual(statuses["fail-fast-governance-contract"], "planned")
        self.assertEqual(statuses["microvm-boot-contract"], "planned")
        self.assertEqual(statuses["durable-workflow-tests"], "planned")
        self.assertEqual(statuses["edge-critic-contract"], "skipped")
        self.assertEqual(statuses["inference-router-contract"], "skipped")
        self.assertEqual(statuses["critic-runner-contract"], "skipped")
        self.assertIn("CI remains authoritative", report.summary)


if __name__ == "__main__":
    unittest.main()
