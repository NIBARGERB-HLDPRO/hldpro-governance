# Issue #189 - Launchd Backlog Issue Reference PDCAR

Date: 2026-04-19
Branch: `fix/issue-189-launchd-issue-ref-20260419`
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/189

## Plan

The active governance mirrors incorrectly linked the Stage 5+ som-worker boot-start integration row to an unrelated stale-checkout measurement bug. Issue #189 is the open issue for the boot-start integration work.

Acceptance criteria:

- `OVERLORD_BACKLOG.md` links the launchd row to #189.
- `docs/PROGRESS.md` mirrors the same #189 reference.
- Historical closeout references that describe the boot-start follow-up no longer point to the stale issue.
- Grep verification finds zero remaining stale boot-start issue mappings.
- Final AC: backlog GitHub sync and structured-plan governance checks pass.

## Do

- Updated the active backlog row from #104 to #189.
- Updated the progress mirror from #104 to #189.
- Corrected two historical closeout notes that described the boot-start follow-up with the stale issue.
- Added issue-specific structured plan and execution-scope evidence for the governance-surface doc change.

## Check

Validation evidence is recorded in `raw/validation/2026-04-19-issue-189-launchd-issue-ref.md`.

Required checks:

| Check | Expected |
|---|---|
| stale boot-start issue-reference grep | zero results |
| `python3 scripts/overlord/check_overlord_backlog_github_alignment.py OVERLORD_BACKLOG.md` | PASS |
| `bash .github/scripts/validate_backlog_gh_sync.sh` | PASS |
| structured plan validator | PASS |
| execution-scope assertion | PASS |

## Adjust

The existing backlog sync gate only checks whether referenced issues are open, so #104 passed even though it was semantically wrong. This slice corrects the mirror without expanding #189 into implementation work.

## Review

This is a bounded governance hygiene fix. No architecture or standards change is included.
