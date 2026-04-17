# Orchestrator Packet queue

> 17 nodes · cohesion 0.30

## Key Concepts

- **TestPacketQueue** (15 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **_packet()** (13 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **._write_inbound()** (13 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **.test_dispatch_accepts_json_execution_scope_ref()** (4 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **test_packet_queue.py** (3 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **.test_dispatch_refuses_markdown_execution_scope_ref()** (3 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **.test_dispatch_requires_approved_issue_backed_plan()** (3 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **.test_dispatch_requires_local_review_artifact_refs_to_exist()** (3 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **.test_dry_run_authorization_does_not_allow_real_dispatch()** (3 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **.test_invalid_packet_fails_schema_before_dispatch()** (3 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **.test_pii_halt_reason_takes_precedence_over_known_failure_halt()** (3 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **.test_pii_packet_halts_before_non_lam_dispatch()** (3 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **.test_repeated_known_failure_context_halts_dispatch()** (3 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **.test_replay_counts_refused_events_deterministically()** (3 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **.test_valid_packet_dry_run_replays_through_queue_without_moving()** (3 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **.test_valid_packet_real_dispatch_moves_file()** (3 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`
- **._write_execution_scope()** (2 connections) — `hldpro-governance/scripts/orchestrator/test_packet_queue.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `hldpro-governance/scripts/orchestrator/test_packet_queue.py`

## Audit Trail

- EXTRACTED: 33 (40%)
- INFERRED: 50 (60%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*