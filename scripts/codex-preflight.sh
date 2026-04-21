#!/usr/bin/env bash
# codex-preflight.sh — verify codex-spark availability before fallback/specialist critique.
#
# Exit codes:
#   0 — spark available (probe returned ok, or quota logs show primary < 100%)
#   1 — spark blocked (usage limit hit; primary window 100%)
#   2 — codex CLI missing or misconfigured
#
# Output: one-line status with limit_id, used %, and local resets_at.
#
# Usage:
#   bash scripts/codex-preflight.sh             # log-check first, probe if logs say OK
#   bash scripts/codex-preflight.sh --probe     # live probe only (costs one call)
#   bash scripts/codex-preflight.sh --log       # log-check only (no API call)
#
# Doc: docs/EXTERNAL_SERVICES_RUNBOOK.md §1 Codex CLI

set -uo pipefail

MODE="${1:-both}"

if ! command -v codex >/dev/null 2>&1; then
  echo "codex-preflight: codex CLI not found on PATH" >&2
  exit 2
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "codex-preflight: python3 required" >&2
  exit 2
fi

check_log() {
  python3 - <<'PY'
import datetime, glob, json, os, sys

SPARK_LIMIT_ID = "codex_bengalfox"
today = datetime.datetime.now().strftime("%Y/%m/%d")
session_dir = os.path.expanduser(f"~/.codex/sessions/{today}")

if not os.path.isdir(session_dir):
    print(f"codex-preflight[log]: no sessions dir at {session_dir}")
    sys.exit(2)

latest = None
for path in sorted(glob.glob(os.path.join(session_dir, "*.jsonl"))):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                if SPARK_LIMIT_ID not in line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                rl = obj.get("payload", {}).get("rate_limits") or {}
                if rl.get("limit_id") == SPARK_LIMIT_ID:
                    latest = (obj.get("timestamp", ""), rl)
    except OSError:
        continue

if latest is None:
    print("codex-preflight[log]: no spark quota snapshot in today's logs")
    sys.exit(2)

ts, rl = latest
primary = rl.get("primary") or {}
secondary = rl.get("secondary") or {}
p_used = primary.get("used_percent") or 0
s_used = secondary.get("used_percent") or 0
p_reset = primary.get("resets_at") or 0
s_reset = secondary.get("resets_at") or 0

def fmt(epoch):
    if not epoch:
        return "n/a"
    return datetime.datetime.fromtimestamp(epoch).strftime("%Y-%m-%d %H:%M %Z").strip()

blocked = p_used >= 100 or s_used >= 100
status = "BLOCKED" if blocked else "OK"
print(
    f"codex-preflight[log]: {status} as_of={ts} "
    f"primary={p_used}% (reset {fmt(p_reset)}) "
    f"secondary={s_used}% (reset {fmt(s_reset)})"
)
sys.exit(1 if blocked else 0)
PY
}

check_probe() {
  local out
  out="$(echo 'say "ok"' | codex exec -m gpt-5.3-codex-spark \
    -c model_reasoning_effort=low --sandbox read-only \
    --skip-git-repo-check - 2>&1 | tail -20)"

  if echo "$out" | grep -qE "hit your usage limit"; then
    local reset
    reset="$(echo "$out" | grep -oE 'try again at [^.]+' | head -n 1)"
    echo "codex-preflight[probe]: BLOCKED (${reset:-no reset parsed})"
    return 1
  fi

  echo "codex-preflight[probe]: OK"
  return 0
}

case "$MODE" in
  --log|log)
    check_log
    ;;
  --probe|probe)
    check_probe
    ;;
  both|"")
    check_log
    rc=$?
    if [ $rc -eq 0 ] || [ $rc -eq 2 ]; then
      check_probe
    else
      exit 1
    fi
    ;;
  -h|--help|help)
    grep '^#' "$0" | sed 's/^# \{0,1\}//'
    ;;
  *)
    echo "codex-preflight: unknown mode '$MODE' (use --probe, --log, or omit for both)" >&2
    exit 2
    ;;
esac
