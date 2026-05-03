#!/bin/bash
# UserPromptSubmit hook: emit the canonical governance session-start contract.
#
# NOTE: Do NOT use set -e in UserPromptSubmit hooks — silent non-zero exits suppress output.

set +e

REPO_ROOT="$HOME/Developer/HLDPRO/hldpro-governance"
if [ ! -d "$REPO_ROOT" ]; then
  exit 0
fi

# Only run in hldpro-governance
REPO_NAME="$(basename "$REPO_ROOT")"
if [ "$REPO_NAME" != "hldpro-governance" ]; then
  exit 0
fi

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
# Session-once guard: only inject on first prompt per session.
SESSION_KEY="${CLAUDE_SESSION_ID:-$$}"
SENTINEL="/tmp/hldpro-gov-pre-session-${SESSION_KEY}"
if [ -f "$SENTINEL" ]; then
  exit 0
fi
touch "$SENTINEL"

python3 "$REPO_ROOT/scripts/session_bootstrap_contract.py" --emit-hook-note
echo ""
(
  cd "$REPO_ROOT" || exit 0
  python3 "$REPO_ROOT/scripts/overlord/check_execution_environment.py" --startup-preflight
)
# Backlog status for current branch
BRANCH_NAME="$(git -C "$REPO_ROOT" branch --show-current 2>/dev/null || true)"
ISSUE_NUMBER=$(printf "%s" "$BRANCH_NAME" | grep -oE "^issue-([0-9]+)-" | grep -oE "[0-9]+" | head -1)
BACKLOG_MATCH="$REPO_ROOT/scripts/overlord/backlog_match.py"

if [ -n "$ISSUE_NUMBER" ]; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  Backlog Status — Branch: $BRANCH_NAME"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  if [ -f "$BACKLOG_MATCH" ]; then
    python3 "$BACKLOG_MATCH" "$ISSUE_NUMBER" 2>&1 || true
  else
    echo "  WARN: backlog_match.py not found at $BACKLOG_MATCH"
  fi
fi

# ── Gap A.1: Done-branch warning ─────────────────────────────────────────────
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

exit 0
