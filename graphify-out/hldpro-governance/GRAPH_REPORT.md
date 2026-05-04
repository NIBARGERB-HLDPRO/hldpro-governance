# Graph Report - hldpro-governance  (2026-05-03)

## Corpus Check
- Large corpus: 3598 files · ~786,681 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 2360 nodes · 4826 edges · 113 communities detected
- Extraction: 47% EXTRACTED · 53% INFERRED · 0% AMBIGUOUS · INFERRED: 2554 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `TestVerifyGovernanceConsumer` - 49 edges
2. `TestActiveIssueBranchContract` - 44 edges
3. `TestAssertExecutionScope` - 43 edges
4. `RepoFixture` - 38 edges
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

### Community 0 - "Remote mcp Verify audit"
Cohesion: 0.04
Nodes (69): build_parser(), _env_has_live_markers(), main(), _run_fixture(), _run_live(), _scan_evidence_dir(), _stage_d_args(), _build_fixture_server() (+61 more)

### Community 1 - "Packet Validate Passes"
Cohesion: 0.05
Nodes (25): _dispatch_packet(), _make_parent_packet(), Cross-family independence violated: both planners are anthropic., anthropic + openai is fine., Parent file absent → warn, don't refuse., Sanity: the patterns file should be present in this worktree., Non-LAM role with PII artifact path must be refused., worker-lam role is allowed to handle PII artifacts. (+17 more)

### Community 2 - "Windows ollama Submit"
Cohesion: 0.05
Nodes (40): AuditWriter, canonical_json(), compute_entry_hmac(), compute_sha256(), Write an audit entry. Returns True if successful, False otherwise.          Args, Return canonical JSON for HMAC computation., Write or update today's manifest., Compute SHA256 hash of bytes. (+32 more)

### Community 3 - "Windows ollama Submit"
Cohesion: 0.03
Nodes (37): Test that clean prompt passes PII detection., Negative test: non-allowlisted model., Test that non-allowlisted model is rejected., Test that allowlisted model passes allowlist check., Negative test: unreachable endpoint., Test that unreachable endpoint raises appropriate error., Test that endpoint timeout is handled., Test that reachable endpoint succeeds. (+29 more)

### Community 4 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.08
Nodes (4): _dispatch_contract(), _plan(), TestActiveIssueBranchContract, TestGovernanceSurfacePlanGate

### Community 5 - "Overlord Assert execution scope"
Cohesion: 0.08
Nodes (52): _branch_issue_number(), _changed_paths(), _changed_paths_from_file(), check_scope(), _current_branch(), ExecutionScope, _format_path(), _git_root() (+44 more)

### Community 6 - "Som client Som client Mcp"
Cohesion: 0.06
Nodes (23): BaseHTTPRequestHandler, build_parser(), build_payload(), _call_fixture(), _call_live(), Check, _fixture_server(), _FixtureMcpHandler (+15 more)

### Community 7 - "Overlord Verify governance consumer"
Cohesion: 0.17
Nodes (1): TestVerifyGovernanceConsumer

### Community 8 - "Overlord Assert execution scope"
Cohesion: 0.18
Nodes (4): _git(), RepoFixture, TestAssertExecutionScope, _working_directory()

### Community 9 - "Packet Validate hitl relay"
Cohesion: 0.08
Nodes (38): build_parser(), build_payload(), _call_fixture(), _call_live(), Check, _fixture_request(), _latest_live_instruction(), main() (+30 more)

### Community 10 - "Overlord Validate handoff package Closeout"
Cohesion: 0.09
Nodes (44): build_parser(), CloseoutDecision, evaluate(), _is_governance_surface(), _is_planning_only(), _issue_number(), main(), _matching_closeouts() (+36 more)

### Community 11 - "Overlord Verify governance consumer"
Cohesion: 0.1
Nodes (43): build_parser(), _consumer_record_relpath(), ConsumerRecord, ConsumerVerifyError, _contains_negated_forbidden_action(), _ensure_remote_reachable_governance_ref(), _expected_checksum(), _expected_entry_failures() (+35 more)

### Community 12 - "Overlord Codex ingestion"
Cohesion: 0.1
Nodes (34): append_fail_fast_block_entry(), append_fail_fast_candidate(), append_fail_fast_table_entry(), append_progress_candidate(), bounded_text(), build_parser(), build_review_context(), build_schema_file() (+26 more)

