#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "overlord" / "check_plan_preflight.py"


def _run(root: Path, *args: str) -> tuple[int, dict]:
    result = subprocess.run(
        ["python3", str(SCRIPT), "--repo-root", str(root), "--json", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode, json.loads(result.stdout)


class TestPlanPreflight(unittest.TestCase):
    def test_code_file_without_recent_plan_blocks_with_route_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            code, payload = _run(root, "--target-path", "scripts/ingest.ts")

        self.assertNotEqual(code, 0)
        self.assertEqual(payload["decision"], "block")
        self.assertIn("PLAN_GATE_BLOCKED: missing_recent_plan", payload["reason"])
        self.assertIn("NEXT_ACTION: create_plan", payload["reason"])
        self.assertIn("TARGET_FILE: scripts/ingest.ts", payload["reason"])
        self.assertIn("BYPASS_ALLOWED: trivial_single_line_only", payload["reason"])

    def test_read_only_intent_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            code, payload = _run(Path(raw), "--target-path", "scripts/ingest.ts", "--intent", "read")

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["decision"], "allow")
        self.assertEqual(payload["reason"], "read_only_intent")

    def test_trivial_single_line_bypass_is_explicitly_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            code, payload = _run(
                Path(raw),
                "--target-path",
                "scripts/ingest.ts",
                "--plan-gate-bypass",
                "--trivial-single-line",
            )

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["reason"], "trivial_single_line_bypass")
        self.assertEqual(payload["bypass_allowed"], "trivial_single_line_only")

    def test_general_bypass_without_trivial_marker_still_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            code, payload = _run(Path(raw), "--target-path", "scripts/ingest.ts", "--plan-gate-bypass")

        self.assertNotEqual(code, 0)
        self.assertIn("PLAN_GATE_BLOCKED: missing_recent_plan", payload["reason"])

    def test_recent_plan_allows_governed_write(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            plans = root / ".claude" / "plans"
            plans.mkdir(parents=True)
            (plans / "issue-449.md").write_text("plan\n", encoding="utf-8")

            code, payload = _run(root, "--target-path", "scripts/ingest.ts")

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["reason"], "recent_plan_found")
        self.assertEqual(payload["plan_ref"], ".claude/plans/issue-449.md")

    def test_stale_plan_does_not_clear_preflight(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            plans = root / ".claude" / "plans"
            plans.mkdir(parents=True)
            plan = plans / "issue-449.md"
            plan.write_text("plan\n", encoding="utf-8")
            stale = time.time() - 4 * 3600
            os.utime(plan, (stale, stale))

            code, payload = _run(root, "--target-path", "scripts/ingest.ts", "--freshness-hours", "3")

        self.assertNotEqual(code, 0)
        self.assertIn("PLAN_GATE_BLOCKED: missing_recent_plan", payload["reason"])

    def test_bash_write_command_detects_target(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            code, payload = _run(
                Path(raw),
                "--command",
                "cat > scripts/ingest.ts <<'TS'\nconsole.log('x')\nTS",
            )

        self.assertNotEqual(code, 0)
        self.assertEqual(payload["target_path"], "scripts/ingest.ts")
        self.assertIn("NEXT_ACTION: create_plan", payload["reason"])

    def test_quoted_awk_comparison_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            code, payload = _run(
                Path(raw),
                "--command",
                "awk '$1 > 1 { print $0 }' input.txt",
            )

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["decision"], "allow")
        self.assertEqual(payload["reason"], "no_write_target_detected")
        self.assertEqual(payload["target_path"], "")

    def test_quoted_jq_comparison_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            code, payload = _run(
                Path(raw),
                "--command",
                "jq '.value > 1' input.json",
            )

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["decision"], "allow")
        self.assertEqual(payload["reason"], "no_write_target_detected")
        self.assertEqual(payload["target_path"], "")

    def test_common_read_only_analysis_pipelines_are_allowed(self) -> None:
        commands = [
            "grep -R 'PLAN_GATE_BLOCKED' docs scripts | sort",
            "rg --files | sort | wc -l",
            "git status --short | wc -l",
            "find docs -type f | sort | head -20",
        ]

        for command in commands:
            with self.subTest(command=command), tempfile.TemporaryDirectory() as raw:
                code, payload = _run(Path(raw), "--command", command)

                self.assertEqual(code, 0, payload)
                self.assertEqual(payload["decision"], "allow")
                self.assertEqual(payload["reason"], "no_write_target_detected")
                self.assertEqual(payload["target_path"], "")

    def test_python_write_command_is_refused_with_routing_signal(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            code, payload = _run(
                Path(raw),
                "--command",
                "python3 - <<'PY'\nfrom pathlib import Path\nPath('x.py').write_text('x')\nPY",
            )

        self.assertNotEqual(code, 0)
        self.assertEqual(payload["target_path"], "<python file write>")
        self.assertIn("PLAN_GATE_BLOCKED: missing_recent_plan", payload["reason"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
