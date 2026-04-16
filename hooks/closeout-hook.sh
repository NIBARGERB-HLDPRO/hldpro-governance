#!/bin/bash
# closeout-hook.sh — Stage 6 Karpathy Loop write-back
# Usage: ./hooks/closeout-hook.sh raw/closeouts/YYYY-MM-DD-{task}.md

set -e

CLOSEOUT_FILE="$1"
GOVERNANCE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$GOVERNANCE_ROOT"
BUILD_SCRIPT="${GOVERNANCE_ROOT}/scripts/knowledge_base/build_graph.py"
TARGET_SCRIPT="${GOVERNANCE_ROOT}/scripts/knowledge_base/graphify_targets.py"
INDEX_SCRIPT="${GOVERNANCE_ROOT}/scripts/knowledge_base/update_knowledge_index.py"

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

# 2. Refresh the governance graph target defined for closeout
echo "[2/4] Updating knowledge graph..."
if [ -f "$BUILD_SCRIPT" ] && [ -f "$TARGET_SCRIPT" ] && [ -f "$INDEX_SCRIPT" ]; then
  if command -v python3.11 >/dev/null 2>&1 && python3.11 -c "import graphify" >/dev/null 2>&1; then
    eval "$(python3 "$TARGET_SCRIPT" show --repo-slug hldpro-governance --format shell)"
    if python3.11 "$BUILD_SCRIPT" \
      --source "${GOVERNANCE_ROOT}/${SOURCE_PATH}" \
      --output "${GOVERNANCE_ROOT}/${OUTPUT_PATH}" \
      --wiki-dir "${GOVERNANCE_ROOT}/${WIKI_PATH}" \
      --repo-slug "${REPO_SLUG}" \
      --no-html 2>&1 | tail -20; then
      python3 "$INDEX_SCRIPT"
      echo "  ✓ Knowledge graph updated for ${REPO_SLUG}"
    else
      echo "  ⚠ graph update failed — continuing without blocking closeout"
    fi
  else
    echo "  ⚠ python3.11 + graphify not available — skipping graph update"
  fi
else
  echo "  ⚠ graphify helper scripts not found — skipping graph update"
fi

# Phase 3a: consolidate memory after graphify
if [ -x "$REPO_ROOT/scripts/consolidate-memory.sh" ]; then
  bash "$REPO_ROOT/scripts/consolidate-memory.sh" --repo hldpro-governance --dry-run && \
    bash "$REPO_ROOT/scripts/consolidate-memory.sh" --repo hldpro-governance || \
    echo "note: consolidate-memory non-fatal failure; continuing closeout"
fi

# 3. Remind to create operator_context row
echo "[3/4] operator_context check..."
if grep -q "^\[x\] Yes — row ID:" "$CLOSEOUT_FILE"; then
  echo "  ✓ operator_context row confirmed in closeout"
else
  echo "  ⚠ REMINDER: Create operator_context row for this decision"
  echo "    Table: operator_context"
  echo "    context_type: 'decision'"
  echo "    content: Decision summary from closeout"
  echo "    relevance_tags: extract from closeout content"
fi

# 4. Commit closeout to governance repo (include graphify-out + wiki if updated in step 2)
echo "[4/4] Committing closeout..."
cd "$GOVERNANCE_ROOT"
git add "$CLOSEOUT_FILE"
git add graphify-out/ wiki/ 2>/dev/null || true
git commit -m "docs(closeout): $(basename "$CLOSEOUT_FILE" .md)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✓ Stage 6 Closeout Complete"
echo "  Next: update wiki/ pages listed in closeout"
echo "        run overlord-sweep to wire new wiki entries"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
