# Issue #589 Cross-Review

Date: 2026-04-29
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/589
Branch: `issue-589-research-specialists`
Execution mode: `planning_only`

## Specialist Findings

- Current governance source has planner/auditor/QA specialist lanes, but no
  dedicated governed local-repo or web/external research specialists.
- Current downstream consumer deploy/verify is still a thin bootstrap path and
  needs an explicit package-managed versus repo-specific rollout model before
  new specialist surfaces can be pushed safely.
- Web/external research should be an exception lane with explicit source
  attribution rather than a default discovery path.

## Planning Verdict

`accepted`

The issue-589 planning scope is correctly bounded to governance source and the
downstream rollout model. Direct consumer-repo mutation remains out of scope
for this branch.
