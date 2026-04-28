# Issue #573 PDCAR: Session Waterfall Runbook Enforcement

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/573
Branch: `issue-573-session-waterfall-runbook-20260428`

## Plan

Turn the Society of Minds waterfall and external-services runbook into an
enforced session-start contract for governance and governed repos. The target
failure mode is ad hoc session behavior: agents skip the supervisor role,
search for CLI/auth/bootstrap paths instead of loading the runbook, and start
implementation without an explicit plan -> alternate-family review -> handoff
-> worker -> QA chain.

## Do

Execution completed in the clean issue-573 worktree after the planning packet
was accepted through the governed Claude Opus review path:

- `CODEX.md`
- `CLAUDE.md`
- `STANDARDS.md`
- `docs/EXTERNAL_SERVICES_RUNBOOK.md`
- `hooks/pre-session-context.sh`
- `.claude/hooks/pre-session-context.sh`
- `.claude/settings.json`
- `scripts/overlord/validate_structured_agent_cycle_plan.py`
- `scripts/overlord/test_validate_structured_agent_cycle_plan.py`
- `scripts/overlord/validate_handoff_package.py`
- `scripts/overlord/test_validate_handoff_package.py`
- `scripts/overlord/verify_governance_consumer.py`
- `scripts/overlord/test_verify_governance_consumer.py`
- `docs/governance-tooling-package.json`
- `.github/workflows/governance-check.yml`
- `tools/local-ci-gate/profiles/hldpro-governance.yml`
- governance evidence/docs updated by the final implementation slice,
  including validation and Stage 6 closeout

## Check

Before implementation:

- governed Claude Opus review captured via the external-services runbook path
- structured plan validation
- planning execution-scope validation
- draft handoff package validation

After implementation:

- focused validator and test coverage for session-start, plan, handoff, and
  consumer-package enforcement: pass
- implementation execution-scope assertion with declared parallel-root warnings
  only: pass
- Stage 6 closeout validation and presence gate: pass
- local CI gate for `hldpro-governance`: pass after forward-gating the new
  handoff evidence rule to issue-573-and-later artifacts

## Adjust

If downstream repo adoption surfaces are required, stop and open issue-backed
follow-ups instead of expanding this governance-first slice. If the current
session-start hook shape cannot enforce the contract cleanly, add a governed
wrapper helper rather than duplicating the checklist into multiple hook files.

## Review

Alternate-family review is required before implementation. The review packet
must cover supervisor/orchestrator role boundaries, exact external-services
CLI/auth/bootstrap paths, required artifact sequencing, and validator/consumer
enforcement scope. The review artifact must be stored at
`raw/cross-review/2026-04-28-issue-573-session-waterfall-runbook.md` with the
dual-signature YAML frontmatter required by `require-cross-review.yml` and
`STANDARDS.md`.

Implementation landed under that accepted review with bounded worker subagents
for the session/bootstrap slice and validator/CI slice, followed by
supervisor-run integration validation and final QA review.
