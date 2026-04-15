#!/usr/bin/env bash
# scripts/windows-ollama/decide.sh — routing decision tree for Windows Ollama Tier-2 fallback
# Returns: LOCAL | WINDOWS | CLOUD | HALT
# Exit codes: 0 (success) or 1 (HALT — PII detected, cannot route)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PII_PATTERNS_FILE="${SCRIPT_DIR}/pii_patterns.yml"

# Default values
PII_FLAG="no"
PROMPT_TEXT=""
PROMPT_FILE=""
LOCAL_DAEMON_STATUS="down"
SPARK_HIGH_STATUS="unknown"
SPARK_MEDIUM_STATUS="unknown"
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
    --spark-high-status)
      SPARK_HIGH_STATUS="$2"
      shift 2
      ;;
    --spark-medium-status)
      SPARK_MEDIUM_STATUS="$2"
      shift 2
      ;;
    --codex-spark-high-status)
      SPARK_HIGH_STATUS="$2"
      shift 2
      ;;
    --codex-spark-medium-status)
      SPARK_MEDIUM_STATUS="$2"
      shift 2
      ;;
    --codex-spark-status)
      SPARK_HIGH_STATUS="$2"
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

# Helper: write fallback decision (enforced — script halts if logging fails)
log_fallback() {
  local fallback="$1"
  if ! bash scripts/model-fallback-log.sh \
    --tier 2 \
    --primary "gpt-5.3-codex-spark" \
    --fallback "$fallback" \
    --reason "auto" \
    --caller "decide.sh"; then
    echo "HALT"
    echo "decide: HALT (fallback_logging_failed, fallback=$fallback)" >&2
    exit 1
  fi
}

# Helper: check PII in text
check_pii() {
  local text="$1"
  local result

  if [[ -z "$text" ]]; then
    return 1
  fi

  if ! result="$(python3 - "$SCRIPT_DIR" "$PII_PATTERNS_FILE" "$text" <<'PY'
import sys

sys.path.insert(0, sys.argv[1])
from _pii import detect_pii, load_pii_patterns

pattern_file = sys.argv[2]
text = sys.argv[3]

try:
    patterns = load_pii_patterns(pattern_file)
except Exception as exc:
    raise SystemExit(f"pii_patterns_unavailable:{exc}")

match = detect_pii(text, patterns)
print(match if match else "NO_PII")
PY
)"; then
  return 2
fi

  if [[ "$result" == "NO_PII" ]]; then
    return 1
  fi

  echo "$result"
  return 0
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
if [[ "$PII_FLAG" == "yes" ]]; then
  echo "HALT"
  echo "decide: HALT (pii=yes, spark_high=$SPARK_HIGH_STATUS, spark_medium=$SPARK_MEDIUM_STATUS, local=$LOCAL_DAEMON_STATUS, win=$WINDOWS_STATUS)" >&2
  exit 1
fi

if [[ -n "$PROMPT_TO_CHECK" ]]; then
  pii_match=""
  if pii_match="$(check_pii "$PROMPT_TO_CHECK")"; then
    echo "HALT"
    echo "decide: HALT (pii=yes:$pii_match, spark_high=$SPARK_HIGH_STATUS, spark_medium=$SPARK_MEDIUM_STATUS, local=$LOCAL_DAEMON_STATUS, win=$WINDOWS_STATUS)" >&2
    exit 1
  else
    pii_check_code=$?
    if [[ "${pii_check_code}" -eq 2 ]]; then
      echo "HALT pii_patterns_unavailable"
      echo "decide: HALT (pii_patterns_unavailable, spark_high=$SPARK_HIGH_STATUS, spark_medium=$SPARK_MEDIUM_STATUS, local=$LOCAL_DAEMON_STATUS, win=$WINDOWS_STATUS)" >&2
      exit 1
    fi
  fi
fi

# 2. Spark primary (if ok, use cloud — skip the fallback ladder)
if [[ "$SPARK_HIGH_STATUS" == "ok" ]]; then
  echo "CLOUD"
  echo "decide: CLOUD (pii=no, spark=high, spark_medium=$SPARK_MEDIUM_STATUS, local=$LOCAL_DAEMON_STATUS, win=$WINDOWS_STATUS)" >&2
  exit 0
fi

# 3. Spark medium fallback
if [[ "$SPARK_MEDIUM_STATUS" == "ok" ]]; then
  echo "CLOUD"
  log_fallback "gpt-5.3-codex-spark@medium"
  echo "decide: CLOUD (pii=no, spark_high=$SPARK_HIGH_STATUS, spark_medium=ok, local=$LOCAL_DAEMON_STATUS, win=$WINDOWS_STATUS)" >&2
  exit 0
fi

# 4. Local warm daemon
if [[ "$LOCAL_DAEMON_STATUS" == "up" ]]; then
  echo "LOCAL"
  log_fallback "mlx-community/Qwen2.5-Coder-7B-Instruct-4bit"
  echo "decide: LOCAL (pii=no, spark_high=$SPARK_HIGH_STATUS, spark_medium=$SPARK_MEDIUM_STATUS, local=up, win=$WINDOWS_STATUS)" >&2
  exit 0
fi

# 5. Windows Ollama
if [[ "$WINDOWS_STATUS" == "ok" ]]; then
  echo "WINDOWS"
  log_fallback "qwen2.5-coder:7b"
  echo "decide: WINDOWS (pii=no, spark_high=$SPARK_HIGH_STATUS, spark_medium=$SPARK_MEDIUM_STATUS, local=$LOCAL_DAEMON_STATUS, win=ok)" >&2
  exit 0
fi

# 6. Cloud fallback (Sonnet cost-flagged)
echo "CLOUD"
log_fallback "claude-sonnet-4-6"
echo "decide: CLOUD (pii=no, spark_high=$SPARK_HIGH_STATUS, spark_medium=$SPARK_MEDIUM_STATUS, local=$LOCAL_DAEMON_STATUS, win=$WINDOWS_STATUS) [fallback]" >&2
exit 0
