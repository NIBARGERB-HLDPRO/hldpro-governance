# Issue 85 — Workflow/Doc Retrieval PDCA/R

Date: 2026-04-09
Issue: [#85](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/85)
Owner: Governance
Status: Complete

## Plan

Keep the slice narrow.

Accepted scope:
- improve workflow/doc-heavy fail-fast retrieval without widening into upstream graphify or broad graph UX work
- keep graphify as the owner/topology layer
- add a deterministic hybrid retrieval path only for workflow-heavy scenarios
- validate the result against the same fail-fast corpus from issue `#66`

Explicitly out of scope:
- upstream graphify package changes
- graph report UX or PR-comment features
- Neo4j, semantic extraction, or model work

## Do

Implemented:
- added the canonical plan artifact at [issue-85-structured-agent-cycle-plan.json](issue-85-structured-agent-cycle-plan.json)
- extended [measure_graphify_usage.py](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85/scripts/knowledge_base/measure_graphify_usage.py) with a deterministic hybrid retrieval mode for `workflow_bug` scenarios
- rebuilt the governance graph artifact under [graphify-out/hldpro-governance](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85/graphify-out/hldpro-governance) so scenario evaluation used current-worktree paths
- updated the scenario corpus in [fail-fast-2026-04-09.json](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85/metrics/graphify-evals/scenarios/fail-fast-2026-04-09.json) to point at the current clean governance worktree
- refreshed the tracked evaluation outputs:
  - [2026-04-09-graphify-vs-search.json](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85/metrics/graphify-evals/2026-04-09-graphify-vs-search.json)
  - [2026-04-09-graphify-vs-search.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85/metrics/graphify-evals/2026-04-09-graphify-vs-search.md)

Hybrid retrieval behavior:
- keep graph-guided owner discovery and graph-link evidence
- augment workflow-heavy scenarios with bounded artifact ranking over `.github/workflows/`, `docs/`, `metrics/`, and `raw/`
- prefer primary workflow YAML over derivative plan/eval artifacts
- suppress self-referential measurement artifacts from hybrid candidate ranking

## Check

Validation run:
- `python3 -m py_compile scripts/knowledge_base/measure_graphify_usage.py`
- `/opt/homebrew/opt/python@3.11/bin/python3.11 scripts/knowledge_base/build_graph.py --source /Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85 --output /Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85/graphify-out/hldpro-governance --no-html`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --require-if-issue-branch --branch-name issue-85-workflow-doc-retrieval`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `git diff --check`

Measured result:
- graphify estimated tokens: `637`
- baseline estimated tokens: `4769`
- graphify materially relevant scenarios: `4/4`
- baseline materially relevant scenarios: `4/4`
- graphify smaller + more relevant wins: `3`

Workflow/doc-heavy improvements over issue `#66`:
- `ff-74-governance-diff-base`
  - issue `#66`: relevance `0`, workflow file missing
  - issue `#85`: relevance `4`, hybrid result now includes `.github/workflows/governance-check.yml`
- `ff-77-sweep-persistence-visibility`
  - issue `#66`: relevance `2`
  - issue `#85`: relevance `5`, hybrid result now includes `.github/workflows/overlord-sweep.yml`

## Do / Check Comparison

What worked:
- graph-guided owner discovery remained useful for code-centric cases
- workflow/doc-heavy cases improved once the retrieval path explicitly favored first-order workflow YAML over derivative plan/measurement artifacts

What failed on the first pass:
- the first hybrid attempt still over-ranked `docs/plans/issue-*` and `metrics/graphify-evals/*` because they repeated the same failure language as the real workflows
- that made the workflow-heavy retrieval look broader without materially improving the owning workflow results

## Adjust

Adjustment made in-slice:
- boosted primary workflow YAML path weighting
- penalized derivative `docs/plans/issue-*` artifacts in workflow-heavy mode
- excluded self-referential `metrics/graphify-evals/*` files from hybrid candidate ranking
- applied a workflow/doc priority multiplier after graph augmentation so workflow files could outrank adjacent code neighbors when the scenario is actually about workflow behavior

Governance guidance updated:
- [STANDARDS.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85/STANDARDS.md)
- [FEATURE_REGISTRY.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85/docs/FEATURE_REGISTRY.md)
- [FAIL_FAST_LOG.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85/docs/FAIL_FAST_LOG.md)
- [OVERLORD_BACKLOG.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85/OVERLORD_BACKLOG.md)

## Review

Decision:
- `#85` is complete
- no second non-graph baseline is needed yet

Validated guidance:
- for code-centric fail-fast work, use graph-guided retrieval first, then bounded repo search on the returned files
- for workflow/doc-heavy fail-fast work, use `hybrid`: graph-guided owner discovery plus bounded workflow/doc artifact ranking with primary workflow YAML favored over derivative documentation
