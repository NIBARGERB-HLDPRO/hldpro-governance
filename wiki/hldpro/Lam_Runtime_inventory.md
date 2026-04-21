# Lam Runtime inventory

> 30 nodes · cohesion 0.11

## Key Concepts

- **build_inventory()** (10 connections) — `hldpro-governance/scripts/lam/runtime_inventory.py`
- **runtime_inventory.py** (9 connections) — `hldpro-governance/scripts/lam/runtime_inventory.py`
- **TestRuntimeInventory** (9 connections) — `hldpro-governance/scripts/lam/test_runtime_inventory.py`
- **load_pii_patterns()** (6 connections) — `hldpro-governance/scripts/windows-ollama/_pii.py`
- **pii_guardrail()** (6 connections) — `hldpro-governance/scripts/lam/runtime_inventory.py`
- **windows_ollama()** (6 connections) — `hldpro-governance/scripts/lam/runtime_inventory.py`
- **FakeResponse** (6 connections) — `hldpro-governance/scripts/lam/test_runtime_inventory.py`
- **detect_pii()** (5 connections) — `hldpro-governance/scripts/windows-ollama/_pii.py`
- **memory_budget()** (5 connections) — `hldpro-governance/scripts/lam/runtime_inventory.py`
- **main()** (4 connections) — `hldpro-governance/scripts/lam/runtime_inventory.py`
- **_run()** (4 connections) — `hldpro-governance/scripts/lam/runtime_inventory.py`
- **_pii.py** (3 connections) — `hldpro-governance/scripts/windows-ollama/_pii.py`
- **_iter_patterns()** (3 connections) — `hldpro-governance/scripts/windows-ollama/_pii.py`
- **import_available()** (3 connections) — `hldpro-governance/scripts/lam/runtime_inventory.py`
- **local_runtime()** (3 connections) — `hldpro-governance/scripts/lam/runtime_inventory.py`
- **mac_hardware()** (3 connections) — `hldpro-governance/scripts/lam/runtime_inventory.py`
- **.test_qwen36_config_and_inventory_budget_stay_aligned()** (3 connections) — `hldpro-governance/scripts/lam/test_runtime_inventory.py`
- **.test_windows_tags_lists_models_without_payloads()** (3 connections) — `hldpro-governance/scripts/lam/test_runtime_inventory.py`
- **test_runtime_inventory.py** (2 connections) — `hldpro-governance/scripts/lam/test_runtime_inventory.py`
- **.test_inventory_has_no_payload_routing()** (2 connections) — `hldpro-governance/scripts/lam/test_runtime_inventory.py`
- **.test_local_qwen_ladder_and_gemma_shadow_policy_are_explicit()** (2 connections) — `hldpro-governance/scripts/lam/test_runtime_inventory.py`
- **.test_pii_guardrail_happy_path_detects_email_and_allows_clean_probe()** (2 connections) — `hldpro-governance/scripts/lam/test_runtime_inventory.py`
- **.test_pii_guardrail_missing_patterns_fails_closed()** (2 connections) — `hldpro-governance/scripts/lam/test_runtime_inventory.py`
- **.test_qwen36_large_worker_is_mac_mlx_on_demand_only()** (2 connections) — `hldpro-governance/scripts/lam/test_runtime_inventory.py`
- **.test_windows_timeout_reports_unreachable_without_payloads()** (2 connections) — `hldpro-governance/scripts/lam/test_runtime_inventory.py`
- *... and 5 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `hldpro-governance/scripts/lam/runtime_inventory.py`
- `hldpro-governance/scripts/lam/test_runtime_inventory.py`
- `hldpro-governance/scripts/windows-ollama/_pii.py`

## Audit Trail

- EXTRACTED: 77 (70%)
- INFERRED: 33 (30%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*