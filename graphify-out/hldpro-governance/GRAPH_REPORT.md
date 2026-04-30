# Graph Report - hldpro-governance  (2026-04-29)

## Corpus Check
- Large corpus: 3460 files · ~733,837 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 2145 nodes · 4412 edges · 103 communities detected
- Extraction: 47% EXTRACTED · 53% INFERRED · 0% AMBIGUOUS · INFERRED: 2344 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `TestVerifyGovernanceConsumer` - 49 edges
2. `TestActiveIssueBranchContract` - 44 edges
3. `TestAssertExecutionScope` - 35 edges
4. `RepoFixture` - 31 edges
5. `_tier1_packet()` - 31 edges
6. `_write_supporting_files()` - 30 edges
7. `_plan()` - 30 edges
8. `TestLocalCiGate` - 27 edges
9. `TestValidateHandoffPackage` - 27 edges
10. `TestDeployGovernanceTooling` - 24 edges

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

### Community 0 - "Deploy Deploy gate Windows"
Cohesion: 0.05
Nodes (62): Exception, ArtifactStats, branch_binding_preflight(), _check_pages_limits(), count_files(), deploy(), emit_evidence(), enforce_pages_limits() (+54 more)

### Community 1 - "Remote mcp Verify audit"
Cohesion: 0.05
Nodes (54): build_parser(), _env_has_live_markers(), main(), _run_fixture(), _run_live(), _scan_evidence_dir(), _stage_d_args(), _build_fixture_server() (+46 more)

### Community 2 - "Packet Validate Passes"
Cohesion: 0.05
Nodes (25): _dispatch_packet(), _make_parent_packet(), Cross-family independence violated: both planners are anthropic., anthropic + openai is fine., Parent file absent → warn, don't refuse., Sanity: the patterns file should be present in this worktree., Non-LAM role with PII artifact path must be refused., worker-lam role is allowed to handle PII artifacts. (+17 more)

### Community 3 - "Windows ollama Submit"
Cohesion: 0.03
Nodes (37): Test that clean prompt passes PII detection., Negative test: non-allowlisted model., Test that non-allowlisted model is rejected., Test that allowlisted model passes allowlist check., Negative test: unreachable endpoint., Test that unreachable endpoint raises appropriate error., Test that endpoint timeout is handled., Test that reachable endpoint succeeds. (+29 more)

### Community 4 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.08
Nodes (4): _dispatch_contract(), _plan(), TestActiveIssueBranchContract, TestGovernanceSurfacePlanGate

### Community 5 - "Overlord Verify governance consumer"
Cohesion: 0.17
Nodes (1): TestVerifyGovernanceConsumer

### Community 6 - "Packet Validate hitl relay"
Cohesion: 0.08
Nodes (38): build_parser(), build_payload(), _call_fixture(), _call_live(), Check, _fixture_request(), _latest_live_instruction(), main() (+30 more)

### Community 7 - "Overlord Assert execution scope"
Cohesion: 0.09
Nodes (44): _branch_issue_number(), _changed_paths(), _changed_paths_from_file(), check_scope(), _current_branch(), ExecutionScope, _format_path(), _git_root() (+36 more)

### Community 8 - "Som client Som client Check"
Cohesion: 0.08
Nodes (23): build_parser(), _changed_files(), check_publish_gate(), _fail(), _git_root(), main(), _package_has_file_index_check(), print_json() (+15 more)

### Community 9 - "Windows ollama Audit"
Cohesion: 0.06
Nodes (30): AuditWriter, canonical_json(), compute_entry_hmac(), compute_sha256(), Write an audit entry. Returns True if successful, False otherwise.          Args, Return canonical JSON for HMAC computation., Write or update today's manifest., Compute SHA256 hash of bytes. (+22 more)

### Community 10 - "Overlord Verify governance consumer"
Cohesion: 0.1
Nodes (43): build_parser(), _consumer_record_relpath(), ConsumerRecord, ConsumerVerifyError, _contains_negated_forbidden_action(), _ensure_remote_reachable_governance_ref(), _expected_checksum(), _expected_entry_failures() (+35 more)

### Community 11 - "Overlord Assert execution scope"
Cohesion: 0.2
Nodes (4): _git(), RepoFixture, TestAssertExecutionScope, _working_directory()

