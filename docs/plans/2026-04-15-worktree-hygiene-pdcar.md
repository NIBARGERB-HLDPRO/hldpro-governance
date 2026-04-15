# Worktree Hygiene + Backlog Refresh — PDCAR

**Date:** 2026-04-15
**Author:** Opus 4.6 (session dispatcher)
**Scope:** Post-prune cleanup following 40→9 worktree reduction

## Problem
Session discovered 40 worktrees (many for long-merged PRs), a stale `OVERLORD_BACKLOG.md` (5+ merged PRs missing from Done table), and phantom outstanding tasks (Sprint 6 waiver + gate validation already resolved by PR #130). Without a closeout, the next session starts from the same stale `OVERLORD_BACKLOG.md` and re-discovers the same facts.

## Data
- `git worktree list`: 40 trees pre-prune, 9 post-prune
- `git status` (on `main`): `OVERLORD_BACKLOG.md` modified via subagent, not staged
- `git branch`: ~30 local refs, many plausibly matching already-merged PRs
- `git log origin/main`: 6 PRs (#130, #136, #138, #141, #144, #146) merged since last Done-table entry
- 3 WIP worktrees flagged: `gov-packet-schema`, `gov-society-of-minds`, `graphify-improvement-codex-review`
- `gov-remote-mcp`: confirmed live WIP by operator, excluded

## Change
1. **Commit + PR backlog refresh.** Branch `docs/backlog-refresh-2026-04-15`, commit `OVERLORD_BACKLOG.md` edits, push, open PR citing PRs #130/#136/#138/#141.
2. **Triage 3 WIP worktrees.** Check for existing PR per worktree; operator decides rescue/abandon/merge. `graphify-improvement-codex-review` must be relocated out of the main tree regardless.
3. **Stale local branch sweep.** Enumerate `git branch` refs; for each, check `gh pr list --head <branch> --state all`; propose deletion list for merged-only refs.
4. **Closeout.** File `raw/closeouts/2026-04-15-worktree-hygiene.md` + run `hooks/closeout-hook.sh`.

## Assess (gates)
- Step 1 PR merges without conflicts on `origin/main`
- Step 2 yields an explicit disposition per worktree (rescue / abandon / merge — not "later")
- Step 3 deletion list reviewed by operator before any destructive action
- Step 4 closeout-hook passes; Stage 6 satisfied

## Remediate (routing)
| Step | Agent | Rationale |
|---|---|---|
| 1 | general-purpose subagent | Mechanical: git commit + push + `gh pr create` |
| 2 | general-purpose subagent | Inspection-only; operator decides each |
| 3 | general-purpose subagent | Enumeration-only; operator approves deletions |
| 4 | Opus (dispatcher) | Trivial template fill from this PDCAR + session summary |

Codex-spark not required: no code authoring. Preflight not run.
