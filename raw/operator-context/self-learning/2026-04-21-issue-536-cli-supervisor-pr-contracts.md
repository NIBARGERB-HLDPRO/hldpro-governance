# CLI And PR Contract Drift

Date: 2026-04-21T22:20:00Z
Issue: #536
Epic: #533
Evidence: `docs/FAIL_FAST_LOG.md`, `docs/ERROR_PATTERNS.md`, `raw/validation/2026-04-21-issue-536-cli-supervisor-pr-contracts.md`
Follow-up: #535 for broader session-error KB/runbook integration

## Summary

Supervised CLI sessions and PR completion can fail for non-product reasons when known contracts are not encoded: Claude stream-json needs `--verbose`, Codex native sessions need `model_reasoning_effort`, pending checks are not final failures, and local `main` is unsafe as a merge path in multi-worktree sessions. Issue #536 records those as pattern `cli-pr-contract-drift` and pins the corrections with focused tests.

## Self-Learning Signal

When a future session sees Claude stream-json verbose errors, missing Codex reasoning-effort pins, `gh pr checks` pending misread as failed, or local-main worktree merge conflicts, retrieve pattern `cli-pr-contract-drift` and route the operator to the supervisor/automerge contract tests before retrying the same command.
