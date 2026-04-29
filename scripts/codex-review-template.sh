#!/usr/bin/env bash
# Shared implementation for repo-local codex-review wrappers.
#
# Usage:
#   bash scripts/codex-review.sh review [branch]    # PR/diff review against branch (default: main)
#   bash scripts/codex-review.sh audit [target]      # Security-focused audit of target file/dir
#   bash scripts/codex-review.sh critique [system]   # Architecture critique of a named system
#   bash scripts/codex-review.sh claude <packet-file> # Self-contained Claude packet review
#
# Output: docs/codex-reviews/YYYY-MM-DD-<mode>.md
# All writes constrained to docs/codex-reviews/ via --sandbox workspace-write

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PERSONA="${CODEX_REVIEW_PERSONA:-$REPO_ROOT/docs/agents/codex-reviewer.md}"
SCHEMA="$REPO_ROOT/docs/codex-reviews/output-schema.json"
OUTPUT_DIR="$REPO_ROOT/docs/codex-reviews"
DATE=$(date -u +%Y-%m-%d)
MODE="${1:-review}"
TARGET="${2:-main}"

if ! command -v codex &>/dev/null; then
  echo "ERROR: codex CLI not found. Install from https://github.com/openai/codex" >&2
  exit 1
fi

if [ ! -f "$PERSONA" ]; then
  echo "ERROR: Persona doc not found at $PERSONA" >&2
  exit 1
fi

OUTPUT_FILE="$OUTPUT_DIR/${DATE}-${MODE}.md"

run_codex_exec_brief() {
  local prompt="$1"
  local brief_file
  local rc

  brief_file="$(mktemp "${TMPDIR:-/tmp}/codex-review-brief.XXXXXX")" || return 1
  printf '%s\n' "$prompt" >"$brief_file"

  bash "$REPO_ROOT/scripts/codex-fire.sh" \
    -m gpt-5.4 \
    -e high \
    -w "$REPO_ROOT" \
    -b "$brief_file" \
    -- \
    --full-auto \
    --add-dir "$OUTPUT_DIR" \
    --output-schema "$SCHEMA" \
    -o "$OUTPUT_FILE"
  rc=$?

  if [ "$rc" -eq 0 ]; then
    rm -f "$brief_file"
  else
    echo "Codex brief retained at: $brief_file" >&2
  fi
  return "$rc"
}

# Read persona for injection
PERSONA_CONTENT=$(cat "$PERSONA")

case "$MODE" in
  review)
    echo "Running Codex code review against branch: $TARGET"
    cd "$REPO_ROOT"
    codex review \
      --base "$TARGET" \
      2>&1 | tee "$OUTPUT_FILE"

    echo ""
    echo "Review saved to: $OUTPUT_FILE"
    ;;

  audit)
    echo "Running Codex security audit on: $TARGET"
    PROMPT="You are reviewing the HLD Pro AI Integration Services codebase for security issues.

${PERSONA_CONTENT}

Focus your security audit on: ${TARGET}

Check for:
1. SQL injection or unsafe query construction
2. Missing auth checks or RLS bypass
3. Exposed secrets or credentials in code
4. Unsafe error messages leaking internals
5. Missing input validation
6. CORS misconfigurations
7. Insecure direct object references

Write your findings to docs/codex-reviews/${DATE}-audit.md using the format described in your persona doc."

    cd "$REPO_ROOT"
    if ! run_codex_exec_brief "$PROMPT"; then
      echo "Audit failed; see CODEX_FAIL output above." >&2
      exit 1
    fi

    echo ""
    echo "Audit saved to: $OUTPUT_FILE"
    ;;

  critique)
    echo "Running Codex architecture critique on: $TARGET"
    PROMPT="You are reviewing the HLD Pro AI Integration Services codebase architecture.

${PERSONA_CONTENT}

Focus your architecture critique on the system: ${TARGET}

Read the relevant source files (AI_INTEGRATION_SERVICES.md, AGENTS.md, docs/ARCHITECTURE.md) and the edge functions for this system.

Evaluate:
1. Separation of concerns
2. Error handling patterns
3. Data flow efficiency
4. Coupling between components
5. Scalability concerns
6. Missing abstractions or over-abstraction

