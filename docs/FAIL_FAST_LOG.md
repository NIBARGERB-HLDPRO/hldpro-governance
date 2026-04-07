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
| Real governed-repo Codex review can run longer than unattended validation budgets | After the CLI/model fixes landed, a real `knocktracker` review still exceeded a 60-second validation budget. Without a hard timeout, the helper can leave long-running Codex sessions hanging and block the sweep loop. | Add `--timeout-seconds` to `codex_ingestion.py`, fail closed with a skip marker when the budget is exceeded, and keep production sweep invocation disabled until unattended runtime and auth behavior are validated at a longer bound. | 2026-04-06 |
| GitHub Actions sweep surfaced only Codex CLI banner text instead of the real failure reason | In non-interactive runners, `codex exec` always emits the stdin/banner preamble on stderr. The helper was truncating that boilerplate first, so production reports showed `Reading additional input from stdin...` instead of the actionable trailing error. | Invoke `codex exec` with an explicit `--` prompt separator and `--color never`, then summarize the last meaningful stderr/stdout lines while stripping the banner boilerplate before writing the skip reason. | 2026-04-06 |
