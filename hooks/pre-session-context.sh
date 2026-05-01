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

if [ -n "$ISSUE_NUMBER" ]; then
  BACKLOG_MATCH="$REPO_ROOT/scripts/overlord/backlog_match.py"
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

exit 0
