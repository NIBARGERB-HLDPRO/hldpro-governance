# Graph Report - .  (2026-04-21)

## Corpus Check
- 106 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1392 nodes · 2798 edges · 70 communities detected
- Extraction: 48% EXTRACTED · 52% INFERRED · 0% AMBIGUOUS · INFERRED: 1455 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `WindowsOllamaSubmitter` - 48 edges
2. `PiiDetectionError` - 44 edges
3. `ModelNotAllowedError` - 44 edges
4. `EndpointUnreachableError` - 44 edges
5. `TestAssertExecutionScope` - 34 edges
6. `RepoFixture` - 30 edges
7. `_tier1_packet()` - 29 edges
8. `AuditWriter` - 28 edges
9. `TestGovernanceSurfacePlanGate` - 24 edges
10. `TestLocalCiGate` - 20 edges

## Surprising Connections (you probably didn't know these)
- `ValidateLocationTests` --uses--> `Finding`  [INFERRED]
  tests/test_codex_ingestion.py → scripts/overlord/codex_ingestion.py
- `MockProvider` --uses--> `RunManifest`  [INFERRED]
  packages/hldpro-sim/tests/test_stampede_consumer_proof.py → packages/hldpro-sim/hldprosim/artifacts.py
- `Submit requests to Windows-Ollama endpoint with PII detection and allowlist enfo` --uses--> `AuditWriter`  [INFERRED]
  scripts/windows-ollama/submit.py → scripts/windows-ollama/audit.py
- `Initialize the submitter.          Args:             endpoint: Windows-Ollama en` --uses--> `AuditWriter`  [INFERRED]
  scripts/windows-ollama/submit.py → scripts/windows-ollama/audit.py
- `Load PII patterns from pii_patterns.yml.` --uses--> `AuditWriter`  [INFERRED]
  scripts/windows-ollama/submit.py → scripts/windows-ollama/audit.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.04