### Community 12 - "Overlord Codex ingestion"
Cohesion: 0.1
Nodes (34): append_fail_fast_block_entry(), append_fail_fast_candidate(), append_fail_fast_table_entry(), append_progress_candidate(), bounded_text(), build_parser(), build_review_context(), build_schema_file() (+26 more)

### Community 13 - "Orchestrator Hitl relay queue"
Cohesion: 0.13
Nodes (38): append_audit(), atomic_write_json(), _base_packet(), _build_decision_packet(), _build_instruction_packet(), build_request(), _build_response_packet(), _build_resume_packet() (+30 more)

### Community 14 - "Overlord Deploy governance tooling"
Cohesion: 0.15
Nodes (34): add_common_args(), apply(), _build_local_ci_plan(), build_plan(), _consumer_record(), _consumer_record_relpath(), _ensure_relative_to(), _ensure_remote_reachable_governance_ref() (+26 more)

### Community 15 - "Orchestrator Packet queue"
Cohesion: 0.12
Nodes (20): append_audit(), _audit_path(), ensure_queue(), load_packet(), _load_plan(), QueueDecision, Replay audit events into logical latest states.      `latest_states` includes ac, replay_audit() (+12 more)

### Community 16 - "Local ci gate Local ci gate Report"
Cohesion: 0.12
Nodes (38): _branch_issue_number(), build_argument_parser(), _build_summary(), _changed_files_from_git(), ChangedFiles, _check_exit_code(), _check_matches_changed_files(), CheckResult (+30 more)

### Community 17 - "Overlord Pentagi sweep"
Cohesion: 0.12
Nodes (34): _expand_home(), governed_repos(), GovernedRepo, load_registry(), repo_names_enabled_for(), repos_enabled_for(), repos_root(), build_payload() (+26 more)

### Community 18 - "Orchestrator Self learning"
Cohesion: 0.14
Nodes (28): atomic_write_yaml(), build_report(), _date_from_text(), duplicate_counts(), enrich_packet(), _entry_id(), LearningEntry, LearningMatch (+20 more)

### Community 19 - "Deploy Deploy gate Missing"
Cohesion: 0.17
Nodes (31): default_env(), deploy_calls(), FakeCompleted, _make_cf_response(), make_runner(), run_gate(), run_gate_expect_error(), test_branch_binding_preflight_fails_on_mismatch() (+23 more)

### Community 20 - "Packages Hldpro sim"
Cohesion: 0.06
Nodes (14): ABC, BaseAggregator, ArtifactWriter, RunManifest, SimulationEngine, PersonaLoader, Load persona JSON files. Resolves local-first, shared fallback., Protocol (+6 more)

### Community 21 - "Overlord Validate handoff package"
Cohesion: 0.23
Nodes (8): _consumer_scope(), _dispatch_contract(), _handoff(), _plan(), _scope(), TestValidateHandoffPackage, _write_json(), _write_supporting_files()

### Community 22 - "Overlord Report governance consumer status"
Cohesion: 0.12
Nodes (22): build_parser(), build_report(), _count_or_none(), inspect_repo(), _load_json(), _load_record(), main(), _managed_paths() (+14 more)

### Community 23 - "Deploy Deploy verifier Domain"
Cohesion: 0.15
Nodes (30): _branch(), build_report(), _cname_note(), _deployment_url(), _domain_label(), _domain_result(), _domains(), emit_summary() (+22 more)

### Community 24 - "Knowledge base Graphify"
Cohesion: 0.13
Nodes (19): add_common_args(), build_plan(), build_refresh_command(), execute_refresh(), find_target(), git_hook_paths(), HelperError, HookPlan (+11 more)

### Community 25 - "Packet Validate Load"
Cohesion: 0.1
Nodes (30): _find_packet_file(), _load_packet(), load_pii_patterns(), _load_schema(), Load and compile PII patterns from pii-patterns.yml., Enforce cross-family independence for tier-1 dual-planner packets.      When pri, Refuse if any consecutive pair in the parent chain shares model_id across differ, Enforce expected handoff sequence with no tier jumps. (+22 more)

### Community 26 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.16
Nodes (29): _agent_registry_has_agent(), _agent_surface_exists(), _alternate_review_identity_gate_applies(), _branch_issue_number(), _display_path(), _find_plan_files(), _is_governance_surface(), _is_planning_evidence_surface() (+21 more)

