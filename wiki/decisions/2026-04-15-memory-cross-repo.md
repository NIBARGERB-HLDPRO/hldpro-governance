# MEMORY.md Cross-Repo Integration Decision

**Date:** 2026-04-15  
**Scope:** 5 governed repositories + hldpro-governance orchestration  
**Decision ID:** MLI-2026-04-15-001

## Decision Summary

Adopt a 3-layer memory loop that treats `operator_context` as the durable write store, keeps FAIL_FAST artifacts PR-reviewable in-repo (`docs/FAIL_FAST_LOG.md` and `docs/ERROR_PATTERNS.md`), and uses `~/.claude/projects/.../memory/MEMORY.md` as the session-prompt read surface, with weekly cross-repo integrity checks and closeout consolidation as the control loop.

## 3-layer architecture

1. `operator_context` (Supabase) — write-optimized durable store
2. `docs/FAIL_FAST_LOG.md` + `docs/ERROR_PATTERNS.md` — PR-reviewable per-repo audit trail
3. `~/.claude/projects/.../memory/MEMORY.md` — session-prompt read surface

## Phases landed

| Issue | What | PR | SHA |
|---|---|---|---|
| #132 | Phase 1 — canonical FAIL_FAST + ERROR_PATTERNS schemas + minimal validator + starter governance log updates | #136 | `4c4ee9b` |
| #133 | Phase 2 — MEMORY.md bootstrap in 4 downstream repos + memory references in governance | #138 | `b502c43` |
| #134 | Phase 3a — consolidate-memory automation + overlord integrity gate + closeout hook wiring | #141 | `4e4881f` |

## Phases deferred

| Issue | What | Issue link |
|---|---|---|
| #137 | Phase 1b caller-repo adoption of FAIL_FAST schema validator and error-pattern references | #137 |
| #143 | Phase 3b per-repo Stop-hook auto-spawn wiring for doc-audit-agent | #143 |

## Operational protocol

1. Claude sessions use repo memory pointers via `~/.claude/projects/.../memory/MEMORY.md`.
2. On failure, sessions append to `docs/FAIL_FAST_LOG.md` and (where available) `docs/ERROR_PATTERNS.md`.
3. `failure-pattern-writeback.yml` writes canonical rows into `operator_context` with dedup semantics.
4. Weekly `overlord-sweep.yml` runs `scripts/overlord/memory_integrity.py` and surfaces any cross-repo MEMORY integrity gaps.
5. Closeout hooks call `scripts/consolidate-memory.sh` so `hldpro-governance` stays authoritative for recent learnings.

## Cross-references

- SoM charter: `wiki/decisions/2026-04-14-society-of-minds-charter.md`
- Epic: [#131](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/131)
- Issue #132 (Phase 1)
- Issue #133 (Phase 2)
- Issue #134 (Phase 3)
- Issue #135 (Phase 4 validation)
- Phase 1 PR: [#136](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/pull/136)
- Phase 2 PR: [#138](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/pull/138)
- Phase 3 PR: [#141](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/pull/141)