Write your findings to docs/codex-reviews/${DATE}-critique.md using the format described in your persona doc."

    cd "$REPO_ROOT"
    if ! run_codex_exec_brief "$PROMPT"; then
      echo "Critique failed; see CODEX_FAIL output above." >&2
      exit 1
    fi

    echo ""
    echo "Critique saved to: $OUTPUT_FILE"
    ;;

  claude)
    echo "Calling Claude Code as specialist reviewer for packet: $TARGET"

    if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
      ENV_CANDIDATES=()
      if [ -n "${CLAUDE_REVIEW_ENV_FILE:-}" ]; then
        ENV_CANDIDATES+=("${CLAUDE_REVIEW_ENV_FILE}")
      else
        ENV_CANDIDATES+=("$REPO_ROOT/.env.local" "$REPO_ROOT/.env")
      fi
      for env_file in "${ENV_CANDIDATES[@]}"; do
        if [ -f "$env_file" ]; then
          CLAUDE_CODE_OAUTH_TOKEN=$(grep '^CLAUDE_CODE_OAUTH_TOKEN=' "$env_file" | cut -d= -f2- || true)
          if [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
            export CLAUDE_CODE_OAUTH_TOKEN
            break
          fi
        fi
      done
    fi

    if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
      echo "ERROR: CLAUDE_CODE_OAUTH_TOKEN not set. Run the canonical bootstrap path for this repo and retry." >&2
      exit 1
    fi

    if [ ! -f "$TARGET" ]; then
      echo "ERROR: claude mode requires a packet file path. Inline shell-built prompt text is not allowed." >&2
      exit 1
    fi

    prompt_file="$(mktemp "${TMPDIR:-/tmp}/claude-review-prompt.XXXXXX")" || exit 1
    packet_source="file"
    packet_path="$TARGET"
    packet_content="$(cat "$TARGET")"

    {
      printf '%s\n\n' "You are the alternate-family specialist reviewer for a governed HLD Pro packet."
      printf '%s\n\n' "$PERSONA_CONTENT"
      printf '%s\n' "Use the caller-supplied review packet below as the full review scope."
      printf '%s\n' "Do not explore the repository or request additional tool-driven context unless"
      printf '%s\n' "the caller explicitly embedded that material in the review packet."
      printf '%s\n\n' "Return concise markdown using the persona output format."
      printf '%s\n' "$packet_content"
    } >"$prompt_file"

    if [ "${CODEX_REVIEW_DRY_RUN:-0}" = "1" ]; then
      echo "DRY_RUN claude mode ready"
      echo "env_surface=${CLAUDE_REVIEW_ENV_FILE:-auto}"
      echo "model=${CLAUDE_REVIEW_MODEL:-claude-opus-4-6}"
      echo "permission_mode=${CLAUDE_REVIEW_PERMISSION_MODE:-bypassPermissions}"
      echo "max_turns=${CLAUDE_REVIEW_MAX_TURNS:-8}"
      echo "allowed_tools=${CLAUDE_REVIEW_ALLOWED_TOOLS:-none}"
      echo "review_contract=self_contained_packet"
      echo "packet_source=${packet_source}"
      if [ -n "$packet_path" ]; then
        echo "packet_path=${packet_path}"
      fi
      echo "prompt_file=${prompt_file}"
      rm -f "$prompt_file"
      exit 0
    fi

    supervisor_cmd=(
      python3 "$REPO_ROOT/scripts/cli_session_supervisor.py"
      --tool claude \
      --role specialist-reviewer \
      --model "${CLAUDE_REVIEW_MODEL:-claude-opus-4-6}" \
      --cwd "$REPO_ROOT" \
      --prompt-file "$prompt_file" \
      --scope-slug "codex-review-template-claude-${DATE}" \
      --handoff-package-ref "${CLAUDE_REVIEW_HANDOFF_PACKAGE_REF:-codex-review-template}" \
      --event-root "$REPO_ROOT/raw/cli-session-events" \
      --stdout-copy "$OUTPUT_FILE" \
      --wall-timeout-sec "${CLAUDE_REVIEW_WALL_TIMEOUT_SECONDS:-900}" \
      --silence-timeout-sec "${CLAUDE_REVIEW_SILENCE_TIMEOUT_SECONDS:-300}" \
      --terminate-grace-sec "${CLAUDE_REVIEW_TERMINATE_GRACE_SECONDS:-5}" \
      --permission-mode "${CLAUDE_REVIEW_PERMISSION_MODE:-bypassPermissions}" \
      --max-turns "${CLAUDE_REVIEW_MAX_TURNS:-8}" \
      --max-budget-usd "${CLAUDE_REVIEW_MAX_BUDGET_USD:-1.00}" \
      --no-session-persistence
    )
    if [ -n "${CLAUDE_REVIEW_ALLOWED_TOOLS:-}" ]; then
      supervisor_cmd+=(--allowed-tools "${CLAUDE_REVIEW_ALLOWED_TOOLS}")
    fi
    if [ -n "${CLAUDE_REVIEW_OUTPUT_FORMAT:-}" ]; then
      supervisor_cmd+=(--output-format "${CLAUDE_REVIEW_OUTPUT_FORMAT}")
    fi

    if ! "${supervisor_cmd[@]}"; then
      echo "Claude review failed; see raw/cli-session-events for session evidence." >&2
      exit 1
    fi
    rm -f "$prompt_file"

    echo ""
    echo "Claude review saved to: $OUTPUT_FILE"
    ;;

  *)
    echo "Usage: bash scripts/codex-review.sh {review|audit|critique|claude} [target]"
    echo ""
    echo "Modes:"
    echo "  review [branch]    — Codex code review against branch (default: main)"
    echo "  audit [path]       — Codex security audit of file or directory"
    echo "  critique [system]  — Codex architecture critique of a named system"
    echo "  claude [packet]    — Claude Code specialist review (called from Codex sessions)"
    exit 1
    ;;
esac