### Community 27 - "Knowledge base Measure graphify usage"
Cohesion: 0.16
Nodes (28): aggregate_file_scores(), augment_workflow_doc_candidates(), baseline_results(), build_summary(), build_trace(), emit_usage_events(), estimate_tokens(), evaluate_relevance() (+20 more)

### Community 28 - "Local ci gate Local ci gate Profile"
Cohesion: 0.07
Nodes (1): TestLocalCiGate

### Community 29 - "Overlord Check local ci gate workflow"
Cohesion: 0.11
Nodes (14): _all_executable_lines(), _all_run_commands(), check_contract(), _contains_main_branch(), _executable_lines(), _failures_for_text(), _has_executable_line_starting_with(), _load_workflow() (+6 more)

### Community 30 - "Cli session supervisor"
Cohesion: 0.16
Nodes (21): append_jsonl(), AttemptResult, build_command(), event_paths(), kill_group(), main(), parse_args(), session_id() (+13 more)

### Community 31 - "Overlord Validate sql schema"
Cohesion: 0.15
Nodes (17): TestValidateSqlSchemaProbeContract, valid_contract(), build_parser(), _column_key(), _contract_paths(), _display(), _fixture_columns(), _load_contract() (+9 more)

### Community 32 - "Overlord Validate provisioning evidence"
Cohesion: 0.17
Nodes (12): ValidateProvisioningEvidenceTest, _default_paths(), _expand_scan_paths(), Finding, _is_env_file(), _is_scan_candidate(), main(), _normalize_repo_path() (+4 more)

### Community 33 - "Overlord Deploy governance tooling"
Cohesion: 0.24
Nodes (1): TestDeployGovernanceTooling

### Community 34 - "Overlord Validate closeout"
Cohesion: 0.16
Nodes (22): build_parser(), CloseoutDecision, evaluate(), _is_governance_surface(), _is_planning_only(), _issue_number(), main(), _matching_closeouts() (+14 more)

### Community 35 - "Overlord Validate handoff package"
Cohesion: 0.22
Nodes (22): _agent_registry_has_agent(), _agent_surface_exists(), _consumer_managed_paths(), _consumer_verifier_acceptance_gate_applies(), _criteria_verification_refs(), _discover_package_files(), _dispatch_contract_gate_applies(), _evidence_ref_gate_applies() (+14 more)

### Community 36 - "Deploy Deploy verifier Title"
Cohesion: 0.27
Nodes (20): FakeTransport, response(), run_report(), test_cache_busting_headers(), test_cname_mismatch_not_blocking(), test_different_deployment_ids(), test_domain_not_200(), test_expected_title_matches() (+12 more)

### Community 37 - "Overlord Org governance compendium"
Cohesion: 0.19
Nodes (21): build(), category_for(), describe_file(), esc(), FileInfo, first_comment(), first_heading(), frontmatter_field() (+13 more)

### Community 38 - "Remote mcp Operator connectivity"
Cohesion: 0.16
Nodes (12): BaseHTTPRequestHandler, build_parser(), build_payload(), _call_fixture(), _call_live(), Check, _fixture_server(), _FixtureMcpHandler (+4 more)

### Community 39 - "Orchestrator Delegation gate"
Cohesion: 0.15
Nodes (11): apply_policy(), classifier_match(), _contains_term(), decide(), deterministic_match(), GateDecision, _load_classifier(), load_rules() (+3 more)

### Community 40 - "Overlord Workflow local coverage"
Cohesion: 0.21
Nodes (12): _actual_workflows(), check_inventory(), _command_file_candidates(), _load_inventory(), main(), _normalize_path(), _validate_coverage(), _validate_required_snippets() (+4 more)

### Community 41 - "Overlord Check overlord backlog github alignment"
Cohesion: 0.14
Nodes (10): check_github_issue_open(), collect_section_lines(), fail(), issue_column_index(), issue_numbers(), main(), parse_markdown_row(), validate_section() (+2 more)

### Community 42 - "Orchestrator Read only observer"
Cohesion: 0.22
Nodes (17): _artifact(), ArtifactStatus, build_reports(), _count_open_issue_metadata(), _daemon_readiness(), _git_commit(), _latest_raw_issue_file(), main() (+9 more)

### Community 43 - "Overlord Deploy local ci gate"
Cohesion: 0.27
Nodes (1): TestDeployLocalCIGate

### Community 44 - "Overlord Check worker handoff route"
Cohesion: 0.37
Nodes (4): _git(), RepoFixture, _scope(), TestWorkerHandoffRoute

