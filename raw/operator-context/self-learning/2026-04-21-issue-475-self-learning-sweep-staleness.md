# Weekly Self-Learning Report Skipped By Pre-Sweep Gate

Date: 2026-04-21T17:31:51Z
Issue: #475
Evidence: GitHub Actions run 24674456168; metrics/self-learning/latest.json; docs/ERROR_PATTERNS.md
Follow-up: #475

## Summary

The self-learning loop was implemented, but its operational proof became stale because the 2026-04-20 scheduled `overlord-sweep` failed before the `Build self-learning knowledge report` step. The blocker was the Codex model-pin scanner flagging an authoritative hldpro-sim provider command and stale local worktree mirrors. The prevention path is to fix the authoritative provider invocation, exclude local worktree mirrors from repo scanners, regenerate `metrics/self-learning/latest.*`, and keep this issue-backed write-back artifact as direct evidence.
