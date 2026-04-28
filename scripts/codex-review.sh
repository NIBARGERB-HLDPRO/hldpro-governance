#!/usr/bin/env bash
# Canonical operator-facing wrapper for governed Codex/Claude specialist review.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export CLAUDE_REVIEW_ENV_FILE="${CLAUDE_REVIEW_ENV_FILE:-$REPO_ROOT/.env.local}"

exec bash "$REPO_ROOT/scripts/codex-review-template.sh" "$@"
