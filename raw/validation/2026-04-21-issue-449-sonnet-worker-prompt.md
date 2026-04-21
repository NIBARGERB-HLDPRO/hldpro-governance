# Issue #449 Sonnet Worker Prompt

You are the Sonnet 4.6 Worker for hldpro-governance issue #449.

You are not alone in the repo. Codex is orchestrator/QA, and other issue worktrees may exist. Do not revert unrelated edits. Keep all writes inside the execution scope:

- `hooks/code-write-gate.sh`
- `hooks/schema-guard.sh`
- `scripts/overlord/check_plan_preflight.py`
- `scripts/overlord/test_check_plan_preflight.py`
- `scripts/overlord/test_schema_guard_hook.py`

Context:

- Parent epic #434 requires structured handoff packages to keep plan -> worker -> QA -> gate acceptance criteria explicit.
- Issue #447 made `hooks/schema-guard.sh` fail loud for Bash write blocks.
- Issue #448 routed new code file writes through Worker handoff evidence.
- Issue #449 now needs an earlier preflight: governed write intent without recent planning evidence must route to plan creation before implementation attempts.

Acceptance criteria:

- Governed code/config writes without recent planning evidence emit `PLAN_GATE_BLOCKED: missing_recent_plan`.
- Missing-plan output includes `NEXT_ACTION: create_plan`, `TARGET_FILE`, `PLANS_DIR`, and explicit bounded bypass guidance.
- Read-only commands are not blocked.
- Trivial single-line bypass is explicit and bounded.
- Bash/Python/heredoc write attempts get the same missing-plan routing signal or a clear refusal.
- Creating/updating a plan clears the preflight for subsequent governed code edits.
- Existing Worker handoff and schema guard protections remain enforced.

Implementation guidance:

- Prefer a small read-only helper at `scripts/overlord/check_plan_preflight.py`.
- The helper should accept repo root, target path or Bash command, intent, plans dir, freshness window, and optional bypass flag, and support `--json`.
- Treat governed code/config extensions as `.sh`, `.py`, `.mjs`, `.js`, `.ts`, `.tsx`, `.go`, `.rb`, `.rs`, `.sql`, `.yml`, and `.yaml`.
- A recent plan is any `*.md` under `.claude/plans` modified within the accepted freshness window.
- Do not make `PLAN_GATE_BYPASS` a general bypass; only allow it when explicitly requested as trivial single-line and report that status.
- Wire `hooks/code-write-gate.sh` and `hooks/schema-guard.sh` with concise, stable output while keeping their current enforcement intact.

Required validation before handoff back to Codex:

- `python3 scripts/overlord/test_check_plan_preflight.py`
- `python3 scripts/overlord/test_schema_guard_hook.py`
- `python3 -m py_compile scripts/overlord/check_plan_preflight.py`
- `bash -n hooks/code-write-gate.sh`
- `bash -n hooks/schema-guard.sh`
