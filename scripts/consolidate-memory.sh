#!/usr/bin/env bash

set -euo pipefail

SCRIPT_NAME="consolidate-memory.sh"
DEFAULT_REPO="hldpro-governance"
REPO_SLUG=""
DRY_RUN=0

usage() {
  cat <<'EOF_USAGE'
Usage: consolidate-memory.sh [--repo <repo-slug>] [--dry-run]

Updates the governed repository MEMORY.md pointer for recent operator_context
learners based on entries since the last MEMORY.md update.

Options:
  --repo <slug>   Target repo slug.
                  Allowed: ai-integration-services, HealthcarePlatform,
                  local-ai-machine, knocktracker, hldpro-governance
  --dry-run       Print planned changes without writing MEMORY.md
  --help          Show this help text
EOF_USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --repo)
      if [ "$#" -lt 2 ]; then
        echo "$SCRIPT_NAME: --repo requires a value" >&2
        usage
        exit 1
      fi
      REPO_SLUG="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --help)
      usage
      exit 0
      ;;
    *)
      echo "$SCRIPT_NAME: unknown option $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [ -z "$REPO_SLUG" ]; then
  TOP_LEVEL="$(git rev-parse --show-toplevel 2>/dev/null || echo "$PWD")"
  REPO_SLUG="$(basename "$TOP_LEVEL")"
fi

case "$REPO_SLUG" in
  ai-integration-services|HealthcarePlatform|local-ai-machine|knocktracker|hldpro-governance)
    ;;
  *)
    echo "$SCRIPT_NAME: unsupported repo slug '$REPO_SLUG'" >&2
    exit 1
    ;;
esac

GOVERNANCE_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$PWD")"
MEMORY_PATH="${HOME}/.claude/projects/-Users-bennibarger-Developer-HLDPRO-${REPO_SLUG}/memory/MEMORY.md"
MEMORY_DIR_LINK="../../.claude/projects/-Users-bennibarger-Developer-HLDPRO-${REPO_SLUG}/memory/"
CLOSEOUT_DIR="${GOVERNANCE_ROOT}/raw/closeouts"
LATEST_POINTER_RE='^- \[Recent operator_context learnings\]\([^)]+\)\s*— .*\; grep operator_context for [^ ]+ to inspect$'

if [ ! -f "$MEMORY_PATH" ]; then
  echo "$SCRIPT_NAME: missing MEMORY.md at $MEMORY_PATH"
  exit 0
fi

get_file_epoch() {
  local file="$1"
  if stat -f '%m' "$file" >/dev/null 2>&1; then
    stat -f '%m' "$file"
    return 0
  fi
  if stat -c '%Y' "$file" >/dev/null 2>&1; then
    stat -c '%Y' "$file"
    return 0
  fi
  return 1
}

was_modified_since() {
  local file="$1"
  local ref_epoch="$2"
  local file_epoch
  if ! file_epoch="$(get_file_epoch "$file")"; then
    return 1
  fi
  [ "$file_epoch" -gt "$ref_epoch" ]
}

to_iso_timestamp() {
  local epoch="$1"
  local ts
  if ts="$(date -u -d "@${epoch}" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null)"; then
    printf '%s\n' "$ts"
    return 0
  fi
  if ts="$(date -u -r "${epoch}" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null)"; then
    printf '%s\n' "$ts"
    return 0
  fi
  return 1
}

TMP_BASE="$(mktemp)"
TMP_FILTER="$(mktemp)"
TMP_NEXT="$(mktemp)"
TMP_WORK="$(mktemp)"
trap 'rm -f "$TMP_BASE" "$TMP_FILTER" "$TMP_NEXT" "$TMP_WORK"' EXIT

LINE_COUNT="$(wc -l < "$MEMORY_PATH" | tr -d ' ')"
if [ "$LINE_COUNT" -gt 200 ]; then
  echo "warning: MEMORY.md has $LINE_COUNT lines, pruning to 200 for governance cap"
  head -n 200 "$MEMORY_PATH" > "$TMP_BASE"
else
  cat "$MEMORY_PATH" > "$TMP_BASE"
fi

if ! LAST_UPDATE_EPOCH="$(get_file_epoch "$MEMORY_PATH")"; then
  LAST_UPDATE_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  LAST_UPDATE_EPOCH="$(date -u +%s)"
else
  if ! LAST_UPDATE_TS="$(to_iso_timestamp "$LAST_UPDATE_EPOCH")"; then
    LAST_UPDATE_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    LAST_UPDATE_EPOCH="$(date -u +%s)"
  fi
fi
LAST_UPDATE_DAY="${LAST_UPDATE_TS%%T*}"

ENTRY_COUNT="0"
if [ -d "$CLOSEOUT_DIR" ]; then
  shopt -s nullglob
  for closeout_file in "$CLOSEOUT_DIR"/*.md; do
    if [ ! -f "$closeout_file" ]; then
      continue
    fi
    if [ "$(basename "$closeout_file")" = "TEMPLATE.md" ]; then
      continue
    fi
    if was_modified_since "$closeout_file" "$LAST_UPDATE_EPOCH"; then
      ENTRY_COUNT=$((ENTRY_COUNT + 1))
    fi
  done
  shopt -u nullglob
fi

if [ "$ENTRY_COUNT" -eq 0 ]; then
  cat "$TMP_BASE" > "$TMP_NEXT"
else
  grep -Ev "$LATEST_POINTER_RE" "$TMP_BASE" > "$TMP_FILTER" || true
  POINTER_LINE="- [Recent operator_context learnings](${MEMORY_DIR_LINK})  — ${ENTRY_COUNT} new entries since ${LAST_UPDATE_DAY}; grep operator_context for ${REPO_SLUG} to inspect"
  printf '%s\n' "$POINTER_LINE" > "$TMP_NEXT"
  if [ -s "$TMP_FILTER" ]; then
    cat "$TMP_FILTER" >> "$TMP_NEXT"
  fi
fi

UPDATED_LINES="$(wc -l < "$TMP_NEXT" | tr -d ' ')"
if [ "$UPDATED_LINES" -gt 200 ]; then
  echo "warning: consolidated MEMORY.md exceeds 200 lines, pruning to 200"
  head -n 200 "$TMP_NEXT" > "$TMP_WORK"
  mv "$TMP_WORK" "$TMP_NEXT"
fi

if cmp -s "$MEMORY_PATH" "$TMP_NEXT"; then
  echo "consolidate-memory: no changes for ${REPO_SLUG}"
  exit 0
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "consolidate-memory dry-run for ${REPO_SLUG}"
  echo "  target: $MEMORY_PATH"
  echo "  entry_count: $ENTRY_COUNT"
  if [ "$ENTRY_COUNT" -gt 0 ]; then
    echo "  would add/update pointer: [Recent operator_context learnings]"
  fi
  echo "  would write consolidated MEMORY.md"
  exit 0
fi

cat "$TMP_NEXT" > "$MEMORY_PATH"
echo "consolidate-memory: updated ${MEMORY_PATH}"
