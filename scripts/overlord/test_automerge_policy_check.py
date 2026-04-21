#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import automerge_policy_check as policy


def eligible_payload() -> dict[str, object]:
    return {
        "repo": {"allow_auto_merge": True},
        "is_draft": False,
        "protected_target": True,
        "mergeable_state": "clean",
        "mergeability_probe": {"source": "github", "uses_local_main": False},
        "required_checks_configured": True,
        "review_requirements_configured": True,
        "labels": ["merge-when-green"],
        "explicit_opt_in_required": True,
        "checks": [
            {"name": "local-ci-gate", "required": True, "status": "completed", "conclusion": "success"},
            {"name": "advisory", "required": False, "status": "completed", "conclusion": "failure"},
        ],
        "reviews": {
            "required_approvals": 1,
            "approvals": 1,
            "code_owner_review_required": True,
            "code_owner_approved": True,
            "review_thread_resolution_required": True,
            "review_threads_resolved": True,
        },
        "governance_artifacts": [
            {"name": "PDCAR", "required": True, "present": True},
            {"name": "closeout", "required": False, "present": False},
        ],
    }


class TestAutomergePolicyCheck(unittest.TestCase):
    def test_eligible_payload_passes(self) -> None:
        result = policy.evaluate(eligible_payload())

        self.assertTrue(result["eligible"])
        self.assertEqual(result["state"], "eligible")
        self.assertEqual(result["blockers"], [])
        self.assertEqual(result["pending"], [])
        self.assertIn("gh pr update-branch", "\n".join(result["merge_guidance"]))
        self.assertIn("disable the repository auto-merge setting", result["rollback"])

    def test_blocks_draft_red_unreviewed_conflicted_pr(self) -> None:
        payload = eligible_payload()
        payload["is_draft"] = True
        payload["mergeable_state"] = "dirty"
        payload["checks"] = [
            {"name": "local-ci-gate", "required": True, "status": "completed", "conclusion": "failure"}
        ]
        payload["reviews"] = {
            "required_approvals": 1,
            "approvals": 0,
            "code_owner_review_required": True,
            "code_owner_approved": False,
            "review_thread_resolution_required": True,
            "review_threads_resolved": False,
        }

        result = policy.evaluate(payload)

        self.assertFalse(result["eligible"])
        blockers = "\n".join(result["blockers"])
        self.assertIn("pull request is draft", blockers)
        self.assertIn("pull request is not cleanly mergeable", blockers)
        self.assertIn("required check not successful", blockers)
        self.assertIn("required approvals missing", blockers)
        self.assertIn("code owner review required", blockers)
        self.assertIn("review threads are not resolved", blockers)

    def test_pending_required_check_is_pending_not_final_failure(self) -> None:
        payload = eligible_payload()
        payload["checks"] = [
            {"name": "local-ci-gate", "required": True, "status": "queued", "conclusion": None}
        ]

        result = policy.evaluate(payload)

        self.assertFalse(result["eligible"])
        self.assertEqual(result["state"], "pending")
        self.assertEqual(result["blockers"], [])
        self.assertIn("required check pending: local-ci-gate", result["pending"])

    def test_blocks_local_main_mergeability_probe(self) -> None:
        payload = eligible_payload()
        payload["mergeability_probe"] = {"source": "local", "uses_local_main": True}

        result = policy.evaluate(payload)

        self.assertFalse(result["eligible"])
        self.assertEqual(result["state"], "blocked")
        self.assertIn("mergeability probe must not use local main", "\n".join(result["blockers"]))

    def test_blocks_disabled_repo_missing_opt_in_and_blocking_label(self) -> None:
        payload = eligible_payload()
        payload["repo"] = {"allow_auto_merge": False}
        payload["labels"] = ["hold"]
        payload["governance_artifacts"] = [{"name": "PDCAR", "required": True, "present": False}]

        result = policy.evaluate(payload)

        self.assertFalse(result["eligible"])
        blockers = "\n".join(result["blockers"])
        self.assertIn("repository auto-merge is disabled", blockers)
        self.assertIn("blocking label present: hold", blockers)
        self.assertIn("explicit automerge opt-in label missing", blockers)
        self.assertIn("required governance artifact missing: PDCAR", blockers)

    def test_cli_returns_two_for_blocked_payload_and_writes_json(self) -> None:
        payload = eligible_payload()
        payload["is_draft"] = True
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "payload.json"
            output_path = Path(tmpdir) / "result.json"
            input_path.write_text(json.dumps(payload), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "automerge_policy_check.py",
                    "--input",
                    str(input_path),
                    "--json-output",
                    str(output_path),
                ],
                cwd=Path(__file__).resolve().parent,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 2)
            written = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertFalse(written["eligible"])
            self.assertIn("pull request is draft", written["blockers"])

    def test_cli_allow_pending_returns_zero_for_expected_pending_checks(self) -> None:
        payload = eligible_payload()
        payload["checks"] = [
            {"name": "local-ci-gate", "required": True, "status": "in_progress", "conclusion": None}
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "payload.json"
            input_path.write_text(json.dumps(payload), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "automerge_policy_check.py",
                    "--input",
                    str(input_path),
                    "--allow-pending",
                ],
                cwd=Path(__file__).resolve().parent,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn('"state": "pending"', result.stdout)


if __name__ == "__main__":
    unittest.main()
