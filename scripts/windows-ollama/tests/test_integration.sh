#!/usr/bin/env bash
# test_integration.sh — issue #432 off-ladder smoke test
# Verifies decide.sh never selects Windows as an active SoM worker route.

set -uo pipefail

DECISION="$(bash scripts/windows-ollama/decide.sh --pii-flag no --prompt-text 'def add(a, b): return a + b  # write a unit test' --local-warm-daemon-status down --codex-spark-status blocked --windows-status ok 2>/dev/null)"
if [ "$DECISION" = "WINDOWS" ]; then
  echo "FAIL: decide.sh returned WINDOWS, but Windows is off the active SoM worker ladder"
  exit 1
fi

echo "PASS: issue #432 off-ladder smoke (decision=$DECISION)"
exit 0
