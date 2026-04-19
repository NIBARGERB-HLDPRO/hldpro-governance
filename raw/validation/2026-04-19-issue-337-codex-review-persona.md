# Issue 337 Validation: Codex Review Default Persona

Date: 2026-04-19
Issue: [#337](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/337)

## Change Under Test

`scripts/codex-review-template.sh` defaults to `docs/agents/codex-reviewer.md`. This slice adds that tracked persona and a fake-Codex regression proving default `audit` setup reaches `scripts/codex-fire.sh` without requiring `CODEX_REVIEW_PERSONA`.

## Local Validation

| Check | Result | Evidence |
|-------|--------|----------|
| Fake-Codex e2e tests | PASS | `python3 -m pytest scripts/test_codex_fire.py` -> 6 passed |
| Shell syntax | PASS | `bash -n scripts/codex-fire.sh scripts/codex-review-template.sh scripts/codex-preflight.sh` |
| Structured plans | PASS | `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .` |
| Governance-surface planning | PASS | `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-337-codex-review-persona --changed-files-file cache/local-ci-gate/reports/changed-files.txt --enforce-governance-surface` |
| Execution scope | PASS | `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-337-codex-review-persona-implementation.json` |
| Codex model pins | PASS | `python3 .github/scripts/check_codex_model_pins.py` |
| Local CI Gate | PASS | `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --report-dir cache/local-ci-gate/reports --json` |
| Stage 6 closeout hook | PASS | `bash hooks/closeout-hook.sh raw/closeouts/2026-04-19-issue-337-codex-review-persona.md` |

## E2E Proof

The new `test_review_template_default_persona_reaches_codex_fire` regression:

- removes `CODEX_REVIEW_PERSONA` from the environment,
- runs `bash scripts/codex-review-template.sh audit scripts/codex-fire.sh`,
- fake-preflights Codex successfully,
- captures the final `codex exec` prompt and arguments from `codex-fire.sh`,
- verifies `gpt-5.4`, `model_reasoning_effort=high`, `docs/codex-reviews`, and the default persona content are present,
- verifies no `CODEX_FAIL` or fail-fast log is produced.

The existing `test_review_template_propagates_wrapper_failure` keeps `CODEX_REVIEW_PERSONA` override coverage.

## Review

Claude CLI focused review returned accepted-with-follow-up. It found the test design sound and requested model frontmatter on the new persona file. The frontmatter was added in this slice.

Evidence: `raw/cross-review/2026-04-19-issue-337-codex-review-persona-review.md`.

## Final Disposition

Issue #337 acceptance criteria are satisfied once Stage 6 closeout passes, PR checks pass, and the implementation PR merges.
