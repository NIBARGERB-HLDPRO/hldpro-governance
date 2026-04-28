#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_closeout.py")
SPEC = importlib.util.spec_from_file_location("validate_closeout", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
validate_closeout = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_closeout
SPEC.loader.exec_module(validate_closeout)


def _write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _json(path: Path, payload: str) -> None:
    _write(path, payload)


class TestValidateCloseout(unittest.TestCase):
    def _repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        _json(
            root / "docs/plans/issue-436-structured-agent-cycle-plan.json",
            '{"issue_number": 436}',
        )
        _json(
            root / "raw/execution-scopes/2026-04-21-issue-436-implementation.json",
            '{"execution_mode": "implementation_ready", "lane_claim": {"issue_number": 436}}',
        )
        _write(root / "raw/validation/2026-04-21-issue-436.md", "validation")
        _write(root / "raw/cross-review/2026-04-21-issue-436.md", "review")
        _write(root / "scripts/overlord/validate_closeout.py", "validator")
        _json(
            root / "raw/handoffs/2026-04-21-issue-436-plan-to-implementation.json",
            """{
              "schema_version": "v1",
              "handoff_id": "issue-436-plan-to-implementation",
              "issue_number": 436,
              "parent_epic_number": 434,
              "lifecycle_state": "implementation_ready",
              "from_role": "codex-orchestrator",
              "to_role": "codex-qa",
              "structured_plan_ref": "docs/plans/issue-436-structured-agent-cycle-plan.json",
              "execution_scope_ref": "raw/execution-scopes/2026-04-21-issue-436-implementation.json",
              "packet_ref": null,
              "package_manifest_ref": null,
              "acceptance_criteria": [
                {
                  "id": "AC1",
                  "statement": "Closeout validator exists.",
                  "verification_refs": ["scripts/overlord/validate_closeout.py"]
                }
              ],
              "validation_commands": ["python3 scripts/overlord/test_validate_closeout.py"],
              "review_artifact_refs": ["raw/cross-review/2026-04-21-issue-436.md"],
              "gate_artifact_refs": [],
              "artifact_refs": ["scripts/overlord/validate_closeout.py"],
              "audit_refs": ["raw/validation/2026-04-21-issue-436.md"],
              "closeout_ref": null,
              "blocked_on": [],
              "handoff_decision": "accepted",
              "created_at": "2026-04-21T10:30:00-05:00"
            }""",
        )
        return tmp, root

    def _closeout(self, root: Path, residuals: str = "None.", lifecycle: str = "Handoff lifecycle: accepted") -> Path:
        path = root / "raw/closeouts/2026-04-21-issue-436.md"
        _write(
            path,
            f"""# Stage 6 Closeout
Date: 2026-04-21
Repo: hldpro-governance
Task ID: GitHub issue #436

## Decision Made
Built closeout hardening.

## Issue Links
Issue #436 and epic #434.

## Schema / Artifact Version
package-handoff schema v1.

## Review And Gate Identity
Review: raw/cross-review/2026-04-21-issue-436.md
Gate: tools/local-ci command result PASS.

## Wired Checks Run
Closeout validator.

## Execution Scope / Write Boundary
Plan: docs/plans/issue-436-structured-agent-cycle-plan.json
Scope: raw/execution-scopes/2026-04-21-issue-436-implementation.json
Handoff: raw/handoffs/2026-04-21-issue-436-plan-to-implementation.json
{lifecycle}

## Validation Commands
Validation: raw/validation/2026-04-21-issue-436.md

## Residual Risks / Follow-Up
{residuals}
""",
        )
        return path

    def test_valid_closeout_passes(self) -> None:
        tmp, root = self._repo()
        with tmp:
            failures = validate_closeout.validate_closeout(root, self._closeout(root))
        self.assertEqual(failures, [])

    def test_missing_referenced_artifact_fails(self) -> None:
        tmp, root = self._repo()
        with tmp:
            (root / "raw/validation/2026-04-21-issue-436.md").unlink()
            failures = validate_closeout.validate_closeout(root, self._closeout(root))
        self.assertTrue(any("referenced artifact does not exist" in failure for failure in failures), failures)

    def test_residual_without_issue_ref_fails(self) -> None:
        tmp, root = self._repo()
        with tmp:
            failures = validate_closeout.validate_closeout(root, self._closeout(root, residuals="Do this later."))
        self.assertTrue(any("residual risks/follow-ups must cite" in failure for failure in failures), failures)

    def test_handoff_without_lifecycle_record_fails(self) -> None:
        tmp, root = self._repo()
        with tmp:
            failures = validate_closeout.validate_closeout(root, self._closeout(root, lifecycle="Lifecycle pending."))
        self.assertTrue(any("requires `Handoff lifecycle: accepted`" in failure for failure in failures), failures)

    def test_placeholder_text_in_required_section_fails(self) -> None:
        tmp, root = self._repo()
        with tmp:
            closeout = self._closeout(root)
            text = closeout.read_text(encoding="utf-8")
            closeout.write_text(text.replace("Issue #436 and epic #434.", "[List issues here]"), encoding="utf-8")
            failures = validate_closeout.validate_closeout(root, closeout)
        self.assertTrue(any("still contains placeholder text" in failure for failure in failures), failures)

    def test_gate_evidence_requires_artifact_or_command_result(self) -> None:
        tmp, root = self._repo()
        with tmp:
            closeout = self._closeout(root)
            text = closeout.read_text(encoding="utf-8")
            closeout.write_text(text.replace("Gate: tools/local-ci command result PASS.", "Gate: Local CI Gate PASS."), encoding="utf-8")
            failures = validate_closeout.validate_closeout(root, closeout)
        self.assertTrue(any("missing gate artifact reference" in failure for failure in failures), failures)

    def test_resolve_closeout_execution_mode_reads_scope(self) -> None:
        tmp, root = self._repo()
        with tmp:
            closeout = self._closeout(root)
            mode = validate_closeout.resolve_closeout_execution_mode(root, closeout)
        self.assertEqual(mode, "implementation_ready")

    def test_resolve_closeout_execution_mode_defaults_planning_only(self) -> None:
        tmp, root = self._repo()
        with tmp:
            (root / "raw/execution-scopes/2026-04-21-issue-436-implementation.json").write_text(
                '{"lane_claim": {"issue_number": 436}}',
                encoding="utf-8",
            )
            closeout = self._closeout(root)
            mode = validate_closeout.resolve_closeout_execution_mode(root, closeout)
        self.assertEqual(mode, "planning_only")

    def test_hook_invokes_validator_before_graph_refresh(self) -> None:
        hook = Path("hooks/closeout-hook.sh").read_text(encoding="utf-8")
        self.assertIn("scripts/overlord/validate_closeout.py", hook)
        self.assertLess(hook.index("$CLOSEOUT_VALIDATOR"), hook.index("[2/4] Updating knowledge graph"))
        self.assertIn('if [ "$CLOSEOUT_MODE" = "planning_only" ]; then', hook)


if __name__ == "__main__":
    unittest.main(verbosity=2)
