#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


MODULE_PATH = Path(__file__).with_name("validate_handoff_package.py")
SPEC = importlib.util.spec_from_file_location("validate_handoff_package", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
validate_handoff_package = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_handoff_package
SPEC.loader.exec_module(validate_handoff_package)


def _plan(issue_number: int) -> dict[str, Any]:
    return {
        "session_id": f"session-{issue_number}",
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
                "file_paths": ["STANDARDS.md"],
            }
        ],
        "specialist_reviews": [
            {
                "reviewer": "researcher",
                "role": "research",
                "focus": "test",
                "status": "accepted",
                "summary": "test",
                "evidence": ["test"],
            }
        ],
        "alternate_model_review": {
            "required": True,
            "reviewer": "reviewer",
            "model_family": "anthropic",
            "status": "accepted",
            "summary": "test",
            "evidence": ["raw/cross-review/example.md"],
        },
        "execution_handoff": {
            "session_agent": "codex",
            "execution_mode": "implementation_ready",
            "approved_scope_summary": "test",
            "next_execution_step": "test",
            "blocked_on": [],
        },
        "material_deviation_rules": ["test"],
        "approved": True,
        "approved_by": ["operator"],
        "approved_at": "2026-04-21T09:30:00-05:00",
    }


def _scope(issue_number: int) -> dict[str, Any]:
    return {
        "expected_execution_root": ".",
        "expected_branch": f"issue-{issue_number}-test",
        "execution_mode": "implementation_ready",
        "allowed_write_paths": ["docs/schemas/", "scripts/overlord/"],
        "forbidden_roots": [],
        "lane_claim": {
            "issue_number": issue_number,
            "claim_ref": f"https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/{issue_number}",
            "claimed_by": "codex",
            "claimed_at": "2026-04-21T09:30:00-05:00",
        },
        "handoff_evidence": {
            "status": "accepted",
            "planner_model": "claude-opus-4-6",
            "implementer_model": "gpt-5.4",
            "accepted_at": "2026-04-21T09:30:00-05:00",
            "evidence_paths": ["docs/plans/issue-438-structured-agent-cycle-plan.json"],
            "active_exception_ref": None,
            "active_exception_expires_at": None,
        },
    }


def _handoff(issue_number: int) -> dict[str, Any]:
    return {
        "schema_version": "v1",
        "handoff_id": f"issue-{issue_number}-plan-to-implementation",
        "issue_number": issue_number,
        "parent_epic_number": 434,
        "lifecycle_state": "implementation_ready",
        "from_role": "planner",
        "to_role": "worker",
        "structured_plan_ref": f"docs/plans/issue-{issue_number}-structured-agent-cycle-plan.json",
        "execution_scope_ref": f"raw/execution-scopes/2026-04-21-issue-{issue_number}-implementation.json",
        "packet_ref": None,
        "package_manifest_ref": None,
        "acceptance_criteria": [
            {
                "id": "AC1",
                "statement": "test",
                "verification_refs": ["docs/schemas/package-handoff.schema.json"],
            }
        ],
        "validation_commands": ["python3 scripts/overlord/test_validate_handoff_package.py"],
        "review_artifact_refs": ["raw/cross-review/example.md"],
        "gate_artifact_refs": [],
        "artifact_refs": ["docs/schemas/package-handoff.schema.json"],
        "audit_refs": [],
        "closeout_ref": None,
        "blocked_on": [],
        "handoff_decision": "accepted",
        "created_at": "2026-04-21T09:30:00-05:00",
    }


def _write_json(root: Path, relative_path: str, payload: dict[str, Any]) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _write_supporting_files(root: Path, issue_number: int = 438) -> Path:
    _write_json(root, f"docs/plans/issue-{issue_number}-structured-agent-cycle-plan.json", _plan(issue_number))
    _write_json(root, f"raw/execution-scopes/2026-04-21-issue-{issue_number}-implementation.json", _scope(issue_number))
    for relative_path in [
        "docs/schemas/package-handoff.schema.json",
        "raw/cross-review/example.md",
        "scripts/overlord/test_validate_handoff_package.py",
    ]:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("test\n", encoding="utf-8")
    return _write_json(root, f"raw/handoffs/2026-04-21-issue-{issue_number}.json", _handoff(issue_number))


class TestValidateHandoffPackage(unittest.TestCase):
    def _run_main(self, root: Path, *args: str) -> tuple[int, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = validate_handoff_package.main(["--root", str(root), *args])
        return code, stdout.getvalue() + stderr.getvalue()

    def test_valid_package_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write_supporting_files(root)
            code, output = self._run_main(root)
        self.assertEqual(code, 0, output)
        self.assertIn("PASS validated 1 package handoff file", output)

    def test_missing_execution_scope_fails_for_implementation_ready(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            (root / "raw/execution-scopes/2026-04-21-issue-438-implementation.json").unlink()
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("execution_scope_ref", output)
        self.assertIn("does not exist", output)

    def test_structured_plan_issue_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            _write_json(root, "docs/plans/issue-438-structured-agent-cycle-plan.json", _plan(999))
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("structured plan issue mismatch", output)

    def test_execution_scope_lane_claim_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            _write_json(root, "raw/execution-scopes/2026-04-21-issue-438-implementation.json", _scope(999))
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("execution scope lane_claim issue mismatch", output)

    def test_accepted_package_requires_closeout_ref(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438)
            payload["lifecycle_state"] = "accepted"
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("requires `packet_ref`", output)
        self.assertIn("requires `closeout_ref`", output)

    def test_validation_ready_package_requires_packet_ref(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438)
            payload["lifecycle_state"] = "validation_ready"
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("requires `packet_ref`", output)

    def test_missing_structured_plan_ref_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            (root / "docs/plans/issue-438-structured-agent-cycle-plan.json").unlink()
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("structured_plan_ref", output)
        self.assertIn("does not exist", output)

    def test_empty_acceptance_criteria_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438)
            payload["acceptance_criteria"] = []
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("acceptance_criteria", output)
        self.assertIn("non-empty array", output)

    def test_unsafe_handoff_ref_fails_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438)
            payload["structured_plan_ref"] = "../outside.json"
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("structured_plan_ref", output)
        self.assertIn("safe repo-relative path", output)

    def test_invalid_handoff_id_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438)
            payload["handoff_id"] = "Issue 438 Handoff"
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("handoff_id", output)
        self.assertIn("must match", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
