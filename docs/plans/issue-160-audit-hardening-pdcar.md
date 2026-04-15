# Issue #160 — Audit-Hardening PDCA/R

**Tier:** 2 (adds 3 enforcement artifacts)
**Canonical plan:** [issue-160-structured-agent-cycle-plan.json](./issue-160-structured-agent-cycle-plan.json)
**Issue:** [hldpro-governance#160](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/160)

## Plan

Three files added on a single branch + one implementation PR:

| Sprint | File | Purpose |
|---|---|---|
| 1 | `scripts/overlord/audit_remote.sh` | Thin `gh api` wrapper for reading a file on remote main without relying on local working tree state. Callable from agents, hooks, CI. |
| 2 | `docs/templates/codex-spark-dispatch-brief.md` | Reusable brief template with the worktree-discipline hard gate + non-destructive-edit clause + diff-scope cap + no-push clause + reporting format. |
| 3 | `agents/verify-completion.md` (surgical patch) | New `## Remote-reading preferred` section mandates the helper script. No existing content removed. |

## Do

Codex-spark executes all 3 sprints on one branch `issue-160-audit-hardening`:

```bash
git fetch origin main
git worktree add -b issue-160-audit-hardening /tmp/issue-160-impl origin/main
cd /tmp/issue-160-impl
# sprint 1: add audit_remote.sh, commit
# sprint 2: add codex-spark-dispatch-brief.md, commit
# sprint 3: insert Remote-reading section into verify-completion.md, commit
# verify: git log --oneline origin/main..HEAD == 3 lines; git diff --name-only origin/main..HEAD == 3 files
```

Dispatcher (Claude) pushes + opens PR; codex-spark does not push or `gh` (per feedback memory `feedback_codex_spark_no_network.md`).

## Check

Per sprint:

- **Sprint 1:** 4 smoke tests (3 known-existing paths across repos, 1 known-missing path) verify stdout content + stderr error structure + exit code. Script <=40 lines.
- **Sprint 2:** All 6 required H2 sections present. Worktree-discipline snippet present verbatim. Example usage appendix references issue #154.
- **Sprint 3:** `git diff` on `verify-completion.md` shows only `+` lines (zero deletions outside insertion boundaries). Every pre-existing heading still present. New section positioned between `## Process` and `## Output Format`.

Global:
- Implementation PR touches exactly 3 files (one per sprint).
- `git log --oneline origin/main..HEAD` returns exactly 3 lines before push.

## Adjust

Deviation rules (from JSON plan `material_deviation_rules`):

- `agents/verify-completion.md` changed on main since plan authored → rebase the surgical patch, do NOT overwrite.
- `scripts/overlord/audit_remote.sh` already exists → HALT and surface, do NOT overwrite.
- Sprint PR touches > 1 file → HALT, scope question.
- Helper script > 40 lines → trim redundant error paths, do NOT widen scope.
- `gh api` rate-limits during smoke tests → file follow-up issue for bounded retry + backoff, do NOT add retry here.

## Review

**Specialist reviews (recorded in JSON plan):**

- Scope reviewer → accepted (3-file cap, each with acceptance gate)
- Non-destructive-edit reviewer → accepted (Sprint 3 surgical-insert-only)
- Implementation-risk reviewer → accepted_with_followup (gh CLI dependency acceptable; follow-up if curl fallback becomes necessary)

**Alternate-model review:** not requested. Tier 2 policy-execution slice (the direction was already established via today's 3 feedback memories and the existing STANDARDS.md §Society of Minds CI-verifiable-artifact principle).

**Closeout protocol (post-implementation merge):** fill `raw/closeouts/2026-04-16-audit-hardening.md` (or whatever date implementation merges) from template, run `hooks/closeout-hook.sh`, update `OVERLORD_BACKLOG.md` to move the "Harden verify-completion audits..." Planned row to Done, close issue #160, update the 3 feedback memories (`feedback_audit_must_read_remote_head.md`, `feedback_codex_worktree_base_contamination.md`, `feedback_codex_spark_no_network.md`) to reference the new script/template as the enforcement mechanism.

## Out of scope (explicit)

- CI lint comparing codex-spark PR scope to plan file_paths (needs plan-shape standardization first).
- Rewriting verify-completion to be LLM-free.
- Updates to overlord / overlord-sweep / overlord-audit agents.
- Helper script in a non-bash language.
- Signing / sandboxing / curl-fallback for the helper script.
