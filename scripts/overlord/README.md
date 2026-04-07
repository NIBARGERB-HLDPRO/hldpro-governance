# Codex Ingestion Helpers

`codex_ingestion.py` operationalizes the weekly Codex review flow:

- `generate`: run a Codex review for a repo and write `review-{date}.json`
- `qualify`: dedupe and validate findings, then write `qualified-{date}.json` and `backlog-{date}.md`
- `status`: list pending backlog files for session-start surfacing
- `promote`: preview or apply approved findings into repo docs

Examples:

```bash
python3 scripts/overlord/codex_ingestion.py generate \
  --repo knocktracker \
  --repo-path ~/Developer/hldpro/knocktracker

python3 scripts/overlord/codex_ingestion.py qualify \
  --repo knocktracker \
  --repo-path ~/Developer/hldpro/knocktracker

python3 scripts/overlord/codex_ingestion.py status --repo knocktracker

python3 scripts/overlord/codex_ingestion.py promote \
  --repo knocktracker \
  --repo-path ~/Developer/hldpro/knocktracker \
  --finding-id F001
```

Notes:

- `generate` defaults to `gpt-5.4`, which works on ChatGPT-backed Codex accounts.
- If your account supports it, pass `--model o3` for a heavier second-opinion pass.
- `generate` precomputes commit subjects, changed files, diffstat, and a bounded patch excerpt outside Codex, then feeds that review context to generic `codex exec` over stdin with `--output-schema`.
- `generate` fails closed with a skip marker if Codex exceeds `--timeout-seconds` (default `180`).
- In trusted CI, prefer staging `CODEX_AUTH_JSON` into `CODEX_HOME/auth.json` before running `generate`; keep `OPENAI_API_KEY` as the fallback path when the CLI supports env-only auth in that runner context.
