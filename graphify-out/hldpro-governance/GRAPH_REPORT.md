# Graph Report - hldpro-governance  (2026-04-21)

## Corpus Check
- Large corpus: 1821 files · ~468,787 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 1421 nodes · 2693 edges · 77 communities detected
- Extraction: 51% EXTRACTED · 49% INFERRED · 0% AMBIGUOUS · INFERRED: 1323 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `TestAssertExecutionScope` - 34 edges
2. `RepoFixture` - 30 edges
3. `_tier1_packet()` - 29 edges
4. `TestGovernanceSurfacePlanGate` - 24 edges
5. `TestLocalCiGate` - 20 edges
6. `TestDeployGovernanceTooling` - 19 edges
7. `TestDeployLocalCIGate` - 16 edges
8. `_write_supporting_files()` - 15 edges
9. `TestPacketQueue` - 15 edges
10. `describe_file()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Return canonical JSON for HMAC computation.` --rationale_for--> `canonical_json()`  [EXTRACTED]
  scripts/windows-ollama/verify_audit.py → scripts/remote-mcp/verify_audit.py
- `Compute SHA256 hash of bytes.` --rationale_for--> `compute_sha256()`  [EXTRACTED]
  scripts/windows-ollama/verify_audit.py → scripts/remote-mcp/verify_audit.py
- `Compute HMAC-SHA256 over entry without entry_hmac field.` --rationale_for--> `compute_entry_hmac()`  [EXTRACTED]
  scripts/windows-ollama/verify_audit.py → scripts/remote-mcp/verify_audit.py
- `verify_audit_dir()` --calls--> `verify_hmac()`  [INFERRED]
  scripts/remote-mcp/verify_audit.py → scripts/windows-ollama/verify_audit.py
- `Verify all audit logs in the directory.     Returns (success: bool, errors: list` --rationale_for--> `verify_audit_dir()`  [EXTRACTED]
  scripts/windows-ollama/verify_audit.py → scripts/remote-mcp/verify_audit.py

## Communities

### Community 0 - "Windows ollama Submit"
Cohesion: 0.05
Nodes (40): AuditWriter, canonical_json(), compute_entry_hmac(), compute_sha256(), Write an audit entry. Returns True if successful, False otherwise.          Args, Return canonical JSON for HMAC computation., Write or update today's manifest., Compute SHA256 hash of bytes. (+32 more)

### Community 1 - "Windows ollama Submit"
Cohesion: 0.03
Nodes (37): Test that clean prompt passes PII detection., Negative test: non-allowlisted model., Test that non-allowlisted model is rejected., Test that allowlisted model passes allowlist check., Negative test: unreachable endpoint., Test that unreachable endpoint raises appropriate error., Test that endpoint timeout is handled., Test that reachable endpoint succeeds. (+29 more)

### Community 2 - "Remote mcp Verify audit"
Cohesion: 0.05
Nodes (47): Modify first_hash in manifest and verify fails., Test that truncated file (missing last line) breaks manifest., Delete last line and verify detects entry_count mismatch., Test that duplicate line (replay) breaks seq monotonicity., Duplicate a line and verify detects non-monotonic seq., Test that tampering with a line breaks the chain., Tamper with line N and verify fails at line N+1., Test that replacing entry_hmac with wrong value fails verification. (+39 more)

### Community 3 - "Packet Validate Passes"
Cohesion: 0.07
Nodes (19): _make_parent_packet(), Cross-family independence violated: both planners are anthropic., anthropic + openai is fine., Parent file absent → warn, don't refuse., Sanity: the patterns file should be present in this worktree., Non-LAM role with PII artifact path must be refused., worker-lam role is allowed to handle PII artifacts., When pii-patterns.yml is absent, validator must refuse (not silently pass). (+11 more)

### Community 4 - "Overlord Codex ingestion"
Cohesion: 0.1
Nodes (34): append_fail_fast_block_entry(), append_fail_fast_candidate(), append_fail_fast_table_entry(), append_progress_candidate(), bounded_text(), build_parser(), build_review_context(), build_schema_file() (+26 more)

### Community 5 - "Overlord Assert execution scope"
Cohesion: 0.2
Nodes (4): _git(), RepoFixture, TestAssertExecutionScope, _working_directory()

### Community 6 - "Local ci gate Local ci gate Report"
Cohesion: 0.12
Nodes (38): _branch_issue_number(), build_argument_parser(), _build_summary(), _changed_files_from_git(), ChangedFiles, _check_exit_code(), _check_matches_changed_files(), CheckResult (+30 more)

