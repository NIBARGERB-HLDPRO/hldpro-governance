# Orchestrator Hitl relay queue

> 11 nodes · cohesion 0.45

## Key Concepts

- **test_hitl_relay_queue.py** (11 connections) — `scripts/orchestrator/test_hitl_relay_queue.py`
- **_request()** (9 connections) — `scripts/orchestrator/test_hitl_relay_queue.py`
- **_process()** (8 connections) — `scripts/orchestrator/test_hitl_relay_queue.py`
- **test_ambiguous_response_produces_clarification_and_no_instruction()** (3 connections) — `scripts/orchestrator/test_hitl_relay_queue.py`
- **test_expired_response_fails_closed_to_dead_letter()** (3 connections) — `scripts/orchestrator/test_hitl_relay_queue.py`
- **test_invalid_packet_lands_in_dead_letter_with_validation_errors()** (3 connections) — `scripts/orchestrator/test_hitl_relay_queue.py`
- **test_replay_reconstructs_decision_path()** (3 connections) — `scripts/orchestrator/test_hitl_relay_queue.py`
- **test_request_changes_response_preserves_feedback_path_without_approval()** (3 connections) — `scripts/orchestrator/test_hitl_relay_queue.py`
- **test_stale_session_fixture_produces_resume_packet()** (3 connections) — `scripts/orchestrator/test_hitl_relay_queue.py`
- **test_valid_approval_response_produces_bounded_session_instruction()** (3 connections) — `scripts/orchestrator/test_hitl_relay_queue.py`
- **test_local_cli_checkpoint_fixture_creates_valid_hitl_request()** (2 connections) — `scripts/orchestrator/test_hitl_relay_queue.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `scripts/orchestrator/test_hitl_relay_queue.py`

## Audit Trail

- EXTRACTED: 21 (41%)
- INFERRED: 30 (59%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*