---
schema_version: v2
pr_number: pre-pr
pr_scope: downstream-governance-tooling-pilot-planning
drafter:
  role: planner-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-18
reviewer:
  role: downstream-pilot-planning-explorer
  model_id: gpt-5.4-mini
  model_family: openai
  signature_date: 2026-04-18
  verdict: ACCEPTED_WITH_EXCEPTION
gate_identity:
  role: deterministic-gates
  model_id: scripts/overlord validators
  model_family: deterministic
  signature_date: 2026-04-18
invariants_checked:
  dual_planner_pairing: false
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: false
---

# Review Memo - Issue #294 Downstream Governance Tooling Pilot

## Review Subject

- Parent epic: [#288](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/288)
- Contract issue: [#290](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/290)
- Deployer issue: [#292](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/292)
- Planning issue: [#294](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/294)
- Plan: `docs/plans/issue-294-structured-agent-cycle-plan.json`
- PDCAR: `docs/plans/issue-294-downstream-governance-pilot-pdcar.md`

## Verdict

ACCEPTED_WITH_EXCEPTION

The planning package may proceed because it keeps downstream repos untouched, names `local-ai-machine` as the deterministic default pilot, and makes final downstream e2e evidence a hard AC before parent #288 can close.

## Accepted Decisions

- Use `local-ai-machine` as the default pilot because the package contract names it and a governance-owned profile exists.
- Treat dirty downstream main checkouts as active parallel lanes; do not clean them.
- Require a clean isolated downstream worktree before writes.
- Require a downstream issue and execution scope before consumer repo edits.
- Require `deploy_governance_tooling.py dry-run`, `apply`, and `verify` from a pinned governance ref.
- Require generated consumer record verification.
- Require managed shim invocation evidence.
- Require deliberate negative-control local failure before remediation.
- Require local pass after remediation.
- Require downstream GitHub Actions pass.
- Require rollback or uninstall proof.
- Keep #288 open until all downstream evidence is linked.

## Same-Family Exception

True alternate-family review is unavailable in this lane. The exception is scoped to the #294 planning package only.

Mitigations:

- subagent planning review,
- deterministic plan validation,
- execution-scope preflight,
- backlog/GitHub alignment,
- Local CI Gate,
- GitHub Actions before merge,
- fresh downstream issue and execution scope before consumer edits.

## Required Boundaries

- Do not edit downstream repos in #294.
- Do not close parent #288 from this planning slice.
- Do not treat governance-only tests as downstream e2e proof.
- Do not select an unprofiled downstream repo without a separate profile issue first.
- Do not skip negative-control failure or rollback proof in the downstream implementation slice.

## Residual Risks

- `local-ai-machine` currently has active unrelated work in its main checkout. The implementation slice must create a clean isolated worktree from the remote default branch before writes.
- The downstream repo may need environment prerequisites for its local profile. Missing prerequisites must be documented as blockers or installed within the downstream issue scope.
- A fallback repo must still have a current governance-owned profile; otherwise the pilot becomes profile implementation, not package deployment proof.
