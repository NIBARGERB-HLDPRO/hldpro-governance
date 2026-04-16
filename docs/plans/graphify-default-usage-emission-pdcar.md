# Graphify Default Usage Emission PDCA/R

## Plan

### Problem

The graphify telemetry contract exists, but the main A/B harness still depends on manual logger calls. That means a 5-10 scenario comparison can complete without producing the append-only usage events needed to inspect actual query traces later.

### Objective

Make the graphify measurement harness emit usage events by default for each scenario and retrieval strategy, while preserving an explicit opt-out for local debugging.

### Scope

- add a reusable append helper to the usage logger module
- make `measure_graphify_usage.py` write usage events by default
- add coverage proving the measurement harness emits query-trace events automatically

## Do

1. Refactor `scripts/knowledge_base/log_graphify_usage.py` to expose a reusable append helper.
2. Update `scripts/knowledge_base/measure_graphify_usage.py` to emit graphify and baseline usage events per scenario by default.
3. Add a `--no-usage-log` escape hatch and a configurable event directory for tests/local runs.
4. Extend the usage logging contract test to verify default event emission.
5. Update the docs to describe the new default behavior.

## Check

- `python3 scripts/knowledge_base/test_graphify_usage_logging_contract.py`
- `python3 -m py_compile scripts/knowledge_base/log_graphify_usage.py scripts/knowledge_base/measure_graphify_usage.py scripts/knowledge_base/test_graphify_usage_logging_contract.py`

## Adjust

The first default-emission slice should stay bounded to the measurement harness. If a later workflow needs automatic logging, it should use the same append helper instead of inventing a second event writer.

## Review

Expected outcome:

- running one A/B measurement command now produces both the metrics artifacts and the append-only usage events needed to inspect the prompt/query/candidate traces after the run
- governance can collect 5-10 comparable runs without relying on manual telemetry discipline
