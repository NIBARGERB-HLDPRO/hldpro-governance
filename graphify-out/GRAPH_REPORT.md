# Graph Report - .  (2026-04-30)

## Corpus Check
- 152 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2181 nodes · 4678 edges · 98 communities detected
- Extraction: 45% EXTRACTED · 55% INFERRED · 0% AMBIGUOUS · INFERRED: 2574 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `TestVerifyGovernanceConsumer` - 49 edges
2. `WindowsOllamaSubmitter` - 48 edges
3. `TestActiveIssueBranchContract` - 44 edges
4. `PiiDetectionError` - 44 edges
5. `ModelNotAllowedError` - 44 edges
6. `EndpointUnreachableError` - 44 edges
7. `TestAssertExecutionScope` - 35 edges
8. `RepoFixture` - 31 edges
9. `_tier1_packet()` - 31 edges
10. `_write_supporting_files()` - 30 edges

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
Nodes (78): AuditWriter, canonical_json(), compute_entry_hmac(), compute_sha256(), Write an audit entry. Returns True if successful, False otherwise.          Args, Return canonical JSON for HMAC computation., Write or update today's manifest., Compute SHA256 hash of bytes. (+70 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (54): build_parser(), _env_has_live_markers(), main(), _run_fixture(), _run_live(), _scan_evidence_dir(), _stage_d_args(), _build_fixture_server() (+46 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (35): BaseHTTPRequestHandler, build_parser(), _changed_files(), check_publish_gate(), _fail(), _git_root(), main(), _package_has_file_index_check() (+27 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (25): _dispatch_packet(), _make_parent_packet(), Cross-family independence violated: both planners are anthropic., anthropic + openai is fine., Parent file absent → warn, don't refuse., Sanity: the patterns file should be present in this worktree., Non-LAM role with PII artifact path must be refused., worker-lam role is allowed to handle PII artifacts. (+17 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (4): _dispatch_contract(), _plan(), TestActiveIssueBranchContract, TestGovernanceSurfacePlanGate

### Community 5 - "Community 5"
Cohesion: 0.17
Nodes (1): TestVerifyGovernanceConsumer

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (38): build_parser(), build_payload(), _call_fixture(), _call_live(), Check, _fixture_request(), _latest_live_instruction(), main() (+30 more)

### Community 7 - "Community 7"
Cohesion: 0.09
Nodes (44): _branch_issue_number(), _changed_paths(), _changed_paths_from_file(), check_scope(), _current_branch(), ExecutionScope, _format_path(), _git_root() (+36 more)

### Community 8 - "Community 8"
Cohesion: 0.09
Nodes (44): build_parser(), CloseoutDecision, evaluate(), _is_governance_surface(), _is_planning_only(), _issue_number(), main(), _matching_closeouts() (+36 more)

### Community 9 - "Community 9"
Cohesion: 0.06
Nodes (20): ABC, BaseAggregator, ArtifactWriter, RunManifest, BaseAggregator, BaseModel, SimulationEngine, PersonaLoader (+12 more)

### Community 10 - "Community 10"
Cohesion: 0.1
Nodes (43): build_parser(), _consumer_record_relpath(), ConsumerRecord, ConsumerVerifyError, _contains_negated_forbidden_action(), _ensure_remote_reachable_governance_ref(), _expected_checksum(), _expected_entry_failures() (+35 more)

### Community 11 - "Community 11"
Cohesion: 0.09
Nodes (39): _expand_home(), governed_repos(), GovernedRepo, load_registry(), repo_names_enabled_for(), repos_enabled_for(), repos_root(), build_payload() (+31 more)

### Community 12 - "Community 12"
Cohesion: 0.13
Nodes (38): append_audit(), atomic_write_json(), _base_packet(), _build_decision_packet(), _build_instruction_packet(), build_request(), _build_response_packet(), _build_resume_packet() (+30 more)

### Community 13 - "Community 13"
Cohesion: 0.2
Nodes (4): _git(), RepoFixture, TestAssertExecutionScope, _working_directory()

### Community 14 - "Community 14"
Cohesion: 0.1
Nodes (34): append_fail_fast_block_entry(), append_fail_fast_candidate(), append_fail_fast_table_entry(), append_progress_candidate(), bounded_text(), build_parser(), build_review_context(), build_schema_file() (+26 more)

### Community 15 - "Community 15"
Cohesion: 0.13
Nodes (37): ArtifactStats, branch_binding_preflight(), _check_pages_limits(), count_files(), deploy(), emit_evidence(), enforce_pages_limits(), extract_deployment_url() (+29 more)

### Community 16 - "Community 16"
Cohesion: 0.12
Nodes (20): append_audit(), _audit_path(), ensure_queue(), load_packet(), _load_plan(), QueueDecision, Replay audit events into logical latest states.      `latest_states` includes ac, replay_audit() (+12 more)

### Community 17 - "Community 17"
Cohesion: 0.15
Nodes (34): add_common_args(), apply(), _build_local_ci_plan(), build_plan(), _consumer_record(), _consumer_record_relpath(), _ensure_relative_to(), _ensure_remote_reachable_governance_ref() (+26 more)

### Community 18 - "Community 18"
Cohesion: 0.12
Nodes (38): _branch_issue_number(), build_argument_parser(), _build_summary(), _changed_files_from_git(), ChangedFiles, _check_exit_code(), _check_matches_changed_files(), CheckResult (+30 more)

### Community 19 - "Community 19"
Cohesion: 0.14
Nodes (28): atomic_write_yaml(), build_report(), _date_from_text(), duplicate_counts(), enrich_packet(), _entry_id(), LearningEntry, LearningMatch (+20 more)

### Community 20 - "Community 20"
Cohesion: 0.09
Nodes (20): active_governance_issue_numbers(), branch_issue_number(), check_branch_parity(), current_branch(), fail(), main(), parse_args(), check_github_issue_open() (+12 more)

### Community 21 - "Community 21"
Cohesion: 0.17
Nodes (31): default_env(), deploy_calls(), FakeCompleted, _make_cf_response(), make_runner(), run_gate(), run_gate_expect_error(), test_branch_binding_preflight_fails_on_mismatch() (+23 more)

### Community 22 - "Community 22"
Cohesion: 0.23
Nodes (8): _consumer_scope(), _dispatch_contract(), _handoff(), _plan(), _scope(), TestValidateHandoffPackage, _write_json(), _write_supporting_files()

### Community 23 - "Community 23"
Cohesion: 0.12
Nodes (22): build_parser(), build_report(), _count_or_none(), inspect_repo(), _load_json(), _load_record(), main(), _managed_paths() (+14 more)

### Community 24 - "Community 24"
Cohesion: 0.15
Nodes (30): _branch(), build_report(), _cname_note(), _deployment_url(), _domain_label(), _domain_result(), _domains(), emit_summary() (+22 more)

### Community 25 - "Community 25"
Cohesion: 0.13
Nodes (19): add_common_args(), build_plan(), build_refresh_command(), execute_refresh(), find_target(), git_hook_paths(), HelperError, HookPlan (+11 more)

### Community 26 - "Community 26"
Cohesion: 0.1
Nodes (30): _find_packet_file(), _load_packet(), load_pii_patterns(), _load_schema(), Load and compile PII patterns from pii-patterns.yml., Enforce cross-family independence for tier-1 dual-planner packets.      When pri, Refuse if any consecutive pair in the parent chain shares model_id across differ, Enforce expected handoff sequence with no tier jumps. (+22 more)

### Community 27 - "Community 27"
Cohesion: 0.16
Nodes (29): _agent_registry_has_agent(), _agent_surface_exists(), _alternate_review_identity_gate_applies(), _branch_issue_number(), _display_path(), _find_plan_files(), _is_governance_surface(), _is_planning_evidence_surface() (+21 more)

### Community 28 - "Community 28"
Cohesion: 0.16
Nodes (28): aggregate_file_scores(), augment_workflow_doc_candidates(), baseline_results(), build_summary(), build_trace(), emit_usage_events(), estimate_tokens(), evaluate_relevance() (+20 more)

### Community 29 - "Community 29"
Cohesion: 0.11
Nodes (14): _all_executable_lines(), _all_run_commands(), check_contract(), _contains_main_branch(), _executable_lines(), _failures_for_text(), _has_executable_line_starting_with(), _load_workflow() (+6 more)

### Community 30 - "Community 30"
Cohesion: 0.07
Nodes (1): TestLocalCiGate

### Community 31 - "Community 31"
Cohesion: 0.15
Nodes (17): TestValidateSqlSchemaProbeContract, valid_contract(), build_parser(), _column_key(), _contract_paths(), _display(), _fixture_columns(), _load_contract() (+9 more)

### Community 32 - "Community 32"
Cohesion: 0.16
Nodes (21): append_jsonl(), AttemptResult, build_command(), event_paths(), kill_group(), main(), parse_args(), session_id() (+13 more)

### Community 33 - "Community 33"
Cohesion: 0.17
Nodes (12): ValidateProvisioningEvidenceTest, _default_paths(), _expand_scan_paths(), Finding, _is_env_file(), _is_scan_candidate(), main(), _normalize_repo_path() (+4 more)

### Community 34 - "Community 34"
Cohesion: 0.24
Nodes (1): TestDeployGovernanceTooling

### Community 35 - "Community 35"
Cohesion: 0.27
Nodes (20): FakeTransport, response(), run_report(), test_cache_busting_headers(), test_cname_mismatch_not_blocking(), test_different_deployment_ids(), test_domain_not_200(), test_expected_title_matches() (+12 more)

### Community 36 - "Community 36"
Cohesion: 0.15
Nodes (11): apply_policy(), classifier_match(), _contains_term(), decide(), deterministic_match(), GateDecision, _load_classifier(), load_rules() (+3 more)

### Community 37 - "Community 37"
Cohesion: 0.19
Nodes (21): build(), category_for(), describe_file(), esc(), FileInfo, first_comment(), first_heading(), frontmatter_field() (+13 more)

### Community 38 - "Community 38"
Cohesion: 0.21
Nodes (12): _actual_workflows(), check_inventory(), _command_file_candidates(), _load_inventory(), main(), _normalize_path(), _validate_coverage(), _validate_required_snippets() (+4 more)

### Community 39 - "Community 39"
Cohesion: 0.1
Nodes (15): Modify first_hash in manifest and verify fails., Test that truncated file (missing last line) breaks manifest., Delete last line and verify detects entry_count mismatch., Test that duplicate line (replay) breaks seq monotonicity., Duplicate a line and verify detects non-monotonic seq., Test that tampering with a line breaks the chain., Tamper with line N and verify fails at line N+1., Test that replacing entry_hmac with wrong value fails verification. (+7 more)

### Community 40 - "Community 40"
Cohesion: 0.19
Nodes (2): _run(), TestPlanPreflight

### Community 41 - "Community 41"
Cohesion: 0.27
Nodes (14): add_common_args(), build_plan(), _common_preview_payload(), DeployError, DeployPlan, _existing_shim_state(), _fail(), _is_relative_to() (+6 more)

### Community 42 - "Community 42"
Cohesion: 0.37
Nodes (4): _git(), RepoFixture, _scope(), TestWorkerHandoffRoute

### Community 43 - "Community 43"
Cohesion: 0.27
Nodes (1): TestDeployLocalCIGate

### Community 44 - "Community 44"
Cohesion: 0.28
Nodes (13): _payload(), _run_hook(), test_hook_allows_edit_on_owned_in_scope_file(), test_hook_allows_multiedit_on_owned_in_scope_file(), test_hook_allows_read_even_when_text_matches_owned_work(), test_hook_blocks_agent_owned_work_before_file_path_logic(), test_hook_blocks_task_tool_owned_work(), test_hook_bypass_allows_and_logs() (+5 more)

### Community 45 - "Community 45"
Cohesion: 0.28
Nodes (14): compare_inventory(), _default_branch_name(), _inventory_rows_from_payload(), InventoryDrift, load_inventory_file(), _load_json(), load_live_inventory(), main() (+6 more)

### Community 46 - "Community 46"
Cohesion: 0.23
Nodes (12): backlog_issues(), build_summary(), collect_active_issue_refs(), current_repo_slug(), fail(), gh_json(), IssueRef, main() (+4 more)

### Community 47 - "Community 47"
Cohesion: 0.32
Nodes (3): _payload(), _run_hook(), TestSchemaGuardHook

### Community 48 - "Community 48"
Cohesion: 0.23
Nodes (14): build_alert(), build_parser(), _contains_sensitive(), _load_payload(), main(), _now(), render_markdown(), _safe_text() (+6 more)

### Community 49 - "Community 49"
Cohesion: 0.14
Nodes (2): FakeResponse, TestRuntimeInventory

### Community 50 - "Community 50"
Cohesion: 0.23
Nodes (6): _check_required_checks(), evaluate(), _labels(), main(), eligible_payload(), TestAutomergePolicyCheck

### Community 51 - "Community 51"
Cohesion: 0.32
Nodes (3): _json(), TestValidateCloseout, _write()

### Community 52 - "Community 52"
Cohesion: 0.27
Nodes (14): build_report(), codex_backlog_status(), extract_runbook_paths(), extract_som_excerpt(), format_hook_note(), git_branch(), main(), parse_args() (+6 more)

### Community 53 - "Community 53"
Cohesion: 0.33
Nodes (13): block_reason(), _clean_token(), detect_bash_write_target(), evaluate(), _extract_cp_mv_install_target(), _extract_dd_target(), _extract_mutation_file_after_options(), _extract_positional_target() (+5 more)

### Community 54 - "Community 54"
Cohesion: 0.26
Nodes (1): GovernedReposValidationTests

### Community 55 - "Community 55"
Cohesion: 0.19
Nodes (8): build_governance(), emit_dispatch_packet(), emit_packet(), main(), Emit a dispatch-ready packet that includes a complete governance block., Emit a minimal or dispatch-ready packet YAML file. Returns path to written file., Build a governance block dict for inclusion in a dispatch-ready packet., TestPacketEmitter

### Community 56 - "Community 56"
Cohesion: 0.28
Nodes (2): run_hook(), TestBranchSwitchGuard

### Community 57 - "Community 57"
Cohesion: 0.42
Nodes (8): CheckExecutionEnvironmentTests, _git(), _make_repo(), _run(), _write(), _write_handoff(), _write_plan(), _write_scope()

### Community 58 - "Community 58"
Cohesion: 0.51
Nodes (1): TestOrgRepoInventory

### Community 59 - "Community 59"
Cohesion: 0.33
Nodes (3): _json(), TestCheckStage6Closeout, _write()

### Community 60 - "Community 60"
Cohesion: 0.42
Nodes (12): _registry(), _repo(), _run(), test_execute_runs_tracked_runner(), test_fresh_report_does_not_trigger(), test_markdown_records_same_source_root_for_dashboard_consumers(), test_missing_report_skips_with_missing_token(), test_missing_runner_is_explicit_when_token_exists() (+4 more)

### Community 61 - "Community 61"
Cohesion: 0.24
Nodes (7): TestValidateSessionErrorPatterns, _write_runbook(), _field_key(), _fields(), _pattern_sections(), _run_cli(), validate()

### Community 62 - "Community 62"
Cohesion: 0.29
Nodes (12): check(), main(), Exercise worktree invocation while still resolving the canonical governance root, Exercise failure when the canonical governance root is absent., Exercise Seek/Ponder bootstrap aliases without leaking synthetic values., Exercise Stampede bootstrap with production Tradier mapping and redaction., Exercise lam bootstrap with command-like vault values and missing optional keys., run_canonical_root_worktree_lam_bootstrap() (+4 more)

### Community 63 - "Community 63"
Cohesion: 0.33
Nodes (1): TestCheckConsumerRolloutPublishGate

### Community 64 - "Community 64"
Cohesion: 0.3
Nodes (2): run_helper(), TestLaneBootstrap

### Community 65 - "Community 65"
Cohesion: 0.5
Nodes (3): _settings(), ValidateSessionContractSurfacesTests, _write()

### Community 66 - "Community 66"
Cohesion: 0.33
Nodes (11): _api_get_projects(), _deployment_metadata(), _domains(), _git_provider_status(), inventory(), _latest_deployment(), _load_json(), main() (+3 more)

### Community 67 - "Community 67"
Cohesion: 0.38
Nodes (10): build_graph(), _community_label(), _derive_path_phrase(), _derive_path_tokens(), infer_community_labels(), main(), _normalize_phrase(), _sanitize_markdown_artifacts() (+2 more)

### Community 68 - "Community 68"
Cohesion: 0.35
Nodes (10): cleanup_advice(), infer_repo_slug(), LanePolicy, load_policy(), main(), _match(), normalize_slug(), parse_args() (+2 more)

### Community 69 - "Community 69"
Cohesion: 0.35
Nodes (9): build_parser(), check_memory_exists(), inspect_repo(), load_memory_lines(), main(), memory_dir_for_repo(), MemoryInspection, parse_pointer_filenames() (+1 more)

### Community 70 - "Community 70"
Cohesion: 0.36
Nodes (8): run_fire(), test_exec_failure_after_successful_preflight_logs_and_signals(), test_preflight_failure_logs_and_exits_fast(), test_preflight_timeout_logs_and_exits_fast(), test_review_template_default_persona_reaches_codex_fire(), test_review_template_propagates_wrapper_failure(), test_success_does_not_write_failure_log(), write_fake_codex()

### Community 71 - "Community 71"
Cohesion: 0.2
Nodes (0): 

### Community 72 - "Community 72"
Cohesion: 0.38
Nodes (9): filtered_targets(), find_target(), load_manifest(), main(), print_json(), print_shell(), print_stage_paths(), print_tsv() (+1 more)

### Community 73 - "Community 73"
Cohesion: 0.4
Nodes (9): build_inventory(), import_available(), local_runtime(), mac_hardware(), main(), memory_budget(), pii_guardrail(), _run() (+1 more)

### Community 74 - "Community 74"
Cohesion: 0.49
Nodes (9): check(), fail(), main(), read_text(), repos_for_static_checkout(), validate_docs_surfaces(), validate_runtime_registry_consumers(), validate_static_checkout_workflow() (+1 more)

### Community 75 - "Community 75"
Cohesion: 0.61
Nodes (8): check(), main(), run_command(), test_logger_backwards_compatible(), test_logger_query_trace_fields(), test_measurement_falls_back_from_stale_governance_repo_path(), test_measurement_outputs_query_traces(), test_schema_shape()

### Community 76 - "Community 76"
Cohesion: 0.46
Nodes (7): collect_repo_metrics(), main(), parse_iso(), pct(), render_markdown(), RepoMetrics, run()

### Community 77 - "Community 77"
Cohesion: 0.32
Nodes (1): MemoryIntegrityTests

### Community 78 - "Community 78"
Cohesion: 0.43
Nodes (6): _load_json(), _load_yaml(), main(), _repo_ref(), _resolve_model_settings(), run_specialist_packet()

### Community 79 - "Community 79"
Cohesion: 0.46
Nodes (4): add_startup_scope_bundle(), make_repo(), run_contract(), SessionBootstrapContractTests

### Community 80 - "Community 80"
Cohesion: 0.48
Nodes (2): _copy_fixture(), TestReadOnlyObserver

### Community 81 - "Community 81"
Cohesion: 0.67
Nodes (6): check(), fail(), load_json(), main(), validate_graphify_reconciliation(), validate_registry_shape()

### Community 82 - "Community 82"
Cohesion: 0.7
Nodes (4): append_event(), build_event(), main(), parse_args()

### Community 83 - "Community 83"
Cohesion: 0.7
Nodes (4): artifact_branch(), artifact_scope(), main(), write_scope()

### Community 84 - "Community 84"
Cohesion: 0.4
Nodes (1): SweepArtifactPrTest

### Community 85 - "Community 85"
Cohesion: 0.7
Nodes (4): _find_hook_command(), main(), _normalized(), validate()

### Community 86 - "Community 86"
Cohesion: 0.8
Nodes (4): _load(), test_invalid_hitl_relay_examples_fail(), test_valid_hitl_relay_examples_pass(), _validator()

### Community 87 - "Community 87"
Cohesion: 0.6
Nodes (2): _packet(), RunSpecialistPacketTests

### Community 88 - "Community 88"
Cohesion: 0.83
Nodes (3): check(), is_ignored(), main()

### Community 89 - "Community 89"
Cohesion: 0.83
Nodes (3): main(), replace_section(), summary_line()

### Community 90 - "Community 90"
Cohesion: 0.5
Nodes (0): 

### Community 91 - "Community 91"
Cohesion: 0.67
Nodes (0): 

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (2): build_scoped_graph(), main()

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (2): main(), render_issue()

### Community 94 - "Community 94"
Cohesion: 1.0
Nodes (0): 

### Community 95 - "Community 95"
Cohesion: 1.0
Nodes (0): 

### Community 96 - "Community 96"
Cohesion: 1.0
Nodes (1): Convenience: load shared dir from bundled package personas/.

### Community 97 - "Community 97"
Cohesion: 1.0
Nodes (1): Build a client from well-known environment variables.

## Knowledge Gaps
- **82 isolated node(s):** `Load persona JSON files. Resolves local-first, shared fallback.`, `Convenience: load shared dir from bundled package personas/.`, `Subprocess-backed provider using codex exec --ephemeral.`, `Cloud stub — not implemented until API keys are provisioned.`, `Replay audit events into logical latest states.      `latest_states` includes ac` (+77 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 94`** (2 nodes): `test_artifacts.py`, `test_artifact_writer_writes_manifest_and_outcomes()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 95`** (2 nodes): `test_engine.py`, `test_engine_passes_template_results_to_provider()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 96`** (1 nodes): `Convenience: load shared dir from bundled package personas/.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 97`** (1 nodes): `Build a client from well-known environment variables.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ConsumerVerifyError` connect `Community 10` to `Community 2`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Why does `GateError` connect `Community 18` to `Community 2`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `WindowsOllamaSubmitter` (e.g. with `main()` and `AuditWriter`) actually correct?**
  _`WindowsOllamaSubmitter` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `PiiDetectionError` (e.g. with `.submit()` and `AuditWriter`) actually correct?**
  _`PiiDetectionError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `ModelNotAllowedError` (e.g. with `.submit()` and `AuditWriter`) actually correct?**
  _`ModelNotAllowedError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Load persona JSON files. Resolves local-first, shared fallback.`, `Convenience: load shared dir from bundled package personas/.`, `Subprocess-backed provider using codex exec --ephemeral.` to the rest of the system?**
  _82 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._