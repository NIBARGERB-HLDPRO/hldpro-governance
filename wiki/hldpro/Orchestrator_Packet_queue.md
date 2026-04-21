# Orchestrator Packet queue

> 39 nodes · cohesion 0.12

## Key Concepts

- **packet_queue.py** (20 connections) — `scripts/orchestrator/packet_queue.py`
- **TestPacketQueue** (16 connections) — `scripts/orchestrator/test_packet_queue.py`
- **_packet()** (14 connections) — `scripts/orchestrator/test_packet_queue.py`
- **._write_inbound()** (14 connections) — `scripts/orchestrator/test_packet_queue.py`
- **transition_packet()** (8 connections) — `scripts/orchestrator/packet_queue.py`
- **validate_for_dispatch()** (7 connections) — `scripts/orchestrator/packet_queue.py`
- **_repo_relative_path()** (5 connections) — `scripts/orchestrator/packet_queue.py`
- **_run_cli()** (5 connections) — `scripts/orchestrator/packet_queue.py`
- **_write_transition_audit()** (4 connections) — `scripts/orchestrator/packet_queue.py`
- **.test_dispatch_accepts_json_execution_scope_ref()** (4 connections) — `scripts/orchestrator/test_packet_queue.py`
- **append_audit()** (3 connections) — `scripts/orchestrator/packet_queue.py`
- **_audit_path()** (3 connections) — `scripts/orchestrator/packet_queue.py`
- **ensure_queue()** (3 connections) — `scripts/orchestrator/packet_queue.py`
- **_load_plan()** (3 connections) — `scripts/orchestrator/packet_queue.py`
- **QueueDecision** (3 connections) — `scripts/orchestrator/packet_queue.py`
- **replay_audit()** (3 connections) — `scripts/orchestrator/packet_queue.py`
- **_validate_execution_scope_ref()** (3 connections) — `scripts/orchestrator/packet_queue.py`
- **_validate_fallback_ref()** (3 connections) — `scripts/orchestrator/packet_queue.py`
- **_validate_local_refs()** (3 connections) — `scripts/orchestrator/packet_queue.py`
- **test_packet_queue.py** (3 connections) — `scripts/orchestrator/test_packet_queue.py`
- **.test_dispatch_refuses_markdown_execution_scope_ref()** (3 connections) — `scripts/orchestrator/test_packet_queue.py`
- **.test_dispatch_refuses_schema_valid_packet_without_governance()** (3 connections) — `scripts/orchestrator/test_packet_queue.py`
- **.test_dispatch_requires_approved_issue_backed_plan()** (3 connections) — `scripts/orchestrator/test_packet_queue.py`
- **.test_dispatch_requires_local_review_artifact_refs_to_exist()** (3 connections) — `scripts/orchestrator/test_packet_queue.py`
- **.test_dry_run_authorization_does_not_allow_real_dispatch()** (3 connections) — `scripts/orchestrator/test_packet_queue.py`
- *... and 14 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `scripts/orchestrator/packet_queue.py`
- `scripts/orchestrator/test_packet_queue.py`

## Audit Trail

- EXTRACTED: 76 (44%)
- INFERRED: 98 (56%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*