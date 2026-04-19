# Issue #212 - §DA Hybrid Delegation Gate PDCA/R

Issue: [#212](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/212)
Branch: `issue-212-da-hybrid-delegation-gate`

## Plan

Implement a governance-owned delegation gate that enforces §DA ownership before orchestrator execution. The gate must use deterministic rules first, support optional MCP/classifier fallback semantics, fail open when the MCP endpoint is unavailable, and preserve read-only routing.

## Do

- Add versioned delegation rules for all eight §DA task types.
- Add deterministic gate logic and hook integration for Agent/Task, Bash, and implementation-scoped Explore.
- Keep `Read` ungated and `Explore` warn-only.
- Log bypasses and warnings to a local governance log.
- Add focused runtime and hook tests.

## Check

Run the delegation gate tests, existing structured-plan and execution-scope gates, hook-adjacent regression tests, Local CI Gate, and GitHub PR checks. The final AC is an executable hook-level proof that the issue #212 failure prompt is intercepted before direct work.

## Act

Merge only after GitHub checks pass. Keep live Qwen/MCP classifier rollout and downstream repo adoption as separately issue-backed work.
