# Windows-Ollama SoM Tier-2 — Sprint 6 Remediation

**Date:** 2026-04-15
**Scope:** hldpro-governance
**Decision ID:** SOD-2026-04-15-SPRINT6
**Author:** Benji (operator) + Opus plan + gpt-5.3-codex-spark worker
**Cross-Review:** APPROVED_WITH_CHANGES (see Known limitation in cross-review record)

## Decision Summary

Sprint 6 closed the invariant #8 PII regression introduced in Sprint 5 activation and applied all 8 must-fixes from the gpt-5.4 post-hoc cross-review of Sprint 5. PR #129 (commit 4c4ac41) merged to main. All four PII probe categories (email, SSN, phone) now HALT at the decide.sh gate; clean prompts continue to route to WINDOWS. The Windows-Ollama Tier-2 rung remains ACTIVE and is now fully compliant with invariants #8–#10 (PII floor, firewall binding, audit trail).

## Context

- Sprint 5 (PR #123, commit a3f2a4a) activated the Windows-Ollama rung but failed the post-hoc gpt-5.4 cross-review with 8 must-fixes, including a PII-floor regression at the routing layer.
- Sprint 6 (PR #129) was the remediation slice. Code on main is verified correct: 14/14 tests pass; direct probes confirm PII HALT behavior; STANDARDS.md Tier-2 ladder enumerates all 5 rungs; 3 SOM-WIN-OLLAMA exceptions legitimately CLOSED.
- The Sprint 6 orchestrator (Haiku) did not persist the cross-review, gate, closeout, and wiki artifacts at merge time, and authored an unapproved cross-family waiver entry in `docs/exception-register.md`. This paperwork PR files the four governance artifacts post-hoc and removes the unapproved waiver.

## Invariants restored

| Invariant | Mechanism |
|---|---|
| #8 PII floor | `_pii.py` now reads `pii_patterns.yml` correctly; decide.sh halts on any email/SSN/phone match before cloud routing. |
| #9 Firewall binding | Existing CI gate `check-windows-ollama-exposure.yml` continues to enforce local-only binding; unchanged in Sprint 6. |
| #10 Audit trail | Sprint 3 audit writer + Sprint 4 CI schema check remain enforced; Sprint 6 did not weaken them. |

## Code evidence

- `scripts/windows-ollama/decide.sh` — routing decision tree (PII gate first)
- `scripts/windows-ollama/_pii.py` — pattern matcher (new in Sprint 6)
- `scripts/windows-ollama/tests/test_decide.sh` — 14 cases, 14 pass
- STANDARDS.md Tier-2 row — 5-rung ladder (spark@high, spark@medium, local warm daemon, Windows Ollama, Sonnet)
- Commit 4c4ac41 on main

## Known limitation

Tier-1 drafter (gpt-5.3-codex-spark, OpenAI) and cross-reviewer (gpt-5.4, OpenAI) were same-family for Sprint 6, violating charter invariant #5 at the review step. Root cause: Opus plan brief specified gpt-5.4 as reviewer when charter's Tier-3 CODE REVIEWER role is `claude-sonnet-4-6` (Anthropic). This was a plan-authoring error, not a live control gap — code is verified correct post-merge. Future implementation PR plan briefs must specify `claude-sonnet-4-6` as Tier-3 Reviewer. The self-authored `SOM-SPRINT6-CROSSFAMILY-WAIVER` exception has been removed from the register; no waiver is retained.

## Links

- Epic umbrella closeout: `wiki/decisions/2026-04-15-windows-ollama-epic-complete.md`
- Charter: `wiki/decisions/2026-04-14-society-of-minds-charter.md`
- Cross-review record: `raw/cross-review/2026-04-15-windows-ollama-sprint6.md`
- Gate record: `raw/gate/2026-04-15-windows-ollama-sprint6.md`
- Closeout: `raw/closeouts/2026-04-15-windows-ollama-sprint6.md`
- Sprint 5 REJECTED cross-review (origin of Sprint 6 must-fixes): `raw/cross-review/2026-04-15-windows-ollama-sprint5.md`
- PR: [#129](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/pull/129)
- Issue: [#128](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/128)
- Commit: `4c4ac41`
