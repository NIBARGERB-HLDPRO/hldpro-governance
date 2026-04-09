# Phase 5 — ASC-Evaluator Graphify PDCA/R

Date: 2026-04-09
Repo Pair: `hldpro-governance` + `ASC-Evaluator`
Operator: Benji / Codex

## Plan

Add ASC-Evaluator to the governance-hosted graphify system using the same product-repo pointer/hook pattern already adopted in HealthcarePlatform.

Success criteria:
- ASC-Evaluator keeps its evaluator persona intact
- Governance stores the canonical ASC graph outputs and wiki articles
- ASC-Evaluator only stores the local pointer and graphify reminder hook
- Governance index links ASC-Evaluator as a first-class graph target

## Do

- Append a minimal graphify section to `ASC-Evaluator/CLAUDE.md`
- Add `ASC-Evaluator/.claude/settings.json` with the governance graph reminder hook
- Build ASC-Evaluator graph outputs into `hldpro-governance/graphify-out/asc-evaluator/`
- Generate governance wiki articles into `hldpro-governance/wiki/asc-evaluator/`
- Update governance index/navigation to include ASC-Evaluator

## Check

- `python3 -m json.tool ASC-Evaluator/.claude/settings.json`
- `git diff --check` in both repos
- Confirm governance outputs exist:
  - `graphify-out/asc-evaluator/GRAPH_REPORT.md`
  - `graphify-out/asc-evaluator/graph.json`
  - `graphify-out/asc-evaluator/community-labels.json`
  - `wiki/asc-evaluator/index.md`

## Adjust

- Keep the ASC-Evaluator persona intact; do not replace it with generic engineering governance text
- Reuse the HealthcarePlatform graphify pointer/hook pattern where possible
- Let governance remain the only tracked home for graphify artifacts

## Review

Expected review focus:
- ASC repo changes are minimal and persona-safe
- Governance graph/wiki output is generated and indexable
- The pattern remains aligned with the approved governance-hosted graphify methodology
