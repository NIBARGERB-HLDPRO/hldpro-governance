#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys


MODULE_PATH = Path(__file__).with_name("deploy_local_ci_gate.py")
SPEC = importlib.util.spec_from_file_location("deploy_local_ci_gate", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
deploy_local_ci_gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = deploy_local_ci_gate
SPEC.loader.exec_module(deploy_local_ci_gate)


class TestDeployLocalCIGate(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.gov = self.root / "hldpro-governance"
        self.gov.mkdir()
        self.product = self.root / "knocktracker"
        self.product.mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _invoke(self, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = deploy_local_ci_gate.main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def _shim(self, relative_path: str = ".hldpro/local-ci.sh") -> Path:
        return self.product / relative_path

    def _write_fake_runner(self, root: Path) -> None:
        runner = root / "tools" / "local-ci-gate" / "bin" / "hldpro-local-ci"
        runner.parent.mkdir(parents=True, exist_ok=True)
        runner.write_text(
            "import json, sys\nprint(json.dumps({'argv': sys.argv[1:]}))\n",
            encoding="utf-8",
        )

    def test_resolve_reports_repo_local_target_and_write_set(self) -> None:
        code, stdout, stderr = self._invoke(
            "resolve",
            "--governance-root",
            str(self.gov),
            "--target-repo",
            str(self.product),
            "--shim-path",
            ".governance/local-ci.sh",
            "--governance-ref",
            "abc123",
        )

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["governance_root"], str(self.gov.resolve()))
        self.assertEqual(payload["governance_ref"], "abc123")
        self.assertEqual(payload["target_repo"], str(self.product.resolve()))
        self.assertEqual(payload["profile"], "hldpro-governance")
        self.assertEqual(payload["shim_path"], str((self.product / ".governance/local-ci.sh").resolve()))
        self.assertEqual(payload["governance_source"], str((self.gov / "tools/local-ci-gate").resolve()))
        self.assertEqual(payload["planned_write_set"], [str((self.product / ".governance/local-ci.sh").resolve())])
        self.assertEqual(payload["existing_shim_state"], "missing")

    def test_dry_run_includes_managed_body_and_command_preview(self) -> None:
        code, stdout, stderr = self._invoke(
            "dry-run",
            "--governance-root",
            str(self.gov),
            "--target-repo",
            str(self.product),
            "--governance-ref",
            "abc123",
        )

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertIn(deploy_local_ci_gate.MANAGED_MARKER, payload["shim_body"])
        self.assertIn("--governance-ref", payload["shim_body"])
        self.assertIn("HLDPRO_GOVERNANCE_ROOT", payload["shim_body"])
        self.assertIn('EMBEDDED_GOVERNANCE_ROOT="', payload["shim_body"])
        self.assertIn('RUNNER_PATH="${GOVERNANCE_ROOT}/tools/local-ci-gate/bin/hldpro-local-ci"', payload["shim_body"])
        self.assertIn('exec python3 "${RUNNER_PATH}" run', payload["shim_body"])
        self.assertIn('--governance-root "${GOVERNANCE_ROOT}"', payload["shim_body"])
        self.assertIn(str(self.gov.resolve()), payload["shim_body"])
        self.assertEqual(payload["planned_write_set"], [str(self._shim().resolve())])
        self.assertEqual(payload["command_preview"][0], deploy_local_ci_gate.sys.executable)

    def test_install_refuses_unmanaged_existing_shim_without_override(self) -> None:
        shim = self._shim()
        shim.parent.mkdir(parents=True, exist_ok=True)
        shim.write_text("#!/usr/bin/env bash\necho unmanaged\n", encoding="utf-8")

        code, stdout, stderr = self._invoke(
            "install",
            "--governance-root",
            str(self.gov),
            "--target-repo",
            str(self.product),
        )

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("refusing to overwrite unmanaged shim", stderr)
        self.assertEqual(shim.read_text(encoding="utf-8"), "#!/usr/bin/env bash\necho unmanaged\n")

    def test_install_with_backup_existing_renames_unmanaged_shim(self) -> None:
        shim = self._shim()
        shim.parent.mkdir(parents=True, exist_ok=True)
        shim.write_text("#!/usr/bin/env bash\necho unmanaged\n", encoding="utf-8")

        code, stdout, stderr = self._invoke(
            "install",
            "--governance-root",
            str(self.gov),
            "--target-repo",
            str(self.product),
            "--backup-existing",
            "--governance-ref",
            "abc123",
        )

        self.assertEqual(code, 0, stderr)
        self.assertIn("installed managed shim", stdout)
        backup = shim.with_name("local-ci.sh.pre-local-ci-gate")
        self.assertTrue(backup.exists())
        self.assertEqual(backup.read_text(encoding="utf-8"), "#!/usr/bin/env bash\necho unmanaged\n")
        body = shim.read_text(encoding="utf-8")
        self.assertIn(deploy_local_ci_gate.MANAGED_MARKER, body)
        self.assertIn("abc123", body)
        self.assertIn("HLDPRO_GOVERNANCE_ROOT", body)
        self.assertIn(str(self.gov.resolve()), body)

    def test_installed_shim_uses_embedded_root_then_env_override(self) -> None:
        override = self.root / "override-governance"
        override.mkdir()
        self._write_fake_runner(self.gov)
        self._write_fake_runner(override)

        code, stdout, stderr = self._invoke(
            "install",
            "--governance-root",
            str(self.gov),
            "--target-repo",
            str(self.product),
            "--governance-ref",
            "abc123",
        )
        self.assertEqual(code, 0, stderr)
        self.assertIn("installed managed shim", stdout)

        fallback = subprocess.run([str(self._shim())], cwd=self.product, capture_output=True, text=True, check=False)
        self.assertEqual(fallback.returncode, 0, fallback.stderr)
        fallback_payload = json.loads(fallback.stdout)
        self.assertIn(str(self.gov.resolve()), fallback_payload["argv"])

        env = os.environ.copy()
        env["HLDPRO_GOVERNANCE_ROOT"] = str(override.resolve())
        overridden = subprocess.run([str(self._shim())], cwd=self.product, env=env, capture_output=True, text=True, check=False)
        self.assertEqual(overridden.returncode, 0, overridden.stderr)
        overridden_payload = json.loads(overridden.stdout)
        self.assertIn(str(override.resolve()), overridden_payload["argv"])

    def test_refresh_updates_managed_shim_content(self) -> None:
        shim = self._shim()
        shim.parent.mkdir(parents=True, exist_ok=True)
        shim.write_text(
            "\n".join(
                [
                    "#!/usr/bin/env bash",
                    deploy_local_ci_gate.MANAGED_MARKER,
                    'exec python3 "/old/runner" run',
                    "",
                ]
            ),
            encoding="utf-8",
        )

        code, stdout, stderr = self._invoke(
            "refresh",
            "--governance-root",
            str(self.gov),
            "--target-repo",
            str(self.product),
            "--governance-ref",
            "def456",
        )

        self.assertEqual(code, 0, stderr)
        self.assertIn("refreshed managed shim", stdout)
        body = shim.read_text(encoding="utf-8")
        self.assertIn(deploy_local_ci_gate.MANAGED_MARKER, body)
        self.assertIn("def456", body)
        self.assertNotIn("/old/runner", body)

    def test_rejects_shim_paths_outside_the_repo_local_allowlist(self) -> None:
        code, stdout, stderr = self._invoke(
            "resolve",
            "--governance-root",
            str(self.gov),
            "--target-repo",
            str(self.product),
            "--shim-path",
            "../escape.sh",
        )

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("shim path must stay under target repo", stderr)


if __name__ == "__main__":
    unittest.main()
