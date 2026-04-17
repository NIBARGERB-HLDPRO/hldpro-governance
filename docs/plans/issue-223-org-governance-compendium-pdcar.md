# PDCAR: Org Governance Compendium And Planning-Path Repair

Date: 2026-04-17
Repo: `hldpro-governance`
Branch: `issue-223-compendium-repair-20260417`
Issue: [#223](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/223)
Related epic: [#224](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/224)
Status: IMPLEMENTATION_READY_AFTER_REVIEW
Canonical plan: `docs/plans/issue-223-structured-agent-cycle-plan.json`

## Problem

The org governance compendium work started in the shared main checkout before a
governing issue, canonical structured JSON plan, or alternate-family review
existed. The local draft may be useful, but it cannot be committed or treated as
approved until it is repaired under issue #223.

The same incident exposed a mechanical planning-gate gap: governance-surface
edits can bypass the strongest structured-plan requirement when they happen on
`main` or a non-issue branch.

## Plan

Use #223 as both the compendium governing issue and the corrective-action record.
The repair is sequenced so planning and review land before implementation:

1. Preserve the process finding.
2. Create the canonical structured JSON plan and PDCAR.
3. Add #223 to the governance backlog mirror.
4. Record alternate-family review.
5. Only after review, decide whether to adopt, rework, or discard the existing
   dirty draft.
6. If adopted, implement from this isolated worktree with explicit validation
   and closeout evidence.
7. Route the broader validator bypass fix into #226 unless it is completed as a
   small, reviewed slice in #223.

## Do

Planning scope for this branch:

- Add `docs/plans/2026-04-17-governance-path-repair-findings.md`.
- Add `docs/plans/issue-223-structured-agent-cycle-plan.json`.
- Add this PDCAR companion.
- Add an `OVERLORD_BACKLOG.md` row for issue #223.
- Add cross-review only after alternate-family review completes.

Implementation scope after review approval:

- Review the existing dirty draft from the shared main checkout as source
  material only.
- Adopt or rework the compendium generator.
- Regenerate the compendium in this isolated worktree.
- Wire weekly sweep only if the generator and generated artifact validate.
- Update registry docs only for implemented behavior.

## Check

Planning checks:

- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-223-compendium-repair-20260417 --require-if-issue-branch`
- JSON parse of `docs/plans/issue-223-structured-agent-cycle-plan.json`
- Alternate-family review recorded before implementation is marked ready.
- Worktree remains isolated from `/Users/bennibarger/Developer/HLDPRO/hldpro-governance`.

Implementation checks, if the draft is adopted:

- `python3 -m py_compile scripts/overlord/build_org_governance_compendium.py`
- `python3 scripts/overlord/build_org_governance_compendium.py --check`
- Relevant workflow/sweep validation for local and CI checkout layouts.
- Stage 6 closeout before closing #223.

## Adjust

Stop and update the plan if:

- Alternate-family review rejects the repair sequence.
- The dirty draft cannot be adopted without broad unplanned rewrites.
- Weekly sweep integration needs a unified governed-repo registry from #225
  before it can be made robust.
- The validator bypass fix is larger than a narrow #223 corrective slice and
  should move to #226.
- Any implementation would require writing to the dirty shared main checkout.

## Review

Required before implementation:

- Codex planning draft: this branch. Completed.
- Claude alternate-family review via local Claude CLI. Completed on
  2026-04-17 with `APPROVED_WITH_CHANGES`.
- Cross-review artifact under `raw/cross-review/`. Completed at
  `raw/cross-review/2026-04-17-org-governance-compendium-repair-plan.md`.

Required review changes applied:

- Approval metadata now reflects the completed review instead of pending review
  state.
- The Sprint 2 to Sprint 3 implementation boundary is explicit. The operator's
  2026-04-17 instruction to proceed, loop through, and use no further HITL is
  recorded as approval for #223 implementation in this isolated worktree only.
- Stage 6 closeout evidence is explicit in the implementation sprint ACs.

## Acceptance Criteria

- Issue #223 remains the governing issue for compendium repair.
- Canonical structured plan exists and validates.
- PDCAR companion exists and matches the JSON plan.
- The process deviation is documented.
- The existing dirty draft is not committed until it is explicitly adopted under
  the reviewed plan.
- The validator bypass is either addressed in #223 or routed into #226.
- Implementation, validation, PR, and closeout happen from an isolated worktree.
