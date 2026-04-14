---
pr_number: TBD
pr_scope: standards
drafter:
  role: architect-claude
  model_id: claude-opus-4-6
  model_family: anthropic
  signature_date: 2026-04-14
reviewer:
  role: architect-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-14
  verdict: APPROVED_WITH_CHANGES
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---

# Tier 1 Dual-Planner Cross-Review — Society-of-Minds Charter

## Subject
Plan capture: `raw/inbox/2026-04-14-society-of-minds-routing-plan.md`
Target PR: governance repo STANDARDS §Society of Minds + 5 reusable workflows + scripts + PR template + agent updates.

---

## Architect-Claude (drafter) — `claude-opus-4-6`
Authored via iterative dialogue with the user (Benji). Full three-tier charter + LAM real-model integration + fallback ladder + enforcement wiring. Self-assessment: APPROVED from drafter perspective; invariants satisfied in first draft per own review.

---

## Architect-Codex (reviewer) — `gpt-5.4 high`

### Verdict: APPROVED_WITH_CHANGES

### Strengths
- Establishes a clear multi-tier routing model with explicit planner, worker, reviewer, and gate roles.
- Preserves the core cross-family planner-review principle by requiring Claude/Codex pairing before Tier 2.
- Adds fallback ladders instead of relying on implicit degradation.
- Identifies enforcement mechanisms for most stated routing intents.
- Treats LAM as a bounded lane rather than a general replacement for planner or cross-review roles.

### Concerns (severity-ranked)
- **CRITICAL: Tier 1 Codex identity inconsistent.** Matrix says codex-spark reviews Opus plans; Round 1 says gpt-5.4 high. Resolve before policy.
- **CRITICAL: PII floor not fully enforceable.** No hard block preventing PII-bearing content from reaching cloud reviewers/non-LAM workers.
- **HIGH: No-self-approval not explicitly enforced.** Needs CI check that drafter, reviewer, gate identities distinct.
- **HIGH: Cross-review enforcement is artifact-presence only.** Needs signature/model-family validation, not just file existence.
- **MEDIUM: Several enforcement rows are wrappers/conventions.** `--model` grep, fallback hooks, LAM routing, exception register can be bypassed without CI-verifiable checks.

### Required changes before Tier 2
1. Resolve Tier 1 Codex identity; pick `gpt-5.4 high` OR `gpt-5.3-codex-spark high` consistently.
2. Add hard no-self-approval rule with CI validation of cross-review metadata.
3. Strengthen `require-cross-review.yml` to validate signatures, model IDs, families, scope, bidirectional status.
4. Explicit PII routing guard: PII-bearing inputs must remain LAM-only; cloud reviewers only redacted/manifest-only.
5. Convert LAM routing from "rules active / Phase 7/8 wiring" into named enforcement artifact or exception-register deferral.
6. Define concrete exception-register path, required fields, owner, expiry, CI/sweep validation.

---

## Resolution — Architect-Claude response to required changes

1. **Tier 1 Codex identity resolved:** `gpt-5.4 high` is Architect-Codex (Tier 1). codex-spark is Worker (Tier 2). Plan-capture amended; all tables consistent.
2. **No-self-approval CI-enforced:** `check-no-self-approval.yml` added; parses cross-review frontmatter, fails if drafter/reviewer/gate identities overlap.
3. **Cross-review validator hardened:** `require-cross-review.yml` now validates YAML frontmatter schema (see plan §Cross-review artifact schema); rejects on missing signatures, same-family pair, same-model pair, missing invariant checks, REJECTED verdict.
4. **PII hard block added:** `check-pii-routing.yml` scans diffs for PII patterns from `scripts/lam/pii-patterns.yml`; fails on any PII match outside LAM-only paths; fails if LAM-eligible work has no `raw/lam-audit/*.manifest.json`.
5. **LAM routing promoted to live enforcement:** `check-lam-availability.yml`, `require-lam-dual-signature.sh`, `check-lam-family-diversity.yml` all live in this PR; no Phase 7/8 deferral for the rules (Phase 7/8 still extend *capabilities*, not enforcement).
6. **Exception register concretized:** `hldpro-governance/docs/exception-register.md` schema specified (rule_id, repo, reason, approver, expiry ≤90d, cadence); overlord-sweep auto-opens issue on past-expiry.

All CRITICAL and HIGH concerns addressed in plan revision dated 2026-04-14. MEDIUM concerns (wrappers bypassable) addressed by CI-verifiable promotion of all enforcement rows in the updated table (plan §Updated enforcement table).

---

## Re-verification pending
Architect-Codex to re-read revised plan and issue final verdict. Expected: `APPROVED`. If new concerns emerge, another round.

## Signatures
- Architect-Claude: claude-opus-4-6 · 2026-04-14 · drafted
- Architect-Codex: gpt-5.4 high · 2026-04-14 · APPROVED_WITH_CHANGES (round 1); re-signature pending revised plan
