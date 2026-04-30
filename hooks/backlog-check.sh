#!/bin/bash
# backlog-check.sh — PreToolUse:Bash gate: verify current branch has an open backlog entry.
# Fail-open on non-issue branches. Hard-fail when issue branch has no open entry.
# Claude Code hook contract: exit 0 = allow, exit 2 = hard block (not used here — we exit 1 for soft block).

set +e

REPO_ROOT="$HOME/Developer/HLDPRO/hldpro-governance"
BACKLOG_MATCH="$REPO_ROOT/scripts/overlord/backlog_match.py"

# Fail-open if helper is missing
if [ ! -f "$BACKLOG_MATCH" ]; then
  echo "BACKLOG-CHECK WARN: backlog_match.py not found at $BACKLOG_MATCH — skipping (fail-open)" >&2
  exit 0
fi

# Extract issue number from branch name (matches issue-<N>-* pattern)
BRANCH_NAME=$(git -C "$REPO_ROOT" branch --show-current 2>/dev/null || true)
ISSUE_NUMBER=$(printf "%s" "$BRANCH_NAME" | grep -oE "^issue-([0-9]+)-" | grep -oE "[0-9]+" | head -1)

# Not on an issue branch — fail-open
if [ -z "$ISSUE_NUMBER" ]; then
  exit 0
fi

# Run backlog_match.py
MATCH_OUTPUT=$(python3 "$BACKLOG_MATCH" "$ISSUE_NUMBER" 2>&1)
MATCH_EXIT=$?

if [ "$MATCH_EXIT" -ne 0 ]; then
  printf "BACKLOG-CHECK FAIL: No open entry for #%s found in docs/PROGRESS.md or OVERLORD_BACKLOG.md.\n" "$ISSUE_NUMBER" >&2
  printf "  Branch: %s\n" "$BRANCH_NAME" >&2
  printf "  Helper output: %s\n" "$MATCH_OUTPUT" >&2
  printf "  Next: add an open entry for #%s to OVERLORD_BACKLOG.md before proceeding.\n" "$ISSUE_NUMBER" >&2
  exit 1
fi

exit 0
