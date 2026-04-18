---
schema_version: v2
pr_number: pre-pr
pr_scope: governance-tooling-distribution-contract
drafter:
  role: implementer-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-18
reviewer:
  role: tooling-surface-explorer
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

# Review Memo - Issue #290 Governance Tooling Distribution Contract

## Review Subject

- Parent epic: [#288](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/288)
- Slice issue: [#290](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/290)
- Runbook: `docs/runbooks/org-governance-tooling-distribution.md`
- Manifest: `docs/governance-tooling-package.json`
- Plan: `docs/plans/issue-290-structured-agent-cycle-plan.json`
- PDCAR: `docs/plans/issue-290-governance-tooling-contract-pdcar.md`

## Verdict

ACCEPTED_WITH_EXCEPTION

The contract slice may proceed because it defines boundaries and does not implement deployment code or edit downstream repos.

## Accepted Decisions

- Pin downstream consumption by governance git SHA.
- Keep semver optional until a later release process exists.
- Separate package core, repo profiles, managed files, repo-local overrides, tracked baselines, and per-run reports.
- Require `.hldpro/governance-tooling.json` as the downstream consumed-version record.
- Require rollback/uninstall semantics before Phase 2 implementation can close.
- Keep `local-ai-machine` as the default Phase 4 pilot under #288.
- Keep final downstream e2e proof as an unresolved parent epic gate.

## Same-Family Exception

True alternate-family review was unavailable in this lane. The exception is scoped to contract documentation and manifest work only.

Mitigations:

- subagent surface review,
- JSON validation,
- structured-plan validation,
- execution-scope preflight,
- backlog alignment,
- Local CI Gate,
- GitHub Actions before merge.

## Required Boundaries

- Do not implement the generalized deployer in #290.
- Do not modify downstream repos in #290.
- Do not close parent #288 from this slice.
- Do not treat local dry-run output as live enforcement proof.

## Residual Risks

- Phase 2 must convert this contract into executable deployer behavior. A doc-only contract is not sufficient for downstream adoption.
- Phase 4 must prove `local-ai-machine` can create a clean adoption worktree before using it as the pilot.
- Phase 5 must include a deliberate negative-control blocker, otherwise the final e2e proof is incomplete.
