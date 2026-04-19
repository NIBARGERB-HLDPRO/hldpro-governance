# Orchestrator Delegation gate

> 22 nodes · cohesion 0.15

## Key Concepts

- **delegation_gate.py** (12 connections) — `scripts/orchestrator/delegation_gate.py`
- **test_delegation_gate.py** (9 connections) — `scripts/orchestrator/test_delegation_gate.py`
- **decide()** (6 connections) — `scripts/orchestrator/delegation_gate.py`
- **deterministic_match()** (5 connections) — `scripts/orchestrator/delegation_gate.py`
- **GateDecision** (5 connections) — `scripts/orchestrator/delegation_gate.py`
- **_run_cli()** (4 connections) — `scripts/orchestrator/delegation_gate.py`
- **apply_policy()** (3 connections) — `scripts/orchestrator/delegation_gate.py`
- **classifier_match()** (3 connections) — `scripts/orchestrator/delegation_gate.py`
- **_contains_term()** (3 connections) — `scripts/orchestrator/delegation_gate.py`
- **load_rules()** (3 connections) — `scripts/orchestrator/delegation_gate.py`
- **_normalize()** (3 connections) — `scripts/orchestrator/delegation_gate.py`
- **.as_dict()** (2 connections) — `scripts/orchestrator/delegation_gate.py`
- **_load_classifier()** (2 connections) — `scripts/orchestrator/delegation_gate.py`
- **OwnerRule** (2 connections) — `scripts/orchestrator/delegation_gate.py`
- **test_bypass_flag_allows_and_records_source()** (1 connections) — `scripts/orchestrator/test_delegation_gate.py`
- **test_classifier_fallback_warns_when_rules_are_inconclusive()** (1 connections) — `scripts/orchestrator/test_delegation_gate.py`
- **test_explore_allows_non_implementation_routing_context()** (1 connections) — `scripts/orchestrator/test_delegation_gate.py`
- **test_explore_is_warn_only_for_implementation_scoped_owned_work()** (1 connections) — `scripts/orchestrator/test_delegation_gate.py`
- **test_high_confidence_agent_owned_work_blocks()** (1 connections) — `scripts/orchestrator/test_delegation_gate.py`
- **test_high_confidence_bash_owned_work_blocks()** (1 connections) — `scripts/orchestrator/test_delegation_gate.py`
- **test_read_is_never_gated()** (1 connections) — `scripts/orchestrator/test_delegation_gate.py`
- **test_rules_cover_all_da_delegation_task_types()** (1 connections) — `scripts/orchestrator/test_delegation_gate.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `scripts/orchestrator/delegation_gate.py`
- `scripts/orchestrator/test_delegation_gate.py`

## Audit Trail

- EXTRACTED: 42 (60%)
- INFERRED: 28 (40%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*