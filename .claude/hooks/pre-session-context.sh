#!/usr/bin/env bash

set +e

REPO_ROOT="$(git -C "${CLAUDE_CWD:-$PWD}" rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$REPO_ROOT" ]; then
  exit 0
fi

python3 "$REPO_ROOT/scripts/session_bootstrap_contract.py" --emit-hook-note
exit 0
