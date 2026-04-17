# Issue #248 — Graphify Hook Helper PDCA/R

Date: 2026-04-17
Issue: [#248](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/248)
Canonical plan: `docs/plans/issue-248-graphify-hook-helper-structured-agent-cycle-plan.json`
Child microslices: [#249](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/249), [#250](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/250), [#251](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/251)

## Define

AIS #1099 identified a real graphify hook failure mode: raw graphify-installed Git hooks can rebuild with the product checkout as the output context and create `graphify-out/` inside AIS. Governance #248 owns the durable fix: an installable helper that routes governed repo graph refreshes through governance-owned manifest paths.

## Research

- `docs/graphify_targets.json` is the source of truth for governed repo graph outputs.
- `scripts/knowledge_base/build_graph.py` is the governance-owned graph builder and writes output directories when invoked.
- The helper must validate output paths before calling `build_graph.py`; refusal after invocation is too late.
- Product repo adoption is separate: AIS #1101 and knocktracker #160 must prove raw graphify hooks are removed or absent and record dry-run evidence for the new helper.
- A worktree creation attempt on 2026-04-17 triggered the current local post-checkout graphify hook and failed with `ModuleNotFoundError: No module named 'graphify'`; that is evidence of the same hook-family fragility, not a reason to patch untracked hooks ad hoc in MS1.

## Plan

1. Land MS1 planning/control artifacts:
   - mirror #248 in `OVERLORD_BACKLOG.md`;
   - add the structured plan JSON;
   - add this PDCAR companion;
   - keep cross-review architecture-scoped and require a real PR number before commit.
2. Execute MS2 from issue #250:
   - implement the managed helper/installer;
   - resolve governance root and manifest paths deterministically;
   - preflight output paths before `build_graph.py`;
   - refuse unmanaged hook overwrite unless explicit backup or force behavior is selected.
3. Execute MS3 from issue #251:
   - document install/dry-run/refresh commands;
   - record AIS and knocktracker adoption handoff requirements;
   - complete Stage 6 closeout.

## Do

MS1 creates only planning/control artifacts. It does not implement the helper and does not edit product repos.

MS2 implementation handoff is pinned to `gpt-5.3-codex-spark` with `model_reasoning_effort=high`.

## Check

MS1 validation:

- `python3 -m json.tool docs/plans/issue-248-graphify-hook-helper-structured-agent-cycle-plan.json >/dev/null`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .`
- `git diff --check`

MS2 validation:

- `python3 scripts/knowledge_base/test_graphify_hook_helper.py`
- `python3 scripts/knowledge_base/test_graphify_governance_contract.py`
- dry-run command against AIS and knocktracker roots, without writing graph artifacts into those product checkouts.

MS3 validation:

- Stage 6 closeout file exists under `raw/closeouts/`.
- `hooks/closeout-hook.sh raw/closeouts/YYYY-MM-DD-issue-248-graphify-hook-helper.md` exits 0.

## Adjust

- If manifest resolution cannot be deterministic, stop and update #248 before implementation continues.
- If the helper cannot prove unsafe product-repo output paths are refused before `build_graph.py`, request another alternate-family review.
- If AIS or knocktracker adoption needs repo-local changes, update the product-repo issue and do not fold those edits into the governance helper PR.
- If existing unmanaged hooks are present, the helper must fail closed unless explicit backup/force behavior is selected.

## Review

Claude alternate review returned `APPROVED_WITH_CHANGES` on 2026-04-17. The accepted changes are:

- #248 must be mirrored in `OVERLORD_BACKLOG.md` before MS2 implementation.
- Cross-review is architecture scope and must use a real integer PR number if committed.
- Manifest paths resolve relative to governance root.
- Output-path safety preflight must run before `build_graph.py`.
- MS2 handoff is pinned to `gpt-5.3-codex-spark` with `model_reasoning_effort=high`.
- Stage 6 closeout is required.
- AIS and knocktracker adoption must prove raw graphify hooks are removed or absent and record helper dry-run evidence.
