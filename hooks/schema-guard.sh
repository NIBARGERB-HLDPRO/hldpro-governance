#!/bin/bash
# schema-guard.sh - PreToolUse:Bash guard with explicit diagnostics.
# Claude Code hook contract: exit 0 = allow, exit 2 = hard block.

set -Euo pipefail

HOOK_NAME="schema-guard"
phase="startup"

fail() {
  local message="$1"
  local code="${2:-2}"
  trap - ERR
  printf '%s: %s\n' "$HOOK_NAME" "$message" >&2
  exit "$code"
}

trap 'rc=$?; printf "%s: INTERNAL: unexpected error at line %s during %s while running: %s\n" "$HOOK_NAME" "$LINENO" "$phase" "$BASH_COMMAND" >&2; exit "$rc"' ERR

phase="read hook payload"
input="$(cat 2>/dev/null || true)"
if [ -z "$input" ]; then
  exit 0
fi

phase="parse hook payload"
parsed="$(
  printf '%s' "$input" | python3 -c '
import json
import sys

try:
    data = json.load(sys.stdin)
except Exception as exc:
    print(json.dumps({"error": f"malformed input payload: {exc}"}))
    raise SystemExit(0)

tool_name = str(data.get("tool_name") or data.get("tool") or "")
tool_input = data.get("tool_input") if isinstance(data.get("tool_input"), dict) else {}
command = str(tool_input.get("command") or "")
print(json.dumps({"tool_name": tool_name, "command": command}))
'
)"
parse_error="$(printf '%s' "$parsed" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("error",""))' 2>/dev/null || true)"
if [ -n "$parse_error" ]; then
  fail "FAIL: ${parse_error}"
fi

tool_name="$(printf '%s' "$parsed" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_name",""))')"
command_text="$(printf '%s' "$parsed" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("command",""))')"

if [ "$tool_name" != "Bash" ]; then
  exit 0
fi

phase="resolve repository root"
repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

phase="validate required schema"
if [ -n "${SCHEMA_GUARD_REQUIRED_SCHEMA:-}" ]; then
  schema_path="$SCHEMA_GUARD_REQUIRED_SCHEMA"
  case "$schema_path" in
    /*) resolved_schema="$schema_path" ;;
    *) resolved_schema="$repo_root/$schema_path" ;;
  esac
  if [ ! -f "$resolved_schema" ]; then
    fail "FAIL: missing schema ${SCHEMA_GUARD_REQUIRED_SCHEMA}"
  fi
fi

phase="run configured validator"
if [ -n "${SCHEMA_GUARD_VALIDATOR:-}" ]; then
  validator_output="$("$SCHEMA_GUARD_VALIDATOR" 2>&1)" || {
    validator_status=$?
    first_line="$(printf '%s\n' "$validator_output" | sed -n '1p')"
    fail "FAIL: validation failed while running ${SCHEMA_GUARD_VALIDATOR} (exit ${validator_status}): ${first_line}"
  }
fi

phase="detect Bash file writes"
write_target="$(
  python3 - "$command_text" <<'PY'
import re
import sys

command = sys.argv[1]
patterns = [
    r"(?<![0-9])>>?\s*([\"']?)([^\\s;&|]+)\1",
    r"\bcat\b[^;&|]*\s>>?\s*([\"']?)([^\\s;&|]+)\1",
    r"\btee\b(?:\s+-[A-Za-z]+)*\s+([\"']?)([^\\s;&|]+)\1",
    r"\b(?:python|python3)\b.*(?:open\(|write_text\()",
]
for pattern in patterns:
    match = re.search(pattern, command, flags=re.S)
    if not match:
        continue
    if "open\\(" in pattern or "write_text" in pattern:
        print("<python file write>")
    else:
        print(match.group(2))
    break
PY
)"

if [ -n "$write_target" ]; then
  fail "BLOCKED: Bash file write detected for ${write_target}; rule: SoM write-boundary. Next action: use the approved edit/Worker handoff path with issue-backed execution scope and accepted handoff evidence."
fi

exit 0
