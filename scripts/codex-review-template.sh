#!/usr/bin/env bash
# codex-review.sh — Codex CLI wrapper for structured code review
#
# Usage:
#   bash scripts/codex-review.sh review [branch]    # PR/diff review against branch (default: main)
#   bash scripts/codex-review.sh audit [target]      # Security-focused audit of target file/dir
#   bash scripts/codex-review.sh critique [system]   # Architecture critique of a named system
#
# Output: docs/codex-reviews/YYYY-MM-DD-<mode>.md
# All writes constrained to docs/codex-reviews/ via --sandbox workspace-write

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PERSONA="$REPO_ROOT/docs/agents/codex-reviewer.md"
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
    codex exec \
      -m gpt-5.4 \
      -c model_reasoning_effort=high \
      --full-auto \
      --add-dir "$OUTPUT_DIR" \
      --output-schema "$SCHEMA" \
      -o "$OUTPUT_FILE" \
      "$PROMPT"

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
    codex exec \
      -m gpt-5.4 \
      -c model_reasoning_effort=high \
      --full-auto \
      --add-dir "$OUTPUT_DIR" \
      --output-schema "$SCHEMA" \
      -o "$OUTPUT_FILE" \
      "$PROMPT"

    echo ""
    echo "Critique saved to: $OUTPUT_FILE"
    ;;

  claude)
    echo "Calling Claude Code as specialist reviewer for: $TARGET"

    # Source token from .env if not already set
    if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ] && [ -f "$REPO_ROOT/.env" ]; then
      CLAUDE_CODE_OAUTH_TOKEN=$(grep '^CLAUDE_CODE_OAUTH_TOKEN=' "$REPO_ROOT/.env" | cut -d= -f2-)
      export CLAUDE_CODE_OAUTH_TOKEN
    fi

    if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
      echo "ERROR: CLAUDE_CODE_OAUTH_TOKEN not set. Run 'claude setup-token' and add to .env" >&2
      exit 1
    fi

    PROMPT="You are reviewing code in the HLD Pro AI Integration Services repo.

${PERSONA_CONTENT}

${TARGET}

Read the relevant files, then provide your findings in markdown format."

    claude -p "$PROMPT" \
      --allowedTools "Read Grep Glob" \
      --max-turns 5 \
      --no-session-persistence \
      --dangerously-skip-permissions \
      2>&1 | tee "$OUTPUT_FILE"

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
    echo "  claude [prompt]    — Claude Code specialist review (called from Codex sessions)"
    exit 1
    ;;
esac
