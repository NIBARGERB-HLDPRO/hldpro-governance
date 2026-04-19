# Issue #200 - Codex Fire Fail-Fast PDCA/R

Branch: `issue-200-codex-fire-failfast`
Issue: [#200](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/200)

## Plan

Add a local dispatcher wrapper for `codex exec` that proves model availability before firing a real brief. The wrapper must fail within a bounded preflight window, log structured failure evidence, and emit an immediate `CODEX_FAIL` line that the dispatcher can see.

## Do

- Create `scripts/codex-fire.sh`.
- Add fake-Codex regression tests for preflight failure, preflight timeout, execution failure, and success.
- Seed `raw/fail-fast-log.md` with the structured table contract.
- Route local dispatcher-style Codex audit and critique calls in `scripts/codex-review-template.sh` through the wrapper.
- Update feature registry, backlog mirror, review, validation, closeout, and local memory evidence for issue #200.

## Check

Final acceptance requires:

- `python3 -m pytest scripts/test_codex_fire.py`
- `bash -n scripts/codex-fire.sh scripts/codex-review-template.sh scripts/codex-preflight.sh`
- `python3 .github/scripts/check_codex_model_pins.py`
- structured plan validation
- execution-scope validation
- backlog/GitHub sync validation
- `git diff --check`
- Local CI Gate against the changed-file list
- focused review acceptance
- GitHub PR checks
- e2e fake-Codex proof that preflight failure, execution failure, and success paths behave as required

## Act

If validation and review pass, publish #200 as a focused PR and merge only after required GitHub checks are green. Any direct Codex call that is not routed through `codex-fire.sh` must be either a dedicated preflight/canary path or a helper with its own bounded timeout and structured failure handling.
