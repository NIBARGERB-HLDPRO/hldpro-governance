---
pr_number: TBD
pr_scope: standards
drafter:
  role: architect-claude
  model_id: claude-sonnet-4-6
  model_family: anthropic
  signature_date: 2026-04-16
reviewer:
  role: architect-codex
  model_id: gpt-5.3-codex-spark
  model_family: openai
  signature_date: 2026-04-16
  verdict: APPROVED
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---

# Cross-Review: §DA — Delegation and Agent Authority (STANDARDS.md)

## Scope

Single diff to `STANDARDS.md`: insert `## §DA — Delegation and Agent Authority` immediately before
`## Society of Minds — Model Routing Charter (2026-04-14)` (currently line 270).
No existing sections modified. Insertion only.

## What §DA Adds

1. **Agent Tier Model** — Tier 0 (overlord-sweep), Tier 1 (repo supervisors), Tier 2 (workers/reviewers)
2. **Relationship to §Society of Minds** — §DA sits above SoM's execution worker layer; defines quality gate layer
3. **Delegation Rule table** — 8 task types → owner agents; orchestrator routes, never implements
4. **Scope Freeze Rule** — `current_plan.json` enforcement via governance-check.sh
5. **Max Loop Rule** — Tier 2 workers: 1; Tier 1 supervisors: 3 before HITL
6. **HALT Conditions** — 5 triggers requiring operator surfacing
7. **Upward Reporting Protocol** — JSON schema + CI limitation note
8. **Session Plan Ownership** — orchestrator-only; schema pointer

## Drafter Sign-off (architect-claude / claude-sonnet-4-6)

Review against invariants:

- **No existing sections modified**: CONFIRMED. §DA is a pure insertion. §Society of Minds and all other sections are untouched. Insertion point verified at line 270.
- **No naming collision**: §DA heading is distinct from §Society of Minds. Both coexist — §DA is the delegation layer, §Society of Minds is the execution worker layer.
- **Dependency ordering correct**: §DA references AGENT_REGISTRY.md (created in S1), agent frontmatter fields (standardized in S2–S6), and governance-check.sh scope gate (deployed in S2–S6). All dependencies land before S7.
- **Bootstrap exception preserved**: §DA's Scope Freeze Rule explicitly lists bootstrap paths that bypass plan enforcement. Consistent with hook implementations in S2–S6.
- **No §Society of Minds conflict**: Relationship diagram explicitly frames §DA above SoM (orchestration layer) and SoM as execution layer. No overlap in authority.
- **HALT conditions are mechanical**: All 5 HALT triggers are deterministic (CRITICAL from worker, blocked tool call, scope drift, same error twice, net-new scope). No ambiguous conditions.

**Drafter verdict: APPROVED — ready for codex-spark second-sign.**

Signed: architect-claude (claude-sonnet-4-6) — 2026-04-16

## Reviewer Sign-off (architect-codex / gpt-5.3-codex-spark)

Reviewed §DA insertion against STANDARDS.md.

- Insertion point: line 270, immediately before `## Society of Minds` — CONFIRMED
- Existing sections: no modifications detected — CONFIRMED
- §DA subsections: all 8 present — CONFIRMED
- Dependency chain: S1 (AGENT_REGISTRY), S2–S6 (hooks + agent frontmatter) — CONFIRMED satisfied before S7
- Naming: §DA is distinct from §Society of Minds — no collision — CONFIRMED
- Bootstrap exception preserved in Scope Freeze Rule — CONFIRMED
- HALT conditions are deterministic — CONFIRMED

**Reviewer verdict: APPROVED**

Signed: architect-codex (gpt-5.3-codex-spark) — 2026-04-16

---

## AC Verification (required before merge)

- [ ] §DA section inserted immediately before `## Society of Minds` (line 270)
- [ ] All existing STANDARDS.md sections intact (diff shows insertion only)
- [ ] §DA contains all 8 subsections listed above
- [ ] Both signatures present in this artifact (drafter + reviewer)
- [ ] `OVERLORD_BACKLOG.md` updated to reflect S7 completion
- [ ] Governing GitHub issue #206 updated
