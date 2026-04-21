# Ops Slack temporal handoff worker

> 41 nodes · cohesion 0.08

## Key Concepts

- **main()** (11 connections) — `local-ai-machine/scripts/ops/test_slack_temporal_handoff_worker_contract.py`
- **slack_temporal_handoff_worker.py** (10 connections) — `local-ai-machine/scripts/ops/slack_temporal_handoff_worker.py`
- **process_approved_row()** (10 connections) — `local-ai-machine/scripts/ops/slack_temporal_handoff_worker.py`
- **main()** (8 connections) — `local-ai-machine/scripts/ops/run_slack_temporal_handoff_e2e_proof.py`
- **main()** (8 connections) — `local-ai-machine/scripts/ops/test_reconciliation_transport_contract.py`
- **send_vsock()** (7 connections) — `local-ai-machine/scripts/ops/reconciliation_transport.py`
- **get_handoff_mode()** (7 connections) — `local-ai-machine/scripts/ops/slack_temporal_handoff_worker.py`
- **send()** (6 connections) — `local-ai-machine/scripts/ops/reconciliation_transport.py`
- **build_handoff_signal()** (6 connections) — `local-ai-machine/scripts/ops/slack_temporal_handoff_worker.py`
- **classify_flow_class()** (6 connections) — `local-ai-machine/scripts/ops/slack_temporal_handoff_worker.py`
- **emit_temporal_signal()** (6 connections) — `local-ai-machine/scripts/ops/slack_temporal_handoff_worker.py`
- **should_use_temporal()** (6 connections) — `local-ai-machine/scripts/ops/slack_temporal_handoff_worker.py`
- **validate_correlation()** (6 connections) — `local-ai-machine/scripts/ops/slack_temporal_handoff_worker.py`
- **send_file()** (5 connections) — `local-ai-machine/scripts/ops/reconciliation_transport.py`
- **Exception** (4 connections)
- **reconciliation_transport.py** (4 connections) — `local-ai-machine/scripts/ops/reconciliation_transport.py`
- **run_slack_temporal_handoff_e2e_proof.py** (4 connections) — `local-ai-machine/scripts/ops/run_slack_temporal_handoff_e2e_proof.py`
- **TransportError** (4 connections) — `local-ai-machine/scripts/ops/reconciliation_transport.py`
- **run_temporal_cli()** (4 connections) — `local-ai-machine/scripts/ops/run_slack_temporal_handoff_e2e_proof.py`
- **HandoffError** (4 connections) — `local-ai-machine/scripts/ops/slack_temporal_handoff_worker.py`
- **main()** (4 connections) — `local-ai-machine/scripts/ops/slack_temporal_handoff_worker.py`
- **write_proof()** (3 connections) — `local-ai-machine/scripts/ops/run_slack_temporal_handoff_e2e_proof.py`
- **test_reconciliation_transport_contract.py** (2 connections) — `local-ai-machine/scripts/ops/test_reconciliation_transport_contract.py`
- **test_slack_temporal_handoff_worker_contract.py** (2 connections) — `local-ai-machine/scripts/ops/test_slack_temporal_handoff_worker_contract.py`
- **utc_now()** (2 connections) — `local-ai-machine/scripts/ops/run_slack_temporal_handoff_e2e_proof.py`
- *... and 16 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `local-ai-machine/scripts/ops/reconciliation_transport.py`
- `local-ai-machine/scripts/ops/run_slack_temporal_handoff_e2e_proof.py`
- `local-ai-machine/scripts/ops/slack_temporal_handoff_worker.py`
- `local-ai-machine/scripts/ops/test_reconciliation_transport_contract.py`
- `local-ai-machine/scripts/ops/test_slack_temporal_handoff_worker_contract.py`

## Audit Trail

- EXTRACTED: 114 (72%)
- INFERRED: 44 (28%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*