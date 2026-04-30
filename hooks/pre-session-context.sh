#!/bin/bash
# UserPromptSubmit hook: emit the canonical governance session-start contract.
#
# NOTE: Do NOT use set -e in UserPromptSubmit hooks — silent non-zero exits suppress output.

set +e

REPO_ROOT="$(git -C "${CLAUDE_CWD:-$PWD}" rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$REPO_ROOT" ]; then
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
exit 0
