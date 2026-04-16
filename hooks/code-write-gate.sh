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