### Community 7 - "Packages Hldpro sim"
Cohesion: 0.06
Nodes (14): ABC, BaseAggregator, ArtifactWriter, RunManifest, SimulationEngine, PersonaLoader, Load persona JSON files. Resolves local-first, shared fallback., Protocol (+6 more)

### Community 8 - "Remote mcp Stage d"
Cohesion: 0.11
Nodes (22): build_parser(), _env_has_live_markers(), main(), _run_fixture(), _run_live(), _scan_evidence_dir(), _stage_d_args(), _build_fixture_server() (+14 more)

### Community 9 - "Som client Som client Error"
Cohesion: 0.09
Nodes (12): RuntimeError, build_parser(), _decode_jwt_payload(), from_env(), main(), Error raised for client-side protocol and transport failures., Decode JWT payload without verifying signature., Minimal HTTP client for Remote MCP Bridge tools. (+4 more)

### Community 10 - "Orchestrator Self learning"
Cohesion: 0.15
Nodes (26): atomic_write_yaml(), build_report(), _date_from_text(), duplicate_counts(), enrich_packet(), _entry_id(), LearningEntry, LearningMatch (+18 more)

### Community 11 - "Knowledge base Graphify"
Cohesion: 0.13
Nodes (19): add_common_args(), build_plan(), build_refresh_command(), execute_refresh(), find_target(), git_hook_paths(), HelperError, HookPlan (+11 more)

### Community 12 - "Packet Validate hitl relay"
Cohesion: 0.12
Nodes (28): _load(), test_duplicate_reply_cannot_produce_instruction(), test_expired_reply_cannot_produce_instruction(), test_low_confidence_clarify_decision_passes_without_instruction(), test_low_confidence_non_clarify_decision_fails_closed(), test_pii_external_channel_fails_closed(), test_response_requires_notification_and_response_ids(), test_session_instruction_requires_matching_target_session() (+20 more)

### Community 13 - "Packet Validate Load"
Cohesion: 0.1
Nodes (30): _find_packet_file(), _load_packet(), load_pii_patterns(), _load_schema(), Load and compile PII patterns from pii-patterns.yml., Enforce cross-family independence for tier-1 dual-planner packets.      When pri, Refuse if any consecutive pair in the parent chain shares model_id across differ, Enforce expected handoff sequence with no tier jumps. (+22 more)

### Community 14 - "Orchestrator Hitl relay queue"
Cohesion: 0.19
Nodes (28): append_audit(), atomic_write_json(), _base_packet(), _build_decision_packet(), _build_instruction_packet(), build_request(), _build_response_packet(), _build_resume_packet() (+20 more)

### Community 15 - "Overlord Deploy governance tooling"
Cohesion: 0.18
Nodes (24): add_common_args(), apply(), _build_local_ci_plan(), build_plan(), _consumer_record(), _consumer_record_relpath(), _ensure_relative_to(), _fail() (+16 more)

### Community 16 - "Overlord Assert execution scope"
Cohesion: 0.15
Nodes (26): _branch_issue_number(), _changed_paths(), _changed_paths_from_file(), check_scope(), _current_branch(), ExecutionScope, _format_path(), _git_root() (+18 more)

### Community 17 - "Knowledge base Measure graphify usage"
Cohesion: 0.16
Nodes (28): aggregate_file_scores(), augment_workflow_doc_candidates(), baseline_results(), build_summary(), build_trace(), emit_usage_events(), estimate_tokens(), evaluate_relevance() (+20 more)

### Community 18 - "Overlord Check local ci gate workflow"
Cohesion: 0.11
Nodes (14): _all_executable_lines(), _all_run_commands(), check_contract(), _contains_main_branch(), _executable_lines(), _failures_for_text(), _has_executable_line_starting_with(), _load_workflow() (+6 more)

### Community 19 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.15
Nodes (2): _plan(), TestGovernanceSurfacePlanGate

### Community 20 - "Overlord Pentagi sweep"
Cohesion: 0.16
Nodes (22): _expand_home(), governed_repos(), GovernedRepo, load_registry(), repo_names_enabled_for(), repos_enabled_for(), repos_root(), build_payload() (+14 more)

### Community 21 - "Overlord Org governance compendium"
Cohesion: 0.19
Nodes (21): build(), category_for(), describe_file(), esc(), FileInfo, first_comment(), first_heading(), frontmatter_field() (+13 more)

### Community 22 - "Remote mcp Operator connectivity"
Cohesion: 0.16
Nodes (12): BaseHTTPRequestHandler, build_parser(), build_payload(), _call_fixture(), _call_live(), Check, _fixture_server(), _FixtureMcpHandler (+4 more)

