# PDCAR — Issue #636

## Plan

Close the parent-owned `#612` mirror hygiene gap that still lists closed child
`#629` as active work in `docs/PROGRESS.md`. Keep the lane limited to that
single PROGRESS mirror reconciliation and issue-local artifacts only.

## Do

- confirm the stale `#629` row is still present in `docs/PROGRESS.md`
- reconcile `#629` out of active `IN PROGRESS` state while preserving honest
  completed-history visibility
- keep `OVERLORD_BACKLOG.md`, `#629`, `#632`, and the broader `#612`
  enforcement surfaces out of scope

## Check

- `docs/PROGRESS.md` no longer lists closed `#629` as active work
- completed-history visibility for `#629` is preserved honestly
- no unrelated governance surfaces are changed
- planning packet, review artifact, and validation artifact remain issue-local

## Adjust

- if the stale `#629` PROGRESS row is already gone by implementation time,
  close `#636` as unnecessary rather than manufacturing work
- if broader `docs/PROGRESS.md` drift is proven and needed, stop and widen
  scope explicitly before editing additional rows

## Review

Success for `#636` is bounded `docs/PROGRESS.md` mirror hygiene only. It does
not claim broader `#612` closure, does not reopen `#629`, and does not absorb
separate stale rows such as `#632` without explicit scope expansion.
