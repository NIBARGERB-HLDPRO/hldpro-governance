#!/bin/sh
set -eu

TARGET_DIR="raw/model-fallbacks"
TARGET_FILE="${TARGET_DIR}/$(date +%F).md"
DATE="$(date +%F)"
SESSION_ID=""
TIER=""
PRIMARY=""
FALLBACK=""
REASON=""
CALLER=""

usage() {
  echo "Usage: $0 --tier <int> --primary <model> --fallback <model> --reason <str> --caller <str>"
  exit 1
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --tier)
      shift
      TIER="$1"
      ;;
    --primary)
      shift
      PRIMARY="$1"
      ;;
    --fallback)
      shift
      FALLBACK="$1"
      ;;
    --reason)
      shift
      REASON="$1"
      ;;
    --caller)
      shift
      CALLER="$1"
      ;;
    *)
      usage
      ;;
  esac
  shift
done

if [ -z "${TIER}" ] || [ -z "${PRIMARY}" ] || [ -z "${FALLBACK}" ] || [ -z "${REASON}" ] || [ -z "${CALLER}" ]; then
  usage
fi

mkdir -p "${TARGET_DIR}"

if command -v uuidgen >/dev/null 2>&1; then
  SESSION_ID="$(uuidgen)"
else
  SESSION_ID="$(date +%s)$RANDOM"
fi

if [ -s "${TARGET_FILE}" ]; then
  printf '\n' >> "${TARGET_FILE}"
fi

cat <<EOF >> "${TARGET_FILE}"
---
date: ${DATE}
session_id: ${SESSION_ID}
tier: ${TIER}
primary_model: ${PRIMARY}
fallback_model: ${FALLBACK}
reason: ${REASON}
caller_script: ${CALLER}
---
EOF
