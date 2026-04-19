# Issue #337 Closeout - Codex Review Persona

Date: 2026-04-19
Repo: hldpro-governance
Task ID: issue-337-codex-review-persona
Issue: [#337](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/337)
Branch: `issue-337-codex-review-persona`

## Decision Made

The governance Codex review template keeps `docs/agents/codex-reviewer.md` as its tracked default persona path, while `CODEX_REVIEW_PERSONA` remains the explicit test/operator override.

## Summary

Restored the default Codex reviewer persona document required by `scripts/codex-review-template.sh`. Extended fake-Codex e2e tests so audit mode proves the default path reaches `codex-fire.sh` and the override path still injects alternate persona content.

## Changes

- Added `docs/agents/codex-reviewer.md`.
- Added default-persona e2e coverage in `scripts/test_codex_fire.py`.
- Added override-persona e2e coverage in `scripts/test_codex_fire.py`.
- Updated issue #337 PDCAR, structured plan, execution scope, same-family exception, validation, backlog mirror, and feature-registry evidence.

## Review

Focused review evidence is recorded in `raw/cross-review/2026-04-19-issue-337-codex-review-persona-review.md`.

## Validation

Validation evidence is recorded in `raw/validation/2026-04-19-issue-337-codex-review-persona.md`.

## Residual Risk

Live Codex audit execution still depends on local Codex CLI authentication and model availability. That surface is intentionally handled by `scripts/codex-fire.sh`; this slice only fixes the template's missing persona default before the wrapper is reached.
