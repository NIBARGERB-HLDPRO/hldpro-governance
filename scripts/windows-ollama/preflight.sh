#!/usr/bin/env bash
# preflight.sh — Windows Ollama LAN reachability + pinned model presence
#
# Modes:
#   --worker  — verify qwen2.5-coder:7b (SoM Tier-2 Worker role)
#   --critic  — verify llama3.1:8b (HP critic role)
#
# Exit codes:
#   0 — endpoint reachable and required model present
#   1 — endpoint unreachable
#   2 — reachable but required model not present
#
# Doc: docs/runbooks/windows-ollama-worker.md

set -uo pipefail

ENDPOINT="${WINDOWS_OLLAMA_URL:-http://172.17.227.49:11434}"
TIMEOUT_SECONDS=5
MODE="${1:---worker}"

case "$MODE" in
  --worker)
    REQUIRED_MODEL="qwen2.5-coder:7b"
    ROLE="SoM Tier-2 Worker"
    ;;
  --critic)
    REQUIRED_MODEL="llama3.1:8b"
    ROLE="HP critic"
    ;;
  *)
    echo "preflight: usage: $0 [--worker|--critic]" >&2
    exit 2
    ;;
esac

if ! command -v curl >/dev/null 2>&1; then
  echo "preflight: curl required" >&2
  exit 2
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "preflight: jq required" >&2
  exit 2
fi

response="$(curl -sS --max-time "$TIMEOUT_SECONDS" "${ENDPOINT}/api/tags" 2>/dev/null)"
rc=$?
if [ $rc -ne 0 ] || [ -z "$response" ]; then
  echo "windows-ollama-preflight[$MODE]: UNREACHABLE endpoint=${ENDPOINT}"
  exit 1
fi

# Parse /api/tags JSON and check for required model
if echo "$response" | jq -e ".models[] | select(.name == \"${REQUIRED_MODEL}\")" >/dev/null 2>&1; then
  echo "windows-ollama-preflight[$MODE]: OK role=${ROLE} endpoint=${ENDPOINT} model_present=${REQUIRED_MODEL}"
  exit 0
else
  echo "windows-ollama-preflight[$MODE]: REACHABLE but REQUIRED MODEL MISSING role=${ROLE} endpoint=${ENDPOINT} required_model=${REQUIRED_MODEL}"
  exit 2
fi
