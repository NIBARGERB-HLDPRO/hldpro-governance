# Cross-Review — Issue #229 Packet Queue and Controlled Orchestration

Date: 2026-04-17
Issue: #229
Reviewer: Claude Opus 4.6
Reviewed worktree: `/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-229-packet-queue-20260417`
Verdict: ACCEPTED_WITH_FOLLOWUP
Final disposition: Accepted after required follow-up changes

## Scope

Read-only alternate-family review of the #229 packet queue diff:

- `docs/schemas/som-packet.schema.yml`
- `scripts/orchestrator/packet_queue.py`
- `scripts/orchestrator/test_packet_queue.py`
- governance-surface classifier update for packet paths
- registry and data dictionary documentation
- #229 plan and PDCAR artifacts

## Findings

### F1 — Replay semantics included dry-run transitions in latest states

Severity: medium
Status: resolved

Reviewer finding: `replay_audit()` updated `latest_states` for accepted dry-run transitions. That is correct for logical audit replay, but ambiguous if a caller expects physical filesystem reconciliation.

Resolution: added a `replay_audit()` docstring clarifying that `latest_states` is the logical accepted state including dry-run rehearsals and is not a physical filesystem reconciliation report.

### F2 — Valid non-dry-run move path lacked direct test coverage

Severity: low
Status: resolved

Reviewer finding: tests covered dry-run happy path and blocked move paths, but not a successful `dry_run=False` file move.

Resolution: added `test_valid_packet_real_dispatch_moves_file`, asserting a valid `inbound -> dispatched` transition removes the source and creates the destination.

### O1 — CLI default moved files unless `--dry-run` was passed

Severity: low observation
Status: resolved

Resolution: changed the CLI to remain dry-run by default and require `--apply` for real file movement.

### O2 — PII enforcement is split across validator and queue

Severity: low observation
Status: accepted

Resolution: accepted as layered defense. The packet validator checks artifact-path PII patterns and the queue checks declared `governance.pii_mode` before dispatch.

## Accepted Review Notes

The reviewer verified that:

- The queue never executes packet payloads.
- Dispatch fails closed on schema failures, missing governance metadata, missing or unapproved plans, empty validation/review fields, and missing authorization.
- Existing packets remain schema-compatible because `governance` is optional at the top level.
- PII modes `tagged`, `detected`, and `lam_only` halt non-LAM dispatch.
- Packet queue paths are now governance surface.
- Atomic write and transition paths use temp-file replacement semantics.

## Result

All required review follow-up changes were applied before closeout validation.
