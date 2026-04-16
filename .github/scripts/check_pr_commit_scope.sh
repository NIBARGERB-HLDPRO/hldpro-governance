#!/usr/bin/env bash
set -euo pipefail
# Checks that a PR does not contain more commits than MAX_COMMITS (default 10).
# Large commit counts are a signal of stale-worktree base contamination.
# Set MAX_COMMITS env var to override the threshold.

MAX_COMMITS="${MAX_COMMITS:-10}"

if [[ -n "${PR_BASE:-}" ]]; then
  base="$PR_BASE"
else
  base="$(git merge-base HEAD origin/main)"
fi

commit_count="$(git rev-list --count "$base..HEAD")"
changed_files="$(git diff --name-only "$base..HEAD")"
file_count="$(echo "$changed_files" | grep -c . || true)"

if [[ "$commit_count" -gt "$MAX_COMMITS" ]]; then
  echo "ERROR: PR contains $commit_count commits (max $MAX_COMMITS)."
  echo ""
  echo "Commits in this PR:"
  git log --oneline "$base..HEAD"
  echo ""
  echo "Changed files:"
  echo "$changed_files"
  echo ""
  echo "If this branch was created from a stale local origin/main, re-create the worktree from a fresh fetch:"
  echo "  git fetch origin main && git worktree add -b <branch> <path> origin/main"
  exit 1
fi

echo "Commits in this PR:"
git log --oneline "$base..HEAD"
echo ""
echo "Changed files ($file_count):"
echo "$changed_files"
echo ""
echo "Scope check passed: $commit_count commits, $file_count files changed."
