#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = REPO_ROOT / "scripts" / "overlord" / "validate_structured_agent_cycle_plan.py"


def _plan(
    issue_number: int,
    *,
    approved: bool = True,
    mode: str = "implementation_ready",
    review_status: str = "accepted",
) -> dict:
    return {
        "session_id": f"test-{issue_number}",
        "issue_number": issue_number,
        "objective": "test",
        "tier": 1,
        "scope_boundary": ["test"],
        "out_of_scope": ["test"],
        "research_summary": "test",
        "research_artifacts": ["test"],
        "sprints": [
            {
                "name": "test",
                "goal": "test",
                "tasks": ["test"],
                "acceptance_criteria": ["test"],
                "file_paths": ["CLAUDE.md"],
            }
        ],
        "specialist_reviews": [
            {
                "reviewer": "test",
                "role": "test",
                "focus": "test",
                "status": "accepted",
                "summary": "test",
                "evidence": ["test"],
            }
        ],
        "alternate_model_review": {
            "required": True,
            "reviewer": "test",
            "model_family": "anthropic",
            "status": review_status,
            "summary": "test",
            "evidence": ["test"],
        },
        "execution_handoff": {
            "session_agent": "codex",
            "execution_mode": mode,
            "approved_scope_summary": "test",
            "next_execution_step": "test",
            "blocked_on": [],
        },
        "material_deviation_rules": ["test"],
        "approved": approved,
        "approved_by": ["test"],
        "approved_at": "2026-04-17T10:00:00-05:00",
    }


