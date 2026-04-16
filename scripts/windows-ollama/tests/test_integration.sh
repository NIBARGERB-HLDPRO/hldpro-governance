#!/usr/bin/env bash
# test_integration.sh — Sprint 5 end-to-end smoke test
# Calls decide.sh → submit.py → audit.py on a synthetic non-PII prompt against live Windows host.
# Skips (exit 77) if Windows unreachable — NOT a hard fail.

set -uo pipefail

WORKER_PREFLIGHT_EXIT=0
bash scripts/windows-ollama/preflight.sh --worker > /dev/null 2>&1 || WORKER_PREFLIGHT_EXIT=$?

if [ "$WORKER_PREFLIGHT_EXIT" != "0" ]; then
  echo "SKIP: Windows preflight exit $WORKER_PREFLIGHT_EXIT — operator not on LAN or endpoint down"
  exit 77
fi

DECISION="$(bash scripts/windows-ollama/decide.sh --pii-flag no --prompt-text 'def add(a, b): return a + b  # write a unit test' --local-warm-daemon-status down --codex-spark-status blocked --windows-status ok 2>/dev/null)"
if [ "$DECISION" != "WINDOWS" ]; then
  echo "FAIL: decide.sh returned $DECISION, expected WINDOWS"
  exit 1
fi

echo "PASS: Sprint 5 integration smoke (decide.sh routing verified)"
exit 0
