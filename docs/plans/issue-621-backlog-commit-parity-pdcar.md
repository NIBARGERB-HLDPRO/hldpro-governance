# Issue #621 PDCAR: Implement Fail-Closed Backlog/Commit-Progression Parity

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/621
Parent: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/615
Prior children:
- https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/617
- https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/619
Dependencies:
- https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/607
- https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/612
Related follow-up:
- https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/614
Branch: `issue-621-backlog-commit-parity-20260430`

## Plan

Implement the next smallest residual child under issue `#615` after `#617`
and `#619`: fail-closed parity on the real root backlog and commit-progression
hook path.

This child owns the root local hook path only. It must not reopen `#617`
startup/helper work, and it must not absorb the mutation-time pre-tool lane
defined by `#619`, the planning-authority contract in `#607`, the
degraded-fallback schema or CI contract in `#612`, or the downstream consumer
verifier work in `#614`.

Mandatory intake for this lane includes:

- `docs/PROGRESS.md`
- `STANDARDS.md`
- issue `#615` plus its critical closeout contract and routing updates
- merged child issues `#617` and `#619`
- issue `#621`
- the live root hook surfaces:
  - `hooks/backlog-check.sh`
  - `hooks/governance-check.sh`
- any smallest helper surface needed for issue-branch backlog or progression parity

## Do

Implementation scope for issue `#621`:

- fail closed on the real root hook path when backlog-first authority is not
  satisfied for the current issue branch
- reconcile the current authority mismatch between repo wording and actual root
  hook behavior so one canonical contract governs branch or commit progression
- keep `OVERLORD_BACKLOG.md` mirror alignment as an existing check, but do not
  let it remain the only gate for issue-branch progression on this repo
- add the smallest shared helper needed for deterministic issue-branch
  backlog/progression parity, if the hooks cannot stay duplicated safely
- add focused tests and validation artifacts for blocked and allowed
  branch/commit progression on the root hook path only
- co-stage the required governance docs for a bounded governance-surface code
  slice: `docs/PROGRESS.md`, `docs/FEATURE_REGISTRY.md`, and the relevant
  `docs/FAIL_FAST_LOG.md` entry
- produce the issue-local Stage 6 closeout artifact for the bounded root-hook
  parity slice

## Check

The lane is acceptable only if it:

- remains bounded to `hooks/backlog-check.sh`, `hooks/governance-check.sh`, the
  smallest shared parity helper if needed, focused tests, required governance
  doc co-staging, and issue-local artifacts
- encodes and fixes the live contradiction directly:
  repo policy wording and root hook behavior must not leave split authority
  between `docs/PROGRESS.md`-driven tracking language and
  `OVERLORD_BACKLOG.md`-only enforcement
- keeps `#617`, `#619`, `#607`, `#612`, and `#614` as external boundaries
- does not broaden into startup/helper work, mutation-time pre-tool work,
  degraded-fallback schema/CI work, or downstream verifier work
- returns concrete blocked and allowed proof on the root hook path rather than
  prose-only assertions
- co-stages the required governance docs for the bounded implementation slice
- carries a valid Stage 6 closeout artifact for the issue-local implementation
  slice

Implementation validation must include:

- focused tests for the touched root hooks and any parity helper
- one blocked case where backlog-first authority is missing on the real root
  path for an issue branch
- one blocked case where commit or branch progression is refused for an
  in-scope governance change
- one allowed case where canonical governed evidence is present and progression
  succeeds
- one allowed out-of-scope or read-only case
- one parity proof showing standards wording, hook behavior, and helper lookup
  all agree on the same canonical authority source
- exact command, exit code, and block or allow message for each case
- `bash -n hooks/backlog-check.sh`
- `bash -n hooks/governance-check.sh`
- the repo-local Stage 6 closeout validator
- the `hldpro-governance` Local CI Gate profile
- `git diff --check`

## Adjust

If this lane starts editing `.claude/settings.json`,
`hooks/pre-session-context.sh`, or
`scripts/overlord/check_execution_environment.py`, stop and keep the work on
the root backlog/commit-progression path only.

If this lane starts editing `hooks/code-write-gate.sh`,
`hooks/schema-guard.sh`, or `scripts/overlord/check_plan_preflight.py`, stop
and keep the work out of the `#619` mutation-time lane.

If this lane starts editing `assert_execution_scope.py`, fallback-log schema
surfaces, CI workflow enforcement, or downstream verifier code, stop and route
that work back to `#612` or `#614`.

If this lane starts claiming repo-wide governance closure, stop and restore the
anti-overclaim boundary: this is a root-hook parity slice only.

## Review

Required before completion:

- research specialist check that the implementation write set stays bounded to
  the root backlog/commit-progression hook path
- QA specialist proof review against the `#615` closeout contract and the
  authority-source parity objective
- critical audit review of the lane ACs and proof obligations
- governed alternate-family review of the implementation packet before
  promotion or closeout

Issue `#621` may close source-repo root backlog/commit-progression parity
only. It cannot be cited as proof that `#607`, `#612`, or `#614` are closed,
and it does not close the broader pre-hook fail-closed program still owned by
`#615`.
