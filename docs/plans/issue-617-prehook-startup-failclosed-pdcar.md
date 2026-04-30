# Issue #617 PDCAR: Implement Fail-Closed Startup Lane-State Surfacing

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/617
Parent: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/615
Dependencies:
- https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/607
- https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/612
Related follow-up:
- https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/614
Branch: `issue-617-prehook-startup-failclosed-20260430`

## Plan

Implement the first source-repo fresh-session/startup slice planned by issue
`#615`.

This child owns the local startup/helper surfacing path and fail-closed unique
scope discovery only. It does not own broader pre-hook write blocking, the
planning-authority contract itself, the degraded-fallback schema/CI contract,
or downstream consumer drift verification.

Mandatory intake for this lane includes:

- `docs/PROGRESS.md`
- issue `#615` plus its recorded critical closeout contract
- dependency issues `#607` and `#612`
- the live local surfaces:
  - `.claude/settings.json`
  - `hooks/pre-session-context.sh`
  - `scripts/overlord/check_execution_environment.py`

## Do

Implementation scope for issue `#617`:

- surface active execution scope, `execution_mode`, `next_role` or
  `next_execution_step`, and required specialists on the local startup/helper
  path
- fail closed when no unique claimed scope can be resolved for an
  execution-capable session
- co-stage the required governance docs for the startup/helper implementation
  slice: `docs/PROGRESS.md`, `docs/FEATURE_REGISTRY.md`, and the relevant
  `docs/FAIL_FAST_LOG.md` pattern entry
- produce the issue-local Stage 6 closeout artifact for the bounded
  governance-surface implementation slice
- add focused startup helper/hook tests and validation artifacts for the
  startup success/fail transcripts only

## Check

The lane is acceptable only if it:

- remains bounded to the local startup/helper surfacing path and does not
  absorb broader pre-hook write-blocking surfaces
- keeps `#607` as the planning-authority dependency rather than absorbing that
  whole contract
- keeps `#612` as the schema/CI degraded-fallback enforcement lane
- keeps `#614` as the downstream consumer verifier/drift-gate lane
- returns one startup success transcript and one expected-fail startup
  transcript
- co-stages the required governance docs for the bounded implementation slice
- carries a valid Stage 6 closeout artifact for the issue-local implementation
  slice
- keeps any broader code-write/pre-hook blocking work for a later child under
  `#615`

Implementation validation must include:

- targeted tests for the touched startup helper/hook surfaces
- the repo-local Stage 6 closeout validator
- the `hldpro-governance` Local CI Gate profile
- `git diff --check`

## Adjust

If this lane starts re-editing the planning-only packet in `#615`, stop and
keep the work on `#617` startup surfaces only.

If this lane drifts into execution-scope schema/validator changes that belong
to `#612`, stop and move that change back to `#612`.

If this lane starts absorbing broader pre-hook write-blocking logic, stop and
route that work into a later child under `#615`.

If this lane starts claiming repo-wide fresh-session impossibility, stop and
restore the anti-overclaim boundary: this is a local source-repo startup slice
only.

## Review

Required before completion:

- research specialist check that the implementation write set stays bounded to
  the startup/helper surfaces above
- QA specialist proof review against the `#615` closeout contract
- governed alternate-family review of the implementation packet before
  promotion/closeout

Issue `#617` may close source-repo startup-surface fail-closed surfacing only.
It cannot be cited as proof that `#607`, `#612`, or `#614` are closed, and it
does not close the broader pre-hook write-blocking work still implied by
`#615`.
