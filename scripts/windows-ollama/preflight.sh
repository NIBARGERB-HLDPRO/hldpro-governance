#!/usr/bin/env bash
# preflight.sh — Windows Ollama LAN reachability + pinned model presence
#
# Exit codes:
#   0 — reachable and at least one pinned model present
#   1 — endpoint unreachable
#   2 — reachable but no pinned models present
#
# Doc: docs/runbooks/windows-ollama-worker.md

set -uo pipefail

ENDPOINT="${WINDOWS_OLLAMA_URL:-http://172.17.227.49:11434}"
TIMEOUT_SECONDS=5
PINNED_MODELS="qwen2.5-coder:7b llama3.1:8b"

if ! command -v curl >/dev/null 2>&1; then
  echo "preflight: curl required" >&2
  exit 2
fi

response="$(curl -sS --max-time "$TIMEOUT_SECONDS" "${ENDPOINT}/api/tags" 2>/dev/null)"
rc=$?
if [ $rc -ne 0 ] || [ -z "$response" ]; then
  echo "windows-ollama-preflight: UNREACHABLE endpoint=${ENDPOINT}"
  exit 1
fi

found_any=0
for model in $PINNED_MODELS; do
  if echo "$response" | grep -q "\"name\":\"${model}\""; then
    found_any=1
    break
  fi
done

if [ $found_any -eq 0 ]; then
  echo "windows-ollama-preflight: REACHABLE but NO PINNED MODELS endpoint=${ENDPOINT}"
  echo "  expected one of: $PINNED_MODELS"
  exit 2
fi

present=""
for model in $PINNED_MODELS; do
  if echo "$response" | grep -q "\"name\":\"${model}\""; then
    present="${present:+$present, }${model}"
  fi
done
echo "windows-ollama-preflight: OK endpoint=${ENDPOINT} pinned_present=[${present}]"
exit 0
