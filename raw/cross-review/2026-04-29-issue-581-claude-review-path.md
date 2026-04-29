---
schema_version: v2
pr_number: pre-pr
pr_scope: standards
drafter:
  role: architect-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-29
reviewer:
  role: architect-claude
  model_id: claude-opus-4-6
  model_family: anthropic
  signature_date: 2026-04-29
  verdict: APPROVED_WITH_CHANGES
gate_identity:
  role: deterministic-local-gate
  model_id: hldpro-local-ci
  model_family: deterministic
  signature_date: 2026-04-29
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---

# Cross-Review — Issue #581 Governed Claude Review Path

## Review Subject

Implementation packet for issue #581: repair the governance-owned Claude
packet-review contract without adding a new operator-facing path. Reviewed
artifacts:

- `docs/plans/issue-581-claude-review-path-pdcar.md`
- `docs/plans/issue-581-claude-review-path-structured-agent-cycle-plan.json`
- `raw/execution-scopes/2026-04-29-issue-581-claude-review-path-implementation.json`
- `raw/handoffs/2026-04-29-issue-581-claude-review-path.json`
- `docs/codex-reviews/2026-04-29-claude.md`

Source files in scope:

- `scripts/codex-review-template.sh`
- `scripts/test_codex_fire.py`
- `STANDARDS.md`
- `docs/EXTERNAL_SERVICES_RUNBOOK.md`

## Verdict

**APPROVED_WITH_CHANGES**

The governed Claude wrapper now returns a usable markdown review artifact for a
bounded packet prompt while preserving `scripts/codex-review.sh claude` as the
only operator-facing path. The review raised two contract clarifications and
both are folded into this slice:

1. document why `bypassPermissions` stays read-only in practice when no tools
   are enabled
2. document the explicit override path for larger packets or different Claude
   reviewer pins

## Findings

### F1 — Self-contained packet contract is the right fix

Changing the template prompt from repo exploration to self-contained packet
scope removes the turn-burning behavior that caused the original `max turns`
and `idle_timeout` failures.

### F2 — No tool access by default is required

The fixed wrapper only passes `--allowed-tools` when
`CLAUDE_REVIEW_ALLOWED_TOOLS` is explicitly set by the execution scope. That
keeps the default review lane deterministic and read-only.

### F3 — `bypassPermissions` is acceptable once no tools are enabled

The live governed replay succeeded in `bypassPermissions` mode and returned a
markdown artifact. The docs must make the rationale explicit so future audits
do not treat the mode name alone as a permission expansion.

### F4 — Larger packets need a documented override path

The default `max_turns=8` is appropriate for bounded packet reviews but should
not silently govern very large multi-file packets. The standards and runbook
must document the explicit override mechanism.

## Resolution Notes

Issue-581 implementation incorporates the required follow-ups:

- `STANDARDS.md` now explains why `bypassPermissions` remains read-only in
  practice for this lane and how execution scopes may override model or turn
  ceilings explicitly.
- `docs/EXTERNAL_SERVICES_RUNBOOK.md` now documents the SSOT override path for
  `CLAUDE_REVIEW_MODEL`, `CLAUDE_REVIEW_MAX_TURNS`, and
  `CLAUDE_REVIEW_ALLOWED_TOOLS`.

## Evidence

- Failure reproduction before the fix: `raw/validation/2026-04-29-issue-581-claude-review-path.md`
- Successful governed wrapper replay after the fix: `docs/codex-reviews/2026-04-29-claude.md`
