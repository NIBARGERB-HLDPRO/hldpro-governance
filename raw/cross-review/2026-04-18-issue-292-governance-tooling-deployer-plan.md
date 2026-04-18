---
schema_version: v2
pr_number: pre-pr
pr_scope: governance-tooling-deployer
drafter:
  role: implementer-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-18
reviewer:
  role: deployer-design-explorer
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

# Review Memo - Issue #292 Governance Tooling Deployer

## Review Subject

- Parent epic: [#288](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/288)
- Contract issue: [#290](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/290)
- Slice issue: [#292](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/292)
- Deployer: `scripts/overlord/deploy_governance_tooling.py`
- Tests: `scripts/overlord/test_deploy_governance_tooling.py`

## Verdict

ACCEPTED_WITH_EXCEPTION

The implementation may proceed because it keeps downstream repos untouched, preserves the compatibility shim deployer, and requires real fixture e2e tests.

## Accepted Decisions

- Add a package-level deployer instead of turning the existing shim deployer into a broad package manager.
- Delegate Local CI shim rendering to `deploy_local_ci_gate.py`.
- Write `.hldpro/governance-tooling.json` as the package consumer record.
- Refuse dirty target repos by default.
- Refuse unmanaged managed-path overwrites by default.
- Prove behavior through temporary git repo fixture tests.
- Keep parent #288 open after #292 closes.

## Same-Family Exception

True alternate-family review was unavailable in this lane. The exception is scoped to the deployer implementation and tests only.

Mitigations:

- subagent design review,
- real fixture e2e tests,
- compatibility shim tests,
- execution-scope preflight,
- structured-plan validation,
- Local CI Gate,
- GitHub Actions before merge.

## Required Boundaries

- Do not edit downstream repos in #292.
- Do not close parent #288 from this slice.
- Do not weaken Local CI Gate or existing managed shim safety behavior.
- Do not treat temporary fixture e2e as the final downstream pilot.

## Residual Risks

- Phase 4 must still run in `local-ai-machine` or a documented replacement repo.
- Phase 5 must still include a deliberate negative-control blocker before closing #288.
