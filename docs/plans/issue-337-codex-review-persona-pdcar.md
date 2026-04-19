# Issue #337 - Codex Review Default Persona PDCA/R

Branch: `docs/issue-337-codex-review-persona`
Issue: [#337](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/337)

## Plan

Restore the default Codex reviewer persona path used by `scripts/codex-review-template.sh` so audit and critique modes do not fail before reaching `scripts/codex-fire.sh`. Preserve `CODEX_REVIEW_PERSONA` as the operator/test override and prove both paths with fake-Codex regression coverage.

## Do

- Add the tracked default persona at `docs/agents/codex-reviewer.md`.
- Add a regression test that runs `bash scripts/codex-review-template.sh audit <target>` without `CODEX_REVIEW_PERSONA` and proves the request reaches `codex-fire.sh`.
- Keep the existing override regression so tests/operators can still provide an alternate persona file.
- Record execution scope, validation, focused review, and Stage 6 closeout evidence.

## Check

Final acceptance requires:

- `python3 -m pytest scripts/test_codex_fire.py`
- `bash -n scripts/codex-fire.sh scripts/codex-review-template.sh scripts/codex-preflight.sh`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-337-codex-review-persona-implementation.json`
- `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --report-dir cache/local-ci-gate/reports --json`
- Focused review acceptance
- GitHub PR checks

## Act

If validation passes, publish the focused #337 PR and merge only after GitHub checks are green. Any broader Codex review wrapper cleanup that is not needed to satisfy the missing persona bug should become a separate issue.
