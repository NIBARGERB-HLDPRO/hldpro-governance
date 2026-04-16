# Issue 77 PDCA/R — Weekly Sweep Persistence Visibility

Date: 2026-04-09
Issue: [#77](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/77)
Owner: nibargerb

## Plan

- stop swallowing graph and metrics persistence failures in the weekly sweep
- report baseline refresh status directly in the weekly issue body
- fail the workflow after report publication if commit or push persistence fails

## Do

- patched `overlord-sweep.yml` to capture `no_changes`, `commit_failed`, `push_failed`, and `success`
- appended `BASELINE REFRESH` status/detail to the generated weekly issue body
- added a final failure step so persistence errors surface in CI after the issue is updated

## Check

Verification target:
- weekly issue clearly states whether graph/metrics baseline refresh persisted
- commit or push failures no longer disappear behind `git push || true`
- workflow still produces the weekly issue before failing on persistence errors

## Adjust

If another persistence path in the sweep still suppresses failure, it belongs in this slice before the issue closes.

## Review

This fix preserves the operator-facing weekly report while making baseline staleness explicit and actionable. The workflow can now distinguish successful refreshes from stale artifacts instead of silently continuing after a failed push.
