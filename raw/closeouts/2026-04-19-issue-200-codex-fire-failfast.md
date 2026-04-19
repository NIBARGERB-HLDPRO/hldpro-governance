# Issue #200 Closeout - Codex Fire Fail-Fast

Date: 2026-04-19
Repo: hldpro-governance
Task ID: issue-200-codex-fire-failfast
Issue: [#200](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/200)
Branch: `issue-200-codex-fire-failfast`

## Decision Made

Codex dispatcher briefs must go through `scripts/codex-fire.sh` so unavailable or failing model calls produce bounded preflight failure, structured log evidence, and an immediate dispatcher-visible `CODEX_FAIL` line.

## Summary

Added `scripts/codex-fire.sh` as the local dispatcher wrapper for Codex brief execution. The wrapper preflights the selected model with a bounded timeout, writes structured failures to `raw/fail-fast-log.md`, emits `CODEX_FAIL`, and exits `1` on failure.

## Changes

- Added fake-Codex e2e tests for preflight failure, preflight timeout, execution failure, success, and review-template failure propagation.
- Routed `scripts/codex-review-template.sh` audit and critique modes through `codex-fire.sh`.
- Retained failed review-template briefs so `CODEX_FAIL` points at an inspectable file.
- Updated the local governance auto-memory note for Codex-spark dispatch behavior.
- Recorded issue #200 structured plan, PDCAR, execution scope, same-family exception, focused review, validation, and backlog/feature-registry evidence.

## Review

Focused subagent review found two call-site gaps and one evidence gap. The call-site gaps were fixed in code and tests; the memory evidence is recorded in validation because the memory file lives outside the repo.

## Validation

Validation evidence is recorded in `raw/validation/2026-04-19-issue-200-codex-fire-failfast.md`.

## Residual Risk

GitHub Actions canary paths and the Python Codex ingestion helper still call `codex exec` directly by design. They are not local dispatcher brief call sites and already have canary or bounded-timeout behavior. If those surfaces need the same wrapper contract later, route them through a separate CI-specific issue because the workflow environment and auth handling differ from local dispatch.
