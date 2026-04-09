# Issue 66 — Graphify Retrieval Quality PDCA/R

Date: 2026-04-09
Issue: [#66](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/66)
Owner: Governance
Status: Complete

## Plan

Keep the slice narrow. Improve fail-fast retrieval quality without expanding into broad graph UX or adoption work.

Accepted scope:
- strengthen graph-guided retrieval ranking with real graph structure
- improve relevance scoring beyond exact top-file string hits
- validate against the same real fail-fast scenario corpus from issue `#65`
- update governance guidance only if the retrieval experiment proves a better pattern

Explicitly out of scope:
- upstream graphify changes
- PR graph comments
- sweep graph dashboards
- semantic extraction
- Neo4j expansion

## Do

Implemented:
- added the canonical plan artifact at [issue-66-structured-agent-cycle-plan.json](issue-66-structured-agent-cycle-plan.json)
- rewrote [measure_graphify_usage.py](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-66/scripts/knowledge_base/measure_graphify_usage.py) to:
  - prefer repo-scoped graph artifacts when they exist
  - use graph links for one-hop propagation
  - aggregate scores at the file level
  - apply community-aware evidence boosting
  - score relevance by owning-file hits plus expected evidence terms
- corrected the scenario corpus in [fail-fast-2026-04-09.json](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-66/metrics/graphify-evals/scenarios/fail-fast-2026-04-09.json) to use the current clean governance worktree
- generated a governance graph artifact under [graphify-out/hldpro-governance](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-66/graphify-out/hldpro-governance)
- reran the measurement corpus and refreshed:
  - [2026-04-09-graphify-vs-search.json](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-66/metrics/graphify-evals/2026-04-09-graphify-vs-search.json)
  - [2026-04-09-graphify-vs-search.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-66/metrics/graphify-evals/2026-04-09-graphify-vs-search.md)

## Check

Validation run:
- `python3 -m py_compile scripts/knowledge_base/measure_graphify_usage.py`
- `/opt/homebrew/opt/python@3.11/bin/python3.11 scripts/knowledge_base/build_graph.py --source ... --output graphify-out/hldpro-governance --no-html`
- `python3 scripts/knowledge_base/measure_graphify_usage.py --repos-root /Users/bennibarger/Developer/HLDPRO --graph-root /Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-66/graphify-out --scenario-file .../metrics/graphify-evals/scenarios/fail-fast-2026-04-09.json --output-dir .../metrics/graphify-evals --date 2026-04-09`

Measured result:
- graphify estimated tokens: `665`
- baseline estimated tokens: `4668`
- graphify materially relevant scenarios: `2/4`
- baseline materially relevant scenarios: `4/4`
- graphify smaller + more relevant wins: `1`

Validated win:
- `ff-76-cited-code-validation`
  - graph-guided retrieval returned [codex_ingestion.py](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-66/scripts/overlord/codex_ingestion.py) and [test_codex_ingestion.py](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-66/tests/test_codex_ingestion.py)
  - graph relevance score: `4`
  - baseline relevance score: `3`
  - graph tokens: `95`
  - baseline tokens: `1129`

## Do / Check Comparison

What improved:
- the experiment is now valid for governance-repo scenarios because it uses a governance graph, not the AIS root graph
- graph-guided retrieval can beat repo search on code-centric fail-fast debugging while staying far smaller in retrieval footprint

What did not improve enough:
- workflow/doc-heavy scenarios such as `ff-74` and `ff-77` still underperform relative to repo search
- that remaining gap is about corpus coverage and retrieval mode, not just ranking

## Adjust

Follow-up created:
- [#85](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/85) Improve fail-fast retrieval for workflow/doc-heavy scenarios

Reason:
- review showed the remaining misses depend heavily on workflow YAML and documentation context
- that is a different problem than the code-graph ranking improvements completed here
- it should be handled as a separate issue-backed slice, not silently folded into `#66`

Governance guidance updated:
- [STANDARDS.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-66/STANDARDS.md)
- [FEATURE_REGISTRY.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-66/docs/FEATURE_REGISTRY.md)
- [FAIL_FAST_LOG.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-66/docs/FAIL_FAST_LOG.md)
- [OVERLORD_BACKLOG.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-66/OVERLORD_BACKLOG.md)

## Review

Decision:
- `#66` is successful as a narrow retrieval-quality slice
- it should not be expanded into report/adoption/UX work in the same issue

Validated guidance:
- for fail-fast debugging, use symptom terms plus mechanism/owner terms
- use graph-guided retrieval first to identify likely owning files and adjacent code paths
- then confirm those returned files with bounded repo search
- do not rely on graph-only retrieval yet for workflow/doc-heavy fail-fast scenarios
