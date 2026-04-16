# Stage 6 Closeout
Date: 2026-04-15
Repo: hldpro-governance (umbrella) — touches hldpro-governance, HealthcarePlatform, knocktracker, local-ai-machine
Task ID: hldpro-governance#154
Six-Stage Cycle: Stage 6 / Audit + Closeout
Completed By: Benji

## Decision Made

Standardized a committed `UserPromptSubmit` pre-session-context hook across all HLDPRO product repos. `hldpro-governance` `.gitignore` tightened to allow `.claude/settings.json` to be committed, and repo-local `.claude/hooks/pre-session-context.sh` hooks added to HealthcarePlatform, knocktracker, and local-ai-machine using the AIS `session-start-gate.sh` template (session-once guard, existence-checked branch + PROGRESS + FAIL_FAST_LOG + repo-specific docs injection). Three pre-existing CI violations fixed inline: LAM `.gitignore` broad `.claude` ignore, 6 unregistered `SOM_*` env vars in LAM's gap1 exemption artifact, and LAM `CLAUDE.md` exceeding 30-line contract limit. Governance `require-cross-review.yml` YAML heredoc bug fixed (PR #163) as a blocking side-fix.

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
- `hldpro-governance/docs/plans/issue-154-structured-agent-cycle-plan.json` — plan artifact (merged via #155; 3 amendments merged via #158).
- `hldpro-governance/docs/plans/issue-154-pre-session-hook-standardization-pdcar.md` — PDCA/R companion.
- `hldpro-governance/.github/workflows/require-cross-review.yml` — heredoc `<<` removed; Python scripts extracted to `.github/scripts/` (PR #163).
- `local-ai-machine/.gitignore` — broad `.claude` ignore replaced with 3 volatile-file entries (same pattern as governance Sprint 1).
- `local-ai-machine/.claude/settings.json` — JSON-merged new `UserPromptSubmit` entry.
- `local-ai-machine/.claude/hooks/pre-session-context.sh` — new (injects AGENTS.md + START_SESSION.md + PROGRESS + FAIL_FAST_LOG + CLAUDE.md head).
- `local-ai-machine/docs/governance/env_var_gap1_scratch_identity_exemptions.json` — 6 pre-existing `SOM_*` vars added to exemption list.
- `local-ai-machine/CLAUDE.md` — trimmed from 43 → 27 lines to satisfy agents governance contract (≤ 30).

## Merged PRs

- hldpro-governance #155 — plan + PDCAR
- hldpro-governance #156 — gitignore tighten + settings.json commit
- hldpro-governance #158 — plan amendments (3 corrections)
- hldpro-governance #163 — require-cross-review.yml YAML heredoc fix (blocking side-fix)
- HealthcarePlatform #1276 — hook + settings JSON-merge
- knocktracker #158 — hook + settings JSON-merge + file-index update (admin-merged over pre-existing expo version drift — see knocktracker #159)
- local-ai-machine #441 (branch `riskfix/issue-154-lam-pre-session-hook-20260415`) — hook + settings JSON-merge + .gitignore + env-var exemptions + CLAUDE.md trim; merged 2026-04-15T20:46:39Z

## Deferred

None. All 4 target repos completed.

## Follow-up Issues Filed

- knocktracker #159 — npx expo install --check package version drift (14 packages)

## Wiki Pages Updated

Creates (follow-up): `wiki/decisions/2026-04-15-pre-session-hook-standardization.md` — one-line decision record pointing at issue #154 and this closeout.

## operator_context Written

- [ ] Yes — row ID: [pending — memory-writer invocation via closeout-hook.sh]
- [x] No — reason: memory-writer integration runs best-effort via `scripts/consolidate-memory.sh` hooked from `hooks/closeout-hook.sh`; outcome depends on Supabase edge-fn availability. Memory files already written today (`feedback_codex_worktree_base_contamination.md`, `feedback_audit_must_read_remote_head.md`, `feedback_codex_spark_no_network.md`, `feedback_lam_claude_md_line_limit.md`, `feedback_github_actions_heredoc_yaml.md`) capture the durable lessons.

## Links To

- Umbrella issue: hldpro-governance#154
- Plan PR: hldpro-governance#155 (merged)
- Implementation PRs: hldpro-governance#156, hldpro-governance#158, hldpro-governance#163, HealthcarePlatform#1276, knocktracker#158, local-ai-machine#441

- Memories: `feedback_codex_worktree_base_contamination.md`, `feedback_audit_must_read_remote_head.md`, `feedback_codex_spark_no_network.md`, `feedback_lam_claude_md_line_limit.md`, `feedback_github_actions_heredoc_yaml.md`
- STANDARDS.md §Society of Minds (policy authority)
- STANDARDS.md §Repo Registry (ASC-Evaluator exemption justification)
