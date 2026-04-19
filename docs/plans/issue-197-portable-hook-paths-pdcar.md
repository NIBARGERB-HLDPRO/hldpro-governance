# Issue #197 - Portable Hook Paths PDCA/R

## Plan

Issue #197 fixes a session-start portability bug in `.claude/settings.json`: hook commands point at `$HOME/Developer/HLDPRO/hldpro-governance/hooks/*.sh`, which only works on one local filesystem layout.

Scope stays narrow:

- Update `.claude/settings.json` hook commands for `pre-session-context.sh` and `code-write-gate.sh`.
- Use the issue-requested `git rev-parse --show-toplevel` pattern so hooks resolve from the active checkout or worktree.
- Prove the commands work from the repository root and from a nested directory.
- Record governance execution artifacts and closeout evidence.

Out of scope:

- Rewriting historical raw validation artifacts, old dispatch briefs, or environment runbook examples that intentionally preserve machine-specific evidence.
- Changing hook script behavior.
- Rolling this pattern into downstream repos. That remains separate issue-backed rollout work if needed.

## Do

Implementation updates `.claude/settings.json` command strings from hardcoded machine-layout paths to:

```json
"bash -c 'bash \"$(git rev-parse --show-toplevel 2>/dev/null || echo $PWD)/hooks/<hook>.sh\"'"
```

This keeps the canonical hook location at repo-root `hooks/`, works in isolated worktrees, and falls back to `$PWD` only when the shell is not inside a git checkout.

## Check

Acceptance criteria:

- All hook commands in `.claude/settings.json` use the portable `git rev-parse` form.
- No `$HOME/Developer/HLDPRO/hldpro-governance` literal remains in `.claude/settings.json`.
- Smoke tests execute both affected hook commands from repo root.
- Smoke tests execute both affected hook commands from a nested directory.
- E2E final AC: settings JSON parses, command extraction proves both commands are portable, direct hook execution succeeds from root/nested paths, execution scope passes, closeout hook passes, and Local CI Gate passes.

## Adjust

If smoke testing shows a hook depends on the caller's current directory instead of the repo root, the fix should stay in the command wrapper or hook-local root detection for that hook only. Do not expand into downstream repo rollout in this slice.

## Review

Reviewer focus should be:

- `.claude/settings.json` contains no machine-specific governance hook path.
- The replacement command still points at repo-root `hooks/`, not `.claude/hooks/`.
- Validation includes root and nested execution evidence.
- Historical evidence paths outside `.claude/settings.json` are not treated as blockers for this issue.
