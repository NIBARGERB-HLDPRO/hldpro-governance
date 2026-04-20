# PDCAR: Issue #384 Backlog Active-Row Drift Repair

Date: 2026-04-20
Branch: `issue-384-backlog-drift-pdcar-20260420`
Issue: [#384](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/384)
Related: [#382](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/382), [PR #383](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/pull/383)

## Plan

Repair the post-merge drift where `OVERLORD_BACKLOG.md` still listed closed issue #382 under `In Progress`. Preserve the audit finding as issue-backed governance work and align the legacy backlog-sync command path with the hardened checker that validates both actionable sections.

## Do

1. Move #382 from active backlog/progress sections to Done with PR #383 and merge commit evidence.
2. Add issue #384 planning evidence for the drift repair and prevention work.
3. Replace the legacy Planned-only `validate_backlog_gh_sync.py` behavior with a compatibility wrapper around `check_overlord_backlog_github_alignment.py`.
4. Add focused coverage proving the legacy entrypoint delegates to the hardened checker.
5. Run focused unit tests, backlog alignment, structured plan validation, execution-scope validation, and local diff checks.

## Check

- `OVERLORD_BACKLOG.md` has no active row for closed #382.
- `docs/PROGRESS.md` no longer lists #382 as an active feature request or operational item.
- The dedicated backlog-sync entrypoint validates the same policy as the hardened checker: active `Planned` and `In Progress` rows require open GitHub issues.
- Focused tests prove wrapper delegation.
- Local validation passes before pushing a PR.

## Adjust

If a future PR intentionally closes an issue at merge time, the issue row must be moved out of actionable sections before merge or followed immediately by a post-merge reconciliation issue. The safer default is to put completion rows in Done during the closing PR and keep `In Progress` empty unless a still-open issue remains active after merge.

## Review

Review should verify the fix is mirror-only plus checker-path parity, with no unrelated graph/wiki churn and no changes to issue-closing semantics.
