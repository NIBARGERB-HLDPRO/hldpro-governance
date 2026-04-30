#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
SCRIPT="${ROOT}/scripts/model-fallback-log.sh"
CHECKER="${ROOT}/.github/scripts/check_fallback_log_schema.py"

fail() {
  echo "[FAIL] $1" >&2
  exit 1
}

assert_contains() {
  needle="$1"
  file="$2"
  if ! grep -Fq -- "$needle" "$file"; then
    fail "expected '$needle' in $file"
  fi
}

assert_not_contains() {
  needle="$1"
  file="$2"
  if grep -Fq -- "$needle" "$file"; then
    fail "did not expect '$needle' in $file"
  fi
}

TMPDIR="$(mktemp -d)"
cleanup() {
  rm -rf "${TMPDIR}"
}
trap cleanup EXIT

export MODEL_FALLBACK_TARGET_DIR="${TMPDIR}/raw/model-fallbacks"
export MODEL_FALLBACK_DATE="2026-04-30"
export MODEL_FALLBACK_SESSION_ID="session-abc123"
TARGET_FILE="${MODEL_FALLBACK_TARGET_DIR}/${MODEL_FALLBACK_DATE}.md"

bash "${SCRIPT}" \
  --tier 1 \
  --primary gpt-5.4 \
  --fallback gpt-5.3-codex-spark \
  --reason "gpt-5.4 unavailable; Spark used for same-family specialist critique" \
  --caller scripts/codex-review.sh

assert_contains "reason: gpt-5.4 unavailable; Spark used for same-family specialist critique" "${TARGET_FILE}"
assert_not_contains "fallback_scope:" "${TARGET_FILE}"

bash "${SCRIPT}" \
  --tier 1 \
  --primary gpt-5.4 \
  --fallback gpt-5.3-codex-spark \
  --reason "gpt-5.4 unavailable; Spark used for same-family specialist critique" \
  --caller scripts/codex-review.sh \
  --fallback-scope alternate_model_review \
  --cross-family-path-unavailable \
  --cross-family-path-ref docs/codex-reviews/2026-04-30-issue-629-claude.md

assert_contains "fallback_scope: alternate_model_review" "${TARGET_FILE}"
assert_contains "cross_family_path_unavailable: true" "${TARGET_FILE}"
assert_contains "cross_family_path_ref: docs/codex-reviews/2026-04-30-issue-629-claude.md" "${TARGET_FILE}"

COUNT="$(grep -c '^---$' "${TARGET_FILE}")"
[ "${COUNT}" -ge 4 ] || fail "expected appended multi-block frontmatter separators"

if bash "${SCRIPT}" \
  --tier 1 \
  --primary gpt-5.4 \
  --fallback gpt-5.3-codex-spark \
  --reason "specific reason" \
  --caller scripts/codex-review.sh \
  --fallback-scope alternate_model_review; then
  fail "degraded invocation without cross-family path ref should fail"
fi

if bash "${SCRIPT}" \
  --tier 1 \
  --primary gpt-5.4 \
  --fallback gpt-5.3-codex-spark \
  --reason "specific reason" \
  --caller scripts/codex-review.sh \
  --fallback-scope unknown \
  --cross-family-path-unavailable \
  --cross-family-path-ref docs/codex-reviews/2026-04-30-issue-629-claude.md; then
  fail "unknown fallback scope should fail"
fi

REPO="${TMPDIR}/repo"
mkdir -p "${REPO}"
cd "${REPO}"
git init >/dev/null 2>&1
git config user.email tests@example.com
git config user.name Tests
printf 'repo\n' > README.md
git add README.md
git commit -m base >/dev/null 2>&1
BASE_SHA="$(git rev-parse HEAD)"
mkdir -p raw/model-fallbacks
cp "${TARGET_FILE}" raw/model-fallbacks/2026-04-30.md
git add raw/model-fallbacks/2026-04-30.md
git commit -m fallback >/dev/null 2>&1
HEAD_SHA="$(git rev-parse HEAD)"
BASE_SHA="${BASE_SHA}" HEAD_SHA="${HEAD_SHA}" python3 "${CHECKER}"

echo "[PASS] model fallback log contract checks passed"
