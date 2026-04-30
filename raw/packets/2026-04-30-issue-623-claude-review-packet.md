Issue: `#623` Implement mutation-time pre-tool fail-closed hardening
Execution mode: `implementation_ready`

Review the bounded implementation slice for issue `#623`.

Required review questions:
1. Does the implementation stay bounded to `.claude/settings.json`, `hooks/code-write-gate.sh`, `hooks/schema-guard.sh`, `scripts/overlord/check_plan_preflight.py`, focused tests, required governance doc co-staging, and issue-local artifacts only?
2. Do `Edit`, `MultiEdit`, and named Bash mutation verbs now fail closed on governed surfaces without canonical `docs/plans/*structured-agent-cycle-plan.json` evidence, while compliant or read-only cases still allow?
3. Do helper-missing, malformed-payload, parse-failure, unknown-decision, and validator/preflight failure conditions now hard-block on the owned local mutation path?
4. Does the slice preserve `#617`, `#621`, `#607`, `#612`, and `#614` as explicit external boundaries and avoid broader hook-stack or CI/schema rewrites?
5. Is the validation/proof chain specific enough to support AC1-AC5 without overclaiming broader `#615` closure?

Files under review:
- `.claude/settings.json`
- `hooks/code-write-gate.sh`
- `hooks/schema-guard.sh`
- `scripts/overlord/check_plan_preflight.py`
- `scripts/overlord/test_check_plan_preflight.py`
- `scripts/overlord/test_schema_guard_hook.py`
- `scripts/orchestrator/test_delegation_hook.py`
- `docs/plans/issue-623-mutation-pretool-hardening-pdcar.md`
- `docs/plans/issue-623-mutation-pretool-hardening-structured-agent-cycle-plan.json`
- `raw/execution-scopes/2026-04-30-issue-623-mutation-pretool-hardening-implementation.json`
- `raw/handoffs/2026-04-30-issue-623-plan-to-implementation.json`
- `raw/validation/2026-04-30-issue-623-mutation-pretool-hardening.md`