### Community 45 - "Overlord Deploy local ci gate"
Cohesion: 0.27
Nodes (14): add_common_args(), build_plan(), _common_preview_payload(), DeployError, DeployPlan, _existing_shim_state(), _fail(), _is_relative_to() (+6 more)

### Community 46 - "Overlord Check progress github issue staleness"
Cohesion: 0.23
Nodes (12): backlog_issues(), build_summary(), collect_active_issue_refs(), current_repo_slug(), fail(), gh_json(), IssueRef, main() (+4 more)

### Community 47 - "Overlord Check org repo inventory"
Cohesion: 0.28
Nodes (14): compare_inventory(), _default_branch_name(), _inventory_rows_from_payload(), InventoryDrift, load_inventory_file(), _load_json(), load_live_inventory(), main() (+6 more)

### Community 48 - "Remote mcp Monitor alert"
Cohesion: 0.23
Nodes (14): build_alert(), build_parser(), _contains_sensitive(), _load_payload(), main(), _now(), render_markdown(), _safe_text() (+6 more)

### Community 49 - "Session bootstrap Extract"
Cohesion: 0.27
Nodes (14): build_report(), codex_backlog_status(), extract_runbook_paths(), extract_som_excerpt(), format_hook_note(), git_branch(), main(), parse_args() (+6 more)

### Community 50 - "Overlord Automerge policy check"
Cohesion: 0.23
Nodes (6): _check_required_checks(), evaluate(), _labels(), main(), eligible_payload(), TestAutomergePolicyCheck

### Community 51 - "Overlord Validate closeout"
Cohesion: 0.32
Nodes (3): _json(), TestValidateCloseout, _write()

### Community 52 - "Lam Runtime inventory"
Cohesion: 0.14
Nodes (2): FakeResponse, TestRuntimeInventory

### Community 53 - "Overlord Schema guard"
Cohesion: 0.35
Nodes (3): _payload(), _run_hook(), TestSchemaGuardHook

### Community 54 - "Overlord Check plan preflight"
Cohesion: 0.26
Nodes (2): _run(), TestPlanPreflight

### Community 55 - "Overlord Validate governed repos"
Cohesion: 0.26
Nodes (1): GovernedReposValidationTests

### Community 56 - "Packet Emit Governance"
Cohesion: 0.19
Nodes (8): build_governance(), emit_dispatch_packet(), emit_packet(), main(), Emit a dispatch-ready packet that includes a complete governance block., Emit a minimal or dispatch-ready packet YAML file. Returns path to written file., Build a governance block dict for inclusion in a dispatch-ready packet., TestPacketEmitter

### Community 57 - "Bootstrap repo Exercise"
Cohesion: 0.29
Nodes (12): check(), main(), Exercise worktree invocation while still resolving the canonical governance root, Exercise failure when the canonical governance root is absent., Exercise Seek/Ponder bootstrap aliases without leaking synthetic values., Exercise Stampede bootstrap with production Tradier mapping and redaction., Exercise lam bootstrap with command-like vault values and missing optional keys., run_canonical_root_worktree_lam_bootstrap() (+4 more)

### Community 58 - "Overlord Check stage6 closeout"
Cohesion: 0.33
Nodes (3): _json(), TestCheckStage6Closeout, _write()

### Community 59 - "Overlord Branch switch guard"
Cohesion: 0.28
Nodes (2): run_hook(), TestBranchSwitchGuard

### Community 60 - "Overlord Check execution environment"
Cohesion: 0.42
Nodes (8): CheckExecutionEnvironmentTests, _git(), _make_repo(), _run(), _write(), _write_handoff(), _write_plan(), _write_scope()

### Community 61 - "Overlord Check org repo inventory"
Cohesion: 0.51
Nodes (1): TestOrgRepoInventory

### Community 62 - "Overlord Validate session error patterns"
Cohesion: 0.24
Nodes (7): TestValidateSessionErrorPatterns, _write_runbook(), _field_key(), _fields(), _pattern_sections(), _run_cli(), validate()

### Community 63 - "Overlord Validate session surfaces"
Cohesion: 0.5
Nodes (3): _settings(), ValidateSessionContractSurfacesTests, _write()

### Community 64 - "Overlord Check consumer rollout publish gate"
Cohesion: 0.33
Nodes (1): TestCheckConsumerRolloutPublishGate

