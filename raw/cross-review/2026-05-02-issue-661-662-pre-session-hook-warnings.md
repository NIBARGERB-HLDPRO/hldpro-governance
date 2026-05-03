---
date: 2026-05-02
issue: 661
slug: pre-session-hook-warnings
reviewer: gpt-5.3-codex-spark
reviewer_model: gpt-5.3-codex-spark
reasoning_effort: high
verdict: APPROVED
---

# Cross-Review — Issues #661 / #662: pre-session hook warnings

**Branch:** `issue-661-pre-session-hook-warnings-20260502`
**PR:** #663
**Reviewer:** gpt-5.3-codex-spark (OpenAI-family, alternate-family review)
**Date:** 2026-05-02

## Review Scope

Alternate-family QA review of the `hooks/pre-session-context.sh` changes (+43 lines)
and `OVERLORD_BACKLOG.md` (+2 rows) implementing:

- **Gap B (#662):** Dispatcher routing table emitted before the session-once sentinel (every prompt).
- **Gap A.1 (#661):** Done-branch warning via `backlog_match.py` reuse (inside session-once guard).
- **Gap A.2 (#661):** Remote-divergence warning via `git fetch` subshell (inside session-once guard).

## Findings

### Correctness

| Check | Result |
|---|---|
| Gap B routing table placed BEFORE sentinel | PASS — lines 19–30, sentinel at line 34 |
| Gap A.1 done-branch warning placed AFTER sentinel | PASS — lines 62–72 |
| Gap A.2 divergence warning placed AFTER sentinel | PASS — lines 73–88 |
| Fail-open: Gap A.1 uses `\|\| true` / no `set -e` | PASS — `set +e` at top; warning block conditional, no exit on fail |
| Fail-open: Gap A.2 uses subshell + `timeout 5` + `\|\| exit 0` | PASS — `timeout 5 git fetch --quiet origin main 2>/dev/null \|\| exit 0` |
| `BACKLOG_MATCH` variable moved before both usage sites | PASS — line 48, available to both backlog status block and Gap A.1 |
| No new files introduced | PASS — only `hooks/pre-session-context.sh` and `OVERLORD_BACKLOG.md` modified |
| `OVERLORD_BACKLOG.md` rows correctly reference #661 and #662 | PASS — two rows prepended to active section |

### Scope Compliance

All changes are bounded to the two issue surfaces. No new scripts, agents, CI workflows, or
config files were added. No existing hook contracts (fail-open, bash-only, session-once semantics)
were altered.

### Session-once Placement

Gap B (routing table) is correctly placed outside the sentinel so it fires on every
`UserPromptSubmit` event, reinforcing the dispatcher critical rule without adding session-start
cost. Gap A.1 and A.2 warnings are correctly inside the sentinel so they fire at most once per
session, consistent with the existing backlog-status block pattern.

### Edge Cases

- Detached HEAD (`$BRANCH_NAME = "HEAD"` or empty): Gap A.2 guard `[ "$BRANCH_NAME" != "HEAD" ]`
  prevents spurious divergence output. Gap A.1 guard `[ -n "$ISSUE_NUMBER" ]` prevents spurious
  backlog-match calls. Both edge cases handled correctly.
- Network unavailable: `timeout 5 ... 2>/dev/null || exit 0` in the subshell ensures the hook
  exits the subshell cleanly with no output on network failure.
- `backlog_match.py` absent: Gap A.1 guarded by `[ -f "$BACKLOG_MATCH" ]`; silent skip.

## Acceptance Criteria Checklist

| AC | Description | Decision |
|----|-------------|----------|
| AC-1 | `bash -n hooks/pre-session-context.sh` exits 0 | PASS |
| AC-2 | Gap B routing table emitted before session-once sentinel | PASS |
| AC-3 | Gap A.1 done-branch warning via `backlog_match.py` reuse | PASS |
| AC-4 | Gap A.2 remote-divergence warning via `git fetch` subshell | PASS |
| AC-5 | `git fetch` failure is silent (fail-open) | PASS |
| AC-6 | No new files | PASS |
| AC-7 | `BACKLOG_MATCH` variable accessible to both usage sites | PASS |
| AC-8 | OVERLORD_BACKLOG.md rows present for #661 and #662 | PASS |

## Verdict

**APPROVED** — Implementation matches plan specification. All acceptance criteria pass.
No blocking findings. No scope creep. Fail-open contracts intact throughout.
