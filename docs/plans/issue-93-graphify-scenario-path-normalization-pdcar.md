# Issue 93 PDCA/R — Graphify Scenario Path Normalization

## Plan

- remove stale absolute `repo_path` values from the fail-fast scenario corpus
- make the measurement harness resolve governance scenarios from the current checkout by default
- keep explicit `repo_path` support for cases that truly need an override
- rerun the tracked batch after normalization to determine whether the earlier regression was path drift or real retrieval degradation

## Do

- normalize `metrics/graphify-evals/scenarios/fail-fast-2026-04-09.json`
- update `scripts/knowledge_base/measure_graphify_usage.py` to resolve repo roots defensively
- extend the usage logging contract test to cover current-checkout resolution and stale-path fallback
- refresh the tracked measurement artifacts and usage-event log

## Check

- `python3 scripts/knowledge_base/test_graphify_usage_logging_contract.py`
- `python3 scripts/knowledge_base/test_graphify_governance_contract.py`
- `python3 -m py_compile scripts/knowledge_base/measure_graphify_usage.py scripts/knowledge_base/test_graphify_usage_logging_contract.py`

## Adjust

If the refreshed run still underperforms after path normalization, treat that as real graphify quality evidence rather than a harness artifact and route it into a separate retrieval-quality follow-up instead of reopening the path-normalization issue.

## Review

Expected outcome:

- scenario fixtures no longer depend on abandoned worktree paths
- clean-checkout measurement runs are stable and reproducible
- the refreshed A/B evidence can be interpreted as current-run data instead of path-dependent noise
