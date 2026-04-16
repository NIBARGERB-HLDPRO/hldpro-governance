#!/bin/bash
# UserPromptSubmit hook: inject governance pre-session context
#
# Fires on every user prompt. Injects wiki/index.md + GRAPH_REPORT.md into context
# so agents that call Read with the wrong env-injected path still get the content.
#
# Root cause this works around: Claude Code session env injects "/Users/bennibarger/"
# (wrong username, 'k') but real username is "bennibarger" ('g'). Read tool fails
# on the injected path; this hook uses shell $HOME which resolves correctly.
#
# Output is shown to Claude as a <user-prompt-submit-hook> system note.
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

# Session-once guard: only inject on first prompt per session
# Uses a tmpfile keyed by CLAUDE_SESSION_ID (set by Claude Code) or PID as fallback
SESSION_KEY="${CLAUDE_SESSION_ID:-$$}"
SENTINEL="/tmp/hldpro-gov-pre-session-${SESSION_KEY}"
if [ -f "$SENTINEL" ]; then
  exit 0
fi
touch "$SENTINEL"

WIKI="$REPO_ROOT/wiki/index.md"
GRAPH="$REPO_ROOT/graphify-out/hldpro-governance/GRAPH_REPORT.md"

# Only inject if both files exist — skip silently on fresh checkouts
if [ ! -f "$WIKI" ] || [ ! -f "$GRAPH" ]; then
  exit 0
fi

echo "=== PRE-SESSION CONTEXT (hldpro-governance) ==="
echo ""
echo "--- wiki/index.md ---"
cat "$WIKI"
echo ""
echo "--- GRAPH_REPORT.md (god nodes only) ---"
# Extract summary + god nodes only to keep context tight
awk '/^## Summary/,/^## Surprising/' "$GRAPH" | head -20
echo ""
echo "=== END PRE-SESSION CONTEXT ==="
