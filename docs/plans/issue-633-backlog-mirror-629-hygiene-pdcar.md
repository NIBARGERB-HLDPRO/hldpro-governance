# PDCAR — Issue #633

## Plan

Close the parent-owned `#612` backlog mirror hygiene gap that still lists closed
child `#629` as active work in `OVERLORD_BACKLOG.md`. Keep the lane limited to
that mirror reconciliation and issue-local artifacts only.

## Do

- confirm the stale `#629` row is still present in `OVERLORD_BACKLOG.md`
- move `#629` out of active `In Progress` state while preserving completed
  history visibility in `Done`
- keep `#632`, `#629`, and the broader `#612` enforcement code surfaces out of
  scope

## Check

- `OVERLORD_BACKLOG.md` no longer lists closed `#629` as active work
- completed-history visibility for `#629` is preserved
- no unrelated governance surfaces are changed
- planning packet, review artifact, and validation artifact remain issue-local

## Adjust

- if matching stale `#629` mirror drift is proven in another governance mirror
  surface, stop and explicitly widen scope before editing it
- if the stale row is already gone by implementation time, close `#633` as
  unnecessary rather than manufacturing work

## Review

Success for `#633` is bounded mirror hygiene only. It does not claim broader
`#612` closure or any new degraded-fallback enforcement progress.
