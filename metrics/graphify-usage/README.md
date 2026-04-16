# Graphify Usage Events

This directory holds append-only JSONL records for graphify usage in governed workflows.

Use:

```bash
python3 scripts/knowledge_base/log_graphify_usage.py \
  --repo hldpro-governance \
  --task-id issue-65 \
  --experiment-id ab-2026-04-09 \
  --session-id current-work \
  --task-type architecture_retrieval \
  --strategy graphify \
  --prompt "Which files own the workflow/doc retrieval path for the governance graph?" \
  --query-term workflow \
  --query-term retrieval \
  --query-term graphify \
  --top-candidate .github/workflows/overlord-sweep.yml \
  --top-candidate scripts/knowledge_base/measure_graphify_usage.py \
  --artifact wiki/index.md \
  --artifact graphify-out/GRAPH_REPORT.md \
  --estimated-tokens 850 \
  --notes "Used governance graph + wiki before repo search"
```

Rules:

- append-only
- log `graphify`, `repo-search`, or `hybrid`
- include the governance artifacts actually read
- include `prompt`, `query_terms`, and `top_candidates` when you want current-work A/B traces to be inspectable later
- use `experiment_id` and `session_id` to group 5-10 run comparisons without overloading `task_id`
- redact or summarize prompts before logging if they include sensitive operator, customer, or secret-bearing context
- use estimated tokens, not guessed “freeform” numbers

Default measurement behavior:

- `scripts/knowledge_base/measure_graphify_usage.py` now emits usage events automatically for each graphify and baseline scenario run
- use `--no-usage-log` only when you explicitly want to skip append-only event emission for a local debugging run
- use `--usage-event-dir <path>` in tests or scratch runs when you do not want to append into the tracked default event file
