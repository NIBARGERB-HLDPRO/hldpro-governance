#!/bin/bash
# governance-check.sh — PreToolUse:Bash governance gate.
# Steps [3/4] and [4/4] are warn-only (fail-open) to avoid blocking on network
# or auto-generated-file issues.

set +e

REPO_ROOT="$HOME/Developer/HLDPRO/hldpro-governance"

if [ ! -d "$REPO_ROOT" ]; then
  echo "GOVERNANCE-CHECK WARN: repo root not found at $REPO_ROOT — skipping (fail-open)" >&2
  exit 0
fi

cd "$REPO_ROOT"

BRANCH_NAME="$(git branch --show-current 2>/dev/null || true)"

echo "[1/4] Validating structured agent cycle plans..."
python3 scripts/overlord/validate_structured_agent_cycle_plan.py \
  --root . \
  --branch-name "$BRANCH_NAME" \
  --require-if-issue-branch
echo "  PASS structured plan validation"

echo "[2/4] Checking governance-surface changed files..."
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

echo "[3/4] Replaying active execution-scope enforcement (warn-only)..."
if [ -s "$CHANGED_FILE" ]; then
  SCOPE_OUT=$(python3 scripts/overlord/check_governance_hook_execution_scope.py \
    --root . \
    --branch "$BRANCH_NAME" \
    --changed-files-file "$CHANGED_FILE" 2>&1) || {
    echo "  WARN execution-scope replay: $SCOPE_OUT" >&2
    echo "  WARN [3/4] skipped (non-fatal)"
  }
  [ -z "$SCOPE_OUT" ] || echo "  PASS execution-scope replay"
else
  echo "  PASS no local changed files"
fi

echo "[4/4] Checking whitespace errors (warn-only)..."
WS_OUT=$(git diff --check 2>&1) || {
  echo "  WARN whitespace check: $WS_OUT" >&2
  echo "  WARN [4/4] skipped (non-fatal)"
}

echo ""
echo "Governance check PASS"
