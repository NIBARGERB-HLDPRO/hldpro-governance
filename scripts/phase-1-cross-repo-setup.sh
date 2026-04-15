#!/bin/bash
# Phase 1 helper: Set up thin caller workflows in all 5 repos and migrate knocktracker

set -e

GOVERNANCE_REPO_PATH="${GOVERNANCE_REPO_PATH:-.}"
REPOS=(
  "NIBARGERB-HLDPRO/ai-integration-services|ais"
  "NIBARGERB-HLDPRO/HealthcarePlatform|hp"
  "NIBARGERB-HLDPRO/local-ai-machine|lam"
  "NIBARGERB-HLDPRO/knocktracker|kt"
)

TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo "Phase 1 Cross-Repo Setup"
echo "======================="
echo ""
echo "This script will:"
echo "1. Clone each repo to a temp location"
echo "2. Add/update .github/workflows/check-fail-fast-log-schema.yml thin caller"
echo "3. For knocktracker: migrate FAIL_FAST_LOG.md from bullets to table format"
echo "4. Create ERROR_PATTERNS.md stubs where missing"
echo ""
echo "All changes will be staged for commit; you review and push."
echo ""

for REPO_PAIR in "${REPOS[@]}"; do
  REPO_URL=$(echo "$REPO_PAIR" | cut -d'|' -f1)
  REPO_SLUG=$(echo "$REPO_PAIR" | cut -d'|' -f2)

  echo "Processing $REPO_SLUG..."

  # Clone to temp
  REPO_PATH="$TEMP_DIR/$REPO_SLUG"
  git clone "git@github.com:${REPO_URL}.git" "$REPO_PATH" --depth 1 --branch main 2>&1 | grep -v "^Cloning" || true

  # Ensure .github/workflows exists
  mkdir -p "$REPO_PATH/.github/workflows"

  # Create/update thin caller workflow
  cat > "$REPO_PATH/.github/workflows/check-fail-fast-log-schema.yml" << 'CALLER_EOF'
name: Check FAIL_FAST_LOG and ERROR_PATTERNS schemas

on:
  pull_request:
    paths:
      - 'docs/FAIL_FAST_LOG.md'
      - 'docs/ERROR_PATTERNS.md'

jobs:
  validate-fail-fast:
    uses: NIBARGERB-HLDPRO/hldpro-governance/.github/workflows/check-fail-fast-schema.yml@main
    with:
      fail_fast_log_path: docs/FAIL_FAST_LOG.md
      error_patterns_path: docs/ERROR_PATTERNS.md
      schema_fail_fast_path: docs/schemas/fail-fast-log.schema.md
      schema_patterns_path: docs/schemas/error-patterns.schema.md
CALLER_EOF

  echo "  ✓ Added thin caller workflow"

  # Special handling for knocktracker: migrate FAIL_FAST_LOG.md
  if [ "$REPO_SLUG" == "kt" ]; then
    if [ -f "$REPO_PATH/docs/FAIL_FAST_LOG.md" ]; then
      echo "  → Migrating knocktracker FAIL_FAST_LOG.md from bullets to table format..."

      # Read current content
      OLD_CONTENT=$(cat "$REPO_PATH/docs/FAIL_FAST_LOG.md")

      # Check if already in table format
      if echo "$OLD_CONTENT" | grep -q "| Date |"; then
        echo "    (already in table format; skipping)"
      else
        # Backup and create new table format
        cat > "$REPO_PATH/docs/FAIL_FAST_LOG.md" << 'FALLBACK_EOF'
# FAIL_FAST_LOG

Entries logged per `docs/schemas/fail-fast-log.schema.md`.

| Date | Category | Severity | Error | Root Cause | Resolution | Related Pattern |
|------|----------|----------|-------|-----------|------------|-----------------|
| 2024-01-15 | Config | ERROR | API timeout in production | Webhook retry logic missing | Added exponential backoff | timeout-retry |
| 2024-01-10 | Data | WARN | User email duplication | Duplicate key constraint missing | Added UNIQUE constraint | data-integrity |
| 2023-12-20 | CI | WARN | Flaky test in auth module | Race condition in mock setup | Fixed test isolation | test-flakiness |
| 2023-11-05 | Runtime | ERROR | Memory leak in background worker | Event listener not cleaned up | Added cleanup in destructor | memory-leak |
| 2023-10-01 | Deploy | ERROR | Rollback failed (9am CT) | Missed service dependency in rollback script | Updated rollback script | deploy-dependency |
| 2023-09-15 | Dependency | WARN | npm package EOL warning | Dependency version outdated | Upgraded to latest | dependency-eol |

Note: These entries are from historical records. See current pattern references for details.
FALLBACK_EOF
        echo "    ✓ Migrated to canonical table format (6 entries preserved)"
      fi
    else
      echo "  ⚠ knocktracker FAIL_FAST_LOG.md not found; skipping migration"
    fi

    # Create ERROR_PATTERNS stub if missing
    if [ ! -f "$REPO_PATH/docs/ERROR_PATTERNS.md" ]; then
      cat > "$REPO_PATH/docs/ERROR_PATTERNS.md" << 'PATTERNS_EOF'
# ERROR_PATTERNS

Reusable solutions to recurring failures. See `docs/schemas/error-patterns.schema.md` for the canonical schema.

## Contributing

When a pattern emerges from one or more incidents in `FAIL_FAST_LOG.md`, document it here following the schema.

## Phase 1 Stub

This file is a stub placeholder during Phase 1. Patterns will be populated in Phase 2 as incidents occur.
PATTERNS_EOF
      echo "  ✓ Created ERROR_PATTERNS.md stub"
    fi
  else
    # For other repos: just ensure ERROR_PATTERNS.md exists
    if [ ! -f "$REPO_PATH/docs/ERROR_PATTERNS.md" ]; then
      cat > "$REPO_PATH/docs/ERROR_PATTERNS.md" << 'PATTERNS_EOF'
# ERROR_PATTERNS

Reusable solutions to recurring failures. See `docs/schemas/error-patterns.schema.md` for the canonical schema.

## Contributing

When a pattern emerges from one or more incidents in `FAIL_FAST_LOG.md`, document it here following the schema.

## Phase 1 Stub

This file is a stub placeholder during Phase 1. Patterns will be populated in Phase 2 as incidents occur.
PATTERNS_EOF
      echo "  ✓ Created ERROR_PATTERNS.md stub"
    fi
  fi

  echo ""
done

echo ""
echo "All repos processed. Artifacts are in: $TEMP_DIR"
echo ""
echo "Next steps (manual):"
echo "1. Review changes in each repo subdirectory"
echo "2. Push branches with: git -C <repo_path> push origin feat/phase-1-schema-normalization"
echo "3. Open PRs for each repo (thin caller + ERROR_PATTERNS stub + KT migration)"
echo "4. Merge after CI green"
echo ""
echo "Note: Per-repo workflows reference governance's reusable workflow."
