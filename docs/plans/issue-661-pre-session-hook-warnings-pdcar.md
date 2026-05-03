# PDCAR — Pre-session Hook Warnings: Stale-Branch Gate + Dispatcher Routing Reminder

**Issues:** #661 (Gap A — stale-branch / remote-divergence gate), #662 (Gap B — routing table reminder)
**Branch:** `issue-661-pre-session-hook-warnings-20260502`
**File:** `hooks/pre-session-context.sh` (single file, two slices)
**Date:** 2026-05-02

---

## Problem

Two dispatcher-enforcement gaps exist in `hooks/pre-session-context.sh`:

**Gap A:** When a session opens on a stale/done branch, context injected by the hook
(OVERLORD_BACKLOG.md, docs/PROGRESS.md) may reflect closed state. The hook has no warning.

**Gap B:** The CLAUDE.md CRITICAL RULE ("NEVER RESPOND DIRECTLY IF AN AGENT EXISTS FOR THE TASK")
fires once per session via the session-once sentinel. After the first prompt the routing table
is never emitted again.

---

## Plan

### Slice 1 — Gap A: Stale-Branch + Remote-Divergence Warning

Insert INSIDE the session-once block, after the existing backlog-status block (after L47),
before `exit 0`. Reuses `scripts/overlord/backlog_match.py` (existing). Bash-only, no new files.

```bash
# ── Gap A.1: Done-branch warning ─────────────────────────────────────────────
BACKLOG_MATCH="$REPO_ROOT/scripts/overlord/backlog_match.py"
BRANCH_NAME="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
ISSUE_NUMBER="$(echo "$BRANCH_NAME" | grep -oE '^issue-([0-9]+)' | grep -oE '[0-9]+')"

if [ -n "$ISSUE_NUMBER" ] && [ -f "$BACKLOG_MATCH" ]; then
  if ! python3 "$BACKLOG_MATCH" "$ISSUE_NUMBER" >/dev/null 2>&1; then
    echo ""
    echo "WARNING: Branch '$BRANCH_NAME' references issue #$ISSUE_NUMBER,"
    echo "  which is NOT in the active backlog (likely Done or closed)."
    echo "  Files on this branch (OVERLORD_BACKLOG.md, docs/PROGRESS.md) may be STALE."
    echo "  Recommended: switch to a fresh origin/main worktree before continuing."
    echo ""
  fi
fi

# ── Gap A.2: Remote-divergence warning ───────────────────────────────────────
if [ -n "$BRANCH_NAME" ] && [ "$BRANCH_NAME" != "HEAD" ]; then
  (
    cd "$REPO_ROOT" || exit 0
    timeout 5 git fetch --quiet origin main 2>/dev/null || exit 0
    LOCAL_MAIN=$(git rev-parse main 2>/dev/null || true)
    REMOTE_MAIN=$(git rev-parse origin/main 2>/dev/null || true)
    if [ -n "$LOCAL_MAIN" ] && [ -n "$REMOTE_MAIN" ] && [ "$LOCAL_MAIN" != "$REMOTE_MAIN" ]; then
      BEHIND=$(git rev-list --count "$LOCAL_MAIN..$REMOTE_MAIN" 2>/dev/null || echo "?")
      echo ""
      echo "WARNING: local 'main' is $BEHIND commit(s) behind 'origin/main'."
      echo "  Pre-session reads may reflect stale state. Run 'git pull' on main."
      echo ""
    fi
  )
fi
```

### Slice 2 — Gap B: Dispatcher Routing Table on Every Prompt

Insert BEFORE the session-once sentinel (before L18, after REPO_NAME guard at L16).
Fires on every `UserPromptSubmit`.

```bash
# ── Gap B: Dispatcher routing table — emit on EVERY prompt ───────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Dispatcher Routing Table (CLAUDE.md §CRITICAL RULE)"
echo "  NEVER RESPOND DIRECTLY IF AN AGENT EXISTS FOR THE TASK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Standards drift / session start  --> overlord"
echo "  Weekly audit / metrics           --> overlord-sweep"
echo "  Deep pattern analysis            --> overlord-audit"
echo "  Completion verification          --> verify-completion"
echo "  (full table: CLAUDE.md §Routing Table)"
echo ""
```

---

## Acceptance Criteria

- [ ] AC-1: `bash -n hooks/pre-session-context.sh` exits 0
- [ ] AC-2: Gap B routing table lines appear on every call (before session-once sentinel)
- [ ] AC-3: Gap A.1 done-branch warning prints when backlog_match.py returns non-zero
- [ ] AC-4: Gap A.2 divergence warning prints when local main is behind origin/main
- [ ] AC-5: `git fetch` failure does not abort the hook — exits cleanly
- [ ] AC-6: No new files created (bash-only edits to `hooks/pre-session-context.sh` plus governance artifacts)

---

## Risks

- **`git fetch` latency:** Wrapped in `timeout 5` + subshell; network failure silenced with `|| exit 0`
- **`backlog_match.py` API drift:** Non-zero-exit check; if signature changes, warning is silently skipped
- **Routing table verbosity:** 8-line block fires on every prompt — intentional per Gap B requirement

---

## Model Routing

- Worker: `gpt-5.3-codex-spark @ high` (mechanical bash edit, no new files)
- Reviewer: dispatcher (push + PR after codex commit)
