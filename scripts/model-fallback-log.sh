#!/bin/sh
set -eu

TARGET_DIR="${MODEL_FALLBACK_TARGET_DIR:-raw/model-fallbacks}"
DATE="${MODEL_FALLBACK_DATE:-$(date +%F)}"
TARGET_FILE="${TARGET_DIR}/${DATE}.md"
SESSION_ID=""
TIER=""
PRIMARY=""
FALLBACK=""
REASON=""
CALLER=""
FALLBACK_SCOPE=""
CROSS_FAMILY_PATH_UNAVAILABLE=0
CROSS_FAMILY_PATH_REF=""

usage() {
  echo "Usage: $0 --tier <int> --primary <model> --fallback <model> --reason <str> --caller <str> [--fallback-scope alternate_model_review --cross-family-path-unavailable --cross-family-path-ref <repo-ref>]"
  exit 1
}

is_placeholder() {
  case "$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')" in
    todo|tbd|n/a|na|placeholder)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
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
    --fallback-scope)
      shift
      FALLBACK_SCOPE="$1"
      ;;
    --cross-family-path-unavailable)
      CROSS_FAMILY_PATH_UNAVAILABLE=1
      ;;
    --cross-family-path-ref)
      shift
      CROSS_FAMILY_PATH_REF="$1"
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

if is_placeholder "${REASON}"; then
  echo "reason must not use placeholder text" >&2
  exit 1
fi

if [ -n "${FALLBACK_SCOPE}" ]; then
  if [ "${FALLBACK_SCOPE}" != "alternate_model_review" ]; then
    echo "fallback_scope must be alternate_model_review when present" >&2
    exit 1
  fi
  if [ "${CROSS_FAMILY_PATH_UNAVAILABLE}" -ne 1 ]; then
    echo "alternate_model_review fallback requires --cross-family-path-unavailable" >&2
    exit 1
  fi
  if [ -z "${CROSS_FAMILY_PATH_REF}" ]; then
    echo "alternate_model_review fallback requires --cross-family-path-ref" >&2
    exit 1
  fi
  if is_placeholder "${CROSS_FAMILY_PATH_REF}"; then
    echo "cross-family-path-ref must not use placeholder text" >&2
    exit 1
  fi
  case "$(printf '%s' "${REASON}" | tr '[:upper:]' '[:lower:]')" in
    other|auto|no_fallback_required)
      echo "alternate_model_review fallback reason must be specific, not generic" >&2
      exit 1
      ;;
  esac
elif [ "${CROSS_FAMILY_PATH_UNAVAILABLE}" -eq 1 ] || [ -n "${CROSS_FAMILY_PATH_REF}" ]; then
  echo "cross-family fallback flags require --fallback-scope alternate_model_review" >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"

if [ -n "${MODEL_FALLBACK_SESSION_ID:-}" ]; then
  SESSION_ID="${MODEL_FALLBACK_SESSION_ID}"
elif command -v uuidgen >/dev/null 2>&1; then
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
EOF

if [ -n "${FALLBACK_SCOPE}" ]; then
  cat <<EOF >> "${TARGET_FILE}"
fallback_scope: ${FALLBACK_SCOPE}
cross_family_path_unavailable: true
cross_family_path_ref: ${CROSS_FAMILY_PATH_REF}
EOF
fi

cat <<EOF >> "${TARGET_FILE}"
---
EOF
