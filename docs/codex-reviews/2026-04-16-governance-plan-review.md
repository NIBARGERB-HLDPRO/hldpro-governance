# Governance Plan Review — 2026-04-16

Date: 2026-04-16
Review scope: Proposed 7-sprint multi-repo governance implementation plan

Status legend: PASS / WARN / BLOCK

## 1) STANDARDS.md §DA insertion point
- PASS: The target insertion point is explicitly “immediately before `## Society of Minds — Model Routing Charter (2026-04-14)`” and current `STANDARDS.md` has that section at line 265. Plan is consistent with requested location.
- PASS: ACs for Sprint 7 require no other section changes and only insertion; no conflicting text in the plan.

## 2) Hook pattern compatibility (`set +e` + stdin)
- PASS: AIS Sprint 2 hook extension explicitly preserves `set +e` and stdin `cat` pattern in the critical block context, and the appended scope-gate block follows that pattern.
- PASS: Local AI Machine existing hook context (first 60 lines reviewed) already uses `set +e` and `cat`-from-stdin.
- WARN: ASC-Evaluator Sprint 6 says create a new hook with set +e + stdin; no existing pattern to diff against, so validation depends on implementation accuracy.

## 3) LAM CLAUDE line-count math / LAM constraints
- PASS: Current `local-ai-machine/CLAUDE.md` is 43 lines. Replacing the SoM section with 3 lines and adding 1 max-lines comment with 2 extra `Do Not` entries keeps total within 45.
- PASS: Sprint 5 explicitly requires CI assertion changed from `≤30` to `<=45`, and keeps a pointer to governance updates.
- WARN: The current SoM block appears ~12 lines long (lines 32–43), so stated “43 - 6 + 2 + 1 = ~40” arithmetic is off; still, resulting file remains within the 45-line constraint.

## 4) Sprint branch isolation / file overlap
- PASS: S1 (hldpro-governance) and S7 (hldpro-governance) touch different files; S7 is explicitly blocked until S1–S6 merge, reducing cross-branch conflict risk.
- PASS: Repositories are partitioned by sprint except for the root backlog/issue dependency path already documented.
- PASS: No two sprints claim the same target file in the same repo except shared `.gitignore` within separate repo branches as expected.

## 5) `preflight-probe.md` model requirement
- PASS: Sprint 2 explicitly calls out `preflight-probe` keep model `haiku` and “do not change”.
- WARN: The “Add to YAML frontmatter” template shows `agent-role: worker` block across all 12 agents before exception note; if copied literally and not adjusted per exception, it could incorrectly downgrade `hldpro-watcher` role semantics.

## 6) Sprint 7 dependency ordering
- PASS: Sprint 7 lists explicit `Blocked by: S1, S2, S3, S4, S5, S6` and issue metadata also says blocked.
- PASS: Cross-review artifact path and post-conditions are specified before merge.

## 7) AC completeness / ambiguity
- WARN: Several AC items are verifiability-heavy but not fully operationalized for execution (e.g., “full section content is defined in v3 patch document”); reviewers will need that attachment to compare against acceptance criteria.
- WARN: Sprint 2 says “All 7 existing checks stay unchanged” yet only the first 4+ logic in the referenced snippet is visible; implementers must ensure count and order remain intact.
- WARN: The `HALT` block text uses a hardcoded “You report. You do not fix” instruction for 12 AIS agents, but this may conflict with existing delegated agent behavior and should be tested in policy review.
- PASS: AGENT_REGISTRY, `.gitignore`, and hook scope-lifecycle instructions are all specified per sprint and generally machine-enforceable.

## Findings summary
- PASS: No hard blockers identified for branch sequencing or §DA placement.
- WARN: Two medium-risk plan ambiguities merit explicit clarification before execution:
  1) avoid ambiguous global replacement of `agent-role: worker` for all AIS agents;
  2) provide explicit normative source for Sprint 7 §DA full content to avoid verification drift.
