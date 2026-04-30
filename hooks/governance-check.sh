#!/bin/bash
# governance-check.sh - local governance gate entrypoint
# Usage: ./hooks/governance-check.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "${CLAUDE_CWD:-$PWD}" rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$REPO_ROOT" ] || [ ! -f "$REPO_ROOT/OVERLORD_BACKLOG.md" ]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

cd "$REPO_ROOT"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  HLD Pro - Governance Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "[1/6] Validating structured agent cycle plans..."
BRANCH_NAME="$(git branch --show-current 2>/dev/null || true)"
python3 scripts/overlord/validate_structured_agent_cycle_plan.py \
  --root . \
  --branch-name "$BRANCH_NAME" \
  --require-if-issue-branch
echo "  PASS structured plan validation"

echo "[2/6] Checking governance-surface changed files..."
CHANGED_FILE="$(mktemp "${TMPDIR:-/tmp}/hldpro-governance-changed.XXXXXX")"
trap 'rm -f "$CHANGED_FILE"' EXIT
{
  git diff --name-only
  git diff --cached --name-only
  git ls-files --others --exclude-standard
} | awk 'NF' | sort -u > "$CHANGED_FILE"

if [ -s "$CHANGED_FILE" ]; then
  python3 scripts/overlord/validate_structured_agent_cycle_plan.py \
    --root . \
    --branch-name "$BRANCH_NAME" \
    --changed-files-file "$CHANGED_FILE" \
    --enforce-governance-surface
  echo "  PASS governance-surface validation"
else
  echo "  PASS no local changed files"
fi

echo "[3/6] Replaying active execution-scope enforcement..."
if [ -s "$CHANGED_FILE" ]; then
  python3 scripts/overlord/check_governance_hook_execution_scope.py \
    --root . \
    --branch "$BRANCH_NAME" \
    --changed-files-file "$CHANGED_FILE"
  echo "  PASS execution-scope replay"
else
  echo "  PASS no local changed files"
fi

echo "[4/6] Checking OVERLORD_BACKLOG issue alignment..."
python3 scripts/overlord/check_overlord_backlog_github_alignment.py
echo "  PASS backlog alignment"

echo "[5/6] Checking current issue branch parity..."
python3 scripts/overlord/check_governance_issue_branch_parity.py
echo "  PASS branch parity"

echo "[6/6] Checking whitespace errors..."
git diff --check
if ! git diff --cached --quiet --exit-code; then
  git diff --cached --check
fi
echo "  PASS whitespace check"

echo ""
echo "Governance check PASS"
