# Graphify Artifact Contract

**Date:** 2026-04-17
**Scope:** hldpro-governance
**Decision ID:** SOD-2026-04-17-GRAPHIFY-ARTIFACT-CONTRACT
**Author:** Codex planning and implementation
**Cross-Review:** APPROVED_WITH_CHANGES in `raw/cross-review/2026-04-17-issue-241-242-planning-review.md`

## Decision Summary

Governance-hosted graphify outputs under scoped `graphify-out/<repo>/` directories are canonical tracked artifacts. Runtime caches, root scratch files, generated root `graph.html`, `.graphify_tmp.json`, and OS noise such as `.DS_Store` remain local-only ignored exceptions.

## Context

Issue #241 came from ambiguity around `graphify-out/`: it is both the canonical home for governance graph artifacts and a place where local graphify runs can leave cache or scratch files. The fix was to document the distinction and make it testable instead of changing cache policy.

## Enforcement

- `.gitignore` keeps canonical scoped graphify outputs stageable while continuing to ignore cache and OS noise.
- `scripts/knowledge_base/test_graphify_governance_contract.py` checks both sides of the contract with `git check-ignore`.
- `README.md` and `docs/COMPENDIUM.md` describe which artifacts are canonical and which artifacts are local-only.
- `graphify-governance-contract.yml` runs the contract test in CI.

## Boundary

Planner write-boundary enforcement was explicitly out of scope for #241 and was completed separately in #242.

## Links

- Issue: [#241](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/241)
- Implementation PR: [#243](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/pull/243)
- Closeout: `raw/closeouts/2026-04-17-graphify-artifact-contract.md`
- Related decision: `wiki/decisions/2026-04-17-planner-write-boundary.md`
