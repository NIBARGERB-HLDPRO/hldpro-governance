#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

import emit


class TestPacketEmitter(unittest.TestCase):
    def test_emit_dispatch_packet_writes_complete_governance_block(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            output = emit.emit_dispatch_packet(
                prior_tier=1,
                prior_role="architect-codex",
                prior_model_id="gpt-5.4",
                prior_model_family="openai",
                next_tier=2,
                artifacts=["docs/plans/issue-437-structured-agent-cycle-plan.json"],
                issue_number=437,
                structured_plan_ref="docs/plans/issue-437-structured-agent-cycle-plan.json",
                execution_scope_ref="raw/execution-scopes/2026-04-21-issue-437-implementation.json",
                validation_commands=["python3 scripts/packet/test_emit.py"],
                review_artifacts=["raw/cross-review/2026-04-21-issue-437.md"],
                fallback_log_ref=None,
                pii_mode="none",
                dispatch_authorized=True,
                dry_run_authorized=True,
                packets_dir=Path(raw),
            )

            payload = yaml.safe_load(Path(output).read_text(encoding="utf-8"))

        self.assertEqual(payload["governance"]["issue_number"], 437)
        self.assertEqual(payload["governance"]["structured_plan_ref"], "docs/plans/issue-437-structured-agent-cycle-plan.json")
        self.assertEqual(payload["governance"]["execution_scope_ref"], "raw/execution-scopes/2026-04-21-issue-437-implementation.json")
        self.assertEqual(payload["governance"]["validation_commands"], ["python3 scripts/packet/test_emit.py"])
        self.assertEqual(payload["governance"]["review_artifacts"], ["raw/cross-review/2026-04-21-issue-437.md"])
        self.assertIsNone(payload["governance"]["fallback_log_ref"])
        self.assertEqual(payload["governance"]["pii_mode"], "none")
        self.assertIs(payload["governance"]["dispatch_authorized"], True)
        self.assertIs(payload["governance"]["dry_run_authorized"], True)

    def test_emit_packet_without_governance_preserves_historical_shape(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            output = emit.emit_packet(
                prior_tier=1,
                prior_role="architect-codex",
                prior_model_id="gpt-5.4",
                prior_model_family="openai",
                next_tier=2,
                artifacts=[],
                packets_dir=Path(raw),
            )
            payload = yaml.safe_load(Path(output).read_text(encoding="utf-8"))

        self.assertNotIn("governance", payload)
        self.assertEqual(payload["prior"]["model_id"], "gpt-5.4")

    def test_cli_rejects_partial_governance_flags(self) -> None:
        stderr = io.StringIO()
        argv = [
            "emit.py",
            "--prior-tier",
            "1",
            "--prior-role",
            "architect-codex",
            "--prior-model-id",
            "gpt-5.4",
            "--prior-model-family",
            "openai",
            "--next-tier",
            "2",
            "--structured-plan-ref",
            "docs/plans/issue-437-structured-agent-cycle-plan.json",
        ]

        with patch("sys.argv", argv), contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as ctx:
                emit.main()

        self.assertNotEqual(ctx.exception.code, 0)
        self.assertIn("--issue-number is required", stderr.getvalue())

    def test_cli_passes_full_governance_block_to_emitter(self) -> None:
        stdout = io.StringIO()
        argv = [
            "emit.py",
            "--prior-tier",
            "1",
            "--prior-role",
            "architect-codex",
            "--prior-model-id",
            "gpt-5.4",
            "--prior-model-family",
            "openai",
            "--next-tier",
            "2",
            "--artifact",
            "docs/plans/issue-437-structured-agent-cycle-plan.json",
            "--issue-number",
            "437",
            "--structured-plan-ref",
            "docs/plans/issue-437-structured-agent-cycle-plan.json",
            "--execution-scope-ref",
            "raw/execution-scopes/2026-04-21-issue-437-packet-dispatch-reconcile-implementation.json",
            "--validation-command",
            "python3.11 scripts/packet/test_emit.py",
            "--review-artifact",
            "raw/cross-review/2026-04-21-issue-437-packet-dispatch-reconcile.md",
            "--fallback-log-ref",
            "raw/model-fallbacks/2026-04-21-issue-437-sonnet-worker-timeout.md",
            "--pii-mode",
            "lam_only",
            "--dispatch-authorized",
            "--dry-run-authorized",
        ]

        with patch("sys.argv", argv), patch.object(emit, "emit_packet", return_value="/tmp/packet.yml") as emit_packet:
            with contextlib.redirect_stdout(stdout):
                emit.main()

        self.assertEqual(stdout.getvalue().strip(), "/tmp/packet.yml")
        governance = emit_packet.call_args.kwargs["governance"]
        self.assertEqual(governance["issue_number"], 437)
        self.assertEqual(governance["structured_plan_ref"], "docs/plans/issue-437-structured-agent-cycle-plan.json")
        self.assertEqual(governance["execution_scope_ref"], "raw/execution-scopes/2026-04-21-issue-437-packet-dispatch-reconcile-implementation.json")
        self.assertEqual(governance["validation_commands"], ["python3.11 scripts/packet/test_emit.py"])
        self.assertEqual(governance["review_artifacts"], ["raw/cross-review/2026-04-21-issue-437-packet-dispatch-reconcile.md"])
        self.assertEqual(governance["fallback_log_ref"], "raw/model-fallbacks/2026-04-21-issue-437-sonnet-worker-timeout.md")
        self.assertEqual(governance["pii_mode"], "lam_only")
        self.assertIs(governance["dispatch_authorized"], True)
        self.assertIs(governance["dry_run_authorized"], True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
