#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
import contextlib
import io
from pathlib import Path

import check_local_ci_gate_workflow_contract as contract


VALID_WORKFLOW = """
name: local-ci-gate
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
env:
  PYTHONDONTWRITEBYTECODE: "1"
jobs:
  local-ci-gate:
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - name: Fetch main for changed-file resolution
        run: git fetch origin main --prune --no-tags
      - name: Normalize PR branch name for Local CI Gate
        if: github.event_name == 'pull_request'
        run: git checkout -B "${{ github.head_ref }}" HEAD
      - name: Validate Local CI Gate workflow contract
        run: python3 scripts/overlord/test_local_ci_gate_workflow_contract.py
      - name: Run Local CI Gate
        run: |
          python3 tools/local-ci-gate/bin/hldpro-local-ci run \\
            --profile hldpro-governance \\
            --json
"""

VALID_INDEPENDENT_WORKFLOW = """
name: graphify-governance-contract
jobs:
  contract:
    steps:
      - name: Validate generated wiki index is committed
        run: |
          python3 scripts/overlord/test_local_ci_gate_workflow_contract.py
"""


class TestLocalCiGateWorkflowContract(unittest.TestCase):
    def test_repository_workflow_contract_passes(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]

        self.assertEqual(contract.check_contract(repo_root), [])

    def test_rejects_dry_run_workflow(self) -> None:
        failures = contract._failures_for_text(
            VALID_WORKFLOW.replace("--json", "--dry-run\n            --json"),
            VALID_INDEPENDENT_WORKFLOW,
        )

        self.assertIn("local-ci-gate workflow must not use --dry-run", failures)

    def test_rejects_shallow_checkout_without_full_history(self) -> None:
        failures = contract._failures_for_text(
            VALID_WORKFLOW.replace("fetch-depth: 0", "fetch-depth: 1"),
            VALID_INDEPENDENT_WORKFLOW,
        )

        self.assertIn("every local-ci-gate checkout step must use fetch-depth: 0", failures)

    def test_rejects_later_shallow_checkout(self) -> None:
        workflow = VALID_WORKFLOW.replace(
            "      - name: Fetch main for changed-file resolution",
            "      - uses: actions/checkout@v6\n        with:\n          fetch-depth: 1\n      - name: Fetch main for changed-file resolution",
        )

        failures = contract._failures_for_text(workflow, VALID_INDEPENDENT_WORKFLOW)

        self.assertIn("every local-ci-gate checkout step must use fetch-depth: 0", failures)

    def test_requires_independent_contract_workflow(self) -> None:
        failures = contract._failures_for_text(VALID_WORKFLOW, "name: graphify-governance-contract\n")

        self.assertIn(
            "an independent CI-visible workflow must run the Local CI Gate workflow contract test",
            failures,
        )

    def test_ignores_dead_text_outside_workflow_steps(self) -> None:
        workflow = """
name: local-ci-gate
# pull_request:
# push:
# branches: [main]
# fetch-depth: 0
# git fetch origin main
# python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance
on:
  workflow_dispatch:
jobs:
  local-ci-gate:
    steps:
      - name: Dead text is not a contract
        run: |
          # git fetch origin main
          # python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance
"""

        failures = contract._failures_for_text(workflow, VALID_INDEPENDENT_WORKFLOW)

        self.assertIn("local-ci-gate workflow must run on pull_request to main", failures)
        self.assertIn("local-ci-gate workflow must run on push to main", failures)
        self.assertIn("local-ci-gate workflow must use actions/checkout", failures)
        self.assertIn("local-ci-gate workflow must fetch origin main for changed-file resolution", failures)
        self.assertIn("local-ci-gate workflow must invoke the Local CI Gate runner", failures)

    def test_rejects_missing_bytecode_suppression(self) -> None:
        failures = contract._failures_for_text(
            VALID_WORKFLOW.replace('env:\n  PYTHONDONTWRITEBYTECODE: "1"\n', ""),
            VALID_INDEPENDENT_WORKFLOW,
        )

        self.assertIn("local-ci-gate workflow must disable Python bytecode writes", failures)

    def test_requires_pr_branch_normalization(self) -> None:
        workflow = VALID_WORKFLOW.replace(
            '      - name: Normalize PR branch name for Local CI Gate\n        if: github.event_name == \'pull_request\'\n        run: git checkout -B "${{ github.head_ref }}" HEAD\n',
            "",
        )

        failures = contract._failures_for_text(workflow, VALID_INDEPENDENT_WORKFLOW)

        self.assertIn("local-ci-gate workflow must normalize branch names only for pull requests", failures)
        self.assertIn("local-ci-gate workflow must normalize the PR branch name before running the gate", failures)

    def test_requires_profile_on_actual_runner_command(self) -> None:
        workflow = VALID_WORKFLOW.replace(
            "--profile hldpro-governance",
            "# --profile hldpro-governance",
        )

        failures = contract._failures_for_text(workflow, VALID_INDEPENDENT_WORKFLOW)

        self.assertIn("local-ci-gate workflow must run the hldpro-governance profile", failures)

    def test_rejects_echoed_runner_command(self) -> None:
        workflow = VALID_WORKFLOW.replace(
            "python3 tools/local-ci-gate/bin/hldpro-local-ci run \\",
            "echo python3 tools/local-ci-gate/bin/hldpro-local-ci run \\",
        )

        failures = contract._failures_for_text(workflow, VALID_INDEPENDENT_WORKFLOW)

        self.assertIn("local-ci-gate workflow must invoke the Local CI Gate runner", failures)

    def test_rejects_echoed_fetch_command(self) -> None:
        workflow = VALID_WORKFLOW.replace(
            "run: git fetch origin main --prune --no-tags",
            "run: echo git fetch origin main --prune --no-tags",
        )

        failures = contract._failures_for_text(workflow, VALID_INDEPENDENT_WORKFLOW)

        self.assertIn("local-ci-gate workflow must fetch origin main for changed-file resolution", failures)

    def test_main_returns_nonzero_for_missing_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)

            with contextlib.redirect_stderr(io.StringIO()):
                code = contract.main(["--root", str(root)])

        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