### Community 13 - "Orchestrator Hitl relay queue"
Cohesion: 0.13
Nodes (38): append_audit(), atomic_write_json(), _base_packet(), _build_decision_packet(), _build_instruction_packet(), build_request(), _build_response_packet(), _build_resume_packet() (+30 more)

### Community 14 - "Deploy Deploy gate Run"
Cohesion: 0.13
Nodes (37): ArtifactStats, branch_binding_preflight(), _check_pages_limits(), count_files(), deploy(), emit_evidence(), enforce_pages_limits(), extract_deployment_url() (+29 more)

### Community 15 - "Packages Hldpro sim"
Cohesion: 0.06
Nodes (14): ABC, BaseAggregator, ArtifactWriter, RunManifest, SimulationEngine, PersonaLoader, Load persona JSON files. Resolves process-agents/ first, then local, then person, Protocol (+6 more)

### Community 16 - "Fail closed missing"
Cohesion: 0.07
Nodes (26): _extract_step_run(), _load_validate_module(), Tests for fail-closed behaviour when BASE_SHA is empty (AC3).  These tests asser, Run a bash snippet and return the completed process., validate_cross_review_evidence must return violations when BASE_SHA is empty., detect_cross_review_violations must fail closed on empty BASE_SHA., detect_cross_review_violations must fail closed on empty HEAD_SHA., detect_cross_review_violations must fail closed when both SHAs are empty. (+18 more)

### Community 17 - "Overlord Deploy governance tooling"
Cohesion: 0.15
Nodes (34): add_common_args(), apply(), _build_local_ci_plan(), build_plan(), _consumer_record(), _consumer_record_relpath(), _ensure_relative_to(), _ensure_remote_reachable_governance_ref() (+26 more)

### Community 18 - "Local ci gate Local ci gate Report"
Cohesion: 0.12
Nodes (38): _branch_issue_number(), build_argument_parser(), _build_summary(), _changed_files_from_git(), ChangedFiles, _check_exit_code(), _check_matches_changed_files(), CheckResult (+30 more)

### Community 19 - "Orchestrator Packet queue"
Cohesion: 0.12
Nodes (20): append_audit(), _audit_path(), ensure_queue(), load_packet(), _load_plan(), QueueDecision, Replay audit events into logical latest states.      `latest_states` includes ac, replay_audit() (+12 more)

### Community 20 - "Overlord Pentagi sweep"
Cohesion: 0.12
Nodes (34): _expand_home(), governed_repos(), GovernedRepo, load_registry(), repo_names_enabled_for(), repos_enabled_for(), repos_root(), build_payload() (+26 more)

### Community 21 - "Overlord Check governance issue branch parity"
Cohesion: 0.09
Nodes (20): active_governance_issue_numbers(), branch_issue_number(), check_branch_parity(), current_branch(), fail(), main(), parse_args(), check_github_issue_open() (+12 more)

### Community 22 - "Orchestrator Self learning"
Cohesion: 0.14
Nodes (28): atomic_write_yaml(), build_report(), _date_from_text(), duplicate_counts(), enrich_packet(), _entry_id(), LearningEntry, LearningMatch (+20 more)

### Community 23 - "Deploy Deploy gate Missing"
Cohesion: 0.17
Nodes (31): default_env(), deploy_calls(), FakeCompleted, _make_cf_response(), make_runner(), run_gate(), run_gate_expect_error(), test_branch_binding_preflight_fails_on_mismatch() (+23 more)

### Community 24 - "Overlord Validate handoff package"
Cohesion: 0.23
Nodes (8): _consumer_scope(), _dispatch_contract(), _handoff(), _plan(), _scope(), TestValidateHandoffPackage, _write_json(), _write_supporting_files()

### Community 25 - "Overlord Report governance consumer status"
Cohesion: 0.12
Nodes (22): build_parser(), build_report(), _count_or_none(), inspect_repo(), _load_json(), _load_record(), main(), _managed_paths() (+14 more)

### Community 26 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.14
Nodes (31): _agent_registry_has_agent(), _agent_surface_exists(), _alternate_review_identity_gate_applies(), _branch_issue_number(), _display_path(), _find_plan_files(), _is_governance_surface(), _is_planning_evidence_surface() (+23 more)

