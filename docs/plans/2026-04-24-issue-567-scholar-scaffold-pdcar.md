# PDCAR: hldpro-sim Scholar Specialty-Agent Scaffold

Date: 2026-04-24
Branch: `review/scholar-acceptance-criteria-20260424`
Repo: `hldpro-governance`
Status: APPROVED — implementation ready
GitHub issue: [#567](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/567)

## Problem

The Scholar operator-input runbook defines a new `hldpro-sim` specialty agent
for technical-analysis extraction, intended for downstream consumption by
`Stampede`. The current package has no Scholar capability surface, no packaged
pointer/spec files, and no consumer-proof path for Stampede-oriented invocation.

## Plan

Implement a bounded initial scaffold inside `packages/hldpro-sim/`:

- package a Scholar pointer file plus five perspective specification markdown
  files matching the committed initial library
- add a small Scholar loader/validator module that resolves the pointer,
  validates package-local consistency, and exposes a requestable capability
  surface
- add one bundled Scholar persona so the capability can be pulled through the
  existing `SimulationEngine` / `PersonaLoader` pattern
- add bounded tests proving:
  - pointer/spec resolution
  - request filtering for selected perspectives
  - a Stampede-style consumer proof invocation through current `hldpro-sim`
    seams

This slice is capability scaffolding only. It does not attempt the full
canonical research package, predictive experiments, or broad product-repo
adoption.

## Scope

In scope:

- `packages/hldpro-sim/hldprosim/scholar.py`
- `packages/hldpro-sim/hldprosim/__init__.py`
- `packages/hldpro-sim/personas/scholar-technical-analyst.json`
- `packages/hldpro-sim/scholar/pointer.yaml`
- `packages/hldpro-sim/scholar/*.md` for the five perspectives
- package tests for Scholar loading and consumer proof
- `OVERLORD_BACKLOG.md`
- `docs/plans/issue-567-scholar-scaffold-structured-agent-cycle-plan.json`
- validation artifact under `raw/validation/`

Out of scope:

- full canonical-source page-level citations and literature completion
- full fitness-test corpus and LLM variance policy
- new provider behavior
- product-repo integration outside bounded proof tests
- closeout/merge paperwork

## Do

1. Add issue-backed plan artifact and backlog row
2. Implement packaged Scholar pointer/spec bundle and loader/validator
3. Add bundled Scholar persona
4. Add tests for pointer validation and Stampede-oriented invocation
5. Record validation evidence

## Check

```bash
python3 -m pytest packages/hldpro-sim/tests/test_scholar.py packages/hldpro-sim/tests/test_stampede_consumer_proof.py
python3 -m pytest packages/hldpro-sim/tests/test_engine.py packages/hldpro-sim/tests/test_providers.py packages/hldpro-sim/tests/test_runner.py packages/hldpro-sim/tests/test_artifacts.py
python3 -m py_compile packages/hldpro-sim/hldprosim/scholar.py
git diff --check
```

## Adjust

If YAML packaging via stdlib-only access becomes awkward, add a narrow runtime
dependency for `PyYAML` and keep the pointer schema small and deterministic.
If the full five-perspective consumer proof becomes too large for one slice,
keep the bundled library complete but limit the proof invocation to a selected
subset while preserving the loader contract.

## Review

Same-model implementation slice in governance-owned package space. No standards
charter change. Independent critical review should focus on whether the package
surface is real and whether the proof remains bounded rather than collapsing
into paperwork-only scaffolding.
