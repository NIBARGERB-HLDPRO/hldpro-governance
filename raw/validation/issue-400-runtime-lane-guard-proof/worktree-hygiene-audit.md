# Issue #400 Worktree Hygiene Audit

Date: 2026-04-20
Mode: no mutation; no worktree deletion, cleanup, reset, or checkout.

## Summary

This audit records the current local `hldpro-governance` sibling worktrees before any backlog item 5 work. It deliberately does not remove stale lanes because another session may own them.

## Status Snapshot

```text
/Users/bennibarger/Developer/HLDPRO/hldpro-governance
  issue-385-remote-mcp-vault-bootstrap-20260420...origin/issue-385-remote-mcp-vault-bootstrap-20260420 [gone]
  clean

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-359-stampede
  codex/issue-359-stampede-overlord-enrollment...origin/codex/issue-359-stampede-overlord-enrollment [gone]
  dirty: graphify-out/GRAPH_REPORT.md, graphify-out/graph.json

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-384-backlog-drift
  issue-384-backlog-drift-pdcar-20260420...origin/issue-384-backlog-drift-pdcar-20260420 [gone]
  clean

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-386-automerge
  issue-386-org-automerge-policy-20260420...origin/issue-386-org-automerge-policy-20260420
  clean

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-386-automerge-main
  issue-386-org-automerge-policy-main-20260420...origin/issue-386-org-automerge-policy-main-20260420
  clean

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-391-automerge-pilot
  issue-391-automerge-pilot-closeout-20260420...origin/issue-391-automerge-pilot-closeout-20260420
  clean

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-393-lane-claim-gate
  issue-393-lane-claim-gate-20260420...origin/issue-393-lane-claim-gate-20260420 [gone]
  clean

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-397-preworktree-lane-gate
  issue-397-preworktree-lane-gate-20260420...origin/issue-397-preworktree-lane-gate-20260420 [gone]
  clean

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-398-consumer-pull-bootstrap
  issue-398-consumer-pull-bootstrap-20260420...origin/issue-398-consumer-pull-bootstrap-20260420
  clean; treated as another active lane

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-400-runtime-lane-guard-proof
  issue-400-runtime-lane-guard-proof-20260420...origin/main
  current lane

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-alerts
  issue-374-remote-mcp-monitor-alerts-20260419...origin/issue-374-remote-mcp-monitor-alerts-20260419 [gone]
  clean

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-connectivity-preflight
  issue-382-remote-mcp-operator-inbound-preflight-20260420...origin/issue-382-remote-mcp-operator-inbound-preflight-20260420 [gone]
  clean

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-launchd-proof
  issue-378-remote-mcp-launchd-live-proof-20260420...origin/issue-378-remote-mcp-launchd-live-proof-20260420 [gone]
  clean

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-monitor
  main...origin/main [behind 46]
  clean

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-remote-mcp-operating-mode
  issue-376-remote-mcp-monitor-operating-mode-20260420...origin/issue-376-remote-mcp-monitor-operating-mode-20260420 [gone]
  clean

/Users/bennibarger/Developer/HLDPRO/hldpro-governance-stage-d-live-tunnel
  issue-370-remote-mcp-live-cloudflare-proof-20260419...origin/issue-370-remote-mcp-live-cloudflare-proof-20260419 [gone]
  clean
```

## Remote Branch Check

Live remote heads still present:

```text
2a6ef6e25e8e00573f70067b2e0da5add21d6680 refs/heads/issue-386-org-automerge-policy-20260420
4c408f75cc4b8997661103ec94a7261e4de6b91b refs/heads/issue-386-org-automerge-policy-main-20260420
4a93318424bbd6d2a4eb3a57277dba6633be5d6a refs/heads/issue-391-automerge-pilot-closeout-20260420
55041f994c7091550f51c6440b851ee46c1aa9ff refs/heads/issue-398-consumer-pull-bootstrap-20260420
```

## Recommendation

- Do not mutate `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-398-consumer-pull-bootstrap`; it is a separate lane.
- Do not clean `/Users/bennibarger/Developer/HLDPRO/hldpro-governance-issue-359-stampede` from this issue because it has dirty graphify artifacts.
- Stale clean worktrees with `[gone]` remote branches are cleanup candidates only after the operator confirms no active session owns them.
