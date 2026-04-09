# Issue 48 PDCA/R — Neo4j Graph Push

Date: 2026-04-09
Issue: [#48](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/48)
Owner: nibargerb

## Plan

- use the new local Neo4j runtime to validate a real governance-hosted graph push
- keep the first proof deterministic by pushing a small governance graph with an explicit scope namespace
- document the initial operator-context mapping contract so future graph enrichment work has a stable target shape

## Do

- added `scripts/knowledge_base/push_graph_to_neo4j.py`
- namespaced pushed node ids as `<scope>:<node_id>` to avoid collisions across multiple repo graphs
- used a governance-hosted `graph.json` as the source of truth instead of rebuilding from a product repo

## Check

Verification target:
- a governance-hosted graph is pushed into local Neo4j through the Python driver
- Neo4j returns the expected node and edge counts for the chosen scope
- the local runtime and push command are both deterministic and documented

## Adjust

Operator-context mapping contract for future enrichment:

| operator_context field | Neo4j target |
|---|---|
| `id` | node `id` (scoped if mixed with graphify repo graphs) |
| `context_type` | `OperatorContext.context_type` property |
| `content` | `OperatorContext.content` property |
| `relevance_tags` | serialized property now; promote to native list property in a later enrichment pass if we need array-native querying |
| `created_at` | `OperatorContext.created_at` property |

Recommended future edge semantics:
- `(:OperatorContext)-[:INFORMS]->(:Entity)` for linked graph nodes
- `(:OperatorContext)-[:DERIVED_FROM]->(:Closeout)` for Stage 6 traceability

## Review

This slice is complete once a real graph push succeeds locally and the remaining work is narrowed to graph-enrichment choices, not basic runtime or transport uncertainty.
