# Codex Brief — pre-session-context.sh hook hardening

**Issues:** #661, #662
**Branch:** `issue-661-pre-session-hook-warnings-20260502`
**Worker model:** `gpt-5.3-codex-spark` @ high
**File to edit:** `hooks/pre-session-context.sh` (one file, two slices)

---

## Your Task

Edit `hooks/pre-session-context.sh` to apply both slices below. No other files may be created or edited (except the governance artifacts listed at the bottom, which already exist as stubs).

Verify `bash -n hooks/pre-session-context.sh` exits 0 after your edits.

Commit with this exact message:
```
feat(hooks): pre-session stale-branch gate and routing reminder (#661, #662)
```

Do NOT push. The dispatcher handles push + PR.

---

## Preflight

Before your first commit, verify the worktree is clean off `origin/main`:

```bash
git fetch origin main
git diff origin/main..HEAD --name-only
```

Expected: only the governance bootstrap artifacts already committed (plan JSON, cross-review, validation stubs, etc.).

---

## Slice 1 — Gap B: Dispatcher Routing Table (fires on EVERY prompt)

**Where to insert:** BEFORE the session-once sentinel block. In the current file, after the `REPO_NAME` guard (the `if [ "$REPO_NAME" != "hldpro-governance" ]` block) and BEFORE the `SESSION_KEY` / `SENTINEL` lines.

**Insert this block:**

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

## Slice 2 — Gap A: Stale-Branch + Remote-Divergence Warnings (inside session-once block)

**Where to insert:** INSIDE the session-once block, AFTER the existing content that outputs wiki/GRAPH_REPORT, and BEFORE the final `exit 0` at the end of the file.

**Insert this block:**

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

---

## Verification

After applying both slices:

```bash
bash -n hooks/pre-session-context.sh
echo "exit code: $?"
```

Must exit 0.

---

## Acceptance Criteria

- AC-1: `bash -n hooks/pre-session-context.sh` exits 0
- AC-2: Gap B routing table lines appear BEFORE the `SESSION_KEY`/`SENTINEL` block (fires every prompt)
- AC-3: Gap A.1 block is INSIDE the session-once block (after `touch "$SENTINEL"`)
- AC-4: Gap A.2 block is adjacent to A.1, uses `timeout 5` subshell
- AC-5: `|| exit 0` guards prevent abort on git fetch failure
- AC-6: No new files created (only `hooks/pre-session-context.sh` modified among code files)

---

## Governance artifacts (already exist as stubs — update after implementation)

- `raw/validation/2026-05-02-issue-661-pre-session-hook-warnings.md` — update AC checklist to PASS
- `raw/cross-review/2026-05-02-issue-661-pre-session-hook-warnings.md` — update table to PASS

---

## Plan refs

- Structured plan: `docs/plans/issue-661-pre-session-hook-warnings-structured-agent-cycle-plan.json`
- PDCAR: `docs/plans/issue-661-pre-session-hook-warnings-pdcar.md`
- Execution scope: `raw/execution-scopes/2026-05-02-issue-661-pre-session-hook-warnings-implementation.json`
