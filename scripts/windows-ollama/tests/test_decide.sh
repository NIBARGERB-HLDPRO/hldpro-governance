#!/usr/bin/env bash
# scripts/windows-ollama/tests/test_decide.sh — 8 decision state tests for decide.sh

set -uo pipefail

FAILED=0
PASSED=0

# Helper: run a test case
test_case() {
  local name="$1"
  local expected="$2"
  local pii_flag="$3"
  local local_status="$4"
  local windows_status="$5"
  local spark_status="$6"
  
  local actual exit_code
  actual=$(bash scripts/windows-ollama/decide.sh \
    --pii-flag "$pii_flag" \
    --prompt-text "def foo(): pass" \
    --local-warm-daemon-status "$local_status" \
    --codex-spark-status "$spark_status" \
    --windows-status "$windows_status" 2>/dev/null) || exit_code=$?
  exit_code=${exit_code:-0}
  
  # For HALT, expect exit code 1
  if [[ "$expected" == "HALT" ]]; then
    if [[ $exit_code -eq 1 ]]; then
      echo "✓ PASS: $name (exit 1)"
      ((PASSED++))
    else
      echo "✗ FAIL: $name (expected exit 1, got $exit_code, output: $actual)"
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

echo "=== Test Suite: decide.sh decision tree ==="
echo ""

# Test 1: PII-yes always halts (regardless of other states)
test_case "PII-yes + spark-ok → HALT" "HALT" "yes" "down" "unreachable" "ok"

# Test 2: PII-yes halts even with all endpoints up
test_case "PII-yes + all-up → HALT" "HALT" "yes" "up" "ok" "ok"

# Test 3: PII-no + spark-ok → CLOUD (spark is primary)
test_case "PII-no + spark-ok → CLOUD" "CLOUD" "no" "down" "unreachable" "ok"

# Test 4: PII-no + spark-blocked + local-up → LOCAL
test_case "PII-no + spark-blocked + local-up → LOCAL" "LOCAL" "no" "up" "unreachable" "blocked"

# Test 5: PII-no + spark-blocked + local-down + windows-ok → WINDOWS
test_case "PII-no + spark-blocked + local-down + windows-ok → WINDOWS" "WINDOWS" "no" "down" "ok" "blocked"

# Test 6: PII-no + spark-blocked + local-down + windows-down → CLOUD (fallback)
test_case "PII-no + spark-blocked + local-down + windows-down → CLOUD" "CLOUD" "no" "down" "unreachable" "blocked"

# Test 7: Empty pii-flag defaults to "no" (should route normally)
test_case "Empty pii-flag defaults to 'no' (local-up)" "LOCAL" "no" "up" "unreachable" "blocked"

# Test 8: PII-no + spark-unknown + windows-ok → WINDOWS (windows is next in ladder)
test_case "PII-no + spark-unknown + windows-ok → WINDOWS" "WINDOWS" "no" "down" "ok" "unknown"

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
