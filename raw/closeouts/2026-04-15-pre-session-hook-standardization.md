# Stage 6 Closeout
Date: 2026-04-15
Repo: hldpro-governance (umbrella) — touches hldpro-governance, HealthcarePlatform, knocktracker, local-ai-machine
Task ID: hldpro-governance#154
Six-Stage Cycle: Stage 6 / Audit + Closeout
Completed By: Benji

## Decision Made

Standardized a committed `UserPromptSubmit` pre-session-context hook across HLDPRO product repos. `hldpro-governance` `.gitignore` tightened to allow `.claude/settings.json` to be committed, and repo-local `.claude/hooks/pre-session-context.sh` hooks added to HealthcarePlatform and knocktracker using the AIS `session-start-gate.sh` template (session-once guard, existence-checked branch + PROGRESS + FAIL_FAST_LOG + repo-specific docs injection). Local-ai-machine deferred pending pre-existing CI drift resolution (LAM issue #439).

## Pattern Identified

- `.gitignore` blanket `settings.json` (bare name, no path prefix) pattern is a common footgun — it silently swallows `.claude/settings.json` which IS intended to be committed. Allow-list `.claude/`-pathed volatile files only.
- Committed UserPromptSubmit hooks are now the canonical way to automate a repo's `Session Start` checklist. Any future repo CLAUDE.md that documents a Session Start section should ship a corresponding `.claude/hooks/pre-session-context.sh` on the same PR.
- Per-repo CI drift (pre-existing) can block rollouts that are otherwise unrelated in scope. Governance-adjacent rollouts should run a pre-check against remote main's CI state before dispatching implementation to avoid discovery-during-merge.

## Contradicts Existing

No. Extends the policy in STANDARDS.md §Society of Minds and the per-repo CLAUDE.md Session Start sections.

## Files Changed

- `hldpro-governance/.gitignore` — drop blanket `settings.json` / `settings.local.json` / `scheduled_tasks.lock`, replace with `.claude/worktrees/` / `.claude/scheduled_tasks.lock` / `.claude/settings.local.json`.
- `hldpro-governance/.claude/settings.json` — committed wiring `UserPromptSubmit → hooks/pre-session-context.sh`.
- `HealthcarePlatform/.claude/settings.json` — JSON-merged new `UserPromptSubmit` entry.
- `HealthcarePlatform/.claude/hooks/pre-session-context.sh` — new (injects PROGRESS + FAIL_FAST_LOG + FEATURE_REGISTRY + SESSION_HANDOFF_HISTORY + CLAUDE.md head).
- `knocktracker/.claude/settings.json` — JSON-merged new `UserPromptSubmit` entry.
- `knocktracker/.claude/hooks/pre-session-context.sh` — new (injects PROGRESS + FAIL_FAST_LOG + AGENTS.md + CLAUDE.md head).
- `knocktracker/docs/file-index.txt` — new hook path added to tracked-file index.
- `hldpro-governance/docs/plans/issue-154-structured-agent-cycle-plan.json` — plan artifact (merged via #155).
- `hldpro-governance/docs/plans/issue-154-pre-session-hook-standardization-pdcar.md` — PDCA/R companion.

## Merged PRs

- hldpro-governance #155 — plan + PDCAR
- hldpro-governance #156 — gitignore tighten + settings.json commit
- HealthcarePlatform #1276 — hook + settings JSON-merge
- knocktracker #158 — hook + settings JSON-merge + file-index update (admin-merged over pre-existing expo version drift — see knocktracker #159)

## Deferred

- local-ai-machine #438 — CLOSED, blocked on local-ai-machine #439 (pre-existing `breaker-mcp-contract` CI drift: 6 SOM_* env vars missing from managed boundary doc). Branch `riskfix/pre-session-hook-20260415` preserved at commit `86a38eb` for resubmission after #439 merges.

## Follow-up Issues Filed

- local-ai-machine #439 — breaker-mcp-contract env var classification drift
- knocktracker #159 — npx expo install --check package version drift (14 packages)

## Wiki Pages Updated

Creates (follow-up): `wiki/decisions/2026-04-15-pre-session-hook-standardization.md` — one-line decision record pointing at issue #154 and this closeout.

## operator_context Written

- [ ] Yes — row ID: [pending — memory-writer invocation via closeout-hook.sh]
- [x] No — reason: memory-writer integration runs best-effort via `scripts/consolidate-memory.sh` hooked from `hooks/closeout-hook.sh`; outcome depends on Supabase edge-fn availability. Memory files already written today (`feedback_codex_worktree_base_contamination.md`, `feedback_audit_must_read_remote_head.md`, `feedback_codex_spark_no_network.md`) capture the durable lessons.

## Links To

- Umbrella issue: hldpro-governance#154
- Plan PR: hldpro-governance#155 (merged)
- Implementation PRs: hldpro-governance#156, HealthcarePlatform#1276, knocktracker#158
- Deferred PR branch: local-ai-machine `riskfix/pre-session-hook-20260415` (blocked on local-ai-machine#439)
- Memories: `feedback_codex_worktree_base_contamination.md`, `feedback_audit_must_read_remote_head.md`, `feedback_codex_spark_no_network.md`
- STANDARDS.md §Society of Minds (policy authority)
- STANDARDS.md §Repo Registry (ASC-Evaluator exemption justification)
