#!/usr/bin/env python3
from __future__ import annotations

import contextlib
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

    def _deploy(self, ref: str | None = None) -> None:
        args = [
            "apply",
            "--governance-root",
            str(REPO_ROOT),
            "--target-repo",
            str(self.product),
            "--governance-ref",
            ref or self.ref,
            "--profile",
            "hldpro-governance",
        ]
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

    def test_verify_passes_for_deployed_pinned_consumer_record(self) -> None:
        self._deploy()

        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["failures"], [])
        self.assertIn("central GitHub rules/settings are report-only", "\n".join(payload["warnings"]))

    def test_verify_fails_when_record_missing(self) -> None:
        code, stdout, stderr = self._invoke(*self._base_args())

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("consumer record missing", stderr)

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


if __name__ == "__main__":
    unittest.main()
