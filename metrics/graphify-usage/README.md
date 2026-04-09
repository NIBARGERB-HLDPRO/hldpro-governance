# Graphify Usage Events

This directory holds append-only JSONL records for graphify usage in governed workflows.

Use:

```bash
python3 scripts/knowledge_base/log_graphify_usage.py \
  --repo hldpro-governance \
  --task-id issue-65 \
  --task-type architecture_retrieval \
  --strategy graphify \
  --artifact wiki/index.md \
  --artifact graphify-out/GRAPH_REPORT.md \
  --estimated-tokens 850 \
  --notes "Used governance graph + wiki before repo search"
```

Rules:

- append-only
- log `graphify`, `repo-search`, or `hybrid`
- include the governance artifacts actually read
- use estimated tokens, not guessed “freeform” numbers
