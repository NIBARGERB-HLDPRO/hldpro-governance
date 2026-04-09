# Graphify Measurement — 2026-04-09

## Summary

- Scenarios: 4
- Graphify hits: 2
- Baseline hits: 4
- Graphify estimated tokens: 665
- Baseline estimated tokens: 4668
- Graphify smaller + more relevant wins: 1
- Second non-graph baseline recommended: False
- Baseline decision: No second non-graph baseline is recommended yet; improve graph-guided ranking against the existing repo-search baseline first.

## Scenario Results

| Scenario | Graphify Relevant | Baseline Relevant | Graphify Score | Baseline Score | Graphify Tokens | Baseline Tokens |
|---|---:|---:|---:|---:|---:|---:|
| ff-74-governance-diff-base | 0 | 1 | 0 | 3 | 197 | 1384 |
| ff-75-raw-feed-redaction | 1 | 1 | 4 | 5 | 119 | 1058 |
| ff-76-cited-code-validation | 1 | 1 | 4 | 3 | 95 | 1129 |
| ff-77-sweep-persistence-visibility | 0 | 1 | 2 | 4 | 254 | 1097 |

## Guidance

- Validated pattern: use symptom terms plus mechanism/owner terms (function, workflow, file family) so graph-guided retrieval can exploit communities and one-hop links instead of only file-name overlap.
- Use graph-guided retrieval first for topology and owning-file discovery, then confirm with repo search on the returned files.
- Baseline decision: No second non-graph baseline is recommended yet; improve graph-guided ranking against the existing repo-search baseline first.
