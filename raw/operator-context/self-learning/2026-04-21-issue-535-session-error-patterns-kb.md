# Session Error Patterns KB Indexed In Self-Learning

Date: 2026-04-21T22:25:00Z
Issue: #535
Epic: #533
Evidence: `raw/validation/2026-04-21-issue-535-session-error-patterns-kb.md`
Follow-up: Continue remaining epic #533 guardrail slices for SQL/schema drift, CLI supervisor contracts, and consumer verifier acceptance.

## Summary

Exact session errors now have a dedicated lookup table at `docs/runbooks/session-error-patterns.md`. The self-learning loop indexes this source as `session_error_pattern`, and report output lists session-error titles, source paths, and summaries so future sessions can retrieve correction paths before retrying stale commands or workflows.

## Pattern

Session corrections that live only in transcripts are not durable enough for autonomous delivery. They need a compact operator KB, a validator, and self-learning report evidence.

## Validation

- PASS `python3 scripts/orchestrator/test_self_learning.py`
- PASS `python3 scripts/overlord/test_validate_session_error_patterns.py`
- PASS `python3 scripts/overlord/validate_session_error_patterns.py docs/runbooks/session-error-patterns.md`
- PASS `python3 scripts/orchestrator/self_learning.py --root . report --output-json /tmp/session-error-patterns-self-learning.json --output-md /tmp/session-error-patterns-self-learning.md`

