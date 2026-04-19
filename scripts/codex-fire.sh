#!/usr/bin/env bash
# Fail-fast wrapper for dispatcher-owned Codex brief execution.
#
# Usage:
#   bash scripts/codex-fire.sh -m <model> -e <effort> -w <worktree> -b <brief-file> [-- <codex exec args>]

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_FILE="${CODEX_FIRE_LOG:-$REPO_ROOT/raw/fail-fast-log.md}"
PREFLIGHT_TIMEOUT_SECONDS="${CODEX_FIRE_TIMEOUT_SECONDS:-5}"

MODEL=""
EFFORT=""
WORKTREE=""
BRIEF=""
PASSTHRU=()

usage() {
  sed -n '2,7p' "$0" | sed 's/^# \{0,1\}//'
}

fail_usage() {
  echo "codex-fire: $1" >&2
  usage >&2
  exit 2
}

escape_cell() {
  local value="$1"
  value="${value//$'\n'/ }"
  value="${value//$'\r'/ }"
  value="${value//|/\\|}"
  printf '%s' "$value"
}

ensure_log() {
  local dir
  dir="$(dirname "$LOG_FILE")"
  mkdir -p "$dir"
  if [ ! -f "$LOG_FILE" ]; then
    {
      echo "# Codex Fire Fail-Fast Log"
      echo ""
      echo "| Timestamp | Surface | Model | Error | Brief |"
      echo "|---|---|---|---|---|"
    } >"$LOG_FILE"
  fi
}

append_failure() {
  local error_msg="$1"
  local timestamp
  timestamp="$(date '+%Y-%m-%d %H:%M')"
  ensure_log
  printf '| %s | codex-exec | %s | %s | %s |\n' \
    "$timestamp" \
    "$(escape_cell "$MODEL")" \
    "$(escape_cell "$error_msg")" \
    "$(escape_cell "$BRIEF")" >>"$LOG_FILE"
}

emit_fail() {
  printf 'CODEX_FAIL: model=%s exit=1 brief=%s — dispatcher must retry or escalate\n' \
    "$MODEL" "$BRIEF"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    -m|--model)
      [ "$#" -ge 2 ] || fail_usage "$1 requires a value"
      MODEL="$2"
      shift 2
      ;;
    -e|--effort)
      [ "$#" -ge 2 ] || fail_usage "$1 requires a value"
      EFFORT="$2"
      shift 2
      ;;
    -w|--worktree)
      [ "$#" -ge 2 ] || fail_usage "$1 requires a value"
      WORKTREE="$2"
      shift 2
      ;;
    -b|--brief)
      [ "$#" -ge 2 ] || fail_usage "$1 requires a value"
      BRIEF="$2"
      shift 2
      ;;
    --)
      shift
      PASSTHRU=("$@")
      break
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail_usage "unknown argument: $1"
      ;;
  esac
done

[ -n "$MODEL" ] || fail_usage "missing -m/--model"
[ -n "$EFFORT" ] || fail_usage "missing -e/--effort"
[ -n "$WORKTREE" ] || fail_usage "missing -w/--worktree"
[ -n "$BRIEF" ] || fail_usage "missing -b/--brief"
[ -d "$WORKTREE" ] || fail_usage "worktree does not exist: $WORKTREE"
[ -f "$BRIEF" ] || fail_usage "brief file does not exist: $BRIEF"

if ! command -v python3 >/dev/null 2>&1; then
  append_failure "python3 not found on PATH"
  emit_fail
  exit 1
fi

preflight_output="$(
  python3 - "$MODEL" "$WORKTREE" "$PREFLIGHT_TIMEOUT_SECONDS" <<'PY'
import subprocess
import sys

model, worktree, timeout_text = sys.argv[1:4]
try:
    timeout_seconds = float(timeout_text)
except ValueError:
    timeout_seconds = 5.0

cmd = [
    "codex",
    "exec",
    "-C",
    worktree,
    "--sandbox",
    "read-only",
    "--skip-git-repo-check",
    "-m",
    model,
    "-c",
    "model_reasoning_effort=low",
    "--color",
    "never",
    "--",
    "-",
]

try:
    result = subprocess.run(
        cmd,
        input="Return exactly: ok\n",
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
except subprocess.TimeoutExpired:
    print(f"preflight timed out after {timeout_seconds:g}s")
    raise SystemExit(124)
except FileNotFoundError:
    print("codex CLI not found on PATH")
    raise SystemExit(127)

output = "\n".join(part for part in [result.stderr.strip(), result.stdout.strip()] if part).strip()
if result.returncode != 0:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    print(lines[-1] if lines else f"codex preflight failed with exit {result.returncode}")
raise SystemExit(result.returncode)
PY
)"
preflight_rc=$?

if [ "$preflight_rc" -ne 0 ]; then
  message="${preflight_output:-codex preflight failed with exit $preflight_rc}"
  append_failure "preflight failed: $message"
  emit_fail
  exit 1
fi

run_output="$(mktemp "${TMPDIR:-/tmp}/codex-fire-output.XXXXXX")"
cmd=(codex exec -C "$WORKTREE" -m "$MODEL" -c "model_reasoning_effort=${EFFORT}")
if [ "${#PASSTHRU[@]}" -gt 0 ]; then
  cmd+=("${PASSTHRU[@]}")
fi
cmd+=(-- -)

"${cmd[@]}" <"$BRIEF" >"$run_output" 2>&1
run_rc=$?

if [ -s "$run_output" ]; then
  cat "$run_output"
fi

if [ "$run_rc" -ne 0 ]; then
  error_msg="$(tail -20 "$run_output" | awk 'NF { line=$0 } END { print line }')"
  append_failure "exec failed: ${error_msg:-codex exec failed with exit $run_rc}"
  rm -f "$run_output"
  emit_fail
  exit 1
fi

rm -f "$run_output"
