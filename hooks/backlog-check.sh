#!/bin/bash
# backlog-check.sh - local backlog/GitHub alignment gate
# Usage: ./hooks/backlog-check.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "${CLAUDE_CWD:-$PWD}" rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$REPO_ROOT" ] || [ ! -f "$REPO_ROOT/OVERLORD_BACKLOG.md" ]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

cd "$REPO_ROOT"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  HLD Pro - Backlog Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "[1/1] Checking OVERLORD_BACKLOG issue alignment..."
python3 scripts/overlord/check_overlord_backlog_github_alignment.py

echo ""
echo "Backlog check PASS"
