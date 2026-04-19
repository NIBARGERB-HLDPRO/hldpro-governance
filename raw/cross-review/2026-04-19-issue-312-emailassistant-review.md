# Issue #312 EmailAssistant Discovery Review

Date: 2026-04-19
Reviewer: Codex subagent `Sartre`
Scope: Read-only EmailAssistant discovery for hldpro-governance#312.

## Verdict

Accepted.

## Findings

- `NIBARGERB-HLDPRO/EmailAssistant` is active, private, and uses default branch `main`.
- The repo has no `.github/workflows/`, no visible workflow runs, and no repo-local CI.
- The direct branch protection endpoint for `main` reports `Branch not protected`; org rulesets apply to main/develop but expose no required status checks for this repo.
- Front-door governance files are absent: `CLAUDE.md`, `AGENTS.md`, `CODEX.md`, `.github/CODEOWNERS`, dependabot, `docs/PROGRESS.md`, `docs/FEATURE_REGISTRY.md`, `docs/DATA_DICTIONARY.md`, `docs/SERVICE_REGISTRY.md`, and `docs/FAIL_FAST_LOG.md`.
- Present files include `README.md`, `LICENSE.txt`, `config.env.template`, and `docs/session-2026-04-01.md`.
- Stack is Python with Flask, Anthropic SDK, Exchange/EWS, Microsoft Graph, SMTP notifications, Windows batch launchers, PyInstaller, and NSIS installer assets.
- Data sensitivity is high: municipal email, PIP/personnel context, credentials, generated drafts, commitments, processed-email state, logs, and style-profile artifacts.

## Recommendation

Classify EmailAssistant as:

- `governance_tier`: `full`
- `security_tier`: `full-pentagi`
- `lifecycle_status`: `active`
- `governance_status`: `adoption_blocked`

Dispatcher registry coverage should land in #312. Repo-local bootstrap should remain downstream issue-backed by `EmailAssistant#1` before source or governance-file edits occur.
