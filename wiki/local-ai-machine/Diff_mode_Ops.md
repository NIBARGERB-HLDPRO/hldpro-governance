# Diff mode Ops

> 373 nodes · cohesion 0.01

## Key Concepts

- **read_text()** (430 connections) — `local-ai-machine/scripts/ops/run_general_self_learning_loop.py`
- **synthesize()** (27 connections) — `local-ai-machine/scripts/edge/diff_mode_synthesizer.py`
- **_sample_payload()** (17 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **_resolve_active_masks()** (8 connections) — `local-ai-machine/scripts/edge/diff_mode_synthesizer.py`
- **test_diff_mode_contract.py** (8 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **TestSynthesizer** (7 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **TestSynthesizerRedaction** (6 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **TestPayloadValidation** (5 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **.test_audit_has_diff_mode_intake_event()** (5 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **.test_mask_attestation_matches_caller_policy()** (5 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **.test_ais_audit_has_redaction_applied_false()** (5 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **.test_hp_app_audit_has_redaction_applied_true()** (5 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **test_remote_assets.py** (4 connections) — `local-ai-machine/services/som-mcp/tests/test_remote_assets.py`
- **TestCallerMaskPolicy** (4 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **.test_drift_report_has_diff_stats()** (4 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **.test_remediation_plan_has_prompt_template()** (4 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **.test_hp_app_produces_redaction_attestation()** (4 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **.test_hp_app_with_phi_redacts_diff()** (4 connections) — `local-ai-machine/tests/test_diff_mode_contract.py`
- **test_install_renders_launchagent_with_active_checkout_pythonpath()** (4 connections) — `local-ai-machine/services/som-mcp/tests/test_install_contract.py`
- **test_install_remote_bridge_renders_self_contained_launchagent()** (4 connections) — `local-ai-machine/services/som-mcp/tests/test_remote_assets.py`
- **_load_caller_mask_policy()** (3 connections) — `local-ai-machine/scripts/edge/diff_mode_synthesizer.py`
- **diff_mode_synthesizer.py** (3 connections) — `local-ai-machine/scripts/edge/diff_mode_synthesizer.py`
- **test_boot_run_contract.py** (3 connections) — `local-ai-machine/scripts/microvm/test_boot_run_contract.py`
- **test_run_scavenger_workload_contract.py** (3 connections) — `local-ai-machine/scripts/microvm/test_run_scavenger_workload_contract.py`
- **test_teardown_telemetry_contract.py** (3 connections) — `local-ai-machine/scripts/microvm/test_teardown_telemetry_contract.py`
- *... and 348 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `local-ai-machine/scripts/edge/diff_mode_synthesizer.py`
- `local-ai-machine/scripts/edge/test_critic_api_postgres_contract.py`
- `local-ai-machine/scripts/edge/test_edge_runtime_parity.py`
- `local-ai-machine/scripts/edge/test_supabase_critic_runtime_contract.py`
- `local-ai-machine/scripts/microvm/test_boot_run_contract.py`
- `local-ai-machine/scripts/microvm/test_run_scavenger_workload_contract.py`
- `local-ai-machine/scripts/microvm/test_teardown_telemetry_contract.py`
- `local-ai-machine/scripts/ops/run_general_self_learning_loop.py`
- `local-ai-machine/scripts/ops/test_adaptive_control_ingestion_contract.py`
- `local-ai-machine/scripts/ops/test_adaptive_control_memory_budget_contract.py`
- `local-ai-machine/scripts/ops/test_adaptive_control_package_contract.py`
- `local-ai-machine/scripts/ops/test_adaptive_control_runtime_contract.py`
- `local-ai-machine/scripts/ops/test_adaptive_kill_switch_trip.py`
- `local-ai-machine/scripts/ops/test_admin_fs_attack_contract.py`
- `local-ai-machine/scripts/ops/test_agent_architecture_manifest_convergence_contract.py`
- `local-ai-machine/scripts/ops/test_agent_config_sql_contract.py`
- `local-ai-machine/scripts/ops/test_branch_residue_classification_contract.py`
- `local-ai-machine/scripts/ops/test_bridge_watchdog_task_contract.py`
- `local-ai-machine/scripts/ops/test_clean_working_branch_governance_contract.py`
- `local-ai-machine/scripts/ops/test_evaluate_scavenger_teardown_alerts_contract.py`

## Audit Trail

- EXTRACTED: 936 (62%)
- INFERRED: 582 (38%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*