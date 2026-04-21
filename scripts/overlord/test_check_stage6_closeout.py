#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import check_stage6_closeout


def _write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _json(path: Path, payload: str) -> None:
    _write(path, payload)


class TestCheckStage6Closeout(unittest.TestCase):
    def _repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        _json(root / "docs/plans/issue-541-structured-agent-cycle-plan.json", '{"issue_number": 541}')
        _json(root / "raw/execution-scopes/2026-04-21-issue-541-implementation.json", '{"lane_claim": {"issue_number": 541}}')
        _write(root / "raw/validation/2026-04-21-issue-541.md", "validation")
        _write(root / "raw/cross-review/2026-04-21-issue-541.md", "review")
        _write(root / "scripts/overlord/check_stage6_closeout.py", "validator")
        _json(
            root / "raw/handoffs/2026-04-21-issue-541.json",
            """{
              "schema_version": "v1",
              "handoff_id": "issue-541",
              "issue_number": 541,
              "parent_epic_number": 533,
              "lifecycle_state": "implementation_ready",
              "from_role": "codex-orchestrator",
              "to_role": "codex-worker",
              "structured_plan_ref": "docs/plans/issue-541-structured-agent-cycle-plan.json",
              "execution_scope_ref": "raw/execution-scopes/2026-04-21-issue-541-implementation.json",
              "packet_ref": null,
              "package_manifest_ref": null,
              "acceptance_criteria": [
                {
                  "id": "AC1",
                  "statement": "Stage 6 closeout is enforced.",
                  "verification_refs": ["scripts/overlord/check_stage6_closeout.py"]
                }
              ],
              "validation_commands": ["python3 scripts/overlord/test_check_stage6_closeout.py"],
              "review_artifact_refs": ["raw/cross-review/2026-04-21-issue-541.md"],
              "gate_artifact_refs": [],
              "artifact_refs": ["scripts/overlord/check_stage6_closeout.py"],
              "audit_refs": ["raw/validation/2026-04-21-issue-541.md"],
              "closeout_ref": null,
              "blocked_on": [],
              "handoff_decision": "accepted",
              "created_at": "2026-04-21T21:35:00Z"
            }""",
        )
        return tmp, root

    def _closeout(self, root: Path, name: str = "raw/closeouts/2026-04-21-issue-541.md") -> str:
        _write(
            root / name,
            """# Stage 6 Closeout
Date: 2026-04-21
Repo: hldpro-governance
Task ID: GitHub issue #541

## Decision Made
Built closeout enforcement.

## Issue Links
Issue #541 and epic #533.

## Schema / Artifact Version
package-handoff schema v1.

## Review And Gate Identity
Review: raw/cross-review/2026-04-21-issue-541.md
Gate: tools/local-ci command result PASS.

## Wired Checks Run
Stage 6 closeout validator.

## Execution Scope / Write Boundary
Plan: docs/plans/issue-541-structured-agent-cycle-plan.json
Scope: raw/execution-scopes/2026-04-21-issue-541-implementation.json
Handoff: raw/handoffs/2026-04-21-issue-541.json
Handoff lifecycle: accepted

## Validation Commands
Validation: raw/validation/2026-04-21-issue-541.md

## Residual Risks / Follow-Up
None.
""",
        )
        return name

    def test_planning_only_changes_do_not_require_closeout(self) -> None:
        tmp, root = self._repo()
        with tmp:
            decision = check_stage6_closeout.evaluate(
                root,
                "issue-541-stage6-closeout-enforcement",
                ["docs/plans/issue-541-stage6-closeout-enforcement-pdcar.md", "raw/execution-scopes/issue-541.json"],
            )

        self.assertFalse(decision.required)
        self.assertEqual(decision.reason, "planning_only_changes")

    def test_implementation_changes_without_closeout_fail(self) -> None:
        tmp, root = self._repo()
        with tmp:
            decision = check_stage6_closeout.evaluate(
                root,
                "issue-541-stage6-closeout-enforcement",
                ["scripts/overlord/check_stage6_closeout.py"],
            )

        self.assertTrue(decision.required)
        self.assertEqual(decision.reason, "missing_stage6_closeout")
        self.assertTrue(any("Stage 6 closeout required" in failure for failure in decision.failures))

    def test_valid_matching_closeout_passes(self) -> None:
        tmp, root = self._repo()
        with tmp:
            closeout = self._closeout(root)
            decision = check_stage6_closeout.evaluate(
                root,
                "issue-541-stage6-closeout-enforcement",
                ["scripts/overlord/check_stage6_closeout.py", closeout],
            )

        self.assertTrue(decision.required)
        self.assertEqual(decision.failures, ())
        self.assertEqual(decision.reason, "stage6_closeout_valid")

    def test_invalid_matching_closeout_fails(self) -> None:
        tmp, root = self._repo()
        with tmp:
            closeout = self._closeout(root)
            (root / "raw/validation/2026-04-21-issue-541.md").unlink()
            decision = check_stage6_closeout.evaluate(
                root,
                "issue-541-stage6-closeout-enforcement",
                ["scripts/overlord/check_stage6_closeout.py", closeout],
            )

        self.assertEqual(decision.reason, "invalid_stage6_closeout")
        self.assertTrue(any("referenced artifact does not exist" in failure for failure in decision.failures))

    def test_multiple_matching_closeouts_fail(self) -> None:
        tmp, root = self._repo()
        with tmp:
            first = self._closeout(root, "raw/closeouts/2026-04-21-issue-541-a.md")
            second = self._closeout(root, "raw/closeouts/2026-04-21-issue-541-b.md")
            decision = check_stage6_closeout.evaluate(
                root,
                "issue-541-stage6-closeout-enforcement",
                ["scripts/overlord/check_stage6_closeout.py", first, second],
            )

        self.assertEqual(decision.reason, "multiple_stage6_closeouts")
        self.assertTrue(decision.failures)

    def test_non_issue_branch_with_governance_changes_fails(self) -> None:
        tmp, root = self._repo()
        with tmp:
            decision = check_stage6_closeout.evaluate(root, "main", ["hooks/closeout-hook.sh"])

        self.assertEqual(decision.reason, "missing_issue_branch")
        self.assertTrue(decision.failures)


if __name__ == "__main__":
    unittest.main(verbosity=2)
