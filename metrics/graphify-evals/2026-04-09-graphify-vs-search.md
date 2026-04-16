# Graphify Measurement — 2026-04-09

## Summary

- Scenarios: 4
- Graphify hits: 4
- Baseline hits: 3
- Graphify estimated tokens: 816
- Baseline estimated tokens: 4776
- Graphify smaller + more relevant wins: 2
- Second non-graph baseline recommended: False
- Baseline decision: No second non-graph baseline is recommended yet; improve graph-guided ranking against the existing repo-search baseline first.

## Scenario Results

| Scenario | Graphify Relevant | Baseline Relevant | Graphify Score | Baseline Score | Graphify Tokens | Baseline Tokens |
|---|---:|---:|---:|---:|---:|---:|
| ff-74-governance-diff-base | 1 | 1 | 4 | 3 | 227 | 1498 |
| ff-75-raw-feed-redaction | 1 | 1 | 4 | 5 | 257 | 1086 |
| ff-76-cited-code-validation | 1 | 0 | 4 | 2 | 95 | 1101 |
| ff-77-sweep-persistence-visibility | 1 | 1 | 4 | 4 | 237 | 1091 |

## Guidance

- Validated pattern: use symptom terms plus mechanism/owner terms (function, workflow, file family) so graph-guided retrieval can exploit communities and one-hop links instead of only file-name overlap.
- Use graph-guided retrieval first for topology and owning-file discovery, then confirm with repo search on the returned files.
- Baseline decision: No second non-graph baseline is recommended yet; improve graph-guided ranking against the existing repo-search baseline first.

## Query Traces

### ff-74-governance-diff-base

- Prompt: Find why reusable governance checks only inspect the last commit in a multi-commit PR.
- Query terms: governance, workflow_call, diff, base, github.event.before
- Graphify candidates: scripts/knowledge_base/measure_graphify_usage.py, .github/workflows/governance-check.yml, .github/workflows/graphify-governance-contract.yml, .github/workflows/overlord-sweep.yml, .github/workflows/overlord-nightly-cleanup.yml
- Baseline candidates: docs/plans/issue-74-governance-diff-base-pdcar.md, docs/plans/issue-74-structured-agent-cycle-plan.json, metrics/graphify-evals/scenarios/fail-fast-2026-04-09.json, metrics/graphify-evals/2026-04-09-graphify-vs-search.json, metrics/graphify-evals/2026-04-09-graphify-vs-search.md

### ff-75-raw-feed-redaction

- Prompt: Find where nightly raw GitHub issue feeds are mirrored and whether issue bodies are being persisted.
- Query terms: raw, github, issues, body, sync
- Graphify candidates: scripts/overlord/check_progress_github_issue_staleness.py, scripts/overlord/check_overlord_backlog_github_alignment.py, scripts/overlord/render_github_issue_feed.py, tests/test_progress_github_issue_staleness.py
- Baseline candidates: docs/plans/issue-75-structured-agent-cycle-plan.json, metrics/graphify-evals/scenarios/fail-fast-2026-04-09.json, docs/plans/issue-75-raw-feed-redaction-pdcar.md, metrics/graphify-evals/2026-04-09-graphify-vs-search.md, .github/workflows/raw-feed-sync.yml

### ff-76-cited-code-validation

- Prompt: Find where Codex finding qualification validates cited file and line references.
- Query terms: codex, qualification, validate_location, finding, line
- Graphify candidates: scripts/overlord/codex_ingestion.py, tests/test_codex_ingestion.py
- Baseline candidates: tests/test_codex_ingestion.py, metrics/graphify-evals/scenarios/fail-fast-2026-04-09.json, docs/plans/issue-76-cited-code-path-validation-pdcar.md, metrics/graphify-evals/2026-04-09-graphify-vs-search.md, docs/plans/issue-76-structured-agent-cycle-plan.json

### ff-77-sweep-persistence-visibility

- Prompt: Find where the weekly sweep persists graph and metrics updates and whether push failures are being ignored.
- Query terms: overlord, sweep, graph, metrics, push
- Graphify candidates: scripts/overlord/codex_ingestion.py, scripts/knowledge_base/measure_graphify_usage.py, scripts/overlord/check_progress_github_issue_staleness.py, .github/workflows/governance-check.yml, .github/workflows/overlord-sweep.yml
- Baseline candidates: metrics/graphify-evals/scenarios/fail-fast-2026-04-09.json, metrics/graphify-evals/2026-04-09-graphify-vs-search.md, docs/FEATURE_REGISTRY.md, docs/plans/issue-77-structured-agent-cycle-plan.json, graphify-out/hldpro-governance/GRAPH_REPORT.md

