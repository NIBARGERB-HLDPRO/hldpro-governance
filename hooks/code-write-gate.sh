#!/bin/bash
# code-write-gate.sh — PreToolUse hook enforcing SoM division of labor
# Fires on Write tool; blocks Claude from creating new code files directly.
# Claude Code hook contract: exit 0 = allow, exit 2 = hard block.
# NOTE: set -e is intentionally omitted — silent non-zero exits would block all commands.

# Read stdin (JSON from Claude Code hook runner)
input="$(cat 2>/dev/null)"

# No input → allow (graceful degradation)
if [ -z "$input" ]; then
  exit 0
fi

# Extract file_path from tool_input
file_path="$(printf '%s' "$input" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null)"

# No path → allow
if [ -z "$file_path" ]; then
  exit 0
fi

file_dir="$(dirname "$file_path")"
while [ ! -d "$file_dir" ] && [ "$file_dir" != "/" ] && [ "$file_dir" != "." ]; do
  file_dir="$(dirname "$file_dir")"
done
repo_root="$(git -C "$file_dir" rev-parse --show-toplevel 2>/dev/null || true)"
if [ -n "$repo_root" ]; then
  validator="$repo_root/scripts/overlord/validate_structured_agent_cycle_plan.py"
  if [ -f "$validator" ]; then
    # If relpath calculation fails for an unusual hook payload, keep the hook's historical graceful-degradation behavior.
    rel_path="$(python3 - "$repo_root" "$file_path" <<'PY' 2>/dev/null || true
import os
import sys

root, path = sys.argv[1], sys.argv[2]
print(os.path.relpath(path, root))
PY
)"
    if [ -n "$rel_path" ]; then
      branch_name="$(git -C "$repo_root" branch --show-current 2>/dev/null || true)"
      changed_file="$(mktemp "${TMPDIR:-/tmp}/governance-surface-change.XXXXXX")"
      printf '%s\n' "$rel_path" > "$changed_file"
      gate_output="$(python3 "$validator" \
        --root "$repo_root" \
        --branch-name "$branch_name" \
        --changed-files-file "$changed_file" \
        --enforce-governance-surface 2>&1)"
      gate_status=$?
      rm -f "$changed_file"
      if [ "$gate_status" -ne 0 ]; then
        reason="$(printf '%s' "$gate_output" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])')"
        printf '%s' "{\"decision\":\"block\",\"reason\":\"BLOCKED: Governance-surface writes require an issue-backed structured JSON plan, accepted review status, and implementation-ready execution handoff.\\n\\n${reason}\"}"
        exit 2
      fi
    fi
  fi
fi

# Bootstrapping exemption: paths inside /.claude/ are always allowed
# (hook scripts must be able to write their own files)
if printf '%s' "$file_path" | grep -q '/.claude/'; then
  exit 0
fi

# Overwrite/edit exemption: file already exists on disk → allow
if [ -f "$file_path" ]; then
  exit 0
fi

# Extract extension (everything after the last dot)
ext=".${file_path##*.}"
# If there was no dot, or the dot is the filename start (dotfile), ext will be
# the whole basename — treat that as no extension and allow.
basename_only="$(basename "$file_path")"
if [ "$ext" = ".$basename_only" ] || [ "$ext" = "." ]; then
  exit 0
fi

# Always-allowed extensions (docs, config, data)
case "$ext" in
  .md|.json|.yaml|.yml|.toml|.env|.txt|.sql|.example|.template)
    exit 0
    ;;
esac

# Blocked code-file extensions
case "$ext" in
  .sh|.py|.mjs|.js|.ts|.tsx|.go|.rb|.rs)
    basename_file="$(basename "$file_path")"
    printf '%s' "{\"decision\":\"block\",\"reason\":\"BLOCKED: New code file '${basename_file}' must be authored by codex-spark, not Claude directly.\\n\\nRule: SoM division of labor — Claude plans + reviews + trivial mechanical edits only.\\nAll new .sh/.py/.mjs/.ts/.js files → codex-spark brief + Agent tool handoff.\\n\\nTo proceed: write a codex-spark brief and use the Agent tool to delegate this task.\"}"
    exit 2
    ;;
esac

# Extension not in blocked list → allow
exit 0
