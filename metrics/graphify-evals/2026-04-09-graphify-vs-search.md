# Graphify Measurement — 2026-04-09

## Summary

- Scenarios: 4
- Graphify hits: 2
- Baseline hits: 4
- Graphify estimated tokens: 759
- Baseline estimated tokens: 4769
- Graphify smaller + more relevant wins: 1
- Second non-graph baseline recommended: False
- Baseline decision: No second non-graph baseline is recommended yet; improve graph-guided ranking against the existing repo-search baseline first.

## Scenario Results

| Scenario | Graphify Relevant | Baseline Relevant | Graphify Score | Baseline Score | Graphify Tokens | Baseline Tokens |
|---|---:|---:|---:|---:|---:|---:|
| ff-74-governance-diff-base | 1 | 1 | 4 | 3 | 204 | 1470 |
| ff-75-raw-feed-redaction | 0 | 1 | 1 | 5 | 243 | 1058 |
| ff-76-cited-code-validation | 0 | 1 | 1 | 3 | 89 | 1136 |
| ff-77-sweep-persistence-visibility | 1 | 1 | 4 | 4 | 223 | 1105 |

## Guidance

- Validated pattern: use symptom terms plus mechanism/owner terms (function, workflow, file family) so graph-guided retrieval can exploit communities and one-hop links instead of only file-name overlap.
- Use graph-guided retrieval first for topology and owning-file discovery, then confirm with repo search on the returned files.
- Baseline decision: No second non-graph baseline is recommended yet; improve graph-guided ranking against the existing repo-search baseline first.

## Query Traces

### ff-74-governance-diff-base

- Prompt: Find why reusable governance checks only inspect the last commit in a multi-commit PR.
- Query terms: governance, workflow_call, diff, base, github.event.before
- Graphify candidates: measure_graphify_usage.py, .github/workflows/governance-check.yml, .github/workflows/overlord-sweep.yml, .github/workflows/overlord-nightly-cleanup.yml, .github/workflows/raw-feed-sync.yml
- Baseline candidates: docs/plans/issue-74-governance-diff-base-pdcar.md, docs/plans/issue-74-structured-agent-cycle-plan.json, metrics/graphify-evals/scenarios/fail-fast-2026-04-09.json, metrics/graphify-evals/2026-04-09-graphify-vs-search.json, docs/FEATURE_REGISTRY.md

### ff-75-raw-feed-redaction

- Prompt: Find where nightly raw GitHub issue feeds are mirrored and whether issue bodies are being persisted.
- Query terms: raw, github, issues, body, sync
- Graphify candidates: check_progress_github_issue_staleness.py, check_overlord_backlog_github_alignment.py, render_github_issue_feed.py, test_progress_github_issue_staleness.py
- Baseline candidates: docs/plans/issue-75-structured-agent-cycle-plan.json, metrics/graphify-evals/scenarios/fail-fast-2026-04-09.json, docs/plans/issue-75-raw-feed-redaction-pdcar.md, .github/workflows/raw-feed-sync.yml, docs/FEATURE_REGISTRY.md

### ff-76-cited-code-validation

- Prompt: Find where Codex finding qualification validates cited file and line references.
- Query terms: codex, qualification, validate_location, finding, line
- Graphify candidates: codex_ingestion.py, test_codex_ingestion.py
- Baseline candidates: tests/test_codex_ingestion.py, metrics/graphify-evals/scenarios/fail-fast-2026-04-09.json, docs/plans/issue-76-cited-code-path-validation-pdcar.md, docs/plans/issue-76-structured-agent-cycle-plan.json, graphify-out/hldpro-governance/GRAPH_REPORT.md

### ff-77-sweep-persistence-visibility

- Prompt: Find where the weekly sweep persists graph and metrics updates and whether push failures are being ignored.
- Query terms: overlord, sweep, graph, metrics, push
- Graphify candidates: codex_ingestion.py, measure_graphify_usage.py, check_progress_github_issue_staleness.py, .github/workflows/governance-check.yml, .github/workflows/overlord-sweep.yml
- Baseline candidates: metrics/graphify-evals/scenarios/fail-fast-2026-04-09.json, docs/plans/issue-77-structured-agent-cycle-plan.json, graphify-out/hldpro-governance/GRAPH_REPORT.md, docs/FEATURE_REGISTRY.md, docs/plans/issue-77-sweep-push-failures-pdcar.md

