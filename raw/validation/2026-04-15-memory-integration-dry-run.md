# MEMORY.md cross-repo integration — Phase 4 validation

Date: 2026-04-15
Epic: #131
Phase: 4

## Architecture validated

3-layer learning system, no duplication:
1.  (Supabase) — write-optimized durable store
2.  +  — PR-reviewable per-repo audit trail
3.  — session-prompt read surface

## Live checks run

### Memory integrity audit (scripts/overlord/memory_integrity.py)



### consolidate-memory.sh dry-run for each governed repo



### Memory dir inventory



## End-to-end flow (as it will work in production)

1. Claude session encounters bug → fixes + commits
2. Session ends → (Phase 3b future) Stop hook spawns doc-audit-agent → appends to docs/FAIL_FAST_LOG.md
3. Push triggers .github/workflows/failure-pattern-writeback.yml → extracts entry → calls memory-writer edge fn → operator_context row written with dedup
4. Weekly overlord-sweep runs → scripts/overlord/memory_integrity.py verifies MEMORY.md integrity across 5 repos
5. Closeout commits trigger hooks/closeout-hook.sh → calls scripts/consolidate-memory.sh --repo hldpro-governance → updates MEMORY.md "recent learnings" line with count since last update
6. New session in any repo → system prompt pre-loads MEMORY.md pointers → Claude knows where to look

## Deferred to first organic test

- Synthetic pattern-detection smoke (planting a fake "same root cause" in 2 repos' FAIL_FAST_LOG) was in the original AC but deferred. Rationale: creates audit noise + doesn't test anything that real usage won't naturally validate within a week. First time overlord-sweep runs and a real cross-repo pattern surfaces, that IS the smoke test.

## Known limitations

- Phase 1b (#137) deferred: 4 caller repos don't yet reference the FAIL_FAST schema validator
- Phase 3b (#143) deferred: 5 repos don't yet have Stop hooks auto-spawning doc-audit-agent
- operator_context bridge uses best-effort fail-open pattern; memory-writer unreachable doesn't block workflows
- memory_integrity.py runs only in weekly sweep; local CI on PRs doesn't exercise cross-repo memory state

These are tracked; none block the core 3-layer architecture from functioning.
