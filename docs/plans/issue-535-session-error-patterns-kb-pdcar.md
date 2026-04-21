# Issue #535 PDCAR: Session Error Patterns KB

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/535
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/533
Branch: `issue-535-session-error-patterns-kb`

## Plan

Session error corrections were scattered across transcripts, progress notes, fail-fast rows, and closeouts. `docs/EXTERNAL_SERVICES_RUNBOOK.md` should remain focused on service auth/runtime/dependency operations, so this slice creates a dedicated session-error KB and indexes it through the existing self-learning loop.

## Do

Add the runbook and reuse existing guardrails:

- `docs/runbooks/session-error-patterns.md`
- `scripts/orchestrator/self_learning.py`
- `scripts/orchestrator/test_self_learning.py`
- `scripts/overlord/validate_session_error_patterns.py`
- `scripts/overlord/test_validate_session_error_patterns.py`
- `hooks/check-errors.sh`
- `.github/workflows/check-fail-fast-schema.yml`
- governance evidence, progress, feature registry, fail-fast, and error pattern updates for issue #535

## Check

Required validation:

- `python3 scripts/orchestrator/test_self_learning.py`
- `python3 scripts/overlord/test_validate_session_error_patterns.py`
- `python3 scripts/overlord/validate_session_error_patterns.py docs/runbooks/session-error-patterns.md`
- `hooks/check-errors.sh`
- `python3 scripts/orchestrator/self_learning.py --root . report --output-json /tmp/session-error-patterns-self-learning.json --output-md /tmp/session-error-patterns-self-learning.md`
- `python3 scripts/overlord/test_workflow_local_coverage.py`
- `python3 scripts/overlord/validate_handoff_package.py --root . raw/handoffs/2026-04-21-issue-535-session-error-patterns-kb.json`
- `python3 scripts/overlord/validate_closeout.py raw/closeouts/2026-04-21-issue-535-session-error-patterns-kb.md --root .`
- `python3 scripts/overlord/check_stage6_closeout.py --root . --branch-name issue-535-session-error-patterns-kb --changed-files-file /tmp/issue-535-changed-files.txt`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-535-session-error-patterns-kb --changed-files-file /tmp/issue-535-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-535-session-error-patterns-kb-implementation.json --changed-files-file /tmp/issue-535-changed-files.txt --require-lane-claim`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`

## Adjust

If the runbook starts to duplicate service operations, keep the service procedure in the service runbook and keep only the exact session signature and correction path in the session-error KB. If new session categories appear, add entries under the existing schema and update the validator only when the seed set changes.

## Review

Closeout must cite the self-learning report output proving `session_error_pattern` is indexed and the runbook entries are discoverable.