### Community 27 - "Deploy Deploy verifier Domain"
Cohesion: 0.15
Nodes (30): _branch(), build_report(), _cname_note(), _deployment_url(), _domain_label(), _domain_result(), _domains(), emit_summary() (+22 more)

### Community 28 - "Knowledge base Graphify"
Cohesion: 0.13
Nodes (19): add_common_args(), build_plan(), build_refresh_command(), execute_refresh(), find_target(), git_hook_paths(), HelperError, HookPlan (+11 more)

### Community 29 - "Packet Validate Load"
Cohesion: 0.1
Nodes (30): _find_packet_file(), _load_packet(), load_pii_patterns(), _load_schema(), Load and compile PII patterns from pii-patterns.yml., Enforce cross-family independence for tier-1 dual-planner packets.      When pri, Refuse if any consecutive pair in the parent chain shares model_id across differ, Enforce expected handoff sequence with no tier jumps. (+22 more)

### Community 30 - "Overlord Deploy local ci gate"
Cohesion: 0.15
Nodes (26): build_parser(), _changed_files(), check_publish_gate(), _fail(), _git_root(), main(), _package_has_file_index_check(), print_json() (+18 more)

### Community 31 - "Knowledge base Measure graphify usage"
Cohesion: 0.16
Nodes (28): aggregate_file_scores(), augment_workflow_doc_candidates(), baseline_results(), build_summary(), build_trace(), emit_usage_events(), estimate_tokens(), evaluate_relevance() (+20 more)

### Community 32 - "Local ci gate Local ci gate Profile"
Cohesion: 0.07
Nodes (1): TestLocalCiGate

### Community 33 - "Overlord Check local ci gate workflow"
Cohesion: 0.11
Nodes (14): _all_executable_lines(), _all_run_commands(), check_contract(), _contains_main_branch(), _executable_lines(), _failures_for_text(), _has_executable_line_starting_with(), _load_workflow() (+6 more)

### Community 34 - "Cli session supervisor"
Cohesion: 0.16
Nodes (21): append_jsonl(), AttemptResult, build_command(), event_paths(), kill_group(), main(), parse_args(), session_id() (+13 more)

### Community 35 - "Overlord Validate sql schema"
Cohesion: 0.15
Nodes (17): TestValidateSqlSchemaProbeContract, valid_contract(), build_parser(), _column_key(), _contract_paths(), _display(), _fixture_columns(), _load_contract() (+9 more)

### Community 36 - "Overlord Validate provisioning evidence"
Cohesion: 0.17
Nodes (12): ValidateProvisioningEvidenceTest, _default_paths(), _expand_scan_paths(), Finding, _is_env_file(), _is_scan_candidate(), main(), _normalize_repo_path() (+4 more)

