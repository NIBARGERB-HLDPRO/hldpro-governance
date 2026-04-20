# Issue #400 Installed Hook Proof

Date: 2026-04-20
Hook: `/Users/bennibarger/.claude/hooks/branch-switch-guard.sh`
Mode: direct PreToolUse JSON input; no `git worktree add` command was executed by Git.

## Command Harness

```bash
hook=/Users/bennibarger/.claude/hooks/branch-switch-guard.sh
run_case() {
  name="$1"
  command_text="$2"
  printf '\n## %s\nCOMMAND=%s\n' "$name" "$command_text"
  printf '{"tool_input":{"command":%s}}\n' "$(printf '%s' "$command_text" | jq -Rs .)" | "$hook"
  code=$?
  printf 'EXIT=%s\n' "$code"
}
```

## Results

### Blocked Unmarked Issue Worktree

```text
COMMAND=git worktree add -b issue-401-unclaimed /tmp/hldpro-issue-401-unclaimed origin/main
BLOCKED: Issue worktree creation requires an explicit lane claim or planning bootstrap.
EXIT=2
```

### Allowed Bootstrap Issue Worktree

```text
COMMAND=HLDPRO_LANE_CLAIM_BOOTSTRAP=1 git worktree add -b issue-401-bootstrap /tmp/hldpro-issue-401-bootstrap origin/main
EXIT=0
```

### Allowed Matching Claimed Scope

```text
COMMAND=HLDPRO_LANE_CLAIM_SCOPE=raw/execution-scopes/2026-04-20-issue-400-runtime-lane-guard-proof-implementation.json git worktree add -b issue-400-runtime-lane-guard-proof-extra /tmp/hldpro-issue-400-extra origin/main
EXIT=0
```

### Blocked Mismatched Claimed Scope

```text
COMMAND=HLDPRO_LANE_CLAIM_SCOPE=raw/execution-scopes/2026-04-20-issue-400-runtime-lane-guard-proof-implementation.json git worktree add -b issue-401-mismatch /tmp/hldpro-issue-401-mismatch origin/main
BLOCKED: Issue worktree creation requires an explicit lane claim or planning bootstrap.
EXIT=2
```

### Allowed Non-Issue Worktree

```text
COMMAND=git worktree add -b scratch-runtime-lane-guard /tmp/hldpro-scratch-runtime-lane-guard origin/main
EXIT=0
```

## Conclusion

The installed runtime hook enforces the #397 issue-lane startup contract: unclaimed issue worktree creation is blocked before filesystem side effects, explicit planning bootstrap is allowed, matching claimed scopes are allowed, mismatched scopes are blocked, and non-issue worktrees remain allowed.
