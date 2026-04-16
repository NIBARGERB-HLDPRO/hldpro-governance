#!/bin/bash
# graphify-autocommit.sh — auto-commit graphify-out/ + wiki/ changes after a session
# Wired as a Stop hook in ~/.claude/settings.json
# Only fires when there are actual changes to stage and the working tree is clean enough to commit.

set -euo pipefail

GOVERNANCE_ROOT="$HOME/Developer/HLDPRO/hldpro-governance"

# Only run from inside the governance repo
if ! git -C "$GOVERNANCE_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  exit 0
fi

cd "$GOVERNANCE_ROOT"

# Check for graphify-out or wiki changes
CHANGES=$(git status --porcelain -- graphify-out/ wiki/ 2>/dev/null)
if [ -z "$CHANGES" ]; then
  exit 0
fi

# Don't auto-commit if there are staged changes from other work — don't pollute someone's in-progress commit
STAGED=$(git diff --cached --name-only 2>/dev/null)
if [ -n "$STAGED" ]; then
  echo "[graphify-autocommit] staged changes detected — skipping auto-commit to avoid polluting in-progress work"
  exit 0
fi

# Get today's date for the commit message
TODAY=$(date +%Y-%m-%d)

# Stage only graphify-out and wiki
git add graphify-out/ wiki/

# Confirm something was actually staged
STAGED_NOW=$(git diff --cached --name-only 2>/dev/null)
if [ -z "$STAGED_NOW" ]; then
  exit 0
fi

git commit -m "chore(graphify): auto-refresh knowledge graph ${TODAY}

Automated commit from graphify-autocommit Stop hook.
Files updated: $(echo "$STAGED_NOW" | wc -l | tr -d ' ') graphify-out/wiki artifacts.
"

echo "[graphify-autocommit] committed graphify-out + wiki changes"