class TestGovernanceSurfacePlanGate(unittest.TestCase):
    def _run(self, root: Path, branch: str, changed: list[str]) -> subprocess.CompletedProcess[str]:
        changed_file = root / "changed.txt"
        changed_file.write_text("\n".join(changed) + "\n", encoding="utf-8")
        return subprocess.run(
            [
                "python3",
                str(VALIDATOR),
                "--root",
                str(root),
                "--branch-name",
                branch,
                "--changed-files-file",
                str(changed_file),
                "--enforce-governance-surface",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def _run_with_scope_gate(self, root: Path, branch: str, changed: list[str]) -> subprocess.CompletedProcess[str]:
        changed_file = root / "changed.txt"
        changed_file.write_text("\n".join(changed) + "\n", encoding="utf-8")
        return subprocess.run(
            [
                "python3",
                str(VALIDATOR),
                "--root",
                str(root),
                "--branch-name",
                branch,
                "--changed-files-file",
                str(changed_file),
                "--enforce-governance-surface",
                "--enforce-planner-boundary-scope",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def _write_scope(self, root: Path, issue_number: int, mode: str = "implementation") -> None:
        scope_path = root / "raw" / "execution-scopes" / f"2026-04-17-issue-{issue_number}-test-{mode}.json"
        scope_path.parent.mkdir(parents=True)
        scope_path.write_text(
            json.dumps(
                {
                    "expected_execution_root": ".",
                    "expected_branch": f"issue-{issue_number}-test",
                    "execution_mode": "planning_only",
                    "allowed_write_paths": ["docs/plans/"],
                    "forbidden_roots": [],
                }
            ),
            encoding="utf-8",
        )

    def test_non_issue_branch_with_governance_surface_change_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = self._run(Path(raw), "main", ["CLAUDE.md"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("governance-surface changes require a branch name containing `issue-<number>`", result.stdout)

    def test_non_issue_branch_does_not_validate_unmatched_plans_for_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            plan_path = root / "docs" / "plans" / "issue-999-structured-agent-cycle-plan.json"
            plan_path.parent.mkdir(parents=True)
            plan_path.write_text(json.dumps(_plan(999, mode="planning_only")), encoding="utf-8")
            result = self._run(root, "main", ["CLAUDE.md"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("governance-surface changes require a branch name containing `issue-<number>`", result.stdout)
        self.assertNotIn("execution_mode must be", result.stdout)

    def test_github_scripts_are_governance_surface(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = self._run(Path(raw), "main", [".github/scripts/check_agent_model_pins.py"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(".github/scripts/check_agent_model_pins.py", result.stdout)

    def test_github_workflows_with_leading_dot_are_governance_surface(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = self._run(Path(raw), "main", ["./.github/workflows/governance-check.yml"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(".github/workflows/governance-check.yml", result.stdout)

    def test_launchd_and_orchestrator_paths_are_governance_surface(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = self._run(Path(raw), "main", ["launchd/com.hldpro.governance-observer.plist", "scripts/orchestrator/read_only_observer.py"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("launchd/com.hldpro.governance-observer.plist", result.stdout)
        self.assertIn("scripts/orchestrator/read_only_observer.py", result.stdout)

    def test_lam_runtime_paths_are_governance_surface(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = self._run(Path(raw), "main", ["scripts/lam/runtime_inventory.py"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("scripts/lam/runtime_inventory.py", result.stdout)

    def test_packet_paths_are_governance_surface(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = self._run(
                Path(raw),
                "main",
                [
                    "scripts/packet/validate.py",
                    "raw/packets/queue/inbound/example.yml",
                    "raw/model-fallbacks/2026-04-17.md",
                ],
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("scripts/packet/validate.py", result.stdout)
        self.assertIn("raw/packets/queue/inbound/example.yml", result.stdout)
        self.assertIn("raw/model-fallbacks/2026-04-17.md", result.stdout)

    def test_self_learning_paths_are_governance_surface(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = self._run(
                Path(raw),
                "main",
                [
                    "raw/operator-context/self-learning/2026-04-17-issue-230-example.md",
                    "metrics/self-learning/latest.json",
                ],
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("raw/operator-context/self-learning/2026-04-17-issue-230-example.md", result.stdout)
        self.assertIn("metrics/self-learning/latest.json", result.stdout)

    def test_pilot_gate_and_metrics_paths_are_governance_surface(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = self._run(
                Path(raw),
                "main",
                [
                    "raw/gate/2026-04-17-e2e-pilot.md",
                    "metrics/pilot/issue-231-e2e-pilot.json",
                ],
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("raw/gate/2026-04-17-e2e-pilot.md", result.stdout)
        self.assertIn("metrics/pilot/issue-231-e2e-pilot.json", result.stdout)

    def test_riskfix_branch_without_issue_number_gets_specific_issue_hint(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = self._run(Path(raw), "riskfix/scope-gate", ["STANDARDS.md"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("branch name containing `issue-<number>`", result.stdout)

    def test_non_governance_surface_change_without_plan_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = self._run(Path(raw), "feature/readme-copy", ["docs/tutorial.md"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_issue_branch_requires_matching_plan(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = self._run(Path(raw), "issue-226-test", ["scripts/overlord/tool.py"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("require a canonical structured plan for issue #226", result.stdout)

    def test_issue_branch_matching_approved_plan_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            plan_path = root / "docs" / "plans" / "issue-226-structured-agent-cycle-plan.json"
            plan_path.parent.mkdir(parents=True)
            plan_path.write_text(json.dumps(_plan(226)), encoding="utf-8")
            result = self._run(root, "issue-226-test", ["scripts/overlord/tool.py"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_planner_boundary_scope_gate_requires_issue_specific_scope(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            plan_path = root / "docs" / "plans" / "issue-231-structured-agent-cycle-plan.json"
            plan_path.parent.mkdir(parents=True)
            plan_path.write_text(json.dumps(_plan(231)), encoding="utf-8")
            result = self._run_with_scope_gate(
                root,
                "issue-231-e2e-pilot",
                [
                    "raw/packets/2026-04-17-issue-231-e2e-pilot.yml",
                    "scripts/orchestrator/packet_queue.py",
                    "docs/plans/issue-231-structured-agent-cycle-plan.json",
                ],
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("require an issue-specific execution scope for issue #231", result.stdout)

    def test_planner_boundary_scope_gate_accepts_matching_scope(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            plan_path = root / "docs" / "plans" / "issue-231-structured-agent-cycle-plan.json"
            plan_path.parent.mkdir(parents=True)
            plan_path.write_text(json.dumps(_plan(231)), encoding="utf-8")
            self._write_scope(root, 231)
            result = self._run_with_scope_gate(
                root,
                "issue-231-test",
                [
                    "raw/packets/2026-04-17-issue-231-e2e-pilot.yml",
                    "scripts/orchestrator/packet_queue.py",
                    "docs/plans/issue-231-structured-agent-cycle-plan.json",
                ],
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_matching_plan_must_be_implementation_ready(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            plan_path = root / "docs" / "plans" / "issue-226-structured-agent-cycle-plan.json"
            plan_path.parent.mkdir(parents=True)
            plan_path.write_text(json.dumps(_plan(226, mode="planning_only")), encoding="utf-8")
            result = self._run(root, "issue-226-test", ["STANDARDS.md"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("execution_mode must be", result.stdout)

    def test_required_alternate_review_must_be_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            plan_path = root / "docs" / "plans" / "issue-226-structured-agent-cycle-plan.json"
            plan_path.parent.mkdir(parents=True)
            plan_path.write_text(json.dumps(_plan(226, review_status="not_requested")), encoding="utf-8")
            result = self._run(root, "issue-226-test", ["scripts/knowledge_base/build_graph.py"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required alternate_model_review must be accepted", result.stdout)

    def test_malformed_json_reports_structured_fail_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            plan_path = root / "docs" / "plans" / "issue-192-structured-agent-cycle-plan.json"
            plan_path.parent.mkdir(parents=True)
            plan_path.write_text('{"session_id": "truncated"', encoding="utf-8")
            result = subprocess.run(
                ["python3", str(VALIDATOR), "--root", str(root)],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL docs/plans/issue-192-structured-agent-cycle-plan.json: could not parse JSON:", result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_malformed_matching_plan_does_not_crash_governance_surface_gate(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            plan_path = root / "docs" / "plans" / "issue-192-structured-agent-cycle-plan.json"
            plan_path.parent.mkdir(parents=True)
            plan_path.write_text('{"issue_number": 192,', encoding="utf-8")
            result = self._run(root, "issue-192-test", ["scripts/overlord/validate_structured_agent_cycle_plan.py"])
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL docs/plans/issue-192-structured-agent-cycle-plan.json: could not parse JSON:", result.stdout)
        self.assertEqual(result.stdout.count("could not parse JSON"), 1)
        self.assertIn("require a canonical structured plan for issue #192", result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_plan_read_error_reports_structured_fail_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            plan_dir = root / "docs" / "plans" / "issue-192-structured-agent-cycle-plan.json"
            plan_dir.mkdir(parents=True)
            result = subprocess.run(
                ["python3", str(VALIDATOR), "--root", str(root)],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL docs/plans/issue-192-structured-agent-cycle-plan.json: could not parse JSON:", result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