### Community 37 - "Cross review evidence"
Cohesion: 0.08
Nodes (15): _load_module(), Tests for cross-review evidence validation (AC2).  These tests verify that a PR, Changes to agents/*.md must trigger cross-review enforcement., Changes to hooks/*.sh must trigger cross-review enforcement., A plain file change (docs/PROGRESS.md) should not trigger enforcement., An empty diff should pass without violations., Changes to .github/workflows/check-*.yml must trigger enforcement., Changes to AGENT_REGISTRY.md must trigger enforcement. (+7 more)

### Community 38 - "Overlord Deploy governance tooling"
Cohesion: 0.24
Nodes (1): TestDeployGovernanceTooling

### Community 39 - "Deploy Deploy verifier Title"
Cohesion: 0.27
Nodes (20): FakeTransport, response(), run_report(), test_cache_busting_headers(), test_cname_mismatch_not_blocking(), test_different_deployment_ids(), test_domain_not_200(), test_expected_title_matches() (+12 more)

### Community 40 - "Overlord Org governance compendium"
Cohesion: 0.19
Nodes (21): build(), category_for(), describe_file(), esc(), FileInfo, first_comment(), first_heading(), frontmatter_field() (+13 more)

### Community 41 - "Orchestrator Delegation gate"
Cohesion: 0.15
Nodes (11): apply_policy(), classifier_match(), _contains_term(), decide(), deterministic_match(), GateDecision, _load_classifier(), load_rules() (+3 more)

### Community 42 - "Overlord Workflow local coverage"
Cohesion: 0.21
Nodes (12): _actual_workflows(), check_inventory(), _command_file_candidates(), _load_inventory(), main(), _normalize_path(), _validate_coverage(), _validate_required_snippets() (+4 more)

### Community 43 - "Overlord Check governance execution scope"
Cohesion: 0.43
Nodes (3): _git(), RepoFixture, TestCheckGovernanceHookExecutionScope

### Community 44 - "Overlord Check plan preflight"
Cohesion: 0.19
Nodes (2): _run(), TestPlanPreflight

### Community 45 - "Orchestrator Read only observer"
Cohesion: 0.22
Nodes (17): _artifact(), ArtifactStatus, build_reports(), _count_open_issue_metadata(), _daemon_readiness(), _git_commit(), _latest_raw_issue_file(), main() (+9 more)

### Community 46 - "Overlord Deploy local ci gate"
Cohesion: 0.27
Nodes (1): TestDeployLocalCIGate

### Community 47 - "Overlord Check worker handoff route"
Cohesion: 0.37
Nodes (4): _git(), RepoFixture, _scope(), TestWorkerHandoffRoute

### Community 48 - "Overlord Schema guard"
Cohesion: 0.32
Nodes (3): _payload(), _run_hook(), TestSchemaGuardHook

### Community 49 - "Overlord Check progress github issue staleness"
Cohesion: 0.23
Nodes (12): backlog_issues(), build_summary(), collect_active_issue_refs(), current_repo_slug(), fail(), gh_json(), IssueRef, main() (+4 more)

### Community 50 - "Overlord Check org repo inventory"
Cohesion: 0.28
Nodes (14): compare_inventory(), _default_branch_name(), _inventory_rows_from_payload(), InventoryDrift, load_inventory_file(), _load_json(), load_live_inventory(), main() (+6 more)

### Community 51 - "Remote mcp Monitor alert"
Cohesion: 0.23
Nodes (14): build_alert(), build_parser(), _contains_sensitive(), _load_payload(), main(), _now(), render_markdown(), _safe_text() (+6 more)

### Community 52 - "Orchestrator Delegation Owned"
Cohesion: 0.28
Nodes (13): _payload(), _run_hook(), test_hook_allows_edit_on_owned_in_scope_file(), test_hook_allows_multiedit_on_owned_in_scope_file(), test_hook_allows_read_even_when_text_matches_owned_work(), test_hook_blocks_agent_owned_work_before_file_path_logic(), test_hook_blocks_task_tool_owned_work(), test_hook_bypass_allows_and_logs() (+5 more)

### Community 53 - "Session bootstrap Extract"
Cohesion: 0.27
Nodes (14): build_report(), codex_backlog_status(), extract_runbook_paths(), extract_som_excerpt(), format_hook_note(), git_branch(), main(), parse_args() (+6 more)

### Community 54 - "Overlord Automerge policy check"
Cohesion: 0.23
Nodes (6): _check_required_checks(), evaluate(), _labels(), main(), eligible_payload(), TestAutomergePolicyCheck

### Community 55 - "Overlord Validate closeout"
Cohesion: 0.32
Nodes (3): _json(), TestValidateCloseout, _write()

### Community 56 - "Lam Runtime inventory"
Cohesion: 0.14
Nodes (2): FakeResponse, TestRuntimeInventory

### Community 57 - "Check acceptance audit"
Cohesion: 0.2
Nodes (13): Tests for check_acceptance_audit.py — functional acceptance audit CI gate., Helper: run check_acceptance_audit.py with given args against a temp audit dir., PASS artifact with matching issue_number and overall_verdict=PASS → exits 0., Non-existent audit dir → exits 1., Audit dir exists but no artifact for the branch issue → exits 1., Non-issue branch (e.g. chore/foo) → exits 0 (exempt)., planning_only flag → exits 0 regardless of audit artifacts., run_check() (+5 more)

### Community 58 - "Overlord Fail fast state"
Cohesion: 0.31
Nodes (13): cmd_check(), cmd_record(), cmd_resolve(), _extract_pattern(), _find_entry(), _load_state(), main(), _now_iso() (+5 more)

### Community 59 - "Overlord Check plan preflight"
Cohesion: 0.33
Nodes (13): block_reason(), _clean_token(), detect_bash_write_target(), evaluate(), _extract_cp_mv_install_target(), _extract_dd_target(), _extract_mutation_file_after_options(), _extract_positional_target() (+5 more)

### Community 60 - "Overlord Validate governed repos"
Cohesion: 0.26
Nodes (1): GovernedReposValidationTests

### Community 61 - "Packet Emit Governance"
Cohesion: 0.19
Nodes (8): build_governance(), emit_dispatch_packet(), emit_packet(), main(), Emit a dispatch-ready packet that includes a complete governance block., Emit a minimal or dispatch-ready packet YAML file. Returns path to written file., Build a governance block dict for inclusion in a dispatch-ready packet., TestPacketEmitter

### Community 62 - "Bootstrap repo Exercise"
Cohesion: 0.29
Nodes (12): check(), main(), Exercise worktree invocation while still resolving the canonical governance root, Exercise failure when the canonical governance root is absent., Exercise Seek/Ponder bootstrap aliases without leaking synthetic values., Exercise Stampede bootstrap with production Tradier mapping and redaction., Exercise lam bootstrap with command-like vault values and missing optional keys., run_canonical_root_worktree_lam_bootstrap() (+4 more)

### Community 63 - "Overlord Check stage6 closeout"
Cohesion: 0.33
Nodes (3): _json(), TestCheckStage6Closeout, _write()

### Community 64 - "Overlord Branch switch guard"
Cohesion: 0.28
Nodes (2): run_hook(), TestBranchSwitchGuard

### Community 65 - "Overlord Check execution environment"
Cohesion: 0.42
Nodes (8): CheckExecutionEnvironmentTests, _git(), _make_repo(), _run(), _write(), _write_handoff(), _write_plan(), _write_scope()

### Community 66 - "Overlord Validate session error patterns"
Cohesion: 0.24
Nodes (7): TestValidateSessionErrorPatterns, _write_runbook(), _field_key(), _fields(), _pattern_sections(), _run_cli(), validate()

### Community 67 - "Overlord Check org repo inventory"
Cohesion: 0.51
Nodes (1): TestOrgRepoInventory

### Community 68 - "Overlord Validate session surfaces"
Cohesion: 0.5
Nodes (3): _settings(), ValidateSessionContractSurfacesTests, _write()

### Community 69 - "Overlord Check consumer rollout publish gate"
Cohesion: 0.33
Nodes (1): TestCheckConsumerRolloutPublishGate

### Community 70 - "Overlord Lane bootstrap"
Cohesion: 0.3
Nodes (2): run_helper(), TestLaneBootstrap

### Community 71 - "Deploy Inventory direct upload projects"
Cohesion: 0.33
Nodes (11): _api_get_projects(), _deployment_metadata(), _domains(), _git_provider_status(), inventory(), _latest_deployment(), _load_json(), main() (+3 more)

### Community 72 - "Conftest Git"
Cohesion: 0.2
Nodes (10): env_no_pr_context(), env_valid_pr_context(), Shared pytest fixtures for governance contract tests.  Fixtures -------- tmp_git, Write a sample cross-review artifact and return (path, frontmatter_dict)., Environment variables simulating a push event with no PR context., Environment variables simulating a valid PR event., Yield a temporary directory initialised as a git repo., sample_cross_review_file() (+2 more)

### Community 73 - "Codex fire Failure"
Cohesion: 0.36
Nodes (8): run_fire(), test_exec_failure_after_successful_preflight_logs_and_signals(), test_preflight_failure_logs_and_exits_fast(), test_preflight_timeout_logs_and_exits_fast(), test_review_template_default_persona_reaches_codex_fire(), test_review_template_propagates_wrapper_failure(), test_success_does_not_write_failure_log(), write_fake_codex()

### Community 74 - "Overlord Lane bootstrap"
Cohesion: 0.35
Nodes (10): cleanup_advice(), infer_repo_slug(), LanePolicy, load_policy(), main(), _match(), normalize_slug(), parse_args() (+2 more)

### Community 75 - "Overlord Memory integrity"
Cohesion: 0.35
Nodes (9): build_parser(), check_memory_exists(), inspect_repo(), load_memory_lines(), main(), memory_dir_for_repo(), MemoryInspection, parse_pointer_filenames() (+1 more)

### Community 76 - "Knowledge base Graph"
Cohesion: 0.38
Nodes (10): build_graph(), _community_label(), _derive_path_phrase(), _derive_path_tokens(), infer_community_labels(), main(), _normalize_phrase(), _sanitize_markdown_artifacts() (+2 more)

### Community 77 - "Overlord Validate cross review evidence"
Cohesion: 0.31
Nodes (9): _cross_review_files(), detect_cross_review_violations(), _is_cross_review_trigger(), main(), Return True if *path* should trigger cross-review enforcement., Return paths that are cross-review artifacts (raw/cross-review/*.md)., Return an error string if newly-introduced cross-review evidence must be rejecte, Validate cross-review evidence for a set of changed files.      Parameters     - (+1 more)

### Community 78 - "Overlord Validate registry surfaces"
Cohesion: 0.49
Nodes (9): check(), fail(), main(), read_text(), repos_for_static_checkout(), validate_docs_surfaces(), validate_runtime_registry_consumers(), validate_static_checkout_workflow() (+1 more)

### Community 79 - "Lam Runtime inventory"
Cohesion: 0.4
Nodes (9): build_inventory(), import_available(), local_runtime(), mac_hardware(), main(), memory_budget(), pii_guardrail(), _run() (+1 more)

### Community 80 - "Knowledge base Graphify targets"
Cohesion: 0.38
Nodes (9): filtered_targets(), find_target(), load_manifest(), main(), print_json(), print_shell(), print_stage_paths(), print_tsv() (+1 more)

### Community 81 - "Packages Hldpro sim Providers"
Cohesion: 0.2
Nodes (0): 

### Community 82 - "Knowledge base Graphify usage logging"
Cohesion: 0.61
Nodes (8): check(), main(), run_command(), test_logger_backwards_compatible(), test_logger_query_trace_fields(), test_measurement_falls_back_from_stale_governance_repo_path(), test_measurement_outputs_query_traces(), test_schema_shape()

### Community 83 - "Session bootstrap Startup"
Cohesion: 0.46
Nodes (4): add_startup_scope_bundle(), make_repo(), run_contract(), SessionBootstrapContractTests

### Community 84 - "Overlord Effectiveness metrics"
Cohesion: 0.46
Nodes (7): collect_repo_metrics(), main(), parse_iso(), pct(), render_markdown(), RepoMetrics, run()

### Community 85 - "Overlord Memory integrity"
Cohesion: 0.32
Nodes (1): MemoryIntegrityTests

### Community 86 - "Packet Run specialist packet"
Cohesion: 0.43
Nodes (6): _load_json(), _load_yaml(), main(), _repo_ref(), _resolve_model_settings(), run_specialist_packet()

### Community 87 - "Overlord Backlog match"
Cohesion: 0.43
Nodes (6): _is_in_done_section(), _issue_pattern(), main(), Return True if line_index falls inside a Done/Completed section heading., Return True if path contains an open (non-Done) entry for issue_number., search_file()

### Community 88 - "Overlord Validate governed repos"
Cohesion: 0.67
Nodes (6): check(), fail(), load_json(), main(), validate_graphify_reconciliation(), validate_registry_shape()

### Community 89 - "Orchestrator Read only observer"
Cohesion: 0.48
Nodes (2): _copy_fixture(), TestReadOnlyObserver

### Community 90 - "Functional acceptance auditor"
Cohesion: 0.6
Nodes (4): _load_json(), _sample_pass_audit(), test_schema_accepts_sample_pass_audit(), test_schema_rejects_missing_overall_verdict()

### Community 91 - "Packages Hldpro sim Process"
Cohesion: 0.33
Nodes (0): 

### Community 92 - "Packages Hldpro sim Stampede"
Cohesion: 0.4
Nodes (4): BaseAggregator, BaseModel, NarrativeAggregator, NarrativeOutcome

### Community 93 - "Overlord Sweep artifact pr"
Cohesion: 0.4
Nodes (1): SweepArtifactPrTest

### Community 94 - "Overlord Validate session surfaces"
Cohesion: 0.7
Nodes (4): _find_hook_command(), main(), _normalized(), validate()

### Community 95 - "Overlord Sweep artifact pr"
Cohesion: 0.7
Nodes (4): artifact_branch(), artifact_scope(), main(), write_scope()

### Community 96 - "Knowledge base Log graphify usage"
Cohesion: 0.7
Nodes (4): append_event(), build_event(), main(), parse_args()

### Community 97 - "Packet Hitl relay schema"
Cohesion: 0.8
Nodes (4): _load(), test_invalid_hitl_relay_examples_fail(), test_valid_hitl_relay_examples_pass(), _validator()

### Community 98 - "Packet Run specialist packet"
Cohesion: 0.6
Nodes (2): _packet(), RunSpecialistPacketTests

### Community 99 - "Deploy Inventory direct upload projects"
Cohesion: 0.5
Nodes (0): 

### Community 100 - "Knowledge base Graphify governance"
Cohesion: 0.83
Nodes (3): check(), is_ignored(), main()

### Community 101 - "Knowledge base Update knowledge"
Cohesion: 0.83
Nodes (3): main(), replace_section(), summary_line()

### Community 102 - "Packages Hldpro sim Stampede"
Cohesion: 0.67
Nodes (2): MockProvider, test_stampede_e2e()

### Community 103 - "Overlord Render github issue feed"
Cohesion: 1.0
Nodes (2): main(), render_issue()

### Community 104 - "Knowledge base Push graph to neo4j"
Cohesion: 1.0
Nodes (2): build_scoped_graph(), main()

### Community 105 - "Packages Hldpro sim Api"
Cohesion: 0.67
Nodes (0): 

### Community 106 - "Packages Hldpro sim Runner"
Cohesion: 0.67
Nodes (0): 

### Community 107 - "Packages Hldpro sim Engine"
Cohesion: 1.0
Nodes (0): 

### Community 108 - "Packages Hldpro sim Artifacts"
Cohesion: 1.0
Nodes (0): 

### Community 109 - "Fail closed missing Each"
Cohesion: 1.0
Nodes (1): Each workflow must contain a step whose run: block exits 1 on empty BASE_SHA.

### Community 110 - "Windows ollama Submit Temporary"
Cohesion: 1.0
Nodes (1): Temporary audit directory for testing.

### Community 111 - "Som client Som client From"
Cohesion: 1.0
Nodes (1): Build a client from well-known environment variables.

### Community 112 - "Packages Hldpro sim Personas"
Cohesion: 1.0
Nodes (1): Convenience: prefer process-agents/ with bundled personas/ fallback.

## Knowledge Gaps
- **180 isolated node(s):** `Shared pytest fixtures for governance contract tests.  Fixtures -------- tmp_git`, `Yield a temporary directory initialised as a git repo.`, `Write a sample cross-review artifact and return (path, frontmatter_dict).`, `Environment variables simulating a push event with no PR context.`, `Environment variables simulating a valid PR event.` (+175 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Packages Hldpro sim Engine`** (2 nodes): `test_engine.py`, `test_engine_passes_template_results_to_provider()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Packages Hldpro sim Artifacts`** (2 nodes): `test_artifacts.py`, `test_artifact_writer_writes_manifest_and_outcomes()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Fail closed missing Each`** (1 nodes): `Each workflow must contain a step whose run: block exits 1 on empty BASE_SHA.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Windows ollama Submit Temporary`** (1 nodes): `Temporary audit directory for testing.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Som client Som client From`** (1 nodes): `Build a client from well-known environment variables.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Packages Hldpro sim Personas`** (1 nodes): `Convenience: prefer process-agents/ with bundled personas/ fallback.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ConsumerVerifyError` connect `Overlord Verify governance consumer` to `Overlord Deploy local ci gate`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Why does `GateError` connect `Local ci gate Local ci gate Report` to `Overlord Deploy local ci gate`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Why does `SomClientError` connect `Som client Som client Mcp` to `Overlord Deploy local ci gate`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **Are the 35 inferred relationships involving `RepoFixture` (e.g. with `.test_allows_changes_in_allowed_paths_dirty_tree_mode()` and `.test_planning_only_diff_inside_allowed_paths_passes()`) actually correct?**
  _`RepoFixture` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `_tier1_packet()` (e.g. with `.test_tier1_without_parent_passes()` and `.test_same_family_dual_planner_refused()`) actually correct?**
  _`_tier1_packet()` has 30 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Shared pytest fixtures for governance contract tests.  Fixtures -------- tmp_git`, `Yield a temporary directory initialised as a git repo.`, `Write a sample cross-review artifact and return (path, frontmatter_dict).` to the rest of the system?**
  _180 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Remote mcp Verify audit` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._