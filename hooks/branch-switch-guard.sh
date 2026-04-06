#!/bin/bash
# Global PreToolUse hook: blocks git checkout/switch branch operations
# Prevents multi-session conflicts where one session's branch switch
# corrupts another session's working directory.
# Allows file-restore operations (git checkout -- <file>, git checkout .)
#
# IMPORTANT: Do NOT use set -e / set -euo pipefail in PreToolUse hooks.
# Silent non-zero exits block ALL Bash commands with "No stderr output".

set +e

INPUT=""
if [ ! -t 0 ]; then
  INPUT=$(cat 2>/dev/null) || true
fi

COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null) || true

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Split on && and ; to get individual command segments
# Use awk for reliable splitting (macOS sed doesn't handle \n in replacement)
BLOCKED=""
while IFS= read -r segment; do
  # Trim whitespace
  trimmed=$(echo "$segment" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  [ -z "$trimmed" ] && continue

  # Only match git checkout/switch at the START of the segment
  # This avoids false positives from commit messages containing "git checkout"
  if ! echo "$trimmed" | grep -qE '^\s*git\s+(checkout|switch)\b'; then
    continue
  fi

  # ALLOW: git checkout with -- anywhere (file restore)
  if echo "$trimmed" | grep -qE '^\s*git\s+checkout\s+(.*\s)?--\s'; then
    continue
  fi

  # ALLOW: git checkout . (restore all files)
  if echo "$trimmed" | grep -qE '^\s*git\s+checkout\s+\.\s*$'; then
    continue
  fi

  # Branch operation detected — record for blocking
  BLOCKED="$trimmed"
  break

done < <(echo "$COMMAND" | awk '{gsub(/&&/,"\n"); gsub(/;/,"\n"); gsub(/\|\|/,"\n"); print}')

if [ -n "$BLOCKED" ]; then
  echo "BLOCKED: Branch switching is not allowed. Multi-session safety risk." >&2
  echo "" >&2
  echo "  Blocked command: $BLOCKED" >&2
  echo "" >&2
  echo "  Use 'EnterWorktree' tool or 'git worktree add' instead." >&2
  echo "  These create isolated working copies that don't affect other sessions." >&2
  echo "" >&2
  echo "  Allowed operations:" >&2
  echo "    git checkout -- <file>     (restore a file)" >&2
  echo "    git checkout .             (restore all files)" >&2
  echo "    git worktree add <path>    (isolated branch work)" >&2
  exit 2
fi

exit 0