### Community 23 - "Orchestrator Delegation gate"
Cohesion: 0.15
Nodes (11): apply_policy(), classifier_match(), _contains_term(), decide(), deterministic_match(), GateDecision, _load_classifier(), load_rules() (+3 more)

### Community 24 - "Local ci gate Local ci gate Profile"
Cohesion: 0.1
Nodes (1): TestLocalCiGate

### Community 25 - "Overlord Verify governance consumer"
Cohesion: 0.2
Nodes (20): build_parser(), _consumer_record_relpath(), ConsumerRecord, ConsumerVerifyError, _expected_managed_paths(), _fail(), _git_root(), _initial_package_version() (+12 more)

### Community 26 - "Overlord Workflow local coverage"
Cohesion: 0.21
Nodes (12): _actual_workflows(), check_inventory(), _command_file_candidates(), _load_inventory(), main(), _normalize_path(), _validate_coverage(), _validate_required_snippets() (+4 more)

### Community 27 - "Orchestrator Packet queue"
Cohesion: 0.2
Nodes (18): append_audit(), _audit_path(), ensure_queue(), load_packet(), _load_plan(), QueueDecision, Replay audit events into logical latest states.      `latest_states` includes ac, replay_audit() (+10 more)

### Community 28 - "Overlord Check overlord backlog github alignment"
Cohesion: 0.14
Nodes (10): check_github_issue_open(), collect_section_lines(), fail(), issue_column_index(), issue_numbers(), main(), parse_markdown_row(), validate_section() (+2 more)

### Community 29 - "Overlord Deploy governance tooling"
Cohesion: 0.32
Nodes (1): TestDeployGovernanceTooling

### Community 30 - "Overlord Validate handoff package"
Cohesion: 0.36
Nodes (6): _handoff(), _plan(), _scope(), TestValidateHandoffPackage, _write_json(), _write_supporting_files()

### Community 31 - "Orchestrator Read only observer"
Cohesion: 0.22
Nodes (17): _artifact(), ArtifactStatus, build_reports(), _count_open_issue_metadata(), _daemon_readiness(), _git_commit(), _latest_raw_issue_file(), main() (+9 more)

### Community 32 - "Overlord Deploy local ci gate"
Cohesion: 0.27
Nodes (1): TestDeployLocalCIGate

### Community 33 - "Overlord Deploy local ci gate"
Cohesion: 0.27
Nodes (14): add_common_args(), build_plan(), _common_preview_payload(), DeployError, DeployPlan, _existing_shim_state(), _fail(), _is_relative_to() (+6 more)

### Community 34 - "Remote mcp Operator inbound preflight"
Cohesion: 0.23
Nodes (10): build_parser(), build_payload(), _call_fixture(), _call_live(), Check, _fixture_request(), _latest_live_instruction(), main() (+2 more)

### Community 35 - "Orchestrator Packet queue"
Cohesion: 0.3
Nodes (2): _packet(), TestPacketQueue

### Community 36 - "Overlord Check progress github issue staleness"
Cohesion: 0.23
Nodes (12): backlog_issues(), build_summary(), collect_active_issue_refs(), current_repo_slug(), fail(), gh_json(), IssueRef, main() (+4 more)

### Community 37 - "Overlord Check org repo inventory"
Cohesion: 0.28
Nodes (14): compare_inventory(), _default_branch_name(), _inventory_rows_from_payload(), InventoryDrift, load_inventory_file(), _load_json(), load_live_inventory(), main() (+6 more)

### Community 38 - "Remote mcp Monitor alert"
Cohesion: 0.23
Nodes (14): build_alert(), build_parser(), _contains_sensitive(), _load_payload(), main(), _now(), render_markdown(), _safe_text() (+6 more)

### Community 39 - "Overlord Verify governance consumer"
Cohesion: 0.3
Nodes (1): TestVerifyGovernanceConsumer

### Community 40 - "Lam Runtime inventory"
Cohesion: 0.14
Nodes (2): FakeResponse, TestRuntimeInventory

### Community 41 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.31
Nodes (13): _branch_issue_number(), _display_path(), _find_plan_files(), _is_governance_surface(), _load_json_safe(), main(), _matching_execution_scopes(), _matching_plan_payloads() (+5 more)

### Community 42 - "Overlord Validate governed repos"
Cohesion: 0.26
Nodes (1): GovernedReposValidationTests

