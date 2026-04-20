# Issue #405 Cleanup Execution Evidence

Date: 2026-04-20

## Command

```bash
for wt in \
  /Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-384-backlog-drift \
  /Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-393-lane-claim-gate \
  /Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-397-preworktree-lane-gate \
  /Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-400-runtime-lane-guard-proof \
  /Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-alerts \
  /Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-connectivity-preflight \
  /Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-launchd-proof \
  /Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-operating-mode \
  /Users/bennibarger/Developer/HLDPRO/hldpro-governance-stage-d-live-tunnel; do
  echo "REMOVE $wt"
  git worktree remove "$wt"
done
```

## Output

```text
REMOVE /Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-384-backlog-drift
REMOVE /Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-393-lane-claim-gate
REMOVE /Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-397-preworktree-lane-gate
REMOVE /Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-400-runtime-lane-guard-proof
REMOVE /Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-alerts
REMOVE /Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-connectivity-preflight
REMOVE /Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-launchd-proof
REMOVE /Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-operating-mode
REMOVE /Users/bennibarger/Developer/HLDPRO/hldpro-governance-stage-d-live-tunnel
```

Result: all approved stale linked worktrees were removed with `git worktree remove`.
