# Same-Family Implementation Exception - Issue #197

Date: 2026-04-19
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/197
Branch: `fix/issue-197-portable-hook-paths`
Expiry: 2026-04-26

## Reason

Issue #197 is a narrow implementation-ready bugfix with explicit acceptance criteria: replace two hardcoded hook command strings in `.claude/settings.json` with the portable `git rev-parse --show-toplevel` wrapper and prove root/nested hook execution.

The same Codex implementation session may author the small settings/documentation patch because the scope is constrained to existing command strings and governance evidence. Independent read-only review remains required before PR closeout.

## Bounds

Allowed:

- `.claude/settings.json`
- `docs/plans/issue-197-portable-hook-paths-pdcar.md`
- `docs/plans/issue-197-structured-agent-cycle-plan.json`
- `raw/exceptions/2026-04-19-issue-197-same-family-implementation.md`
- `raw/execution-scopes/2026-04-19-issue-197-portable-hook-paths-implementation.json`
- `raw/validation/2026-04-19-issue-197-portable-hook-paths.md`
- `raw/closeouts/2026-04-19-issue-197-portable-hook-paths.md`
- `OVERLORD_BACKLOG.md`
- `docs/PROGRESS.md`
- Stage 6 generated graph/wiki artifacts

Not allowed:

- Downstream repo edits.
- Hook script semantic changes.
- Broad cleanup of historical path strings outside `.claude/settings.json`.

## Review Requirement

Before PR closeout, a read-only reviewer agent must inspect the diff for scope, command correctness, and validation adequacy.
