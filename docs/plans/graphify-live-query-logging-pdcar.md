# Graphify Live Query Logging PDCA/R

## Plan

### Problem

Governance can run deterministic graphify-vs-baseline retrieval comparisons, but the current live usage event path does not record the actual prompt, query terms, or ranked candidates used during current work. That makes 5-10 A/B tests measurable only in aggregate, not inspectable at the query level.

### Objective

Add a schema-backed telemetry path that exposes:

- the live prompt
- the live query terms
- the ranked candidates returned for the retrieval strategy
- optional experiment/session identifiers for grouping A/B runs

Keep the change backward compatible with existing usage events and align the offline evaluation outputs so live and deterministic runs can be compared directly.

### Scope

- Extend the graphify usage-event schema with optional query-trace fields.
- Extend the logging CLI to accept and emit those fields.
- Extend the deterministic A/B evaluation output to surface prompt, query terms, and returned candidates in both JSON and Markdown.
- Add a contract test that validates the schema, logger, and evaluation-output shape.

## Do

1. Update `docs/schemas/graphify-usage-event.schema.json`.
2. Update `scripts/knowledge_base/log_graphify_usage.py`.
3. Update `scripts/knowledge_base/measure_graphify_usage.py`.
4. Update `metrics/graphify-usage/README.md`.
5. Add `scripts/knowledge_base/test_graphify_usage_logging_contract.py`.
6. Record the capability in `README.md` and `docs/FEATURE_REGISTRY.md`.

## Check

Required local checks:

- `python3 scripts/knowledge_base/test_graphify_usage_logging_contract.py`
- `python3 -m py_compile scripts/knowledge_base/log_graphify_usage.py scripts/knowledge_base/measure_graphify_usage.py scripts/knowledge_base/test_graphify_usage_logging_contract.py`

## Adjust

Bounded compatibility decision:

- Existing usage events remain valid because the new query-trace fields are optional.
- New offline measurement artifacts become more inspectable without changing the existing summary keys.

If later live usage reveals prompt sensitivity concerns, the next slice should add a redacted-prompt mode rather than removing the query-trace contract.

## Review

Expected outcome:

- Governance can run 5-10 graphify A/B tests and inspect the actual prompt/query terms/candidate files instead of only hit-rate summaries.
- Live usage and deterministic scenarios share the same conceptual trace surface, reducing interpretation drift between experiments and real work.
