#!/bin/bash
# closeout-hook.sh — Stage 6 Karpathy Loop write-back
# Usage: ./hooks/closeout-hook.sh raw/closeouts/YYYY-MM-DD-{task}.md

set -e

CLOSEOUT_FILE="$1"
GOVERNANCE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AI_INTEGRATION_ROOT="${GOVERNANCE_ROOT}/../ai-integration-services"

if [ -z "$CLOSEOUT_FILE" ]; then
  echo "ERROR: No closeout file specified."
  echo "Usage: ./hooks/closeout-hook.sh raw/closeouts/YYYY-MM-DD-{task}.md"
  exit 1
fi

if [ ! -f "$CLOSEOUT_FILE" ]; then
  echo "ERROR: Closeout file not found: $CLOSEOUT_FILE"
  exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  HLD Pro — Stage 6 Closeout Hook"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Validate template fields filled
echo "[1/4] Validating closeout template..."
REQUIRED_FIELDS=("Date:" "Repo:" "Task ID:" "Decision Made")
for field in "${REQUIRED_FIELDS[@]}"; do
  if ! grep -q "$field" "$CLOSEOUT_FILE"; then
    echo "ERROR: Required field missing from closeout: $field"
    exit 1
  fi
done
echo "  ✓ Template validated"

# 2. Run graphify --update on ai-integration-services
echo "[2/4] Updating knowledge graph..."
if [ -d "$AI_INTEGRATION_ROOT" ]; then
  cd "$AI_INTEGRATION_ROOT"
  if command -v graphify >/dev/null 2>&1; then
    if graphify . --update --no-viz 2>&1 | tail -5; then
      echo "  ✓ Knowledge graph updated"
    else
      echo "  ⚠ graphify update failed — continuing without blocking closeout"
    fi
  else
    echo "  ⚠ graphify not installed — skipping graph update"
  fi
else
  echo "  ⚠ ai-integration-services not found at $AI_INTEGRATION_ROOT — skipping graph update"
fi

# 3. Remind to create operator_context row
echo "[3/4] operator_context check..."
if grep -q "Yes — row ID:" "$CLOSEOUT_FILE"; then
  echo "  ✓ operator_context row confirmed in closeout"
else
  echo "  ⚠ REMINDER: Create operator_context row for this decision"
  echo "    Table: operator_context"
  echo "    context_type: 'decision'"
  echo "    content: Decision summary from closeout"
  echo "    relevance_tags: extract from closeout content"
fi

# 4. Commit closeout to governance repo
echo "[4/4] Committing closeout..."
cd "$GOVERNANCE_ROOT"
git add "$CLOSEOUT_FILE"
git commit -m "docs(closeout): $(basename "$CLOSEOUT_FILE" .md)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✓ Stage 6 Closeout Complete"
echo "  Next: update wiki/ pages listed in closeout"
echo "        run overlord-sweep to wire new wiki entries"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
