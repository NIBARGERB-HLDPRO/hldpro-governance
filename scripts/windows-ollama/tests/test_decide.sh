#!/usr/bin/env bash
# scripts/windows-ollama/tests/test_decide.sh — 13 decision state tests for decide.sh

set -uo pipefail

FAILED=0
PASSED=0
PII_PATTERN_FILE="scripts/windows-ollama/pii_patterns.yml"
PII_PATTERN_BACKUP="$(mktemp)"
cp "$PII_PATTERN_FILE" "$PII_PATTERN_BACKUP"

restore_patterns() {
  cp "$PII_PATTERN_BACKUP" "$PII_PATTERN_FILE"
}
cleanup() {
  restore_patterns
  rm -f "$PII_PATTERN_BACKUP"
}
trap cleanup EXIT

# Helper: run a test case
test_case() {
  local name="$1"
  local expected="$2"
  local pii_flag="$3"
  local local_status="$4"
  local windows_status="$5"
  local spark_high_status="$6"
  local spark_medium_status="$7"
  local prompt="$8"

  local actual exit_code
  actual=$(bash scripts/windows-ollama/decide.sh \
    --pii-flag "$pii_flag" \
    --prompt-text "$prompt" \
    --local-warm-daemon-status "$local_status" \
    --spark-high-status "$spark_high_status" \
    --spark-medium-status "$spark_medium_status" \
    --windows-status "$windows_status" 2>/dev/null) || exit_code=$?
  exit_code=${exit_code:-0}

  if [[ "$expected" == "HALT" ]]; then
    if [[ $exit_code -eq 1 && "$actual" == HALT* ]]; then
      echo "✓ PASS: $name (exit 1, output: $actual)"
      ((PASSED++))
    else
      echo "✗ FAIL: $name (expected HALT, got '$actual' exit $exit_code)"
      ((FAILED++))
    fi
  else
    if [[ "$actual" == "$expected" && $exit_code -eq 0 ]]; then
      echo "✓ PASS: $name (output: $actual, exit 0)"
      ((PASSED++))
    else
      echo "✗ FAIL: $name (expected '$expected' exit 0, got '$actual' exit $exit_code)"
      ((FAILED++))
    fi
  fi
}

set_pattern_file_missing() {
  rm -f "$PII_PATTERN_FILE"
}

set_pattern_file_malformed() {
  cat > "$PII_PATTERN_FILE" <<'EOF'
patterns:
  email:
    regex: "(unclosed
EOF
}

echo "=== Test Suite: decide.sh decision tree ==="
echo ""

# Test 1: PII-yes + spark-high ok → HALT
test_case "PII-yes + spark-high-ok → HALT" "HALT" "yes" "down" "unreachable" "ok" "blocked" "def foo(): pass"

# Test 2: PII no (email pattern) + spark-high ok → HALT
test_case "PII-no email + spark-high-ok → HALT" "HALT" "no" "down" "unreachable" "ok" "blocked" "jane@example.com"

# Test 3: PII no (SSN pattern) + spark-high ok → HALT
test_case "PII-no ssn + spark-high-ok → HALT" "HALT" "no" "down" "unreachable" "ok" "blocked" "SSN: 123-45-6789"

# Test 4: PII no (phone pattern) + spark-high ok → HALT
test_case "PII-no phone + spark-high-ok → HALT" "HALT" "no" "down" "unreachable" "ok" "blocked" "555-555-5555"

# Test 5: PII-yes with all routes up -> HALT
test_case "PII-yes + all-up → HALT" "HALT" "yes" "up" "ok" "ok" "ok" "def foo(): pass"

# Test 6: PII-no + spark-high blocked + spark-medium ok → CLOUD (medium)
test_case "PII-no + spark-high-blocked + spark-medium-ok → CLOUD" "CLOUD" "no" "down" "unreachable" "blocked" "ok" "def foo(): pass"

# Test 7: PII-no + missing pii_patterns.yml → HALT
restore_patterns
set_pattern_file_missing
test_case "PII-no + missing pii_patterns.yml → HALT" "HALT" "no" "down" "unreachable" "blocked" "blocked" "no pii here"
restore_patterns

# Test 8: PII-no + malformed pii_patterns.yml → HALT
set_pattern_file_malformed
test_case "PII-no + malformed pii_patterns.yml → HALT" "HALT" "no" "down" "unreachable" "blocked" "blocked" "no pii here"
restore_patterns

# Test 9: PII-no + spark-high blocked + local-up → LOCAL
test_case "PII-no + spark-high-blocked + local-up → LOCAL" "LOCAL" "no" "up" "unreachable" "blocked" "blocked" "def foo(): pass"

# Test 10: PII-no + spark-high blocked + local-down + windows-ok → WINDOWS
test_case "PII-no + spark-high-blocked + local-down + windows-ok → WINDOWS" "WINDOWS" "no" "down" "ok" "blocked" "blocked" "def foo(): pass"

# Test 11: PII-no + spark-high blocked + local-down + windows-down → CLOUD
test_case "PII-no + spark-high-blocked + local-down + windows-down → CLOUD" "CLOUD" "no" "down" "unreachable" "blocked" "blocked" "def foo(): pass"

# Test 12: PII-no + empty prompt → LOCAL
test_case "PII-no + empty prompt → LOCAL" "LOCAL" "no" "up" "unreachable" "blocked" "blocked" ""

# Test 13: PII-no + spark-unknown + windows-ok → WINDOWS
test_case "PII-no + spark-unknown + windows-ok → WINDOWS" "WINDOWS" "no" "down" "ok" "unknown" "blocked" "def foo(): pass"

echo ""
echo "=== Summary ==="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [[ $FAILED -eq 0 ]]; then
  echo "All tests passed!"
  exit 0
else
  echo "Some tests failed!"
  exit 1
fi
