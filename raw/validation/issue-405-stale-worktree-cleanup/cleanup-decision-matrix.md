# Issue #405 Cleanup Decision Matrix

Date: 2026-04-20
Mode: live local/remote/issue-state refresh before deletion.

## Removal Rule

Remove only when all are true:

- linked worktree, not primary
- clean working tree
- remote tracking branch is gone
- governing GitHub issue is closed
- not current #405

Preserve when any are true:

- primary worktree
- dirty working tree
- open issue
- live remote branch
- current lane

## Decisions

| Path | Branch | Issue State | Local State | Remote State | Decision | Reason |
|---|---|---:|---|---|---|---|
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance` | `issue-385-remote-mcp-vault-bootstrap-20260420` | #385 closed | clean before cleanup; later dirty with concurrent #407 backlog row | gone | keep | primary worktree; common `.git` owner |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-359-stampede` | `codex/issue-359-stampede-overlord-enrollment` | #359 not checked here | dirty | gone | keep | dirty graphify artifacts |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-384-backlog-drift` | `issue-384-backlog-drift-pdcar-20260420` | #384 closed | clean | gone | remove | safe stale linked worktree |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-386-automerge` | `issue-386-org-automerge-policy-20260420` | not needed | clean | live | keep | live remote branch |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-386-automerge-main` | `issue-386-org-automerge-policy-main-20260420` | not needed | clean | live | keep | live remote branch |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-391-automerge-pilot` | `issue-391-automerge-pilot-closeout-20260420` | not needed | clean | live | keep | live remote branch |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-393-lane-claim-gate` | `issue-393-lane-claim-gate-20260420` | #393 closed | clean | gone | remove | safe stale linked worktree |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-397-preworktree-lane-gate` | `issue-397-preworktree-lane-gate-20260420` | #397 closed | clean | gone | remove | safe stale linked worktree |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-398-consumer-pull-bootstrap` | `issue-398-consumer-pull-bootstrap-20260420` | not needed | clean | live | keep | live remote branch |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-398-consumer-pull-closeout` | `issue-398-consumer-pull-closeout-20260420` | not needed | clean | live | keep | live remote branch |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-400-runtime-lane-guard-proof` | `issue-400-runtime-lane-guard-proof-20260420` | #400 closed | clean | gone | remove | safe stale linked worktree |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-403-consumer-pull-adoption` | `issue-403-consumer-pull-adoption-20260420` | #403 open | dirty | tracks `origin/main` | keep | active open lane |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-405-stale-worktree-cleanup` | `issue-405-stale-worktree-cleanup-20260420` | #405 open | clean | tracks `origin/main` | keep | current lane |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-alerts` | `issue-374-remote-mcp-monitor-alerts-20260419` | #374 closed | clean | gone | remove | safe stale linked worktree |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-connectivity-preflight` | `issue-382-remote-mcp-operator-inbound-preflight-20260420` | #382 closed | clean | gone | remove | safe stale linked worktree |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-launchd-proof` | `issue-378-remote-mcp-launchd-live-proof-20260420` | #378 closed | clean | gone | remove | safe stale linked worktree |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-monitor` | `main` | n/a | clean | behind | keep | main worktree |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-operating-mode` | `issue-376-remote-mcp-monitor-operating-mode-20260420` | #376 closed | clean | gone | remove | safe stale linked worktree |
| `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-stage-d-live-tunnel` | `issue-370-remote-mcp-live-cloudflare-proof-20260419` | #370 closed | clean | gone | remove | safe stale linked worktree |

## Approved Removal Set

- `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-384-backlog-drift`
- `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-393-lane-claim-gate`
- `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-397-preworktree-lane-gate`
- `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-400-runtime-lane-guard-proof`
- `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-alerts`
- `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-connectivity-preflight`
- `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-launchd-proof`
- `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-operating-mode`
- `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-stage-d-live-tunnel`
