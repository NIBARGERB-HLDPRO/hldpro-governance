# Issue #337 - Codex Review Persona PDCA/R

Branch: `issue-337-codex-review-persona`
Issue: [#337](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/337)

## Plan

Restore the tracked default persona used by `scripts/codex-review-template.sh` so normal audit and critique invocations do not fail before they reach `scripts/codex-fire.sh`. Keep the `CODEX_REVIEW_PERSONA` override for tests and operators.

## Do

- Add `docs/agents/codex-reviewer.md`.
- Extend fake-Codex tests to cover default persona routing.
- Extend fake-Codex tests to prove `CODEX_REVIEW_PERSONA` override content is honored.
- Record issue #337 planning, execution scope, same-family exception, review, validation, closeout, backlog, and feature-registry evidence.

## Check

Final acceptance requires:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest scripts/test_codex_fire.py`
- `bash -n scripts/codex-fire.sh scripts/codex-review-template.sh scripts/codex-preflight.sh`
- `python3 .github/scripts/check_codex_model_pins.py`
- `python3 -m py_compile scripts/test_codex_fire.py`
- structured plan validation
- execution-scope validation
- backlog/GitHub sync validation
- `git diff --check`
- Local CI Gate against the changed-file list
- focused review acceptance
- Stage 6 closeout hook
- GitHub PR checks

## Act

If validation and review pass, publish #337 as a focused PR and merge only after CI is green. The final e2e acceptance proof is the fake-Codex test suite proving that both default and override persona paths reach the fail-fast wrapper.
