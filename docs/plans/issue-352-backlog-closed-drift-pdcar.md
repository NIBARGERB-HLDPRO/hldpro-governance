# Issue #352 - Backlog Closed-Issue Drift PDCAR

Date: 2026-04-19
Branch: `fix/issue-352-backlog-closed-drift-20260419`
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/352

## Plan

`OVERLORD_BACKLOG.md` is a roadmap/status mirror, while GitHub Issues are the execution backlog. The actionable `In Progress` section contained closed issue refs, so a new session could incorrectly select completed work. This slice reconciles the mirror and hardens the validator so closed issue refs fail before merge.

Acceptance criteria:

- `OVERLORD_BACKLOG.md` has no closed issues in `Planned` or `In Progress`.
- Closed work is moved to `Done` or removed only when already represented by an existing Done row.
- `scripts/overlord/check_overlord_backlog_github_alignment.py` fails when an actionable row references a closed issue.
- Focused e2e/unit coverage proves a closed issue in `In Progress` fails.
- Structured plan, execution scope, validation evidence, and Stage 6 closeout are recorded.
- Final AC: Local CI Gate and GitHub PR checks pass before issue closeout.

## Do

- Created issue #352 as the governing GitHub issue.
- Removed stale closed issue rows from actionable backlog mirrors.
- Added Done evidence rows for closed work that still needed governance visibility.
- Updated the Overlord backlog validator to check issue state through GitHub, not only issue-reference syntax.
- Added focused validator coverage for closed `In Progress` issue refs.
- Set `GH_TOKEN` for the governance and Local CI Gate workflow checks so the GitHub state lookup is available in CI.

## Check

Validation commands are recorded in `raw/validation/2026-04-19-issue-352-backlog-closed-drift.md`.

Required checks:

| Check | Expected |
|---|---|
| `python3 scripts/overlord/test_check_overlord_backlog_github_alignment.py` | PASS |
| `python3 scripts/overlord/check_overlord_backlog_github_alignment.py` | PASS |
| structured plan validator | PASS |
| execution-scope assertion | PASS |
| Local CI Gate | PASS |
| Stage 6 closeout hook | PASS |

## Adjust

The original drift was not a missing issue-reference problem; every stale row had an issue ref. The control needed to verify issue state for both `Planned` and `In Progress`, while keeping historical closed work under `Done`.

## Review

Read-only reviewer Pauli confirmed the stale `In Progress` refs for #200, #212, #213, #214, #223, #224, #296, and #298, and confirmed #298 already had a matching Done row. This slice folds that review into the reconciliation and leaves broader backlog taxonomy changes out of scope.
