# Cross-Review — Issue #227 Read-Only Observer

Date: 2026-04-17
Issue: #227
Reviewer: Claude Opus 4.6
Reviewed worktree: `/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-227-readonly-observer-20260417`
Verdict: APPROVED_WITH_CHANGES
Final disposition: Accepted after required changes

## Scope

Read-only alternate-family review of the #227 observer diff:

- `scripts/orchestrator/read_only_observer.py`
- `scripts/orchestrator/test_read_only_observer.py`
- `launchd/com.hldpro.governance-observer.plist`
- `docs/runbooks/always-on-governance.md`
- governance-surface classifier updates for `launchd/` and `scripts/orchestrator/`
- #227 plan, PDCAR, and registry documentation

## Findings

### F1 — launchd plist hardcoded local machine paths

Severity: blocking template portability issue
Status: resolved

Reviewer finding: the checked-in plist used `/Users/bennibarger/Developer/HLDPRO/hldpro-governance/...` paths directly. That would fail for another checkout and was not safe as a reusable template.

Resolution: replaced checked-in paths with `__REPO_ROOT__` placeholders and updated the runbook install command to render the template with `sed "s#__REPO_ROOT__#$(pwd)#g"` before `launchctl bootstrap`.

### F2 — Directory artifact fingerprints only hashed names

Severity: non-blocking report quality issue
Status: resolved

Reviewer finding: directory artifacts hashed sorted relative paths but not file contents.

Resolution: directory fingerprints now hash `relative_path:sha256(file)` entries for each file.

### F3 — Raw issue feed discovery used a fixed date

Severity: non-blocking brittleness
Status: resolved

Reviewer finding: the observer looked for `2026-04-09-*` raw issue files directly.

Resolution: raw issue feed discovery now selects the latest matching `raw/github-issues/*-<repo>.md` file by repo display name, directory name, or slug.

## Accepted Review Notes

The reviewer verified that:

- `write_reports()` writes only to `report_root/projects/<repo_slug>/reports/`.
- `--check-only` writes nothing.
- No packet modules or `raw/packets/` paths are used.
- `packet_enqueue_enabled` is hardcoded false.
- Tests cover write boundaries, packet non-interference, CLI check-only behavior, report path prefixes, and artifact hash fields.
- The launchd runbook documents manual install, health check, bootout, removal, and emergency kill.
- The #226 governance-surface classifier was extended to cover `launchd/` and `scripts/orchestrator/`.

## Result

All required review changes were applied before closeout validation.
