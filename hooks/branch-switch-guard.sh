#!/bin/bash
# Global PreToolUse hook: blocks git checkout/switch branch operations
# Prevents multi-session conflicts where one session's branch switch
# corrupts another session's working directory.
# Allows file-restore operations (git checkout -- <file>, git checkout .)
# Blocks issue worktree creation unless the command explicitly declares a
# planning bootstrap or points to an existing claimed execution scope.
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
WORKTREE_BLOCKED=""
WORKTREE_REASON=""
while IFS= read -r segment; do
  # Trim whitespace
  trimmed=$(echo "$segment" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  [ -z "$trimmed" ] && continue

  # Strip leading VAR=value assignments for command matching while retaining
  # the original segment for explicit bootstrap/scope markers.
  command_part=$(echo "$trimmed" | sed -E 's/^([A-Za-z_][A-Za-z0-9_]*=[^[:space:]]+[[:space:]]+)*//')

  if echo "$command_part" | grep -qE '^\s*git\s+worktree\s+add\b' &&
     echo "$command_part" | grep -qE '(^|[[:space:]])(-b|-B|--branch)[[:space:]]+[^[:space:]]*issue-[0-9]+'; then
    lane_payload=$(python3 - "$command_part" <<'PY' 2>/dev/null || true
import json
import re
import shlex
import sys

tokens = shlex.split(sys.argv[1])
branch = ""
worktree = ""
for index, token in enumerate(tokens):
    if token in {"-b", "-B", "--branch"} and index + 1 < len(tokens):
        branch = tokens[index + 1]
        if index + 2 < len(tokens):
            worktree = tokens[index + 2]
        break
match = re.search(r"issue-([0-9]+)", branch)
print(json.dumps({"branch": branch, "worktree": worktree, "issue": match.group(1) if match else ""}))
PY
)
    branch_name=$(echo "$lane_payload" | jq -r '.branch // empty' 2>/dev/null) || branch_name=""
    worktree_path=$(echo "$lane_payload" | jq -r '.worktree // empty' 2>/dev/null) || worktree_path=""
    branch_issue=$(echo "$lane_payload" | jq -r '.issue // empty' 2>/dev/null) || branch_issue=""
    repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || repo_root=""
    repo_slug=$(echo "$trimmed" | sed -nE 's/.*(^|[[:space:]])HLDPRO_REPO_SLUG=([^[:space:]]+).*/\2/p' | head -n 1)
    if [ -z "$repo_slug" ]; then
      repo_slug="${HLDPRO_REPO_SLUG:-}"
    fi
    if [ -z "$repo_slug" ] && [ -n "$repo_root" ]; then
      repo_slug=$(basename "$repo_root")
    fi
    if [ -n "$repo_root" ] && [ -n "$branch_name" ] && [ -n "$worktree_path" ] && [ -n "$branch_issue" ] &&
       [ -f "$repo_root/scripts/overlord/lane_bootstrap.py" ]; then
      lane_output=$(python3 "$repo_root/scripts/overlord/lane_bootstrap.py" \
        --repo-root "$repo_root" \
        --repo-slug "$repo_slug" \
        --json \
        validate \
        --branch-name "$branch_name" \
        --worktree-path "$worktree_path" \
        --issue-number "$branch_issue" 2>/dev/null)
      lane_status=$?
      if [ "$lane_status" -ne 0 ]; then
        WORKTREE_BLOCKED="$trimmed"
        WORKTREE_REASON=$(echo "$lane_output" | jq -r '.reason // "repo-specific lane policy rejected worktree command"' 2>/dev/null)
        break
      fi
    fi

    if echo "$trimmed" | grep -qE '(^|[[:space:]])HLDPRO_LANE_CLAIM_BOOTSTRAP=1([[:space:]]|$)'; then
      continue
    fi

    scope_ref=$(echo "$trimmed" | sed -nE 's/.*(^|[[:space:]])HLDPRO_LANE_CLAIM_SCOPE=([^[:space:]]+).*/\2/p' | head -n 1)
    if [ -n "$branch_issue" ] && [ -n "$scope_ref" ]; then
      repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || repo_root=""
      if [ -n "$repo_root" ]; then
        python3 - "$repo_root" "$scope_ref" "$branch_issue" <<'PY' >/dev/null 2>&1
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
scope_ref = pathlib.Path(sys.argv[2])
issue = int(sys.argv[3])
scope_path = scope_ref if scope_ref.is_absolute() else root / scope_ref
payload = json.loads(scope_path.read_text(encoding="utf-8"))
claim = payload.get("lane_claim")
if not isinstance(claim, dict) or claim.get("issue_number") != issue:
    raise SystemExit(1)
PY
        if [ "$?" -eq 0 ]; then
          continue
        fi
      fi
    fi

    WORKTREE_BLOCKED="$trimmed"
    break
  fi

  # Only match git checkout/switch at the START of the segment
  # This avoids false positives from commit messages containing "git checkout"
  if ! echo "$command_part" | grep -qE '^\s*git\s+(checkout|switch)\b'; then
    continue
  fi

  # ALLOW: git checkout with -- anywhere (file restore)
  if echo "$command_part" | grep -qE '^\s*git\s+checkout\s+(.*\s)?--\s'; then
    continue
  fi

  # ALLOW: git checkout . (restore all files)
  if echo "$command_part" | grep -qE '^\s*git\s+checkout\s+\.\s*$'; then
    continue
  fi

  # Branch operation detected — record for blocking
  BLOCKED="$trimmed"
  break

done < <(echo "$COMMAND" | awk '{gsub(/&&/,"\n"); gsub(/;/,"\n"); gsub(/\|\|/,"\n"); print}')

if [ -n "$WORKTREE_BLOCKED" ]; then
  echo "BLOCKED: Issue worktree creation requires an explicit lane claim or planning bootstrap." >&2
  if [ -n "$WORKTREE_REASON" ]; then
    echo "  Lane policy: $WORKTREE_REASON" >&2
    echo "" >&2
  fi
  echo "" >&2
  echo "  Blocked command: $WORKTREE_BLOCKED" >&2
  echo "" >&2
  echo "  Allowed issue-lane bootstrap forms:" >&2
  echo "    HLDPRO_LANE_CLAIM_BOOTSTRAP=1 git worktree add -b issue-<n>-<slug> <path> <base>" >&2
  echo "    HLDPRO_REPO_SLUG=HealthcarePlatform HLDPRO_LANE_CLAIM_BOOTSTRAP=1 git worktree add -b sandbox/issue-<n>-pr-pending-<scope> <path>/issue-<n>-pr-pending-<scope> <base>" >&2
  echo "    HLDPRO_LANE_CLAIM_SCOPE=raw/execution-scopes/<scope>.json git worktree add -b issue-<n>-<slug> <path> <base>" >&2
  echo "" >&2
  echo "  The scope form must include lane_claim.issue_number matching issue-<n>." >&2
  exit 2
fi

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
