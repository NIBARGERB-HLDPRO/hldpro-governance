#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys
from unittest import mock


MODULE_PATH = Path(__file__).with_name("deploy_governance_tooling.py")
REPO_ROOT = MODULE_PATH.resolve().parents[2]
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("deploy_governance_tooling", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
deploy_governance_tooling = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = deploy_governance_tooling
SPEC.loader.exec_module(deploy_governance_tooling)


class TestDeployGovernanceTooling(unittest.TestCase):
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
        self.ref = "abc123"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _invoke(self, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            mock.patch.object(deploy_governance_tooling, "_ensure_remote_reachable_governance_ref", return_value=None),
        ):
            code = deploy_governance_tooling.main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def _base_args(self) -> list[str]:
        return [
            "--governance-root",
            str(REPO_ROOT),
            "--target-repo",
            str(self.product),
            "--governance-ref",
            self.ref,
            "--profile",
            "hldpro-governance",
        ]

    def _record(self) -> Path:
        return (self.product / ".hldpro" / "governance-tooling.json").resolve()

    def _shim(self) -> Path:
        return (self.product / ".hldpro" / "local-ci.sh").resolve()

    def test_dry_run_plans_managed_files_without_writing(self) -> None:
        code, stdout, stderr = self._invoke("dry-run", *self._base_args())

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "planned")
        self.assertEqual(payload["governance_ref"], self.ref)
        self.assertEqual(payload["package_version"], "0.1.0-contract")
        self.assertEqual(payload["profile"], "hldpro-governance")
        self.assertIn(str(self._shim()), payload["planned_write_set"])
        self.assertIn(str(self._record()), payload["planned_write_set"])
        self.assertFalse(self._shim().exists())
        self.assertFalse(self._record().exists())

    def test_apply_writes_managed_shim_and_consumer_record(self) -> None:
        code, stdout, stderr = self._invoke("apply", *self._base_args())

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "applied")
        self.assertTrue(self._shim().exists())
        self.assertTrue(self._record().exists())
        self.assertIn(deploy_governance_tooling.deploy_local_ci_gate.MANAGED_MARKER, self._shim().read_text(encoding="utf-8"))
        record = json.loads(self._record().read_text(encoding="utf-8"))
        self.assertEqual(record["schema_version"], 1)
        self.assertEqual(record["governance_ref"], self.ref)
        self.assertEqual(record["package_version"], "0.1.0-contract")
        self.assertEqual(record["profile"], "hldpro-governance")
        self.assertEqual(record["overrides"], [])
        self.assertEqual({item["path"] for item in record["managed_files"]}, {".hldpro/local-ci.sh", ".hldpro/governance-tooling.json"})

    def test_apply_consumer_profile_records_required_session_contract_surfaces(self) -> None:
        (self.product / "CLAUDE.md").write_text("thin pointer\n", encoding="utf-8")
        (self.product / "CODEX.md").write_text("thin pointer\n", encoding="utf-8")
        runbook = self.product / "docs" / "EXTERNAL_SERVICES_RUNBOOK.md"
        runbook.parent.mkdir(parents=True, exist_ok=True)
        runbook.write_text("governance pointer\n", encoding="utf-8")
        review = self.product / "scripts" / "codex-review.sh"
        review.parent.mkdir(parents=True, exist_ok=True)
        review.write_text("#!/usr/bin/env bash\n# claude\n", encoding="utf-8")

        code, stdout, stderr = self._invoke(
            "apply",
            "--governance-root",
            str(REPO_ROOT),
            "--target-repo",
            str(self.product),
            "--governance-ref",
            self.ref,
            "--profile",
            "stampede",
            "--allow-dirty-target",
        )

        self.assertEqual(code, 0, stderr)
        record = json.loads(self._record().read_text(encoding="utf-8"))
        self.assertEqual(record["schema_version"], 2)
        self.assertEqual(record["package_version"], "0.3.0-hard-gated-som")
        self.assertEqual(
            {item["path"] for item in record["managed_files"]},
            {
                ".hldpro/local-ci.sh",
                ".hldpro/governance-tooling.json",
                ".hldpro/hldpro-sim.json",
                ".claude/settings.json",
                "CLAUDE.md",
                "CODEX.md",
                "docs/EXTERNAL_SERVICES_RUNBOOK.md",
                "scripts/codex-review.sh",
            },
        )

    def test_verify_passes_after_apply(self) -> None:
        apply_code, _, apply_err = self._invoke("apply", *self._base_args())
        self.assertEqual(apply_code, 0, apply_err)

        code, stdout, stderr = self._invoke("verify", *self._base_args())

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "verified")
        self.assertEqual(payload["failures"], [])

    def test_rollback_removes_managed_files(self) -> None:
        apply_code, _, apply_err = self._invoke("apply", *self._base_args())
        self.assertEqual(apply_code, 0, apply_err)

        code, stdout, stderr = self._invoke("rollback", *self._base_args(), "--allow-dirty-target")

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "rolled_back")
        self.assertFalse(self._shim().exists())
        self.assertFalse(self._record().exists())

    def test_apply_is_idempotent_for_managed_files(self) -> None:
        first_code, _, first_err = self._invoke("apply", *self._base_args())
        self.assertEqual(first_code, 0, first_err)
        second_code, stdout, stderr = self._invoke("apply", *self._base_args(), "--allow-dirty-target")

        self.assertEqual(second_code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "applied")
        self.assertTrue(self._shim().exists())
        self.assertTrue(self._record().exists())

    def test_apply_refuses_unmanaged_shim_by_default(self) -> None:
        self._shim().parent.mkdir(parents=True, exist_ok=True)
        self._shim().write_text("#!/usr/bin/env bash\necho unmanaged\n", encoding="utf-8")

        code, stdout, stderr = self._invoke("apply", *self._base_args(), "--allow-dirty-target")

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("refusing to overwrite unmanaged shim", stderr)
        self.assertFalse(self._record().exists())

    def test_apply_refuses_unmanaged_consumer_record_by_default(self) -> None:
        self._record().parent.mkdir(parents=True, exist_ok=True)
        self._record().write_text("not json\n", encoding="utf-8")

        code, stdout, stderr = self._invoke("apply", *self._base_args(), "--allow-dirty-target")

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("refusing to overwrite unmanaged consumer record", stderr)

    def test_apply_refuses_dirty_target_by_default(self) -> None:
        (self.product / "dirty.txt").write_text("dirty\n", encoding="utf-8")

        code, stdout, stderr = self._invoke("apply", *self._base_args())

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("refusing to modify dirty target repo", stderr)
        self.assertFalse(self._shim().exists())
        self.assertFalse(self._record().exists())

    def test_verify_fails_when_record_is_missing(self) -> None:
        code, stdout, stderr = self._invoke("verify", *self._base_args())

        self.assertEqual(code, 1)
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "failed")
        self.assertIn("consumer record missing or unmanaged", "\n".join(payload["failures"]))
        self.assertEqual(stderr, "")

    def test_verify_fails_when_managed_shim_body_is_tampered(self) -> None:
        apply_code, _, apply_err = self._invoke("apply", *self._base_args())
        self.assertEqual(apply_code, 0, apply_err)
        self._shim().write_text(
            self._shim().read_text(encoding="utf-8").replace("abc123", "wrong-ref"),
            encoding="utf-8",
        )

        code, stdout, stderr = self._invoke("verify", *self._base_args())

        self.assertEqual(code, 1)
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "failed")
        self.assertIn("managed shim content mismatch", "\n".join(payload["failures"]))
        self.assertEqual(stderr, "")

    def test_rollback_refuses_unmanaged_record_before_removing_shim(self) -> None:
        apply_code, _, apply_err = self._invoke("apply", *self._base_args())
        self.assertEqual(apply_code, 0, apply_err)
        self._record().write_text("not json\n", encoding="utf-8")

        code, stdout, stderr = self._invoke("rollback", *self._base_args(), "--allow-dirty-target")

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("refusing to remove unmanaged consumer record", stderr)
        self.assertTrue(self._shim().exists())
        self.assertTrue(self._record().exists())

    def test_real_e2e_apply_verify_rollback_against_temp_git_repo(self) -> None:
        dry_code, dry_stdout, dry_err = self._invoke("dry-run", *self._base_args())
        self.assertEqual(dry_code, 0, dry_err)
        self.assertEqual(json.loads(dry_stdout)["status"], "planned")

        apply_code, apply_stdout, apply_err = self._invoke("apply", *self._base_args())
        self.assertEqual(apply_code, 0, apply_err)
        self.assertEqual(json.loads(apply_stdout)["status"], "applied")

        verify_code, verify_stdout, verify_err = self._invoke("verify", *self._base_args())
        self.assertEqual(verify_code, 0, verify_err)
        self.assertEqual(json.loads(verify_stdout)["status"], "verified")

    def test_apply_fails_when_remote_governance_ref_is_not_reachable(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            mock.patch.object(
                deploy_governance_tooling,
                "_ensure_remote_reachable_governance_ref",
                side_effect=deploy_governance_tooling.GovernanceDeployError("unreachable sha"),
            ),
        ):
            code = deploy_governance_tooling.main(["apply", *self._base_args()])
        self.assertEqual(code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("unreachable sha", stderr.getvalue())

    def test_dry_run_does_not_require_remote_governance_ref_reachability(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            mock.patch.object(
                deploy_governance_tooling,
                "_ensure_remote_reachable_governance_ref",
                side_effect=deploy_governance_tooling.GovernanceDeployError("unreachable sha"),
            ),
        ):
            code = deploy_governance_tooling.main(["dry-run", *self._base_args()])
        self.assertEqual(code, 0, stderr.getvalue())
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["status"], "planned")

    def test_rollback_does_not_require_remote_governance_ref_reachability(self) -> None:
        apply_code, _, apply_err = self._invoke("apply", *self._base_args())
        self.assertEqual(apply_code, 0, apply_err)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            mock.patch.object(
                deploy_governance_tooling,
                "_ensure_remote_reachable_governance_ref",
                side_effect=deploy_governance_tooling.GovernanceDeployError("unreachable sha"),
            ),
        ):
            code = deploy_governance_tooling.main(["rollback", *self._base_args(), "--allow-dirty-target"])
        self.assertEqual(code, 0, stderr.getvalue())
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["status"], "rolled_back")

        rollback_code, rollback_stdout, rollback_err = self._invoke("rollback", *self._base_args(), "--allow-dirty-target")
        self.assertEqual(rollback_code, 0, rollback_err)
        self.assertEqual(json.loads(rollback_stdout)["status"], "rolled_back")
        self.assertFalse(self._shim().exists())
        self.assertFalse(self._record().exists())

    def test_apply_fails_when_governance_ref_is_not_remote_reachable(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            mock.patch.object(
                deploy_governance_tooling,
                "_ensure_remote_reachable_governance_ref",
                side_effect=deploy_governance_tooling.GovernanceDeployError("governance_ref must be reachable"),
            ),
        ):
            code = deploy_governance_tooling.main(["apply", *self._base_args()])

        self.assertEqual(code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("governance_ref must be reachable", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
