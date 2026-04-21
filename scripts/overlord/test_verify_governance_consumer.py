#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("verify_governance_consumer.py")
DEPLOY_MODULE_PATH = Path(__file__).with_name("deploy_governance_tooling.py")
REPO_ROOT = MODULE_PATH.resolve().parents[2]
sys.path.insert(0, str(MODULE_PATH.parent))

DEPLOY_SPEC = importlib.util.spec_from_file_location("deploy_governance_tooling", DEPLOY_MODULE_PATH)
assert DEPLOY_SPEC is not None
assert DEPLOY_SPEC.loader is not None
deploy_governance_tooling = importlib.util.module_from_spec(DEPLOY_SPEC)
sys.modules[DEPLOY_SPEC.name] = deploy_governance_tooling
DEPLOY_SPEC.loader.exec_module(deploy_governance_tooling)

SPEC = importlib.util.spec_from_file_location("verify_governance_consumer", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
verify_governance_consumer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = verify_governance_consumer
SPEC.loader.exec_module(verify_governance_consumer)


class TestVerifyGovernanceConsumer(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.product = self.root / "consumer"
        self.product.mkdir()
        subprocess.run(["git", "init"], cwd=self.product, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.product, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.product, check=True)
        (self.product / "README.md").write_text("# consumer\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=self.product, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=self.product, check=True, capture_output=True, text=True)
        self.ref = "a" * 40

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _deploy(self, ref: str | None = None, profile: str = "hldpro-governance", package_version: str = "") -> None:
        args = [
            "apply",
            "--governance-root",
            str(REPO_ROOT),
            "--target-repo",
            str(self.product),
            "--governance-ref",
            ref or self.ref,
            "--profile",
            profile,
        ]
        if package_version:
            args.extend(["--package-version", package_version])
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            code = deploy_governance_tooling.main(args)
        self.assertEqual(code, 0)

    def _invoke(self, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = verify_governance_consumer.main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def _base_args(self) -> list[str]:
        return [
            "--governance-root",
            str(REPO_ROOT),
            "--target-repo",
            str(self.product),
            "--profile",
            "hldpro-governance",
            "--governance-ref",
            self.ref,
        ]

    def _record(self) -> Path:
        return self.product / ".hldpro" / "governance-tooling.json"

    def _shim(self) -> Path:
        return self.product / ".hldpro" / "local-ci.sh"

    def _read_record(self) -> dict:
        return json.loads(self._record().read_text(encoding="utf-8"))

    def _write_record(self, record: dict) -> None:
        self._record().write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    def _valid_override(self, reason: str = "temporary governance exception") -> dict:
        return {
            "issue": "#474",
            "reason": reason,
            "owner": "governance",
            "review_cadence": "quarterly",
        }

    def _next_package_version(self) -> str:
        manifest = json.loads((REPO_ROOT / "docs" / "governance-tooling-package.json").read_text(encoding="utf-8"))
        return manifest["versioning"]["next_contract_version"]

    def _required_constraints(self, profile: str) -> list[str]:
        manifest = json.loads((REPO_ROOT / "docs" / "governance-tooling-package.json").read_text(encoding="utf-8"))
        return manifest["profile_contract"]["required_profiles"][profile]["required_constraints"]

    def test_verify_passes_for_deployed_pinned_consumer_record(self) -> None:
        self._deploy()

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["failures"], [])
        self.assertEqual(payload["observed_overrides"], [])
        self.assertIn("central GitHub rules/settings are report-only", "\n".join(payload["warnings"]))

    def test_verify_fails_when_record_missing(self) -> None:
        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("consumer record missing", stderr)

    def test_verify_fails_when_governance_root_is_typoed(self) -> None:
        self._deploy()
        missing_root = self.root / "hldpro-governnance"

        code, stdout, stderr = self._invoke(
            "--governance-root",
            str(missing_root),
            "--target-repo",
            str(self.product),
            "--profile",
            "hldpro-governance",
            "--governance-ref",
            self.ref,
        )

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("governance root does not exist", stderr)

    def test_verify_fails_when_record_is_malformed_shape(self) -> None:
        record = self.product / ".hldpro" / "governance-tooling.json"
        record.parent.mkdir(parents=True)
        record.write_text("[]\n", encoding="utf-8")

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("consumer record must be a JSON object", stderr)

    def test_verify_fails_when_governance_ref_is_not_sha(self) -> None:
        self._deploy(ref="governance-tooling-v0.1.0")

        code, stdout, stderr = self._invoke(
            "--governance-root",
            str(REPO_ROOT),
            "--target-repo",
            str(self.product),
            "--profile",
            "hldpro-governance",
        )

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "failed")
        self.assertIn("governance_ref must be an exact 40-character lowercase git SHA", "\n".join(payload["failures"]))

    def test_verify_fails_when_shim_missing_marker(self) -> None:
        self._deploy()
        self._shim().write_text("#!/usr/bin/env bash\necho unmanaged\n", encoding="utf-8")

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("managed local CI shim missing marker", "\n".join(payload["failures"]))

    def test_verify_fails_when_expected_profile_mismatches(self) -> None:
        self._deploy()

        code, stdout, stderr = self._invoke(
            "--governance-root",
            str(REPO_ROOT),
            "--target-repo",
            str(self.product),
            "--profile",
            "knocktracker",
        )

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("profile mismatch", "\n".join(payload["failures"]))

    def test_verify_fails_when_managed_file_record_omits_expected_path(self) -> None:
        self._deploy()
        record = json.loads(self._record().read_text(encoding="utf-8"))
        record["managed_files"] = [item for item in record["managed_files"] if item["path"] != ".hldpro/local-ci.sh"]
        self._record().write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("managed_files missing expected path", "\n".join(payload["failures"]))

    def test_verify_fails_when_profile_is_unknown(self) -> None:
        self._deploy()
        record = self._read_record()
        record["profile"] = "unknown-repo-profile"
        self._write_record(record)

        code, stdout, stderr = self._invoke(
            "--governance-root",
            str(REPO_ROOT),
            "--target-repo",
            str(self.product),
        )

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("unknown profile", "\n".join(payload["failures"]))

    def test_verify_fails_when_profile_is_missing(self) -> None:
        self._deploy()
        record = self._read_record()
        record.pop("profile")
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("consumer record missing field: profile", "\n".join(payload["failures"]))
        self.assertIn("profile must be a non-empty string", "\n".join(payload["failures"]))

    def test_verify_fails_for_mutable_governance_workflow_ref(self) -> None:
        self._deploy()
        workflow = self.product / ".github" / "workflows" / "governance.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text(
            "jobs:\n  check:\n    uses: NIBARGERB-HLDPRO/hldpro-governance/.github/workflows/governance-check.yml@main\n",
            encoding="utf-8",
        )

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("reusable workflow ref must be pinned", "\n".join(payload["failures"]))

    def test_verify_fails_workflow_ref_is_tag(self) -> None:
        self._deploy()
        workflow = self.product / ".github" / "workflows" / "governance.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text(
            "jobs:\n  check:\n    uses: NIBARGERB-HLDPRO/hldpro-governance/.github/workflows/governance-check.yml@v1.0.0\n",
            encoding="utf-8",
        )

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("reusable workflow ref must be pinned", failures_text)
        self.assertIn("@v1.0.0", failures_text)

    def test_verify_fails_workflow_ref_is_short_sha(self) -> None:
        self._deploy()
        workflow = self.product / ".github" / "workflows" / "governance.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text(
            "jobs:\n  check:\n    uses: NIBARGERB-HLDPRO/hldpro-governance/.github/workflows/governance-check.yml@abc1234\n",
            encoding="utf-8",
        )

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("reusable workflow ref must be pinned", failures_text)
        self.assertIn("@abc1234", failures_text)

    def test_verify_fails_workflow_ref_sha_mismatch(self) -> None:
        self._deploy()
        workflow = self.product / ".github" / "workflows" / "governance.yml"
        workflow.parent.mkdir(parents=True)
        wrong_sha = "b" * 40
        workflow.write_text(
            f"jobs:\n  check:\n    uses: NIBARGERB-HLDPRO/hldpro-governance/.github/workflows/governance-check.yml@{wrong_sha}\n",
            encoding="utf-8",
        )

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("reusable workflow ref SHA mismatch", failures_text)
        self.assertIn(wrong_sha, failures_text)

    def test_verify_fails_stale_workflow_ref_before_acceptance(self) -> None:
        self._deploy()
        workflow = self.product / ".github" / "workflows" / "governance.yml"
        workflow.parent.mkdir(parents=True)
        stale_sha = "c" * 40
        workflow.write_text(
            "jobs:\n"
            "  governance:\n"
            "    uses: "
            f"NIBARGERB-HLDPRO/hldpro-governance/.github/workflows/governance-check.yml@{stale_sha}\n",
            encoding="utf-8",
        )

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("reusable workflow ref SHA mismatch", failures_text)
        self.assertIn(stale_sha, failures_text)

    def test_verify_fails_for_managed_hook_checksum_drift(self) -> None:
        self._deploy()
        hook = self.product / ".claude" / "hooks" / "pre-tool-use.sh"
        hook.parent.mkdir(parents=True)
        hook.write_text("# hldpro-governance managed\necho ok\n", encoding="utf-8")
        record = self._read_record()
        record["managed_files"].append(
            {
                "path": ".claude/hooks/pre-tool-use.sh",
                "type": "managed_hook",
                "sha256": "0" * 64,
            }
        )
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("managed file checksum drift", "\n".join(payload["failures"]))

    def test_verify_fails_for_managed_hook_missing_marker(self) -> None:
        self._deploy()
        hook = self.product / ".claude" / "hooks" / "pre-tool-use.sh"
        hook.parent.mkdir(parents=True)
        hook.write_text("echo unmanaged\n", encoding="utf-8")
        record = self._read_record()
        record["managed_files"].append({"path": ".claude/hooks/pre-tool-use.sh", "type": "managed_hook"})
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("managed file missing marker", "\n".join(payload["failures"]))

    def test_verify_fails_for_invalid_override_metadata_and_reports_observed_override(self) -> None:
        self._deploy()
        record = self._read_record()
        record["overrides"] = [{"issue": "#454", "reason": "fixture"}]
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["observed_overrides"], [{"issue": "#454", "reason": "fixture"}])
        self.assertIn("missing required override metadata: owner", "\n".join(payload["failures"]))
        self.assertIn("review_cadence or expires_at", "\n".join(payload["failures"]))

    def test_verify_fails_for_malformed_local_overrides(self) -> None:
        self._deploy()
        record = self._read_record()
        record["local_overrides"] = [{"issue": "#537", "reason": "fixture"}]
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["observed_overrides"], [{"issue": "#537", "reason": "fixture"}])
        failures_text = "\n".join(payload["failures"])
        self.assertIn("local_overrides[0] missing required override metadata: owner", failures_text)
        self.assertIn("local_overrides[0] missing required override metadata: review_cadence or expires_at", failures_text)

    def test_verify_fails_override_empty_owner(self) -> None:
        self._deploy()
        record = self._read_record()
        override = self._valid_override()
        override["owner"] = ""
        record["overrides"] = [override]
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("non-empty string: owner", failures_text)

    def test_verify_fails_override_non_string_reason(self) -> None:
        self._deploy()
        record = self._read_record()
        override = self._valid_override()
        override["reason"] = 42
        record["overrides"] = [override]
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("non-empty string: reason", failures_text)

    def test_verify_fails_override_empty_expires_at(self) -> None:
        self._deploy()
        record = self._read_record()
        override = {
            "issue": "#474",
            "reason": "temporary governance exception",
            "owner": "governance",
            "expires_at": "",
        }
        record["overrides"] = [override]
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("review_cadence or expires_at", failures_text)

    def test_verify_fails_override_weakens_healthcareplatform_hipaa(self) -> None:
        self._deploy()
        record = self._read_record()
        record["overrides"] = [self._valid_override("disable HIPAA checks for development")]
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("forbidden override", failures_text)
        self.assertIn("HealthcarePlatform", failures_text)

    def test_verify_fails_override_disables_seek_plan_mode(self) -> None:
        self._deploy()
        record = self._read_record()
        record["overrides"] = [self._valid_override("disable plan-mode enforcement for quick deploy")]
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("forbidden override", failures_text)
        self.assertIn("plan-mode", failures_text)

    def test_verify_fails_override_routes_pii_away_from_lam(self) -> None:
        self._deploy()
        record = self._read_record()
        record["overrides"] = [self._valid_override("route PII to cloud storage for analytics")]
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("forbidden override", failures_text)
        self.assertIn("LAM", failures_text)

    def test_verify_fails_override_core_fork_without_exception(self) -> None:
        self._deploy()
        record = self._read_record()
        record["overrides"] = [self._valid_override("fork core package to add local patches")]
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("forbidden override", failures_text)
        self.assertIn("core fork", failures_text)

    def test_verify_fails_override_disables_ci_required_gate(self) -> None:
        self._deploy()
        record = self._read_record()
        record["overrides"] = [self._valid_override("disable required-gate for hotfix deploy")]
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("forbidden override", failures_text)
        self.assertIn("CI-required gates", failures_text)

    def test_verify_fails_override_dry_run_as_live_evidence(self) -> None:
        self._deploy()
        record = self._read_record()
        record["overrides"] = [self._valid_override("treat dry-run results as live enforcement evidence")]
        self._write_record(record)

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        failures_text = "\n".join(payload["failures"])
        self.assertIn("forbidden override", failures_text)
        self.assertIn("dry-run", failures_text)

    def test_verify_fails_when_healthcareplatform_v2_profile_weakens_constraints(self) -> None:
        next_version = self._next_package_version()
        self._deploy(profile="healthcareplatform", package_version=next_version)
        constraints = self._required_constraints("healthcareplatform")
        record = self._read_record()
        record["schema_version"] = 2
        record["profile_constraints"] = [item for item in constraints if "strict lane naming" not in item]
        self._write_record(record)

        code, stdout, stderr = self._invoke(
            "--governance-root",
            str(REPO_ROOT),
            "--target-repo",
            str(self.product),
            "--profile",
            "healthcareplatform",
            "--governance-ref",
            self.ref,
            "--package-version",
            next_version,
        )

        self.assertEqual(code, 1, stderr)
        payload = json.loads(stdout)
        self.assertIn("profile constraints missing required constraint", "\n".join(payload["failures"]))

    def test_verify_passes_for_valid_v2_managed_consumer(self) -> None:
        next_version = self._next_package_version()
        self._deploy(profile="healthcareplatform", package_version=next_version)
        hook = self.product / ".claude" / "hooks" / "pre-tool-use.sh"
        hook.parent.mkdir(parents=True)
        hook.write_text("# hldpro-governance managed\necho ok\n", encoding="utf-8")
        record = self._read_record()
        record["schema_version"] = 2
        record["profile_constraints"] = self._required_constraints("healthcareplatform")
        record["overrides"] = [
            {
                "issue": "#454",
                "reason": "fixture stricter local hook",
                "owner": "governance",
                "review_cadence": "quarterly",
            }
        ]
        record["managed_files"].append(
            {
                "path": ".claude/hooks/pre-tool-use.sh",
                "type": "managed_hook",
                "sha256": hashlib.sha256(hook.read_bytes()).hexdigest(),
            }
        )
        self._write_record(record)
        workflow = self.product / ".github" / "workflows" / "governance.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text(
            f"jobs:\n  check:\n    uses: NIBARGERB-HLDPRO/hldpro-governance/.github/workflows/governance-check.yml@{self.ref}\n",
            encoding="utf-8",
        )

        code, stdout, stderr = self._invoke(
            "--governance-root",
            str(REPO_ROOT),
            "--target-repo",
            str(self.product),
            "--profile",
            "healthcareplatform",
            "--governance-ref",
            self.ref,
            "--package-version",
            next_version,
        )

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["failures"], [])
        self.assertEqual(payload["observed_overrides"][0]["owner"], "governance")


if __name__ == "__main__":
    unittest.main()
