# Issue #640 — Slice B: Hook Wiring (Policy/Hook/CI Hardening)

**Issue:** #640
**Epic:** #638
**Branch:** issue-640-slice-b-remediation-20260430
**Date:** 2026-04-30
**Worker:** claude-sonnet-4-6 (Stage 2 Worker)

## Summary

Wire all required hooks with \$HOME-anchored paths; add PostToolUse "*" gate; backlog_match.py + fail_fast_state.py shared helpers.

## Scope

| File | Change |
|------|--------|
| `.claude/settings.json` | Replace git rev-parse with \$HOME-anchored paths; add governance-check + backlog-check to PreToolUse Bash |
| `hooks/backlog-check.sh` | Full rewrite: extract issue from branch, call backlog_match.py, fail-open on non-issue branches |
| `hooks/check-errors.sh` | Full rewrite: PostToolUse fail-fast gate calling fail_fast_state.py check + record |
| `hooks/governance-check.sh` | Collapse to 4 steps; steps [3/4] and [4/4] become warn-only |
| `hooks/pre-session-context.sh` | Append backlog-status block before exit 0 |
| `scripts/overlord/backlog_match.py` | New: shared helper searching PROGRESS.md + OVERLORD_BACKLOG.md |
| `scripts/overlord/fail_fast_state.py` | New: shared helper for fail-fast state at ~/.claude/fail-fast-state.json |
