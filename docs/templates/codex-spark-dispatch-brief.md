## Preflight

Run this first and include the full command output in your session notes:

```bash
bash scripts/codex-preflight.sh --log
```

Do not start the issue slice until preflight completes with PASS.

## Worktree discipline (HARD GATE)

Create and verify worktrees exactly as below before any commit:

```bash
cd ~/Developer/HLDPRO/<repo>
git fetch origin main
git worktree add -b <branch-name> /tmp/<worktree-name> origin/main
cd /tmp/<worktree-name>
git log --oneline origin/main..HEAD   # HARD GATE: must be empty before first commit
```

If `git log --oneline origin/main..HEAD` shows any lines, HALT and re-create the worktree from a fresh `origin/main`.

## Non-destructive editing

For committed JSON settings (`.claude/settings.json`), use JSON-merge updates only; never overwrite the file wholesale.
For `.gitignore`, apply minimal surgical patches that preserve existing generated lines.
For CLAUDE.md-style docs, use append-only updates at the end of the file unless a full rewrite is explicitly requested.

Use issue #154 as prior art for this exact edit discipline and audit trail.

## Diff scope cap

Per-sprint `file_paths` are enforced. Do not modify anything outside the current sprint’s declared files.
If `git diff --name-only origin/main..HEAD` shows a fourth file, immediately HALT and report the violation.

## No push / no gh

Codex-spark is a local executor with no remote network operations in this environment.
Do not run `git push`, do not call `gh` for remote ops, and do not open PRs.
See `feedback_codex_spark_no_network.md`.

## Report format

At each handoff, include:

- branch name
- worktree path
- `git log --oneline origin/main..HEAD`
- `git diff --name-only origin/main..HEAD`
- blockers (if any)

## Example usage

Issue #154 — Pre-session hook standardization

- Branch: `issue-154-pre-session-hook`
- Worktree: `/tmp/issue-154-pre-session-hook`
- Start command:

```bash
cd ~/Developer/HLDPRO/hldpro-governance
git fetch origin main
git worktree add -b issue-154-pre-session-hook /tmp/issue-154-pre-session-hook origin/main
cd /tmp/issue-154-pre-session-hook
git log --oneline origin/main..HEAD
```

- Verified log: `<empty>`
- H2 sections written: Preflight, Worktree discipline, Non-destructive editing, Diff scope cap, No push / no gh, Report format
- 1st sprint files: `agents/pre-session.md`, `agents/pre-session-hook.md`
- 2nd sprint file: `docs/templates/codex-spark-dispatch-brief.md`
- 3rd sprint file: `docs/agents.md`
- Reported blockers: none
- Diff scope after completion: exactly the files declared by each sprint
