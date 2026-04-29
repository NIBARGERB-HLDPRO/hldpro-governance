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


def _dispatch_contract(primary_session_family: str = "openai") -> dict[str, Any]:
    return {
        "primary_session_family": primary_session_family,
        "owned_roles": [
            {
                "role": "alternate_model_review",
                "model_family": "anthropic" if primary_session_family == "openai" else "openai",
            }
        ],
        "wrapper_path": "scripts/codex-review.sh",
        "wrapper_id": "claude" if primary_session_family == "openai" else "codex",
        "packet_transport_mode": "file",
        "output_artifact_refs": ["raw/cross-review/example.md"],
        "fallback_policy": {
            "same_family_only": True,
            "ordered_models": (
                [
                    {"family": "openai", "model_id": "gpt-5.3-codex-spark"},
                    {"family": "openai", "model_id": "gpt-5.4"},
                ]
                if primary_session_family == "openai"
                else [
                    {"family": "anthropic", "model_id": "claude-sonnet-4-6"},
                    {"family": "anthropic", "model_id": "claude-opus-4-6"},
                ]
            ),
        },
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


def _consumer_scope(issue_number: int) -> dict[str, Any]:
    scope = _scope(issue_number)
    scope["allowed_write_paths"] = [
        ".hldpro/governance-tooling.json",
        "scripts/overlord/verify_governance_consumer.py",
    ]
    return scope


def _handoff(issue_number: int, *, created_at: str = "2026-04-28T20:45:00Z") -> dict[str, Any]:
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
        "dispatch_contract": _dispatch_contract(),
        "specialist_agent": None,
        "packet_transport": None,
        "packet_output_ref": None,
        "availability_ref": None,
        "acceptance_criteria": [
            {
                "id": "AC1",
                "statement": "test",
                "verification_refs": ["docs/schemas/package-handoff.schema.json"],
            }
        ],
        "validation_commands": ["python3 scripts/overlord/test_validate_handoff_package.py"],
        "review_artifact_refs": ["raw/cross-review/example.md"],
        "gate_artifact_refs": ["raw/gate/example.md"],
        "artifact_refs": ["docs/schemas/package-handoff.schema.json"],
        "audit_refs": [],
        "closeout_ref": None,
        "blocked_on": [],
        "handoff_decision": "accepted",
        "created_at": created_at,
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
        "raw/gate/example.md",
        "scripts/overlord/test_validate_handoff_package.py",
        "scripts/codex-review.sh",
    ]:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("test\n", encoding="utf-8")
    (root / "AGENT_REGISTRY.md").write_text(
        "| Agent | Repo | Tier | Role | Model | Max Loops | Write Paths |\n"
        "|-------|------|------|------|-------|-----------|-------------|\n"
        "| codex-reviewer | hldpro-governance | 2 | worker | gpt-5.4 | 1 | docs/codex-reviews/ |\n"
        "| sim-runner | hldpro-governance | 2 | worker | claude-sonnet-4-6 | 1 | raw/packets/outbound/ |\n",
        encoding="utf-8",
    )
    agents_dir = root / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / "sim-runner.md").write_text("sim runner\n", encoding="utf-8")
    hldpro_state = root / "docs" / "hldpro-sim-consumer-pull-state.json"
    hldpro_state.parent.mkdir(parents=True, exist_ok=True)
    hldpro_state.write_text(
        json.dumps(
            {
                "package": "hldpro-sim",
                "managed_personas": {"personas": ["asc-medical-director.json"]},
            }
        ),
        encoding="utf-8",
    )
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

    def test_historical_package_without_dispatch_contract_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438, created_at="2026-04-28T20:45:00Z")
            payload.pop("dispatch_contract", None)
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertEqual(code, 0, output)

    def test_current_package_without_dispatch_contract_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438, created_at="2026-04-29T17:15:00Z")
            payload.pop("dispatch_contract", None)
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("require `dispatch_contract`", output)

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

    def test_implementation_ready_requires_non_empty_review_artifact_refs(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438)
            payload["review_artifact_refs"] = []
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("requires non-empty `review_artifact_refs`", output)

    def test_implementation_complete_package_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438)
            payload["lifecycle_state"] = "implementation_complete"
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertEqual(code, 0, output)

    def test_in_progress_requires_non_empty_gate_artifact_refs(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438)
            payload["lifecycle_state"] = "in_progress"
            payload["gate_artifact_refs"] = []
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("requires non-empty `gate_artifact_refs`", output)

    def test_historical_implementation_ready_package_is_grandfathered_without_new_evidence_refs(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438, created_at="2026-04-21T09:30:00-05:00")
            payload["review_artifact_refs"] = []
            payload["gate_artifact_refs"] = []
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertEqual(code, 0, output)

    def test_validation_ready_requires_non_empty_review_and_gate_artifact_refs(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438)
            payload["lifecycle_state"] = "validation_ready"
            payload["packet_ref"] = "raw/packets/issue-438-validation.md"
            payload["review_artifact_refs"] = []
            payload["gate_artifact_refs"] = []
            packet = root / "raw/packets/issue-438-validation.md"
            packet.parent.mkdir(parents=True, exist_ok=True)
            packet.write_text("packet\n", encoding="utf-8")
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("requires non-empty `review_artifact_refs`", output)
        self.assertIn("requires non-empty `gate_artifact_refs`", output)

    def test_accepted_requires_non_empty_review_and_gate_artifact_refs(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438)
            payload["lifecycle_state"] = "accepted"
            payload["packet_ref"] = "raw/packets/issue-438-release.md"
            payload["closeout_ref"] = "raw/closeouts/issue-438.md"
            payload["review_artifact_refs"] = []
            payload["gate_artifact_refs"] = []
            packet = root / "raw/packets/issue-438-release.md"
            packet.parent.mkdir(parents=True, exist_ok=True)
            packet.write_text("packet\n", encoding="utf-8")
            closeout = root / "raw/closeouts/issue-438.md"
            closeout.parent.mkdir(parents=True, exist_ok=True)
            closeout.write_text("closeout\n", encoding="utf-8")
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("requires non-empty `review_artifact_refs`", output)
        self.assertIn("requires non-empty `gate_artifact_refs`", output)

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

    def test_accepted_consumer_managed_handoff_requires_consumer_verifier_command(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            _write_json(root, "raw/execution-scopes/2026-04-21-issue-438-implementation.json", _consumer_scope(438))
            payload = _handoff(438)
            payload["created_at"] = "2026-04-21T22:40:00Z"
            payload["validation_commands"] = ["python3 scripts/overlord/test_validate_handoff_package.py"]
            payload["acceptance_criteria"][0]["verification_refs"] = ["raw/validation/issue-438.md"]
            (root / "raw/validation").mkdir(parents=True, exist_ok=True)
            (root / "raw/validation/issue-438.md").write_text("consumer verifier missing\n", encoding="utf-8")
            _write_json(root, str(package.relative_to(root)), payload)

            code, output = self._run_main(root, str(package))

        self.assertNotEqual(code, 0)
        self.assertIn("requires a `verify_governance_consumer.py` validation command", output)

    def test_accepted_consumer_managed_handoff_requires_verifier_evidence_refs(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            _write_json(root, "raw/execution-scopes/2026-04-21-issue-438-implementation.json", _consumer_scope(438))
            payload = _handoff(438)
            payload["created_at"] = "2026-04-21T22:40:00Z"
            payload["validation_commands"] = [
                "python3 scripts/overlord/verify_governance_consumer.py --target-repo /tmp/consumer"
            ]
            payload["acceptance_criteria"][0]["verification_refs"] = ["docs/schemas/package-handoff.schema.json"]
            _write_json(root, str(package.relative_to(root)), payload)

            code, output = self._run_main(root, str(package))

        self.assertNotEqual(code, 0)
        self.assertIn("requires verifier evidence refs", output)

    def test_accepted_consumer_managed_handoff_passes_with_verifier_command_and_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            _write_json(root, "raw/execution-scopes/2026-04-21-issue-438-implementation.json", _consumer_scope(438))
            validation = root / "raw/validation/issue-438-consumer-verifier.md"
            validation.parent.mkdir(parents=True, exist_ok=True)
            validation.write_text("PASS consumer verifier\n", encoding="utf-8")
            payload = _handoff(438)
            payload["created_at"] = "2026-04-21T22:40:00Z"
            payload["validation_commands"] = [
                "python3 scripts/overlord/verify_governance_consumer.py --target-repo /tmp/consumer"
            ]
            payload["acceptance_criteria"][0]["verification_refs"] = [
                "raw/validation/issue-438-consumer-verifier.md"
            ]
            _write_json(root, str(package.relative_to(root)), payload)

            code, output = self._run_main(root, str(package))

        self.assertEqual(code, 0, output)

    def test_specialist_agent_handoff_requires_packet_contract_fields(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438)
            payload["specialist_agent"] = "codex-reviewer"
            _write_json(root, str(package.relative_to(root)), payload)

            code, output = self._run_main(root, str(package))

        self.assertNotEqual(code, 0)
        self.assertIn("`packet_transport` must be 'file'", output)
        self.assertIn("require `packet_ref` under `raw/packets/`", output)

    def test_sim_runner_handoff_requires_hldpro_sim_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            packet = root / "raw/packets/issue-438-sim-runner.md"
            packet.parent.mkdir(parents=True, exist_ok=True)
            packet.write_text("sim packet\n", encoding="utf-8")
            output_ref = root / "raw/packets/outbound/issue-438-sim-runner-manifest.json"
            output_ref.parent.mkdir(parents=True, exist_ok=True)
            output_ref.write_text("{}", encoding="utf-8")
            payload = _handoff(438)
            payload["specialist_agent"] = "sim-runner"
            payload["packet_transport"] = "file"
            payload["packet_ref"] = "raw/packets/issue-438-sim-runner.md"
            payload["packet_output_ref"] = "raw/packets/outbound/issue-438-sim-runner-manifest.json"
            payload["dispatch_contract"]["output_artifact_refs"] = [
                "raw/cross-review/example.md",
                "raw/packets/outbound/issue-438-sim-runner-manifest.json",
            ]
            payload["availability_ref"] = "AGENT_REGISTRY.md"
            _write_json(root, str(package.relative_to(root)), payload)

            code, output = self._run_main(root, str(package))

        self.assertNotEqual(code, 0)
        self.assertIn("require non-null `package_manifest_ref`", output)

    def test_specialist_agent_handoff_passes_with_registered_agent_packet_contract(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            packet = root / "raw/packets/issue-438-codex-reviewer.md"
            packet.parent.mkdir(parents=True, exist_ok=True)
            packet.write_text("review packet\n", encoding="utf-8")
            review = root / "docs/codex-reviews/issue-438-codex-reviewer.md"
            review.parent.mkdir(parents=True, exist_ok=True)
            review.write_text("review output\n", encoding="utf-8")
            payload = _handoff(438)
            payload["specialist_agent"] = "codex-reviewer"
            payload["packet_transport"] = "file"
            payload["packet_ref"] = "raw/packets/issue-438-codex-reviewer.md"
            payload["packet_output_ref"] = "docs/codex-reviews/issue-438-codex-reviewer.md"
            payload["dispatch_contract"]["output_artifact_refs"] = [
                "raw/cross-review/example.md",
                "docs/codex-reviews/issue-438-codex-reviewer.md",
            ]
            payload["availability_ref"] = "AGENT_REGISTRY.md"
            _write_json(root, str(package.relative_to(root)), payload)

            code, output = self._run_main(root, str(package))

        self.assertEqual(code, 0, output)

    def test_dispatch_contract_rejects_cross_family_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            package = _write_supporting_files(root)
            payload = _handoff(438)
            payload["dispatch_contract"]["fallback_policy"]["ordered_models"] = [
                {"family": "openai", "model_id": "gpt-5.3-codex-spark"},
                {"family": "anthropic", "model_id": "claude-opus-4-6"},
            ]
            _write_json(root, str(package.relative_to(root)), payload)
            code, output = self._run_main(root, str(package))
        self.assertNotEqual(code, 0)
        self.assertIn("must match `openai`", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
