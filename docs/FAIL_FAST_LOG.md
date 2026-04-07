# Fail-Fast Log

> Governance-repo error patterns and resolutions.
> Read this before retrying a failing overlord workflow, helper command, or Codex ingestion run.

## Format

Use this table format:

| Error | Root Cause | Resolution | Date |
|-------|-----------|------------|------|

## Category: TOOLING — Codex CLI, scripts, and operator helpers

| Error | Root Cause | Resolution | Date |
|-------|-----------|------------|------|
| Codex ingestion helper skipped live review generation during first real validation | The first live helper path assumed `codex exec review --base ... [PROMPT]` was supported, but Codex CLI `v0.118.0` rejects that combination. The same helper also defaulted to `o3`, which is not available on this ChatGPT-backed Codex account. | Use generic `codex exec` with `--output-schema`, parse the final JSON object from stdout, and default to `gpt-5.4` unless the operator explicitly selects another supported model. Keep validation artifacts in `~/Developer/hldpro/.codex-ingestion/{repo}/` so failures remain auditable. | 2026-04-06 |