### Community 65 - "Overlord Lane bootstrap"
Cohesion: 0.3
Nodes (2): run_helper(), TestLaneBootstrap

### Community 66 - "Deploy Inventory direct upload projects"
Cohesion: 0.33
Nodes (11): _api_get_projects(), _deployment_metadata(), _domains(), _git_provider_status(), inventory(), _latest_deployment(), _load_json(), main() (+3 more)

### Community 67 - "Codex fire Failure"
Cohesion: 0.36
Nodes (8): run_fire(), test_exec_failure_after_successful_preflight_logs_and_signals(), test_preflight_failure_logs_and_exits_fast(), test_preflight_timeout_logs_and_exits_fast(), test_review_template_default_persona_reaches_codex_fire(), test_review_template_propagates_wrapper_failure(), test_success_does_not_write_failure_log(), write_fake_codex()

### Community 68 - "Overlord Lane bootstrap"
Cohesion: 0.35
Nodes (10): cleanup_advice(), infer_repo_slug(), LanePolicy, load_policy(), main(), _match(), normalize_slug(), parse_args() (+2 more)

### Community 69 - "Overlord Memory integrity"
Cohesion: 0.35
Nodes (9): build_parser(), check_memory_exists(), inspect_repo(), load_memory_lines(), main(), memory_dir_for_repo(), MemoryInspection, parse_pointer_filenames() (+1 more)

### Community 70 - "Knowledge base Graph"
Cohesion: 0.38
Nodes (10): build_graph(), _community_label(), _derive_path_phrase(), _derive_path_tokens(), infer_community_labels(), main(), _normalize_phrase(), _sanitize_markdown_artifacts() (+2 more)

### Community 71 - "Orchestrator Delegation Owned"
Cohesion: 0.45
Nodes (10): _payload(), _run_hook(), test_hook_allows_read_even_when_text_matches_owned_work(), test_hook_blocks_agent_owned_work_before_file_path_logic(), test_hook_blocks_task_tool_owned_work(), test_hook_bypass_allows_and_logs(), test_hook_configured_mcp_endpoint_fails_open_on_unavailable_gate(), test_hook_preserves_new_code_file_block_for_common_extensions() (+2 more)

### Community 72 - "Overlord Validate registry surfaces"
Cohesion: 0.49
Nodes (9): check(), fail(), main(), read_text(), repos_for_static_checkout(), validate_docs_surfaces(), validate_runtime_registry_consumers(), validate_static_checkout_workflow() (+1 more)

### Community 73 - "Lam Runtime inventory"
Cohesion: 0.4
Nodes (9): build_inventory(), import_available(), local_runtime(), mac_hardware(), main(), memory_budget(), pii_guardrail(), _run() (+1 more)

### Community 74 - "Knowledge base Graphify targets"
Cohesion: 0.38
Nodes (9): filtered_targets(), find_target(), load_manifest(), main(), print_json(), print_shell(), print_stage_paths(), print_tsv() (+1 more)

### Community 75 - "Packages Hldpro sim Providers"
Cohesion: 0.2
Nodes (0): 

### Community 76 - "Knowledge base Graphify usage logging"
Cohesion: 0.61
Nodes (8): check(), main(), run_command(), test_logger_backwards_compatible(), test_logger_query_trace_fields(), test_measurement_falls_back_from_stale_governance_repo_path(), test_measurement_outputs_query_traces(), test_schema_shape()

### Community 77 - "Session bootstrap Startup"
Cohesion: 0.46
Nodes (4): add_startup_scope_bundle(), make_repo(), run_contract(), SessionBootstrapContractTests

### Community 78 - "Overlord Check plan preflight"
Cohesion: 0.46
Nodes (7): block_reason(), detect_bash_write_target(), evaluate(), is_governed_path(), main(), parse_args(), recent_plan()

### Community 79 - "Overlord Effectiveness metrics"
Cohesion: 0.46
Nodes (7): collect_repo_metrics(), main(), parse_iso(), pct(), render_markdown(), RepoMetrics, run()

### Community 80 - "Overlord Memory integrity"
Cohesion: 0.32
Nodes (1): MemoryIntegrityTests

### Community 81 - "Packet Run specialist packet"
Cohesion: 0.43
Nodes (6): _load_json(), _load_yaml(), main(), _repo_ref(), _resolve_model_settings(), run_specialist_packet()

