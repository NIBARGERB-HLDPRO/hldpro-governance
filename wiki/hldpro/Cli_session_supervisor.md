# Cli session supervisor

> 27 nodes · cohesion 0.16

## Key Concepts

- **test_cli_session_supervisor.py** (15 connections) — `scripts/test_cli_session_supervisor.py`
- **cli_session_supervisor.py** (12 connections) — `scripts/cli_session_supervisor.py`
- **stream_attempt()** (10 connections) — `scripts/cli_session_supervisor.py`
- **events()** (8 connections) — `scripts/test_cli_session_supervisor.py`
- **run_supervisor()** (8 connections) — `scripts/test_cli_session_supervisor.py`
- **write_fake()** (8 connections) — `scripts/test_cli_session_supervisor.py`
- **test_intermittent_output_avoids_idle_timeout()** (4 connections) — `scripts/test_cli_session_supervisor.py`
- **test_nonzero_failure_is_recorded_without_retry()** (4 connections) — `scripts/test_cli_session_supervisor.py`
- **test_retry_halts_after_one_additional_timeout()** (4 connections) — `scripts/test_cli_session_supervisor.py`
- **test_retry_once_can_recover_from_timeout()** (4 connections) — `scripts/test_cli_session_supervisor.py`
- **test_silent_stall_hits_idle_timeout_and_kills_process()** (4 connections) — `scripts/test_cli_session_supervisor.py`
- **test_success_event_captures_stdout_and_schema_fields()** (4 connections) — `scripts/test_cli_session_supervisor.py`
- **test_total_timeout_overrides_active_output()** (4 connections) — `scripts/test_cli_session_supervisor.py`
- **main()** (3 connections) — `scripts/cli_session_supervisor.py`
- **append_jsonl()** (2 connections) — `scripts/cli_session_supervisor.py`
- **AttemptResult** (2 connections) — `scripts/cli_session_supervisor.py`
- **build_command()** (2 connections) — `scripts/cli_session_supervisor.py`
- **event_paths()** (2 connections) — `scripts/cli_session_supervisor.py`
- **kill_group()** (2 connections) — `scripts/cli_session_supervisor.py`
- **parse_args()** (2 connections) — `scripts/cli_session_supervisor.py`
- **session_id()** (2 connections) — `scripts/cli_session_supervisor.py`
- **sha256_bytes()** (2 connections) — `scripts/cli_session_supervisor.py`
- **utcnow()** (2 connections) — `scripts/cli_session_supervisor.py`
- **test_claude_native_argv_preserves_explicit_verbose()** (1 connections) — `scripts/test_cli_session_supervisor.py`
- **test_claude_stream_json_native_argv_adds_verbose()** (1 connections) — `scripts/test_cli_session_supervisor.py`
- *... and 2 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `scripts/cli_session_supervisor.py`
- `scripts/test_cli_session_supervisor.py`

## Audit Trail

- EXTRACTED: 52 (46%)
- INFERRED: 62 (54%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*