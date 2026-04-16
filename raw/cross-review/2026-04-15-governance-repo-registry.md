---
pr_number: 0
pr_scope: standards
drafter:
  role: architect-claude
  model_id: claude-sonnet-4-6
  model_family: anthropic
  signature_date: 2026-04-15
reviewer:
  role: architect-codex
  model_id: gpt-5.3-codex-spark
  model_family: openai
  signature_date: 2026-04-15
  verdict: APPROVED_WITH_CHANGES
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---

# Cross-Review: governance repo registry entry + hook path convention

## Change Summary

1. Add `hldpro-governance` to the STANDARDS.md Repo Registry with tier `Governance-owner` and `Baseline` security.
2. Add a clarifying note below the registry table documenting that governance repo hooks live at `hooks/` (committed, repo-wide) while product repos use `.claude/hooks/` (local-only, gitignored). Both satisfy the Required Governance hook contract.
3. Commit `hooks/pre-session-context.sh` — the `UserPromptSubmit` hook for pre-session context injection — to the governance repo's `hooks/` directory.

## Drafter Assessment (claude-sonnet-4-6)

**Scope:** Narrow documentation-only standards change. No executable logic altered. Three-part change:
- Registry row addition: low risk, fills a genuine gap (governance repo was unregistered).
- Hook convention note: clarifies existing practice, does not change behavior.
- Hook script commit: moves an already-functioning local hook into the committed repo; `hooks/` is the established pattern for governance (`closeout-hook.sh` already lives there).

**Invariant checks:**
- No PII, no security-sensitive code.
- No tier-skip risk — this is documentation of existing structure.
- Hook script uses `$HOME` and `$REPO_ROOT` correctly; session-once guard prevents per-prompt noise.

**Risks:** None identified. If the hook convention note creates confusion for product repos that read STANDARDS.md, the note should be tightened — but the distinction is accurate and necessary given the gitignore structure.

**Verdict:** APPROVED (drafter side). Awaiting Codex reviewer.

## Reviewer Notes (gpt-5.3-codex-spark, 2026-04-15)

**Verdict:** APPROVED_WITH_CHANGES

The diff matches the stated change scope — registry row, hook-path convention note, and committed hook script all consistent with change summary. One non-blocking standards/doc issue flagged: the convention note's example implies `UserPromptSubmit` hooks are always local-only, but `pre-session-context.sh` is now committed in `hooks/`. Wording updated in STANDARDS.md to clarify the distinction (session-local *invocation* wired in local `settings.json`; hook *script* committed for repo-wide discoverability). No PII/security regression. Dual-planner, self-approval, and cross-family independence invariants intact.