### Community 82 - "Overlord Validate governed repos"
Cohesion: 0.67
Nodes (6): check(), fail(), load_json(), main(), validate_graphify_reconciliation(), validate_registry_shape()

### Community 83 - "Orchestrator Read only observer"
Cohesion: 0.48
Nodes (2): _copy_fixture(), TestReadOnlyObserver

### Community 84 - "Packages Hldpro sim Stampede"
Cohesion: 0.4
Nodes (4): BaseAggregator, BaseModel, NarrativeAggregator, NarrativeOutcome

### Community 85 - "Overlord Sweep artifact pr"
Cohesion: 0.4
Nodes (1): SweepArtifactPrTest

### Community 86 - "Overlord Validate session surfaces"
Cohesion: 0.7
Nodes (4): _find_hook_command(), main(), _normalized(), validate()

### Community 87 - "Overlord Sweep artifact pr"
Cohesion: 0.7
Nodes (4): artifact_branch(), artifact_scope(), main(), write_scope()

### Community 88 - "Knowledge base Log graphify usage"
Cohesion: 0.7
Nodes (4): append_event(), build_event(), main(), parse_args()

### Community 89 - "Packet Hitl relay schema"
Cohesion: 0.8
Nodes (4): _load(), test_invalid_hitl_relay_examples_fail(), test_valid_hitl_relay_examples_pass(), _validator()

### Community 90 - "Packet Run specialist packet"
Cohesion: 0.6
Nodes (2): _packet(), RunSpecialistPacketTests

### Community 91 - "Deploy Inventory direct upload projects"
Cohesion: 0.5
Nodes (0): 

### Community 92 - "Knowledge base Graphify governance"
Cohesion: 0.83
Nodes (3): check(), is_ignored(), main()

### Community 93 - "Knowledge base Update knowledge"
Cohesion: 0.83
Nodes (3): main(), replace_section(), summary_line()

### Community 94 - "Packages Hldpro sim Stampede"
Cohesion: 0.67
Nodes (2): MockProvider, test_stampede_e2e()

### Community 95 - "Overlord Render github issue feed"
Cohesion: 1.0
Nodes (2): main(), render_issue()

### Community 96 - "Knowledge base Push graph to neo4j"
Cohesion: 1.0
Nodes (2): build_scoped_graph(), main()

### Community 97 - "Packages Hldpro sim Runner"
Cohesion: 0.67
Nodes (0): 

### Community 98 - "Packages Hldpro sim Engine"
Cohesion: 1.0
Nodes (0): 

### Community 99 - "Packages Hldpro sim Artifacts"
Cohesion: 1.0
Nodes (0): 

### Community 100 - "Windows ollama Submit Temporary"
Cohesion: 1.0
Nodes (1): Temporary audit directory for testing.

### Community 101 - "Som client Som client From"
Cohesion: 1.0
Nodes (1): Build a client from well-known environment variables.

### Community 102 - "Packages Hldpro sim Personas"
Cohesion: 1.0
Nodes (1): Convenience: load shared dir from bundled package personas/.

## Knowledge Gaps
- **127 isolated node(s):** `Exercise lam bootstrap with command-like vault values and missing optional keys.`, `Exercise worktree invocation while still resolving the canonical governance root`, `Exercise failure when the canonical governance root is absent.`, `Exercise Seek/Ponder bootstrap aliases without leaking synthetic values.`, `Exercise Stampede bootstrap with production Tradier mapping and redaction.` (+122 more)
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

- **Why does `ConsumerVerifyError` connect `Overlord Verify governance consumer` to `Som client Som client Check`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Why does `GateError` connect `Local ci gate Local ci gate Report` to `Som client Som client Check`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 28 inferred relationships involving `RepoFixture` (e.g. with `.test_allows_changes_in_allowed_paths_dirty_tree_mode()` and `.test_planning_only_diff_inside_allowed_paths_passes()`) actually correct?**
  _`RepoFixture` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `_tier1_packet()` (e.g. with `.test_tier1_without_parent_passes()` and `.test_same_family_dual_planner_refused()`) actually correct?**
  _`_tier1_packet()` has 30 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Exercise lam bootstrap with command-like vault values and missing optional keys.`, `Exercise worktree invocation while still resolving the canonical governance root`, `Exercise failure when the canonical governance root is absent.` to the rest of the system?**
  _127 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Deploy Deploy gate Windows` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
- **Should `Remote mcp Verify audit` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._