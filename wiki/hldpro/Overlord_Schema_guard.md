# Overlord Schema guard

> 16 nodes · cohesion 0.32

## Key Concepts

- **_run_hook()** (13 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **TestSchemaGuardHook** (13 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **_payload()** (12 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **test_schema_guard_hook.py** (3 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **.test_allowed_read_only_command_remains_allowed()** (3 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **.test_blocked_bash_file_write_has_stderr()** (3 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **.test_common_read_only_analysis_pipelines_remain_allowed()** (3 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **.test_missing_helper_fails_closed()** (3 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **.test_missing_schema_has_explicit_stderr()** (3 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **.test_python_file_write_policy_block_has_stderr()** (3 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **.test_quoted_awk_comparison_remains_allowed()** (3 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **.test_quoted_jq_comparison_remains_allowed()** (3 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **.test_trivial_plan_bypass_still_reaches_som_write_block()** (3 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **.test_unknown_helper_decision_fails_closed()** (3 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **.test_validator_nonzero_is_summarized()** (3 connections) — `scripts/overlord/test_schema_guard_hook.py`
- **.test_malformed_input_payload_has_stderr()** (2 connections) — `scripts/overlord/test_schema_guard_hook.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `scripts/overlord/test_schema_guard_hook.py`

## Audit Trail

- EXTRACTED: 30 (39%)
- INFERRED: 46 (61%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*