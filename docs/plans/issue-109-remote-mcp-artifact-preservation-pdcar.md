# Issue #109 - Remote MCP Bridge Artifact Preservation PDCAR

Date: 2026-04-19
Branch: `issue-109-preserve-remote-mcp-plan-20260419`
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109

## Plan

Issue #109 is the governing Cloud -> Local MCP Bridge epic. Its issue body pointed at planning and cross-review artifacts that only existed on stale remote branch `feat/remote-mcp-bridge`. Before deleting that stale branch, preserve the useful governance history on `main` and leave implementation stages tracked by #109.

Acceptance criteria:

- `raw/inbox/2026-04-14-remote-mcp-bridge-plan.md` exists on the active branch.
- `raw/cross-review/2026-04-14-remote-mcp-bridge.md` exists on the active branch with historical `schema_version: v1` metadata so current no-self-approval checks can parse it.
- `raw/handoff/2026-04-14-session-end.md` exists on the active branch for session continuity.
- `docs/exception-register.md` records active exception `SOM-RMB-ROUND2-WAIVED-001` until 2026-05-14.
- Stale `_worktrees/gov-remote-mcp/...` references are replaced with repo-local `raw/inbox/...` references.
- The stale `docs/windows-ollama-sprint3-closeout` branch is confirmed redundant before deletion because its substantive closeout and decision artifacts already match `main`.
- Final AC: local governance validation and GitHub PR checks pass before stale remote branch deletion.

## Do

- Restored the Remote MCP Bridge plan, cross-review/resolution artifact, and session handoff from `origin/feat/remote-mcp-bridge`.
- Added `schema_version: v1` to the historical rejected cross-review artifact for compatibility with current parser gates.
- Restored the active round-2 waiver entry to the exception register.
- Updated Windows-Ollama references that previously pointed to a private worktree path.
- Added issue #109 to the active backlog mirror for this preservation slice.

## Check

Validation commands are recorded in `raw/validation/2026-04-19-issue-109-remote-mcp-artifact-preservation.md`.

Required checks:

| Check | Expected |
|---|---|
| restored file existence checks | PASS |
| stale worktree reference search | PASS |
| cross-review no-self-approval parser check | PASS |
| structured plan JSON validation | PASS |
| execution-scope assertion | PASS |
| Local CI Gate | PASS |
| Stage 6 closeout hook | PASS |

## Adjust

The Remote MCP cross-review remains intentionally historical: it records a rejected round 1 plus operator-waived round 2, not a merge-approval artifact for new architecture changes. This slice does not implement the bridge and does not close issue #109.

## Review

No alternate-family architecture review is required for this preservation slice because the architecture decision is not changing. The preserved artifact itself records the original Architect-Claude draft, Architect-Codex rejection, revised plan response, and operator waiver.
