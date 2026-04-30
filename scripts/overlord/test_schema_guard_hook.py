#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / "hooks" / "schema-guard.sh"


def _payload(command: str) -> str:
    return json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})


def _run_hook(
    payload: str,
    *,
    env: dict[str, str] | None = None,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    merged_env = dict(os.environ)
    if env:
        merged_env.update(env)
    return subprocess.run(
        ["bash", str(HOOK)],
        cwd=cwd or REPO_ROOT,
        input=payload,
        text=True,
        capture_output=True,
        env=merged_env,
        check=False,
    )


class TestSchemaGuardHook(unittest.TestCase):
    def test_blocked_bash_file_write_has_stderr(self) -> None:
        result = _run_hook(_payload("cat > scripts/new_file.py <<'PY'\nprint('x')\nPY"))

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("schema-guard: BLOCKED: Bash file write detected for scripts/new_file.py", result.stderr)
        self.assertIn("SoM write-boundary", result.stderr)
        self.assertIn("Worker handoff", result.stderr)

    def test_trivial_plan_bypass_still_reaches_som_write_block(self) -> None:
        result = _run_hook(
            _payload("cat > scripts/new_file.py <<'PY'\nprint('x')\nPY"),
            env={"PLAN_GATE_BYPASS": "true", "PLAN_GATE_TRIVIAL_SINGLE_LINE": "true"},
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema-guard: BLOCKED: Bash file write detected", result.stderr)
        self.assertIn("SoM write-boundary", result.stderr)
        self.assertIn("Worker handoff", result.stderr)

    def test_missing_schema_has_explicit_stderr(self) -> None:
        result = _run_hook(
            _payload("git status --short"),
            env={"SCHEMA_GUARD_REQUIRED_SCHEMA": "docs/schemas/does-not-exist.schema.json"},
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema-guard: FAIL: missing schema docs/schemas/does-not-exist.schema.json", result.stderr)

    def test_malformed_input_payload_has_stderr(self) -> None:
        result = _run_hook("{not-json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema-guard: FAIL: malformed input payload", result.stderr)

    def test_validator_nonzero_is_summarized(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            validator = Path(raw) / "validator.sh"
            validator.write_text("#!/bin/bash\necho validator detail >&2\nexit 7\n", encoding="utf-8")
            validator.chmod(0o755)

            result = _run_hook(
                _payload("git status --short"),
                env={"SCHEMA_GUARD_VALIDATOR": str(validator)},
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema-guard: FAIL: validation failed while running", result.stderr)
        self.assertIn("exit 7", result.stderr)
        self.assertIn("validator detail", result.stderr)

    def test_allowed_read_only_command_remains_allowed(self) -> None:
        result = _run_hook(_payload("git status --short"))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_quoted_awk_comparison_remains_allowed(self) -> None:
        result = _run_hook(_payload("awk '$1 > 1 { print $0 }' input.txt"))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_quoted_jq_comparison_remains_allowed(self) -> None:
        result = _run_hook(_payload("jq '.value > 1' input.json"))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_common_read_only_analysis_pipelines_remain_allowed(self) -> None:
        commands = [
            "grep -R 'PLAN_GATE_BLOCKED' docs scripts | sort",
            "rg --files | sort | wc -l",
            "git status --short | wc -l",
            "find docs -type f | sort | head -20",
        ]

        for command in commands:
            with self.subTest(command=command):
                result = _run_hook(_payload(command))

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, "")

    def test_python_file_write_policy_block_has_stderr(self) -> None:
        result = _run_hook(_payload("python3 - <<'PY'\nfrom pathlib import Path\nPath('x.py').write_text('x')\nPY"))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema-guard: PLAN_GATE_BLOCKED", result.stderr)
        self.assertIn("<python file write>", result.stderr)

    def test_missing_helper_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)

            result = _run_hook(_payload("cat > scripts/new_file.py <<'PY'\nprint('x')\nPY"), cwd=root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema-guard: FAIL: missing helper scripts/overlord/check_plan_preflight.py", result.stderr)

    def test_unknown_helper_decision_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            helper_dir = root / "scripts" / "overlord"
            helper_dir.mkdir(parents=True)
            helper = helper_dir / "check_plan_preflight.py"
            helper.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps({'decision': 'warn', 'target_path': 'scripts/new_file.py'}))\n",
                encoding="utf-8",
            )
            helper.chmod(0o755)

            result = _run_hook(_payload("cat > scripts/new_file.py <<'PY'\nprint('x')\nPY"), cwd=root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema-guard: FAIL: unknown check_plan_preflight.py decision 'warn'", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
