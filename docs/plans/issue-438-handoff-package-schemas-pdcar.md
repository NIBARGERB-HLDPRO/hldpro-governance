# PDCAR: Issue #438 Handoff Package Schemas

Issue: [#438](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/438)  
Parent epic: [#434](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/434)  
Date: 2026-04-21

## Plan

Add the schema and first validation layer for structured model/agent handoff
packages. Keep the slice limited to governance SSOT, schema, validator, tests,
and evidence. Defer CI wiring, packet emitter reconciliation, and closeout-hook
hardening to child issues #435, #437, and #436.

## Do

- Add `docs/schemas/package-handoff.schema.json`.
- Add `docs/schemas/execution-scope.schema.json`.
- Extend structured-plan `execution_handoff` with optional handoff package refs.
- Add a concrete package handoff artifact under `raw/handoffs/`.
- Add deterministic package-handoff validator and focused tests.
- Update standards/schema docs and backlog/progress mirrors.

## Check

- Schema JSON parses.
- Handoff package validator accepts valid examples and rejects missing/mismatched refs.
- Structured-plan validator remains backward compatible with historical plans.
- Execution-scope assertion tests still pass.
- Local CI Gate passes.

## Adjust

- Keep `packet_ref` nullable until issue #437 reconciles dispatch-ready packet authoring.
- Keep closeout refs nullable until accepted/released lifecycle states.
- Leave GitHub CI wiring to issue #435 to avoid mixing schema definition with rollout hardening.

## Review

Standards/schema scope requires cross-review evidence in
`raw/cross-review/2026-04-21-issue-438-handoff-package-schemas.md`.
