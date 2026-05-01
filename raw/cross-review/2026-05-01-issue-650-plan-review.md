# Cross-Review: Epic #650 Governance Policy Refresh — Structured Plan

**Date:** 2026-05-01
**Plan ref:** docs/plans/issue-650-governance-policy-refresh-structured-agent-cycle-plan.json
**Planner:** claude-opus-4.7 (anthropic family)
**Reviewer:** gpt-5.4 high (openai family, Tier 1 cross-family plan reviewer)
**Verdict:** ACCEPTED (iteration 2 — plan patched after BLOCKED iteration 1)
**Invocation:** `codex exec --ephemeral --skip-git-repo-check --sandbox read-only -m gpt-5.4 -c model_reasoning_effort=high`

---

## Reviewer Verdict (gpt-5.4 @ high, openai family)

**Overall verdict: BLOCKED** — four enforcement and verifiability gaps prevent worker dispatch.

The slice boundaries and artifact path patterns are mostly clean: F, G, and H use non-overlapping file sets, the cross-review artifact paths follow the expected `raw/cross-review/YYYY-MM-DD-*.md` shape, and the plan clearly documents fallup direction and same-family QA prohibition. The blocking problems are enforcement and verifiability: the H->F dependency is not fully enforceable through AC-H8 as written, several ACs require manual or external judgment rather than a pure Bash/pytest check, the functional-acceptance-auditor gate is only explicit on Slice F (not uniformly on G and H), and there is model-family name leakage outside routing-table/approval-only contexts.

**Checklist:**
- [x] (a) Slices atomic and non-overlapping file_paths — PASS
- [ ] (b) Slice H → Slice F dependency enforceable — FAIL
- [ ] (c) All ACs independently machine-verifiable — FAIL
- [ ] (d) Functional-acceptance-auditor gate wired on all slices — FAIL
- [x] (e) Cross-review artifact paths follow dual-signature pattern — PASS
- [ ] (f) No model-family leakage in rule text — FAIL
- [x] (g) Fallup direction correctly documented — PASS
- [x] (h) Same-family QA prohibition documented — PASS

---

## Findings Requiring Plan Patch

**Finding 1 (b): AC-H8 not sufficient for H→F dependency enforcement**
`grep -n 'functional-acceptance-auditor' STANDARDS.md` shows token presence but does not prove Slice F merged to origin/main, nor that the match is inside §PDCAR. Must add: (1) a separate gh CLI command verifying Slice F (#651) merge commit exists on main, and (2) a section-scope grep confirming match is in §PDCAR context.

**Finding 2 (c): ACs not independently machine-verifiable**
- AC-G7 "Issue #614 has a cross-reference comment" must specify: `gh issue view 614 --json comments --jq '[.comments[].body | select(contains("652"))] | length'` returning > 0.
- AC-F8/G8/H9 "dual-signed" has no commandable definition. Must specify: `grep -c "Signature:" <artifact_path>` returning >= 2.
- AC-H1 "correct frontmatter" is ambiguous. Must specify exact grep: `grep -cE "^(model|tier|tools|authority-scope|write-paths):" agents/functional-acceptance-auditor.md` returning >= 5.

**Finding 3 (d): Functional-acceptance-auditor gate not explicit on G and H**
AC-F9 explicitly names the auditor. AC-G9 and AC-H10 only require PASS audit artifacts without stating the artifact must be produced by `functional-acceptance-auditor`. Must add "produced by functional-acceptance-auditor per agents/functional-acceptance-auditor.md protocol" to both ACs.

**Finding 4 (f): Model-family name leakage**
Model names appear in `objective`, AC-F3, and AC-F5 outside routing-table or approval-only fields, violating `material_deviation_rules[7]`. Replace with tier-based references (e.g., "Tier 1 planners" not "claude-opus-4.X and Codex 5.X high" in objective text).

---

## Required Next Action

1. Patch plan to address findings 1–4.
2. Re-submit for gpt-5.4 cross-family re-review using the same invocation path.
3. On ACCEPTED verdict, update `alternate_model_review.status` and dispatch Slice F and G workers.
4. Slice H remains BLOCKED until Slice F merges.

---

## Signatures

**Reviewer Signature (openai family):**
Model: gpt-5.4 | Reasoning: high | Date: 2026-05-01 | Verdict: BLOCKED | tokens: 11,212

**Author Signature (anthropic family):**
Model: claude-opus-4.7 | Role: Tier 1 planner | Date: 2026-05-01 | Artifact: docs/plans/issue-650-governance-policy-refresh-structured-agent-cycle-plan.json
