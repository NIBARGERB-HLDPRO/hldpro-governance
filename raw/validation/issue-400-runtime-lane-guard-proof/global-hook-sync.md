# Issue #400 Global Hook Sync Evidence

Date: 2026-04-20

## Before Sync

Command:

```bash
shasum -a 256 hooks/branch-switch-guard.sh /Users/bennibarger/.claude/hooks/branch-switch-guard.sh
```

Output:

```text
5bbe3c93d4ae36c42e8aae862c9ee3dcdf5f655c1f42316cfe4fe2d05aa38f8d  hooks/branch-switch-guard.sh
38ca235c33b5d22b196f8a5169caf2207d0f3c5c0a681ab2ebff5bca877cff10  /Users/bennibarger/.claude/hooks/branch-switch-guard.sh
```

Result: drift found. The installed global hook was stale relative to repo `origin/main`.

## Sync Action

Command:

```bash
mkdir -p /Users/bennibarger/.claude/hooks
cp hooks/branch-switch-guard.sh /Users/bennibarger/.claude/hooks/branch-switch-guard.sh
chmod +x /Users/bennibarger/.claude/hooks/branch-switch-guard.sh
```

## After Sync

Command:

```bash
shasum -a 256 hooks/branch-switch-guard.sh /Users/bennibarger/.claude/hooks/branch-switch-guard.sh
```

Output:

```text
5bbe3c93d4ae36c42e8aae862c9ee3dcdf5f655c1f42316cfe4fe2d05aa38f8d  hooks/branch-switch-guard.sh
5bbe3c93d4ae36c42e8aae862c9ee3dcdf5f655c1f42316cfe4fe2d05aa38f8d  /Users/bennibarger/.claude/hooks/branch-switch-guard.sh
```

Result: installed global hook matches the repo-owned hook.
