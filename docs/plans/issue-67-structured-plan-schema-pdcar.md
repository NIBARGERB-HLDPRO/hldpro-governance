# Issue 67 PDCA/R — Structured Agent Cycle Plans Org-Wide

Date: 2026-04-09
Issue: [#67](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/67)
Owner: nibargerb

## Plan

- add a governance-owned canonical schema for structured agent cycle plans
- add a reusable validation path so CI can fail malformed plan artifacts
- update the shared governance contract so JSON plans are canonical and Markdown is optional companion material
- record any repo-adoption follow-up explicitly before closing

## Do

- added `docs/schemas/structured-agent-cycle-plan.schema.json`
- added `scripts/overlord/validate_structured_agent_cycle_plan.py`
- updated reusable governance CI to validate plan artifacts
- updated standards and docs to make structured JSON the canonical plan artifact

## Check

Verification target:
- the schema file is valid JSON
- the validator passes on valid plan artifacts
- governance CI can run the validator before execution starts

## Adjust

Review did surface remaining repo-level rollout work. Follow-up issue [#68](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/68) was opened to cover convergence/adoption across governed repos instead of pretending governance-only standardization finished product-repo migration.

## Review

This slice is complete because governance now owns the schema, validator, and reusable CI contract, and the remaining repo rollout work is explicit in issue [#68](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/68) rather than implicit future intent.
