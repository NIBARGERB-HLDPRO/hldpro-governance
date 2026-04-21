# Stage 6 Closeout Passive Gate

Date: 2026-04-21T21:50:00Z
Issue: #541
Epic: #533
Evidence: `docs/FAIL_FAST_LOG.md`, `docs/ERROR_PATTERNS.md`, `raw/validation/2026-04-21-issue-541-stage6-closeout-enforcement.md`
Follow-up: #533 for cross-sprint guardrail rollout oversight

## Summary

Stage 6 closeouts were not occurring reliably because the closeout validator only ran after a closeout existed. The correction is a merge-path presence gate: `scripts/overlord/check_stage6_closeout.py` detects issue-backed implementation/governance-surface diffs, requires a matching `raw/closeouts/*issue-NNN*.md`, and then delegates closeout integrity to the existing `validate_closeout.py`.

## Self-Learning Signal

When future sessions see missing closeouts after implementation work, retrieve pattern `stage6-closeout-passive-gate`. The fix is not to rewrite the closeout template; the fix is to keep closeout presence wired into CI/Local CI and keep planning-only exemptions tested.
