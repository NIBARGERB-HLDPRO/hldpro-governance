#!/bin/bash
# graphify-autocommit.sh — Stop hook safety net for graphify artifacts

set +e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ -z "$REPO_ROOT" ] || [ ! -d "$REPO_ROOT" ]; then
  echo "WARNING: graphify-autocommit: unable to resolve repo root" >&2
  exit 0
fi

cd "$REPO_ROOT" || {
  echo "WARNING: graphify-autocommit: unable to cd to repo root: $REPO_ROOT" >&2
  exit 0
}

DIRTY="$(git status --porcelain graphify-out/ wiki/ 2>/dev/null)"
if [ $? -ne 0 ]; then
  echo "WARNING: graphify-autocommit: unable to inspect graphify artifacts" >&2
  exit 0
fi

if [ -z "$DIRTY" ]; then
  exit 0
fi

git add graphify-out/ wiki/ 2>/dev/null
if [ $? -ne 0 ]; then
  echo "WARNING: graphify-autocommit: unable to stage graphify artifacts" >&2
  exit 0
fi

git commit -m "chore(graphify): auto-commit graph refresh $(date +%Y-%m-%d)"
if [ $? -ne 0 ]; then
  echo "WARNING: graphify-autocommit: unable to commit graphify artifacts" >&2
  exit 0
fi

exit 0
