#!/usr/bin/env bash
# scripts/windows-ollama/decide.sh — routing decision tree for Windows Ollama Tier-2 fallback
# Returns: LOCAL | WINDOWS | CLOUD | HALT
# Exit codes: 0 (success) or 1 (HALT — PII detected, cannot route)

set -uo pipefail

# Default values
PII_FLAG="no"
PROMPT_TEXT=""
PROMPT_FILE=""
LOCAL_DAEMON_STATUS="down"
CODEX_SPARK_STATUS="unknown"
WINDOWS_STATUS="unreachable"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --pii-flag)
      PII_FLAG="$2"
      shift 2
      ;;
    --prompt-text)
      PROMPT_TEXT="$2"
      shift 2
      ;;
    --prompt-file)
      PROMPT_FILE="$2"
      shift 2
      ;;
    --local-warm-daemon-status)
      LOCAL_DAEMON_STATUS="$2"
      shift 2
      ;;
    --codex-spark-status)
      CODEX_SPARK_STATUS="$2"
      shift 2
      ;;
    --windows-status)
      WINDOWS_STATUS="$2"
      shift 2
      ;;
    *)
      echo "Unknown flag: $1" >&2
      exit 1
      ;;
  esac
done

# Helper: check PII in text
check_pii() {
  local text="$1"
  local patterns_file="scripts/windows-ollama/pii_patterns.yml"
  
  # If pii_patterns.yml exists, parse patterns (simple yaml grep for now)
  if [[ -f "$patterns_file" ]]; then
    # Extract pattern values from yaml (lines starting with '- ')
    while IFS= read -r pattern; do
      if [[ -n "$pattern" ]] && [[ "$text" =~ $pattern ]]; then
        return 0  # PII found
      fi
    done < <(grep "^  - " "$patterns_file" | sed 's/^  - //' | sed "s/'//g" | sed 's/"//g')
  fi
  
  return 1  # No PII found
}

# Get prompt text for inline PII check
PROMPT_TO_CHECK=""
if [[ -n "$PROMPT_TEXT" ]]; then
  PROMPT_TO_CHECK="$PROMPT_TEXT"
elif [[ -n "$PROMPT_FILE" && -f "$PROMPT_FILE" ]]; then
  PROMPT_TO_CHECK="$(cat "$PROMPT_FILE")"
fi

# Decision tree (order matters: PII halts first)

# 1. PII floor: explicit flag or inline detection
if [[ "$PII_FLAG" == "yes" ]] || (check_pii "$PROMPT_TO_CHECK"); then
  echo "HALT" 
  echo "decide: HALT (pii=yes, spark=$CODEX_SPARK_STATUS, local=$LOCAL_DAEMON_STATUS, win=$WINDOWS_STATUS)" >&2
  exit 1
fi

# 2. Spark primary (if ok, use cloud — skip the fallback ladder)
if [[ "$CODEX_SPARK_STATUS" == "ok" ]]; then
  echo "CLOUD"
  echo "decide: CLOUD (pii=no, spark=ok, local=$LOCAL_DAEMON_STATUS, win=$WINDOWS_STATUS)" >&2
  exit 0
fi

# 3. Local warm daemon
if [[ "$LOCAL_DAEMON_STATUS" == "up" ]]; then
  echo "LOCAL"
  echo "decide: LOCAL (pii=no, spark=$CODEX_SPARK_STATUS, local=up, win=$WINDOWS_STATUS)" >&2
  exit 0
fi

# 4. Windows Ollama
if [[ "$WINDOWS_STATUS" == "ok" ]]; then
  echo "WINDOWS"
  echo "decide: WINDOWS (pii=no, spark=$CODEX_SPARK_STATUS, local=$LOCAL_DAEMON_STATUS, win=ok)" >&2
  exit 0
fi

# 5. Cloud fallback (Sonnet cost-flagged)
echo "CLOUD"
echo "decide: CLOUD (pii=no, spark=$CODEX_SPARK_STATUS, local=$LOCAL_DAEMON_STATUS, win=$WINDOWS_STATUS) [fallback]" >&2
exit 0
