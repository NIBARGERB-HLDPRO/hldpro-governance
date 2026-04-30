Issue: `#617` Implement fail-closed startup lane-state surfacing
Execution mode: `implementation_ready`

Review the bounded startup/helper implementation for issue `#617`.

Required review questions:
1. Does the implementation remain narrowly bounded to the local source-repo startup/helper surfacing path and unique claimed-scope discovery only?
2. Does it surface deterministic `PASS startup execution context` and `BLOCKED startup execution context` behavior without absorbing broader pre-hook write-blocking work?
3. Does it explicitly preserve `#607`, `#612`, and `#614` as separate owned lanes?
4. Are the focused proof artifacts sufficient for this slice: local tests, implementation scope/handoff, and startup success/expected-fail transcripts?

Files under review:
- `.claude/settings.json`
- `hooks/pre-session-context.sh`
- `scripts/overlord/check_execution_environment.py`
- `scripts/overlord/test_check_execution_environment.py`
- `scripts/test_session_bootstrap_contract.py`
- `docs/plans/issue-617-prehook-startup-failclosed-pdcar.md`
- `docs/plans/issue-617-prehook-startup-failclosed-structured-agent-cycle-plan.json`
- `raw/execution-scopes/2026-04-30-issue-617-prehook-startup-failclosed-implementation.json`
- `raw/handoffs/2026-04-30-issue-617-plan-to-implementation.json`
- `raw/validation/2026-04-30-issue-617-prehook-startup-failclosed.md`
