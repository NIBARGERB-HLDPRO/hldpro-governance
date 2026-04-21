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

repo_root_from_cwd="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -n "$repo_root_from_cwd" ]; then
  delegation_gate="$repo_root_from_cwd/scripts/orchestrator/delegation_gate.py"
  if [ -f "$delegation_gate" ]; then
    tool_payload="$(printf '%s' "$input" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    tool_name = str(data.get('tool_name') or data.get('tool') or '')
    tool_input = data.get('tool_input') if isinstance(data.get('tool_input'), dict) else {}
    task_text = (
        tool_input.get('description')
        or tool_input.get('prompt')
        or tool_input.get('command')
        or tool_input.get('task')
        or ''
    )
    print(json.dumps({'tool_name': tool_name, 'task_text': str(task_text)}))
except Exception:
    print(json.dumps({'tool_name': '', 'task_text': ''}))
" 2>/dev/null || printf '%s' '{"tool_name":"","task_text":""}')"
    tool_name="$(printf '%s' "$tool_payload" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null || true)"
    task_text="$(printf '%s' "$tool_payload" | python3 -c "import json,sys; print(json.load(sys.stdin).get('task_text',''))" 2>/dev/null || true)"

    case "$tool_name" in
      Agent|Task|Bash|Explore|Read)
        if [ -n "$task_text" ]; then
          delegation_log="${DELEGATION_GATE_LOG:-$repo_root_from_cwd/.claude/governance.log}"
          bypass=false
          if printf '%s' "$task_text" | grep -qE '^[[:space:]]*--bypass-delegation-gate([[:space:]]|$)'; then
            bypass=true
          fi

          if [ -n "$DELEGATION_GATE_URL" ]; then
            request_json="$(python3 - "$tool_name" "$task_text" <<'PY' 2>/dev/null || printf '{}'
import json
import sys