### Community 43 - "Bootstrap repo Exercise"
Cohesion: 0.29
Nodes (12): check(), main(), Exercise vault discovery from sibling governance worktrees., Exercise vault discovery from HLDPRO/var/worktrees/* governance worktrees., Exercise Seek/Ponder bootstrap aliases without leaking synthetic values., Exercise Stampede bootstrap with production Tradier mapping and redaction., Exercise lam bootstrap with command-like vault values and missing optional keys., run_nested_var_worktree_lam_bootstrap() (+4 more)

### Community 44 - "Overlord Check org repo inventory"
Cohesion: 0.51
Nodes (1): TestOrgRepoInventory

### Community 45 - "Overlord Pentagi sweep"
Cohesion: 0.42
Nodes (12): _registry(), _repo(), _run(), test_execute_runs_tracked_runner(), test_fresh_report_does_not_trigger(), test_markdown_records_same_source_root_for_dashboard_consumers(), test_missing_report_skips_with_missing_token(), test_missing_runner_is_explicit_when_token_exists() (+4 more)

### Community 46 - "Overlord Automerge policy check"
Cohesion: 0.27
Nodes (6): _check_required_checks(), evaluate(), _labels(), main(), eligible_payload(), TestAutomergePolicyCheck

### Community 47 - "Overlord Validate handoff package"
Cohesion: 0.49
Nodes (10): _discover_package_files(), _is_url(), _load_json(), main(), _normalize_repo_path(), _read_json_ref(), _repo_file_exists(), _validate_acceptance_criteria() (+2 more)

### Community 48 - "Knowledge base Graph"
Cohesion: 0.38
Nodes (10): build_graph(), _community_label(), _derive_path_phrase(), _derive_path_tokens(), infer_community_labels(), main(), _normalize_phrase(), _sanitize_markdown_artifacts() (+2 more)

### Community 49 - "Orchestrator Hitl relay queue"
Cohesion: 0.45
Nodes (10): _process(), _request(), test_ambiguous_response_produces_clarification_and_no_instruction(), test_expired_response_fails_closed_to_dead_letter(), test_invalid_packet_lands_in_dead_letter_with_validation_errors(), test_local_cli_checkpoint_fixture_creates_valid_hitl_request(), test_replay_reconstructs_decision_path(), test_request_changes_response_preserves_feedback_path_without_approval() (+2 more)

### Community 50 - "Orchestrator Delegation Owned"
Cohesion: 0.45
Nodes (10): _payload(), _run_hook(), test_hook_allows_read_even_when_text_matches_owned_work(), test_hook_blocks_agent_owned_work_before_file_path_logic(), test_hook_blocks_task_tool_owned_work(), test_hook_bypass_allows_and_logs(), test_hook_configured_mcp_endpoint_fails_open_on_unavailable_gate(), test_hook_preserves_new_code_file_block() (+2 more)

### Community 51 - "Overlord Validate registry surfaces"
Cohesion: 0.49
Nodes (9): check(), fail(), main(), read_text(), repos_for_static_checkout(), validate_docs_surfaces(), validate_runtime_registry_consumers(), validate_static_checkout_workflow() (+1 more)

### Community 52 - "Lam Runtime inventory"
Cohesion: 0.4
Nodes (9): build_inventory(), import_available(), local_runtime(), mac_hardware(), main(), memory_budget(), pii_guardrail(), _run() (+1 more)

### Community 53 - "Knowledge base Graphify targets"
Cohesion: 0.38
Nodes (9): filtered_targets(), find_target(), load_manifest(), main(), print_json(), print_shell(), print_stage_paths(), print_tsv() (+1 more)

### Community 54 - "Packages Hldpro sim Providers"
Cohesion: 0.2
Nodes (0): 

### Community 55 - "Codex fire Failure"
Cohesion: 0.5
Nodes (8): run_fire(), test_exec_failure_after_successful_preflight_logs_and_signals(), test_preflight_failure_logs_and_exits_fast(), test_preflight_timeout_logs_and_exits_fast(), test_review_template_default_persona_reaches_codex_fire(), test_review_template_propagates_wrapper_failure(), test_success_does_not_write_failure_log(), write_fake_codex()

### Community 56 - "Overlord Branch switch guard"
Cohesion: 0.39
Nodes (2): run_hook(), TestBranchSwitchGuard

### Community 57 - "Overlord Memory integrity"
Cohesion: 0.42
Nodes (7): check_memory_exists(), inspect_repo(), load_memory_lines(), main(), memory_dir_for_repo(), parse_pointer_filenames(), validate_frontmatter()

### Community 58 - "Knowledge base Graphify usage logging"
Cohesion: 0.61
Nodes (8): check(), main(), run_command(), test_logger_backwards_compatible(), test_logger_query_trace_fields(), test_measurement_falls_back_from_stale_governance_repo_path(), test_measurement_outputs_query_traces(), test_schema_shape()

### Community 59 - "Overlord Effectiveness metrics"
Cohesion: 0.46
Nodes (7): collect_repo_metrics(), main(), parse_iso(), pct(), render_markdown(), RepoMetrics, run()

### Community 60 - "Overlord Validate governed repos"
Cohesion: 0.67
Nodes (6): check(), fail(), load_json(), main(), validate_graphify_reconciliation(), validate_registry_shape()

### Community 61 - "Orchestrator Read only observer"
Cohesion: 0.48
Nodes (2): _copy_fixture(), TestReadOnlyObserver

### Community 62 - "Packages Hldpro sim Stampede"
Cohesion: 0.4
Nodes (4): BaseAggregator, BaseModel, NarrativeAggregator, NarrativeOutcome

### Community 63 - "Knowledge base Log graphify usage"
Cohesion: 0.7
Nodes (4): append_event(), build_event(), main(), parse_args()

### Community 64 - "Packet Hitl relay schema"
Cohesion: 0.8
Nodes (4): _load(), test_invalid_hitl_relay_examples_fail(), test_valid_hitl_relay_examples_pass(), _validator()

### Community 65 - "Knowledge base Graphify governance"
Cohesion: 0.83
Nodes (3): check(), is_ignored(), main()

### Community 66 - "Knowledge base Update knowledge"
Cohesion: 0.83
Nodes (3): main(), replace_section(), summary_line()

### Community 67 - "Packet Emit Yaml"
Cohesion: 0.67
Nodes (3): emit_packet(), main(), Emit a packet YAML file.     Returns: path to written file

### Community 68 - "Packages Hldpro sim Stampede"
Cohesion: 0.67
Nodes (2): MockProvider, test_stampede_e2e()

### Community 69 - "Overlord Render github issue feed"
Cohesion: 1.0
Nodes (2): main(), render_issue()

### Community 70 - "Knowledge base Push graph to neo4j"
Cohesion: 1.0
Nodes (2): build_scoped_graph(), main()

### Community 71 - "Packages Hldpro sim Runner"
Cohesion: 0.67
Nodes (0): 

### Community 72 - "Packages Hldpro sim Engine"
Cohesion: 1.0
Nodes (0): 

### Community 73 - "Packages Hldpro sim Artifacts"
Cohesion: 1.0
Nodes (0): 

### Community 74 - "Windows ollama Submit Temporary"
Cohesion: 1.0
Nodes (1): Temporary audit directory for testing.

### Community 75 - "Som client Som client From"
Cohesion: 1.0
Nodes (1): Build a client from well-known environment variables.

### Community 76 - "Packages Hldpro sim Personas"
Cohesion: 1.0
Nodes (1): Convenience: load shared dir from bundled package personas/.

## Knowledge Gaps
- **117 isolated node(s):** `Exercise lam bootstrap with command-like vault values and missing optional keys.`, `Exercise vault discovery from sibling governance worktrees.`, `Exercise vault discovery from HLDPRO/var/worktrees/* governance worktrees.`, `Exercise Seek/Ponder bootstrap aliases without leaking synthetic values.`, `Exercise Stampede bootstrap with production Tradier mapping and redaction.` (+112 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Packages Hldpro sim Engine`** (2 nodes): `test_engine.py`, `test_engine_passes_template_results_to_provider()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Packages Hldpro sim Artifacts`** (2 nodes): `test_artifacts.py`, `test_artifact_writer_writes_manifest_and_outcomes()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Windows ollama Submit Temporary`** (1 nodes): `Temporary audit directory for testing.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Som client Som client From`** (1 nodes): `Build a client from well-known environment variables.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Packages Hldpro sim Personas`** (1 nodes): `Convenience: load shared dir from bundled package personas/.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GateError` connect `Local ci gate Local ci gate Report` to `Som client Som client Error`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Why does `HelperError` connect `Knowledge base Graphify` to `Som client Som client Error`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `RepoFixture` (e.g. with `.test_allows_changes_in_allowed_paths_dirty_tree_mode()` and `.test_planning_only_diff_inside_allowed_paths_passes()`) actually correct?**
  _`RepoFixture` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `_tier1_packet()` (e.g. with `.test_tier1_without_parent_passes()` and `.test_same_family_dual_planner_refused()`) actually correct?**
  _`_tier1_packet()` has 28 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Exercise lam bootstrap with command-like vault values and missing optional keys.`, `Exercise vault discovery from sibling governance worktrees.`, `Exercise vault discovery from HLDPRO/var/worktrees/* governance worktrees.` to the rest of the system?**
  _117 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Windows ollama Submit` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
- **Should `Windows ollama Submit` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._