Nodes (73): AuditWriter, canonical_json(), compute_entry_hmac(), compute_sha256(), Write an audit entry. Returns True if successful, False otherwise.          Args, Return canonical JSON for HMAC computation., Write or update today's manifest., Compute SHA256 hash of bytes. (+65 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (47): Modify first_hash in manifest and verify fails., Test that truncated file (missing last line) breaks manifest., Delete last line and verify detects entry_count mismatch., Test that duplicate line (replay) breaks seq monotonicity., Duplicate a line and verify detects non-monotonic seq., Test that tampering with a line breaks the chain., Tamper with line N and verify fails at line N+1., Test that replacing entry_hmac with wrong value fails verification. (+39 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (24): BaseHTTPRequestHandler, build_parser(), build_payload(), _call_fixture(), _call_live(), Check, _fixture_server(), _FixtureMcpHandler (+16 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (19): _make_parent_packet(), Cross-family independence violated: both planners are anthropic., anthropic + openai is fine., Parent file absent → warn, don't refuse., Sanity: the patterns file should be present in this worktree., Non-LAM role with PII artifact path must be refused., worker-lam role is allowed to handle PII artifacts., When pii-patterns.yml is absent, validator must refuse (not silently pass). (+11 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (20): ABC, BaseAggregator, ArtifactWriter, RunManifest, BaseAggregator, BaseModel, SimulationEngine, PersonaLoader (+12 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (39): _expand_home(), governed_repos(), GovernedRepo, load_registry(), repo_names_enabled_for(), repos_enabled_for(), repos_root(), build_payload() (+31 more)

### Community 6 - "Community 6"
Cohesion: 0.1
Nodes (34): append_fail_fast_block_entry(), append_fail_fast_candidate(), append_fail_fast_table_entry(), append_progress_candidate(), bounded_text(), build_parser(), build_review_context(), build_schema_file() (+26 more)

### Community 7 - "Community 7"
Cohesion: 0.2
Nodes (4): _git(), RepoFixture, TestAssertExecutionScope, _working_directory()

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (38): _branch_issue_number(), build_argument_parser(), _build_summary(), _changed_files_from_git(), ChangedFiles, _check_exit_code(), _check_matches_changed_files(), CheckResult (+30 more)

### Community 9 - "Community 9"
Cohesion: 0.15
Nodes (26): atomic_write_yaml(), build_report(), _date_from_text(), duplicate_counts(), enrich_packet(), _entry_id(), LearningEntry, LearningMatch (+18 more)

### Community 10 - "Community 10"
Cohesion: 0.13
Nodes (19): add_common_args(), build_plan(), build_refresh_command(), execute_refresh(), find_target(), git_hook_paths(), HelperError, HookPlan (+11 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (28): _load(), test_duplicate_reply_cannot_produce_instruction(), test_expired_reply_cannot_produce_instruction(), test_low_confidence_clarify_decision_passes_without_instruction(), test_low_confidence_non_clarify_decision_fails_closed(), test_pii_external_channel_fails_closed(), test_response_requires_notification_and_response_ids(), test_session_instruction_requires_matching_target_session() (+20 more)

### Community 12 - "Community 12"
Cohesion: 0.1
Nodes (30): _find_packet_file(), _load_packet(), load_pii_patterns(), _load_schema(), Load and compile PII patterns from pii-patterns.yml., Enforce cross-family independence for tier-1 dual-planner packets.      When pri, Refuse if any consecutive pair in the parent chain shares model_id across differ, Enforce expected handoff sequence with no tier jumps. (+22 more)

### Community 13 - "Community 13"
Cohesion: 0.13
Nodes (22): build_parser(), _env_has_live_markers(), main(), _run_fixture(), _run_live(), _scan_evidence_dir(), _stage_d_args(), _build_fixture_server() (+14 more)

### Community 14 - "Community 14"
Cohesion: 0.19
Nodes (28): append_audit(), atomic_write_json(), _base_packet(), _build_decision_packet(), _build_instruction_packet(), build_request(), _build_response_packet(), _build_resume_packet() (+20 more)

### Community 15 - "Community 15"
Cohesion: 0.16
Nodes (28): aggregate_file_scores(), augment_workflow_doc_candidates(), baseline_results(), build_summary(), build_trace(), emit_usage_events(), estimate_tokens(), evaluate_relevance() (+20 more)

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (26): _branch_issue_number(), _changed_paths(), _changed_paths_from_file(), check_scope(), _current_branch(), ExecutionScope, _format_path(), _git_root() (+18 more)

### Community 17 - "Community 17"
Cohesion: 0.18
Nodes (24): add_common_args(), apply(), _build_local_ci_plan(), build_plan(), _consumer_record(), _consumer_record_relpath(), _ensure_relative_to(), _fail() (+16 more)

### Community 18 - "Community 18"
Cohesion: 0.11
Nodes (14): _all_executable_lines(), _all_run_commands(), check_contract(), _contains_main_branch(), _executable_lines(), _failures_for_text(), _has_executable_line_starting_with(), _load_workflow() (+6 more)

### Community 19 - "Community 19"
Cohesion: 0.15
Nodes (2): _plan(), TestGovernanceSurfacePlanGate

### Community 20 - "Community 20"
Cohesion: 0.15
Nodes (11): apply_policy(), classifier_match(), _contains_term(), decide(), deterministic_match(), GateDecision, _load_classifier(), load_rules() (+3 more)

### Community 21 - "Community 21"
Cohesion: 0.19
Nodes (21): build(), category_for(), describe_file(), esc(), FileInfo, first_comment(), first_heading(), frontmatter_field() (+13 more)

### Community 22 - "Community 22"
Cohesion: 0.2
Nodes (18): append_audit(), _audit_path(), ensure_queue(), load_packet(), _load_plan(), QueueDecision, Replay audit events into logical latest states.      `latest_states` includes ac, replay_audit() (+10 more)

### Community 23 - "Community 23"
Cohesion: 0.21
Nodes (12): _actual_workflows(), check_inventory(), _command_file_candidates(), _load_inventory(), main(), _normalize_path(), _validate_coverage(), _validate_required_snippets() (+4 more)

### Community 24 - "Community 24"
Cohesion: 0.2
Nodes (20): build_parser(), _consumer_record_relpath(), ConsumerRecord, ConsumerVerifyError, _expected_managed_paths(), _fail(), _git_root(), _initial_package_version() (+12 more)

### Community 25 - "Community 25"
Cohesion: 0.1
Nodes (1): TestLocalCiGate

### Community 26 - "Community 26"
Cohesion: 0.32
Nodes (1): TestDeployGovernanceTooling

### Community 27 - "Community 27"
Cohesion: 0.14
Nodes (10): check_github_issue_open(), collect_section_lines(), fail(), issue_column_index(), issue_numbers(), main(), parse_markdown_row(), validate_section() (+2 more)

### Community 28 - "Community 28"
Cohesion: 0.3
Nodes (2): _packet(), TestPacketQueue

### Community 29 - "Community 29"
Cohesion: 0.27
Nodes (14): add_common_args(), build_plan(), _common_preview_payload(), DeployError, DeployPlan, _existing_shim_state(), _fail(), _is_relative_to() (+6 more)

### Community 30 - "Community 30"
Cohesion: 0.27
Nodes (1): TestDeployLocalCIGate

### Community 31 - "Community 31"
Cohesion: 0.23
Nodes (10): build_parser(), build_payload(), _call_fixture(), _call_live(), Check, _fixture_request(), _latest_live_instruction(), main() (+2 more)

### Community 32 - "Community 32"
Cohesion: 0.28
Nodes (14): compare_inventory(), _default_branch_name(), _inventory_rows_from_payload(), InventoryDrift, load_inventory_file(), _load_json(), load_live_inventory(), main() (+6 more)

### Community 33 - "Community 33"
Cohesion: 0.23
Nodes (12): backlog_issues(), build_summary(), collect_active_issue_refs(), current_repo_slug(), fail(), gh_json(), IssueRef, main() (+4 more)

### Community 34 - "Community 34"
Cohesion: 0.23
Nodes (14): build_alert(), build_parser(), _contains_sensitive(), _load_payload(), main(), _now(), render_markdown(), _safe_text() (+6 more)

### Community 35 - "Community 35"
Cohesion: 0.14
Nodes (2): FakeResponse, TestRuntimeInventory

### Community 36 - "Community 36"
Cohesion: 0.3
Nodes (1): TestVerifyGovernanceConsumer

### Community 37 - "Community 37"
Cohesion: 0.26
Nodes (1): GovernedReposValidationTests

### Community 38 - "Community 38"
Cohesion: 0.31
Nodes (13): _branch_issue_number(), _display_path(), _find_plan_files(), _is_governance_surface(), _load_json_safe(), main(), _matching_execution_scopes(), _matching_plan_payloads() (+5 more)

### Community 39 - "Community 39"
Cohesion: 0.51
Nodes (1): TestOrgRepoInventory

### Community 40 - "Community 40"
Cohesion: 0.42
Nodes (12): _registry(), _repo(), _run(), test_execute_runs_tracked_runner(), test_fresh_report_does_not_trigger(), test_markdown_records_same_source_root_for_dashboard_consumers(), test_missing_report_skips_with_missing_token(), test_missing_runner_is_explicit_when_token_exists() (+4 more)

### Community 41 - "Community 41"
Cohesion: 0.29
Nodes (12): check(), main(), Exercise vault discovery from sibling governance worktrees., Exercise vault discovery from HLDPRO/var/worktrees/* governance worktrees., Exercise Seek/Ponder bootstrap aliases without leaking synthetic values., Exercise Stampede bootstrap with production Tradier mapping and redaction., Exercise lam bootstrap with command-like vault values and missing optional keys., run_nested_var_worktree_lam_bootstrap() (+4 more)

### Community 42 - "Community 42"
Cohesion: 0.27
Nodes (6): _check_required_checks(), evaluate(), _labels(), main(), eligible_payload(), TestAutomergePolicyCheck

### Community 43 - "Community 43"
Cohesion: 0.38
Nodes (10): build_graph(), _community_label(), _derive_path_phrase(), _derive_path_tokens(), infer_community_labels(), main(), _normalize_phrase(), _sanitize_markdown_artifacts() (+2 more)

### Community 44 - "Community 44"
Cohesion: 0.45
Nodes (10): _payload(), _run_hook(), test_hook_allows_read_even_when_text_matches_owned_work(), test_hook_blocks_agent_owned_work_before_file_path_logic(), test_hook_blocks_task_tool_owned_work(), test_hook_bypass_allows_and_logs(), test_hook_configured_mcp_endpoint_fails_open_on_unavailable_gate(), test_hook_preserves_new_code_file_block() (+2 more)

### Community 45 - "Community 45"
Cohesion: 0.45
Nodes (10): _process(), _request(), test_ambiguous_response_produces_clarification_and_no_instruction(), test_expired_response_fails_closed_to_dead_letter(), test_invalid_packet_lands_in_dead_letter_with_validation_errors(), test_local_cli_checkpoint_fixture_creates_valid_hitl_request(), test_replay_reconstructs_decision_path(), test_request_changes_response_preserves_feedback_path_without_approval() (+2 more)

### Community 46 - "Community 46"
Cohesion: 0.2
Nodes (0): 

### Community 47 - "Community 47"
Cohesion: 0.38
Nodes (9): filtered_targets(), find_target(), load_manifest(), main(), print_json(), print_shell(), print_stage_paths(), print_tsv() (+1 more)

### Community 48 - "Community 48"
Cohesion: 0.4
Nodes (9): build_inventory(), import_available(), local_runtime(), mac_hardware(), main(), memory_budget(), pii_guardrail(), _run() (+1 more)

### Community 49 - "Community 49"
Cohesion: 0.49
Nodes (9): check(), fail(), main(), read_text(), repos_for_static_checkout(), validate_docs_surfaces(), validate_runtime_registry_consumers(), validate_static_checkout_workflow() (+1 more)

### Community 50 - "Community 50"
Cohesion: 0.61
Nodes (8): check(), main(), run_command(), test_logger_backwards_compatible(), test_logger_query_trace_fields(), test_measurement_falls_back_from_stale_governance_repo_path(), test_measurement_outputs_query_traces(), test_schema_shape()

### Community 51 - "Community 51"
Cohesion: 0.42
Nodes (7): check_memory_exists(), inspect_repo(), load_memory_lines(), main(), memory_dir_for_repo(), parse_pointer_filenames(), validate_frontmatter()

### Community 52 - "Community 52"
Cohesion: 0.39
Nodes (2): run_hook(), TestBranchSwitchGuard

### Community 53 - "Community 53"
Cohesion: 0.5
Nodes (8): run_fire(), test_exec_failure_after_successful_preflight_logs_and_signals(), test_preflight_failure_logs_and_exits_fast(), test_preflight_timeout_logs_and_exits_fast(), test_review_template_default_persona_reaches_codex_fire(), test_review_template_propagates_wrapper_failure(), test_success_does_not_write_failure_log(), write_fake_codex()

### Community 54 - "Community 54"
Cohesion: 0.46
Nodes (7): collect_repo_metrics(), main(), parse_iso(), pct(), render_markdown(), RepoMetrics, run()

### Community 55 - "Community 55"
Cohesion: 0.48
Nodes (2): _copy_fixture(), TestReadOnlyObserver

### Community 56 - "Community 56"
Cohesion: 0.67
Nodes (6): check(), fail(), load_json(), main(), validate_graphify_reconciliation(), validate_registry_shape()

### Community 57 - "Community 57"
Cohesion: 0.4
Nodes (5): detect_pii(), _iter_patterns(), load_pii_patterns(), Load and validate pii patterns from pii_patterns.yml., Scan text for PII patterns from YAML patterns.      Falls back to the previous b

### Community 58 - "Community 58"
Cohesion: 0.7
Nodes (4): append_event(), build_event(), main(), parse_args()

### Community 59 - "Community 59"
Cohesion: 0.8
Nodes (4): _load(), test_invalid_hitl_relay_examples_fail(), test_valid_hitl_relay_examples_pass(), _validator()

### Community 60 - "Community 60"
Cohesion: 0.83
Nodes (3): check(), is_ignored(), main()

### Community 61 - "Community 61"
Cohesion: 0.83
Nodes (3): main(), replace_section(), summary_line()

### Community 62 - "Community 62"
Cohesion: 0.67
Nodes (3): emit_packet(), main(), Emit a packet YAML file.     Returns: path to written file

### Community 63 - "Community 63"
Cohesion: 0.67
Nodes (0): 

### Community 64 - "Community 64"
Cohesion: 1.0
Nodes (2): build_scoped_graph(), main()

### Community 65 - "Community 65"
Cohesion: 1.0
Nodes (2): main(), render_issue()

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (0): 

### Community 67 - "Community 67"
Cohesion: 1.0
Nodes (0): 

### Community 68 - "Community 68"
Cohesion: 1.0
Nodes (1): Convenience: load shared dir from bundled package personas/.

### Community 69 - "Community 69"
Cohesion: 1.0
Nodes (1): Build a client from well-known environment variables.

## Knowledge Gaps
- **72 isolated node(s):** `Load persona JSON files. Resolves local-first, shared fallback.`, `Convenience: load shared dir from bundled package personas/.`, `Subprocess-backed provider using codex exec --ephemeral.`, `Cloud stub — not implemented until API keys are provisioned.`, `Replay audit events into logical latest states.      `latest_states` includes ac` (+67 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 66`** (2 nodes): `test_artifacts.py`, `test_artifact_writer_writes_manifest_and_outcomes()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (2 nodes): `test_engine.py`, `test_engine_passes_template_results_to_provider()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (1 nodes): `Convenience: load shared dir from bundled package personas/.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 69`** (1 nodes): `Build a client from well-known environment variables.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GateError` connect `Community 8` to `Community 2`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `WindowsOllamaSubmitter` (e.g. with `main()` and `AuditWriter`) actually correct?**
  _`WindowsOllamaSubmitter` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `PiiDetectionError` (e.g. with `.submit()` and `AuditWriter`) actually correct?**
  _`PiiDetectionError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `ModelNotAllowedError` (e.g. with `.submit()` and `AuditWriter`) actually correct?**
  _`ModelNotAllowedError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `EndpointUnreachableError` (e.g. with `.submit()` and `AuditWriter`) actually correct?**
  _`EndpointUnreachableError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Load persona JSON files. Resolves local-first, shared fallback.`, `Convenience: load shared dir from bundled package personas/.`, `Subprocess-backed provider using codex exec --ephemeral.` to the rest of the system?**
  _72 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._