print(json.dumps({"tool_name": sys.argv[1], "task_description": sys.argv[2]}))
PY
)"
            gate_result="$(curl -sS --max-time 2 "$DELEGATION_GATE_URL" \
              -H 'Content-Type: application/json' \
              -d "$request_json" 2>/dev/null || printf '%s' '{"decision":"ALLOW","owner":"","confidence":0,"reason":"delegation gate unavailable fail-open","source":"mcp-fail-open"}')"
          else
            bypass_arg=""
            if [ "$bypass" = true ]; then
              bypass_arg="--bypass"
            fi
            gate_result="$(python3 "$delegation_gate" \
              --tool-name "$tool_name" \
              --task-description "$task_text" \
              $bypass_arg \
              --json 2>/dev/null || printf '%s' '{"decision":"ALLOW","owner":"","confidence":0,"reason":"delegation gate script unavailable fail-open","source":"script-fail-open"}')"
          fi

          decision="$(printf '%s' "$gate_result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('decision','ALLOW'))" 2>/dev/null || printf 'ALLOW')"
          owner="$(printf '%s' "$gate_result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('owner',''))" 2>/dev/null || true)"
          confidence="$(printf '%s' "$gate_result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('confidence',0))" 2>/dev/null || printf '0')"
          reason="$(printf '%s' "$gate_result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('reason',''))" 2>/dev/null || true)"

          case "$decision" in
            BLOCK)
              mkdir -p "$(dirname "$delegation_log")" 2>/dev/null || true
              printf '%s BLOCK %s owner=%s confidence=%s reason=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$tool_name" "$owner" "$confidence" "$reason" >> "$delegation_log" 2>/dev/null || true
              escaped_reason="$(printf '%s' "GOVERNANCE BLOCK: This task belongs to ${owner} per §DA. Spawn that agent instead. ${reason}" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])')"
              printf '%s' "{\"decision\":\"block\",\"reason\":\"${escaped_reason}\"}"
              exit 2
              ;;
            WARN)
              mkdir -p "$(dirname "$delegation_log")" 2>/dev/null || true
              printf '%s WARN %s owner=%s confidence=%s reason=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$tool_name" "$owner" "$confidence" "$reason" >> "$delegation_log" 2>/dev/null || true
              ;;
            ALLOW)
              if [ "$bypass" = true ]; then
                mkdir -p "$(dirname "$delegation_log")" 2>/dev/null || true
                printf '%s BYPASS %s reason=explicit-bypass\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$tool_name" >> "$delegation_log" 2>/dev/null || true
              fi
              ;;
          esac
        fi
        ;;
    esac
  fi
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
      plan_preflight="$repo_root/scripts/overlord/check_plan_preflight.py"
      if [ -f "$plan_preflight" ]; then
        trivial_flag=""
        if [ "${PLAN_GATE_TRIVIAL_SINGLE_LINE:-}" = "true" ]; then
          trivial_flag="--trivial-single-line"
        fi
        plan_result="$(python3 "$plan_preflight" \
          --repo-root "$repo_root" \
          --target-path "$rel_path" \
          --intent write \
          $trivial_flag \
          --json 2>/dev/null || true)"
        plan_decision="$(printf '%s' "$plan_result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('decision','allow'))" 2>/dev/null || printf 'allow')"
        if [ "$plan_decision" = "block" ]; then
          plan_reason="$(printf '%s' "$plan_result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('reason',''))" 2>/dev/null || true)"
          escaped_reason="$(printf '%s' "$plan_reason" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])')"
          printf '%s' "{\"decision\":\"block\",\"reason\":\"${escaped_reason}\"}"
          exit 2
        fi
      fi

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

      # Planner-boundary execution-scope enforcement is warning-only in local hooks.
      boundary_scope_candidate=false
      case "$rel_path" in
        CLAUDE.md|README.md|STANDARDS.md|OVERLORD_BACKLOG.md|docs/DATA_DICTIONARY.md|docs/FEATURE_REGISTRY.md|docs/PROGRESS.md|docs/SERVICE_REGISTRY.md|\
        .github/workflows/*|.github/scripts/*|agents/*|docs/schemas/*|hooks/*|launchd/*|raw/closeouts/*|raw/cross-review/*|raw/execution-scopes/*|\
        raw/gate/*|raw/model-fallbacks/*|raw/operator-context/*|raw/packets/*|metrics/*|scripts/knowledge_base/*|scripts/lam/*|scripts/orchestrator/*|\
        scripts/overlord/*|scripts/packet/*|wiki/*|docs/plans/*)
          boundary_scope_candidate=true
          ;;
      esac

      if [ "$boundary_scope_candidate" = true ]; then
        scope_validator="$repo_root/scripts/overlord/assert_execution_scope.py"
        issue_token="$(printf '%s\n' "$branch_name" | grep -oE 'issue-[0-9]+' | head -n 1 || true)"
        issue_number="${issue_token#issue-}"

        if [ -f "$scope_validator" ] && [ -n "$issue_number" ] && [ -d "$repo_root/raw/execution-scopes" ]; then
          mapfile -t implementation_scopes < <(find "$repo_root/raw/execution-scopes" -maxdepth 1 -type f -name "*issue-${issue_number}*implementation*.json" | sort)
          mapfile -t planning_scopes < <(find "$repo_root/raw/execution-scopes" -maxdepth 1 -type f -name "*issue-${issue_number}*planning*.json" | sort)

          selected_scope=""
          if [ "${#implementation_scopes[@]}" -eq 1 ]; then
            selected_scope="${implementation_scopes[0]}"
          elif [ "${#planning_scopes[@]}" -eq 1 ]; then
            selected_scope="${planning_scopes[0]}"
          fi

          if [ -z "$selected_scope" ]; then
            if [ "${#implementation_scopes[@]}" -gt 1 ] || [ "${#planning_scopes[@]}" -gt 1 ]; then
              echo "WARN planner-boundary execution-scope check skipped: multiple matching scope files for issue-${issue_number}" >&2
            else
              echo "WARN planner-boundary execution-scope check skipped: no scope file matched issue-${issue_number}" >&2
            fi
          else
            scope_changed_file="$(mktemp "${TMPDIR:-/tmp}/planner-boundary-change.XXXXXX")"
            printf '%s\n' "$rel_path" > "$scope_changed_file"
            scope_output="$(python3 "$scope_validator" \
              --scope "$selected_scope" \
              --changed-files-file "$scope_changed_file" 2>&1)"
            scope_status=$?
            rm -f "$scope_changed_file"
            if [ "$scope_status" -ne 0 ]; then
              echo "WARN planner-boundary drift detected (warning-only in local hook):" >&2
              echo "$scope_output" >&2
            fi
          fi
        fi
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
    if [ -n "$repo_root" ] && [ -n "$rel_path" ] && [ -f "$repo_root/scripts/overlord/check_worker_handoff_route.py" ]; then
      lane_role="${HLDPRO_LANE_ROLE:-${SOM_LANE_ROLE:-planner}}"
      route_result="$(python3 "$repo_root/scripts/overlord/check_worker_handoff_route.py" \
        --repo-root "$repo_root" \
        --target-path "$rel_path" \
        --branch-name "${branch_name:-}" \
        --role "$lane_role" \
        --json 2>/dev/null || true)"
      route_decision="$(printf '%s' "$route_result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('decision','block'))" 2>/dev/null || printf 'block')"
      route_reason="$(printf '%s' "$route_result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('reason',''))" 2>/dev/null || true)"
      if [ "$route_decision" = "allow" ]; then
        exit 0
      fi
      if [ -n "$route_reason" ]; then
        escaped_reason="$(printf '%s' "$route_reason" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])')"
        printf '%s' "{\"decision\":\"block\",\"reason\":\"${escaped_reason}\"}"
        exit 2
      fi
    fi
    printf '%s' "{\"decision\":\"block\",\"reason\":\"BLOCKED: New code file '${basename_file}' must be authored by an approved Worker, not directly by the planning/orchestration lane.\\n\\nRule: SoM division of labor — Codex orchestrates, Opus plans, Sonnet or bounded local Qwen workers implement, Codex QA reviews, and gates verify.\\nNew .sh/.py/.mjs/.ts/.js files require an issue-backed execution scope and Worker handoff.\\n\\nNext: create/update raw/execution-scopes/<date>-issue-<n>-worker-implementation.json and raw/handoffs/<date>-issue-<n>-<scope>.json; include the target file in allowed_write_paths; set execution_mode to implementation_ready; set handoff_evidence.status to accepted; then rerun from the approved Worker lane.\"}"
    exit 2
    ;;
esac

# Extension not in blocked list → allow
exit 0
