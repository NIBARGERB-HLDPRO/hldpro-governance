# Issue #154 — Pre-Session UserPromptSubmit Hook Standardization (PDCA/R)

**Tier:** 2 (mechanical rollout of an already-codified policy)
**Canonical plan:** [issue-154-structured-agent-cycle-plan.json](./issue-154-structured-agent-cycle-plan.json)
**Issue:** [hldpro-governance#154](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/154)

## Plan

Four PRs, produced by codex-spark after this plan PR merges:

| # | Repo | File(s) | Operation |
|---|---|---|---|
| 1 | `hldpro-governance` | `.gitignore`, `.claude/settings.json` | Surgical .gitignore patch (replace blanket `settings.json` with 3 specific allow-list entries); commit existing `.claude/settings.json` as-is. |
| 2 | `HealthcarePlatform` | `.claude/settings.json`, `.claude/hooks/pre-session-context.sh` | JSON-merge new `UserPromptSubmit` entry into existing settings; add new hook script injecting PROGRESS + FAIL_FAST_LOG + FEATURE_REGISTRY + SESSION_HANDOFF_HISTORY + CLAUDE.md head. |
| 3 | `local-ai-machine` | same pair | Same merge; hook injects PROGRESS + FAIL_FAST_LOG + AGENTS.md + START_SESSION.md + CLAUDE.md head. |
| 4 | `knocktracker` | same pair | Same merge; hook injects PROGRESS + FAIL_FAST_LOG + AGENTS.md + CLAUDE.md head. |

## Do

Codex-spark dispatch (after plan merge). One worktree per sprint, each off fresh `origin/main`:

```bash
git fetch origin main
git worktree add -b <branch> <path> origin/main
# MUST: `git log --oneline origin/main..HEAD` → empty before first commit
```

Per feedback memories `feedback_codex_worktree_base_contamination.md` and `feedback_audit_must_read_remote_head.md` (both written today after AIS #1035 + HP #1274 contamination incidents), this empty-check is a hard gate.

**Non-destructive editing requirements** (user directive, 2026-04-15):
- `.claude/settings.json` on target repos: **JSON-merge**, preserve every existing `PreToolUse` and `PostToolUse` hook byte-for-byte. Do not overwrite.
- `.gitignore` on governance: **surgical line edit**. Do not rewrite.
- New hook scripts: fresh file creation only (no existing file to preserve).

## Check

Per sprint (acceptance gates in the JSON plan):

1. **Diff scope:** PR touches only the files listed in its `sprint.file_paths`. Max 2 files per PR.
2. **Preservation:** for repos with pre-existing `.claude/settings.json`, `jq` comparison confirms all pre-existing `PreToolUse`/`PostToolUse` entries survived byte-for-byte.
3. **Behavior:** fresh local clone + open Claude Code session → hook fires → branch name and existence-checked docs surface in system reminder.
4. **Idempotency:** second prompt in same session does NOT re-inject (session-once guard working).
5. **Graceful degradation:** mocking each injected file as missing one-at-a-time → hook continues, logs absence, does not error.

## Adjust

Deviation rules (from JSON plan `material_deviation_rules`):

- Malformed existing `settings.json` → halt that sprint, record, do not overwrite.
- Real path of `PROGRESS.md` / `FAIL_FAST_LOG.md` differs from plan → update the hook script, do NOT create missing files.
- Dirty worktree base detected → halt, re-create from fresh fetch.
- PR would touch > 2 files → halt and surface scope question.
- AIS Codex-ingestion path parameterization needed → split into separate follow-up issue.

## Review

**Specialist reviews (recorded in JSON plan):**

- Scope reviewer → accepted (mechanical rollout only)
- Non-destructive-edit reviewer → accepted (JSON-merge/surgical-patch required)
- Anti-contamination reviewer → accepted (worktree hygiene guardrails required)

**Alternate-model review:** not required for Tier 2 mechanical rollout of an already-codified policy. STANDARDS.md cross-review obligation applies to architecture/standards-*change* PRs; this PR executes on an existing standard.

**Closeout protocol:** after 4 implementation PRs merge, fill `raw/closeouts/2026-04-XX-pre-session-hook-standardization.md` from the template, run `hooks/closeout-hook.sh`, verify graph reflects change, update `OVERLORD_BACKLOG.md` and close issue #154.

## Out of scope (explicit)

- AIS hook behavior changes (aligned already; Codex-ingestion path parameterization tracked separately if needed).
- ASC-Evaluator inclusion (exempt per STANDARDS.md repo registry).
- New hook events (`SessionStart`, `Stop`) or hook behaviors beyond the defined injection set.
- Cross-repo CI lint for settings.json shape (potential follow-up).
