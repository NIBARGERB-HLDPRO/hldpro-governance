# Issue 241 PDCA/R - Graphify-Out Artifact Contract

Date: 2026-04-17
Issue: [#241](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/241)
Scope: `hldpro-governance` planning only
Execution mode: planning-only; implementation must be handed to pinned repo agents after approval
Canonical plan: `docs/plans/issue-241-graphify-out-artifact-contract-structured-agent-cycle-plan.json`
Related follow-up: [#242](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/242) for planner write-boundary enforcement

## Contract

- `graphify-out/` is a governance-hosted canonical graph output root.
- Canonical scoped graph artifacts under `graphify-out/<repo>/` should be committed during graph creation or refresh.
- Local runtime cache and OS files are not completion evidence unless this issue explicitly changes that policy.
- Markdown PDCAR is companion context; the canonical execution plan is `issue-241-graphify-out-artifact-contract-structured-agent-cycle-plan.json`.
- Codex and Claude Opus planning roles must not implement this slice directly; execution is handed to the pinned governance agent path after planning approval.
- Planner write-boundary enforcement is out of scope for #241 and tracked separately in #242.

## Plan

- Clarify why `graphify-out/cache/` appears as ignored noise while `graphify-out/` remains canonical.
- Split the artifact contract into explicit tracked outputs and explicit local-only exceptions.
- Align `.gitignore` wording and rules with the canonical/local-only split.
- Add a guard so manifest-defined canonical graph output paths cannot become fully ignored without a failing contract check.
- Keep the implementation narrow: artifact contract, ignore-rule clarity, and validation only.
- Do not widen #241 into the planner write-boundary issue; reference #242 for that control.

## Do

Planning-only actions completed in this slice:

- Created issue #241 as the governing GitHub issue.
- Created issue #242 for the separate planner write-boundary enforcement gap.
- Captured current root cause from repo research:
  - `.gitignore` ignores any root `cache/` directory and explicitly ignores `graphify-out/cache/`.
  - normal `git status --short graphify-out` is clean.
  - `git status --ignored --short graphify-out` reports ignored local-only paths such as `graphify-out/cache/` and `graphify-out/.DS_Store`.
  - 46 files under `graphify-out/` are already tracked canonical artifacts.
  - weekly sweep and closeout staging use broad directory staging, while the contract test only verifies outputs live under `graphify-out/`.

Implementation handoff should do only the following:

- Update `.gitignore` comments/rules to state whether `graphify-out/cache/` is local-only or canonical.
- Update docs that describe graphify artifact ownership if they still blur canonical output with cache output.
- Extend graphify governance contract tests to verify manifest-defined output paths are not fully ignored and expected canonical artifacts are stageable.
- Leave `.DS_Store` ignored.
- Do not commit cache files unless the issue explicitly changes cache policy.
- Do not implement planner-model write-boundary enforcement in this slice.

## Check

Implementation is not complete until the pinned execution agent verifies:

- `python3 scripts/knowledge_base/test_graphify_governance_contract.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .`
- `git check-ignore -v graphify-out/<repo>/GRAPH_REPORT.md` returns no ignore match for every manifest-defined repo output.
- `git status --short graphify-out` distinguishes canonical tracked changes from ignored cache/OS noise.
- `git show HEAD:docs/plans/issue-241-graphify-out-artifact-contract-pdcar.md`
- `git show HEAD:docs/plans/issue-241-graphify-out-artifact-contract-structured-agent-cycle-plan.json`

## Adjust

- If cache is required for reproducible graph builds, make that an explicit policy change and update `.gitignore`, docs, and contract tests together.
- If cache is only runtime acceleration, keep it ignored and make the local-only exception explicit in docs and tests.
- If broad directory staging keeps creating ambiguity, replace or wrap it with a canonical artifact allowlist generated from the manifest.
- If stale agent docs still point to root `graphify-out/GRAPH_REPORT.md`, route that as issue-backed cleanup unless it is required for this acceptance path.
- If planner/write-boundary enforcement is required before implementation, use #242; do not absorb that work into #241.

## Review

The issue is not that `graphify-out/` is untracked. The issue is that the canonical graph root contains ignored runtime children, and the contract does not explicitly separate canonical artifacts from local-only cache. The implementation should remove that ambiguity without widening into graph quality, retrieval ranking, or unrelated graphify output changes.

Alternate-family review: Claude Opus returned `APPROVED_WITH_CHANGES` on 2026-04-17. The review explicitly recommended keeping #241 and #242 separate, shipping #241 first, and resolving #242's planner-boundary design details before implementation.
