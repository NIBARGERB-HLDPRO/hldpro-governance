#!/usr/bin/env bash
# Usage: audit_remote.sh <repo> <path> [ref] (default ref=main)
# Fetches repos/NIBARGERB-HLDPRO/<repo>/contents/<path>?ref=<ref> via gh api.
# Decodes the `.content` field with base64 -d and prints to stdout.
# Exit 1: repository/path/ref not found.
# Exit 2: any other fetch/decode failure.
set -eu -o pipefail

repo=${1:?Usage: audit_remote.sh <repo> <path> [ref]}
path=$2
ref=${3:-main}

if ! api_resp=$(gh api "repos/NIBARGERB-HLDPRO/${repo}/contents/${path}?ref=${ref}" 2>&1); then
  if printf '%s' "$api_resp" | grep -qE '"status":\s*404|"Not Found"|404'; then
    echo "{\"error\":\"not-found\",\"repo\":\"${repo}\",\"path\":\"${path}\",\"ref\":\"${ref}\"}" >&2
    exit 1
  fi
  detail=$(printf '%s' "$api_resp" | tr '\n' ' ' | cut -c1-180)
  echo "{\"error\":\"fetch-failed\",\"detail\":\"${detail}\"}" >&2
  exit 2
fi

encoded=$(printf '%s' "$api_resp" | sed -n 's/.*"content":[[:space:]]*"\([^"]*\)".*/\1/p')
if [ -z "$encoded" ]; then
  echo '{"error":"fetch-failed","detail":"missing content field"}' >&2
  exit 2
fi
printf '%b' "$encoded" | base64 -d
