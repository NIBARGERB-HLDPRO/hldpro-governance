#!/bin/bash
# check-errors.sh — PostToolUse:* gate: read stdin, check/record error patterns via fail_fast_state.py.
# Fail-open on infrastructure errors (missing helper, I/O errors).
# Claude Code hook contract: exit 0 = allow, exit 2 = hard block.

set +e

REPO_ROOT="$HOME/Developer/HLDPRO/hldpro-governance"
FAIL_FAST_PY="$REPO_ROOT/scripts/overlord/fail_fast_state.py"

# Fail-open if helper is missing
if [ ! -f "$FAIL_FAST_PY" ]; then
  exit 0
fi

# Read stdin (PostToolUse result JSON or raw text)
STDIN_TEXT=$(cat 2>/dev/null || true)

# Run check: exits 1 if a recurrent error pattern is detected
CHECK_OUTPUT=$(printf "%s" "$STDIN_TEXT" | python3 "$FAIL_FAST_PY" check 2>&1)
CHECK_EXIT=$?

if [ "$CHECK_EXIT" -ne 0 ]; then
  printf "%s\n" "$CHECK_OUTPUT" >&2
  exit 1
fi

# Record the result (errors swallowed — fail-open)
printf "%s" "$STDIN_TEXT" | python3 "$FAIL_FAST_PY" record 2>/dev/null || true

exit 0
