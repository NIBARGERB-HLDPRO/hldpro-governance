# Hook Command Classification Drift

Date: 2026-04-21T21:20:00Z
Issue: #538
Epic: #533
Evidence: `docs/FAIL_FAST_LOG.md`, `docs/ERROR_PATTERNS.md`, `raw/validation/2026-04-21-issue-538-hook-guardrail-reliability.md`
Follow-up: #535 for the broader session-error patterns KB and runbook surface

## Summary

Session guardrails failed in two directions: read-only analysis commands were blocked because quoted `awk` and `jq` comparisons looked like redirects to raw regexes, while force-push policy remained advisory instead of locally enforced. The fix is to keep command intent classification centralized in `scripts/overlord/check_plan_preflight.py`, route `schema-guard.sh` through that classifier, strip heredoc bodies before branch matching, and block force-push flags and `+` refspecs in `hooks/branch-switch-guard.sh`.

## Self-Learning Signal

When a future session sees `schema-guard: BLOCKED: Bash file write detected` for comparison text or sees force-push output in session logs, lookup should retrieve pattern `hook-command-classification-drift` and route the operator to update the shared classifier plus hook fixture tests instead of adding another local regex layer.
