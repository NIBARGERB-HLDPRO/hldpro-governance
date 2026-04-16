# Graph Report - local-ai-machine  (2026-04-09)

## Corpus Check
- Large corpus: 570 files · ~822,939 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 3089 nodes · 5106 edges · 417 communities detected
- Extraction: 53% EXTRACTED · 47% INFERRED · 0% AMBIGUOUS · INFERRED: 2416 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `handleSlackWebhook()` - 52 edges
2. `PostgresStore` - 41 edges
3. `tick()` - 25 edges
4. `run()` - 21 edges
5. `json()` - 17 edges
6. `acquire()` - 16 edges
7. `GatewayError` - 16 edges
8. `runCommand()` - 15 edges
9. `main()` - 15 edges
10. `main()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `mcpReadCircuitState()` --calls--> `json()`  [INFERRED]
  local-ai-machine/supabase/functions/critic_api/index.ts → local-ai-machine/supabase/functions/slack_webhook/index.ts
- `proxyJson()` --calls--> `json()`  [INFERRED]
  local-ai-machine/supabase/functions/critic_api/index.ts → local-ai-machine/supabase/functions/slack_webhook/index.ts
- `proxyStatus()` --calls--> `json()`  [INFERRED]
  local-ai-machine/supabase/functions/critic_api/index.ts → local-ai-machine/supabase/functions/slack_webhook/index.ts
- `proxyMcp()` --calls--> `json()`  [INFERRED]
  local-ai-machine/supabase/functions/critic_api/index.ts → local-ai-machine/supabase/functions/slack_webhook/index.ts

## Communities

### Community 0 - "Slack webhook Supabase"
Cohesion: 0.05
Nodes (98): addReceivedReaction(), appendIngressAudit(), appendInteractiveReceiptAudit(), applyPendingActionDecision(), buildAdvisoryXml(), buildCommandPrompt(), buildDecisionFollowupPrompt(), buildDecisionFollowupPromptFromContext() (+90 more)

### Community 1 - "Critic api postgres"
Cohesion: 0.06
Nodes (41): _apply_failover(), _apply_memory_budget(), apply_token_budget(), _as_embedding(), build_active_policy_artifact_from_shadow(), build_candidate_prompt(), build_compaction_candidate_artifact(), build_compaction_policy_artifact() (+33 more)

### Community 2 - "Control plane Cli bridge"
Cohesion: 0.06
Nodes (75): applyMediaContext(), applyThreadContext(), bootstrapAllowedNetworkHosts(), bridgePendingActionRunId(), bridgePendingActionStepId(), buildDecisionButtons(), buildIntentScope(), bytesToHex() (+67 more)

### Community 3 - "Ops Hp Api"
Cohesion: 0.03
Nodes (73): _get_facility_id(), main(), Test prestudy document request link creation via prestudy-portal edge function., Test finding create and read., Test AI draft report generation (skip if no ANTHROPIC_API_KEY)., Get a facility_id — try listing, fall back to seed., Run all API tests and return combined results., Test JWT refresh and token validity. (+65 more)

### Community 4 - "Ops Run local wifi gateway"
Cohesion: 0.06
Nodes (65): BaseHTTPRequestHandler, append_audit_event(), authorize_request(), build_audit_event(), build_get_response(), build_job_record(), cleanup_expired_or_abandoned_requests(), cleanup_terminal_temp() (+57 more)

### Community 5 - "Ops Inference Run"
Cohesion: 0.04
Nodes (72): call_escalation(), _call_grounding(), _call_opus_grounding(), call_spot_vlm(), call_vlm(), _emit_grounding_event(), emit_learning_event(), evaluate_escalation() (+64 more)

### Community 6 - "Workflows Durable adapter Runtime"
Cohesion: 0.05
Nodes (36): assertAbort(), routeToAirlock(), atomicWriteJson(), buildSignalPayload(), loadJsonObject(), requiredString(), TemporalExecutionAdapter, buildHostAdapterRequest() (+28 more)

### Community 7 - "Critic api reference"
Cohesion: 0.11
Nodes (33): adaptation_hash(), append_compaction_audit_bundle(), _apply_failover(), audit(), auto_demote_active_policies(), build_active_policy_artifact_from_shadow(), build_compaction_candidate_artifact(), build_compaction_policy_artifact() (+25 more)

### Community 8 - "Ops Session lock"
Cohesion: 0.11
Nodes (43): acquire(), _branch_is_locked(), build_registry_entry(), _cleanup_session(), _current_branch(), derive_lane_family(), find_registry_conflicts(), force_release() (+35 more)

### Community 9 - "Ops Run phase h hitl"
Cohesion: 0.15
Nodes (34): assert_command_policy_event(), assert_dual_audit(), assert_host_command_resume_link(), assert_intent_mandate(), assert_policy_event(), assert_project_ref_alignment(), assert_step_capability_issuance(), assert_transaction_capability_issuance() (+26 more)

### Community 10 - "Ops Slack temporal handoff worker"
Cohesion: 0.09
Nodes (32): Exception, Raised when transport delivery fails., Atomically write a reconciliation event to a file path., Send a reconciliation event over vsock to the given CID:port.      Uses AF_VSOCK, Dispatch a reconciliation event through the selected transport.      Args:, send(), send_file(), send_vsock() (+24 more)

### Community 11 - "Microvms Mcp server Secure"
Cohesion: 0.11
Nodes (24): append_audit_event(), BaselineGuardrail, BPFExecutionTracer, build_execution_verdict(), build_tool_command(), calculate_tool_identity_hash(), dispatch_tool(), fetch_patient_logs_from_db() (+16 more)

### Community 12 - "Ops Run survey calibration pipeline"
Cohesion: 0.1
Nodes (33): call_survey_api(), call_vlm(), compare_with_known(), create_test_visit(), default_run_id(), encode_image_base64(), evaluate_images(), generate_hitl_review_file() (+25 more)

### Community 13 - "Control plane Scavenger orchestrator"
Cohesion: 0.14
Nodes (31): appendRepoLearningEvent(), atomicWriteJson(), bootScavengerVm(), buildScavengerReport(), checkGpuPressure(), checkSystemIdleState(), currentCommitSha(), decodeOutput() (+23 more)

### Community 14 - "Clients Ios Gateway"
Cohesion: 0.08
Nodes (24): CodingKey, Decodable, CodingKeys, completedAt, createdAt, error, expiresAt, requestId (+16 more)

### Community 15 - "Ops Run facility survey"
Cohesion: 0.12
Nodes (27): call_api(), complete_survey(), _extract_facility_name(), get_or_create_visit(), get_state_dir(), _get_user_id_from_jwt(), load_dotenv(), load_state() (+19 more)

### Community 16 - "Ops Upload scavenger teardown bundles"
Cohesion: 0.18
Nodes (25): atomic_write_json(), baseline_state(), build_parser(), collect_bundle_files(), copy_tree(), env_or_default(), load_manifest(), load_state() (+17 more)

### Community 17 - "Ops Generate ai draft report"
Cohesion: 0.12
Nodes (25): assemble_report(), _call_claude(), _call_openai(), generate_ai_narratives(), generate_docx(), generate_html(), generate_placeholder_narratives(), load_dotenv() (+17 more)

### Community 18 - "Critic runner Panel"
Cohesion: 0.18
Nodes (21): appendAuditEvent(), appendLearningEvent(), buildPanelVerdict(), buildSinglePanelVerdict(), callCritic(), callCriticWithAudit(), criticRoleScope(), envFlag() (+13 more)

### Community 19 - "Ops Run general self learning loop"
Cohesion: 0.23
Nodes (20): append_jsonl(), build_checkpoint_payload(), fail_closed(), main(), materialize_slice_commands(), parse_args(), paths_overlap(), read_json() (+12 more)

### Community 20 - "Ops Enforce lane isolation"
Cohesion: 0.26
Nodes (19): changed_files(), ChangedFile, current_branch(), fail(), _in_scope(), info(), _load_runbook_targets(), main() (+11 more)

### Community 21 - "Ops Supervisor max loop enforcer"
Cohesion: 0.13
Nodes (12): discover_agents(), parse_agent_max_loops(), Extract max-loops value from agent YAML frontmatter., Discover all agents with max-loops declarations.      Returns a dict keyed by ag, Tracks agent invocations and enforces max-loops at runtime., Check if an agent is allowed another invocation., Record an agent invocation. Raises if max-loops exceeded., Return the full invocation manifest for artifact emission. (+4 more)

### Community 22 - "Ops Run pinecroft survey"
Cohesion: 0.19
Nodes (18): call_api(), complete_survey(), get_or_create_visit(), _get_user_id_from_jwt(), load_dotenv(), load_state(), main(), parse_args() (+10 more)

### Community 23 - "Ops Run adaptive compaction eval batch"
Cohesion: 0.26
Nodes (18): append_evidence(), append_learning_event(), apply_migrations(), build_shadow_artifact(), family_configs(), filter_family_configs(), get(), load_dotenv() (+10 more)

### Community 24 - "Ops Run gui visual loop"
Cohesion: 0.24
Nodes (17): build_ollama_prompt(), detect_blank_screenshot(), detect_png_dimensions(), ensure_resized_copy(), estimate_visual_budget(), fail_summary(), invoke_ollama(), load_json() (+9 more)

### Community 25 - "Ops Generate repo compendiums"
Cohesion: 0.18
Nodes (10): ConvertTo-HexString(), Get-Anchor(), Get-CodeFence(), Get-RepoFingerprint(), Get-Sha256ForFile(), Get-Sha256ForString(), Get-TopLevelName(), Read-TextFile() (+2 more)

### Community 26 - "Control plane Agent listener"
Cohesion: 0.22
Nodes (4): AgentConfigListener, jitter(), requireEnv(), terminateInFlightExecution()

### Community 27 - "Ops Local wifi gateway runtime"
Cohesion: 0.27
Nodes (15): build_multipart(), check(), fail(), get_image_request(), get_web_client(), load_audit_events(), load_job_record(), main() (+7 more)

### Community 28 - "Ops Runpod spot orchestrator"
Cohesion: 0.26
Nodes (14): get_api_key(), get_ollama_url(), get_pod_id(), graphql(), load_dotenv(), main(), parse_args(), pod_start() (+6 more)

### Community 29 - "Ops Check phase e runtime readiness"
Cohesion: 0.37
Nodes (13): _check_env(), _check_presidio_available(), _check_publishable_key(), _check_slack_manifest_exists(), _check_supabase_cli(), _check_tailscale_acl_exists(), _check_tailscale_binary(), _check_tailscale_bind_ip() (+5 more)

### Community 30 - "Ops Prune scavenger teardown object store stub"
Cohesion: 0.27
Nodes (12): build_parser(), collect_entries(), ensure_nonnegative(), env_or_default(), main(), object_store_config(), path_bytes(), path_mtime() (+4 more)

### Community 31 - "Control plane Synthesizer adapter"
Cohesion: 0.31
Nodes (9): assert(), assertNoUnknownKeys(), loadSchema(), toRiskReport(), validateAgainstSchema(), validateRawFinding(), validateRemediationPlanShape(), validateRiskReportShape() (+1 more)

### Community 32 - "Control plane Society review loop"
Cohesion: 0.28
Nodes (11): assert(), buildSignalsFromDrift(), confidenceForChange(), isUuid(), main(), mapScopeToLane(), maybeInsertHitlConsultation(), parseArgs() (+3 more)

### Community 33 - "Ops Verify delegated authorization stub"
Cohesion: 0.29
Nodes (11): atomic_write_json(), build_parser(), load_json(), load_nonce_set(), main(), parse_token(), resolve_paths(), save_seen_nonces() (+3 more)

### Community 34 - "Ops Promote general loop clone result"
Cohesion: 0.32
Nodes (12): build_manifest(), fail(), governance_match(), highest_accepted_sequence(), main(), parse_json_list(), path_in_scope(), read_registry() (+4 more)

### Community 35 - "Ops Audit branch residue"
Cohesion: 0.37
Nodes (12): BranchReport, classify(), delete_safe_branches(), is_anchor(), main(), merged_into_origin_main(), open_prs(), parse_branches() (+4 more)

### Community 36 - "Ops Worktree hygiene preflight runtime"
Cohesion: 0.41
Nodes (12): add_origin_main_tracking_worktree(), add_remote_branch_worktree(), add_session_lock(), add_unpublished_worktree(), build_fake_gh(), check(), fail(), git_setup() (+4 more)

### Community 37 - "Ops Materialize scavenger teardown bundle"
Cohesion: 0.31
Nodes (12): atomic_write_json(), baseline_state(), build_parser(), bundle_needed(), collect_outbox(), collect_summaries(), copy_records(), load_state() (+4 more)

### Community 38 - "Ops Run phase h receipt update"
Cohesion: 0.36
Nodes (12): auth_test(), build_card_blocks(), compute_slack_signature(), _env(), env_required(), fail(), info(), _load_env_file() (+4 more)

### Community 39 - "Gatekeeper Enforce"
Cohesion: 0.42
Nodes (11): assert_rule(), canonicalize_command(), _critic_identity(), enforce_lane_isolation_policy(), enforce_optional_mrp_attestation(), enforce_single_critic_verdict(), json_pointer_get(), load_json() (+3 more)

### Community 40 - "Ops Evaluate scavenger teardown alerts"
Cohesion: 0.32
Nodes (11): atomic_write_json(), baseline_state(), build_parser(), evaluate(), fail(), load_json(), load_state(), main() (+3 more)

### Community 41 - "Ops Run general loop clone integration"
Cohesion: 0.42
Nodes (11): current_head(), fail(), main(), parse_json_list(), prepare_backend(), read_json(), reset_clone_runtime(), run() (+3 more)

### Community 42 - "Ops Opus ground ungrounded"
Cohesion: 0.32
Nodes (11): build_manifest_index(), export_work_queue(), get_run_dir(), import_results(), is_negative_observation(), main(), Import Opus grounding results back into router JSON files., (facility, image_name) -> absolute path. (+3 more)

### Community 43 - "Ops Run temporal host adapter"
Cohesion: 0.3
Nodes (7): atomic_write_json(), build_parser(), build_signal(), load_json(), main(), process_request(), required_str()

### Community 44 - "Verify control plane"
Cohesion: 0.56
Nodes (10): fail(), get_latest_merged_riskfix_pr(), gh_get(), main(), ok(), token_from_gh_cli(), verify_closeout_comment(), verify_required_status_checks() (+2 more)

### Community 45 - "Control plane Redaction airlock"
Cohesion: 0.29
Nodes (7): deterministic_mask(), _entity_token(), presidio_tokenize(), redact_clinical_payload(), RedactionAirlockError, RedactionResult, RuntimeError

### Community 46 - "Control plane Knowledge integrator"
Cohesion: 0.33
Nodes (7): executeWithSLA(), gatekeeperValidation(), generateFailsafeAuditHash(), handleCrossDocQuery(), loadSchema(), SingletonQueue, validateParsed()

### Community 47 - "Ops Prune scavenger teardown telemetry"
Cohesion: 0.33
Nodes (9): artifact_suffix(), build_parser(), collect_target_files(), ensure_nonnegative(), main(), process(), resolve_audit_path(), summarize_inventory() (+1 more)

### Community 48 - "Ops Apply merge readiness pack"
Cohesion: 0.42
Nodes (10): capability_mode_from_env(), fail(), load_json(), main(), normalize_path(), patch_loc_budget(), patch_target_files(), path_allowed() (+2 more)

### Community 49 - "Ops Check worktree hygiene"
Cohesion: 0.42
Nodes (10): classify_worktree(), has_active_session_lock(), is_anchor(), main(), parse_worktrees(), read_branch_status(), read_prs(), render_human() (+2 more)

### Community 50 - "Ops Sync agent configs"
Cohesion: 0.44
Nodes (10): derive_agent_role(), fail(), is_valid_relative_path(), load_changed_files(), load_grammar_schema(), main(), ok(), post_config() (+2 more)

### Community 51 - "Serve hitl review"
Cohesion: 0.2
Nodes (4): HITLHandler, Handle POST /api/save-image-review — save one image's review state., Serves the HITL HTML and proxies /images/ requests to local filesystem., SimpleHTTPRequestHandler

### Community 52 - "Critic api postgres live"
Cohesion: 0.4
Nodes (9): apply_migrations(), assert_true(), fetch_memory_correction(), get(), main(), pick_free_port(), post(), sha256_canonical() (+1 more)

### Community 53 - "Ops Run gui visual loop runtime"
Cohesion: 0.38
Nodes (9): approved_minimal_verdict(), _build_test_png(), check(), fail(), main(), make_manifest(), Build a minimal valid PNG >10KB for blank-guard compatibility., rejected_verdict() (+1 more)

### Community 54 - "Ops Delegated execution envelope"
Cohesion: 0.44
Nodes (9): atomic_write_json(), build_parser(), ensure_same_workflow(), existing_ref(), load_json(), load_primary_context(), main(), required_str() (+1 more)

### Community 55 - "Ops Run vlm area routed eval"
Cohesion: 0.36
Nodes (9): call_vlm(), evaluate_image(), get_prompts_for_area(), load_dotenv(), load_prompt_config(), main(), parse_args(), Evaluate one image with area-routed domain prompts. (+1 more)

### Community 56 - "Ops Export scavenger teardown telemetry"
Cohesion: 0.38
Nodes (9): build_parser(), compute_sha256(), load_json(), main(), parse_sha256_sidecar(), process(), route_pair(), route_pair_safe() (+1 more)

### Community 57 - "Ops Run adaptive compaction repo"
Cohesion: 0.4
Nodes (9): apply_migrations(), get(), load_dotenv(), main(), pick_free_port(), post(), require_repo_patterns(), sha256_canonical() (+1 more)

### Community 58 - "Control plane Hitl checkpoint kill"
Cohesion: 0.47
Nodes (8): appendSigkillLog(), checkpointAndKill(), getPublishableKey(), loadResumeBundle(), requireEnv(), restUrl(), serviceHeaders(), writeCheckpoint()

### Community 59 - "Control plane Execution capability"
Cohesion: 0.36
Nodes (8): decideCommandCapability(), decideFileWriteCapability(), decideNetworkEgressCapability(), normalizePath(), parseCommandsScope(), parseFilesScope(), parseNetworkScope(), pathAllowed()

### Community 60 - "Ops Run adaptive compaction repo shadow"
Cohesion: 0.44
Nodes (8): get(), load_dotenv(), load_latest_shadow_ready_bundle(), main(), pick_free_port(), post(), sha256_canonical(), wait_for_server()

### Community 61 - "Ops Run adaptive compaction repo active"
Cohesion: 0.44
Nodes (8): get(), load_dotenv(), load_latest_shadow_ready_bundle(), main(), pick_free_port(), post(), sha256_canonical(), wait_for_server()

### Community 62 - "Ops Run general self learning loop runtime"
Cohesion: 0.42
Nodes (8): check(), fail(), load_json(), main(), run_runner(), write_lock(), write_queue(), write_registry()

### Community 63 - "Ops Resolve logical resource stub"
Cohesion: 0.5
Nodes (8): atomic_write_json(), build_parser(), emit_event(), load_json(), load_mapping(), main(), resolve(), validate_required()

### Community 64 - "Ops Run adaptive compaction repo runtime"
Cohesion: 0.44
Nodes (8): get(), latest_active_summary(), load_dotenv(), main(), pick_free_port(), post(), run_fresh_activation(), wait_for_server()

### Community 65 - "Ops Apply slack manifest"
Cohesion: 0.5
Nodes (8): _env(), fail(), _load_env_file(), main(), resolve_token(), rotate_config_token(), slack_post(), _upsert_env_values()

### Community 66 - "Ops Bridge health watchdog"
Cohesion: 0.47
Nodes (8): _check_bridge_auth_api(), _cooldown_ok(), _env(), fail(), _first_nonempty(), _load_env_file(), main(), _record_heal()

### Community 67 - "Ops Run batch surveys"
Cohesion: 0.33
Nodes (8): load_facility_state(), main(), parse_args(), print_comparison_summary(), Run run_facility_e2e_survey.py for a single facility., Load state.json for a completed facility run., Print a comparison table across all facilities., run_facility()

### Community 68 - "Ops Provision phase e machine"
Cohesion: 0.44
Nodes (8): _ensure_user(), _env(), _find_user_by_email(), _http_json(), _list_users(), _load_env_file(), main(), _upsert_env_values()

### Community 69 - "Ops Report repo learning loop"
Cohesion: 0.36
Nodes (6): build_report(), effective_prevention_artifact(), load_events(), main(), now_iso(), write_outputs()

### Community 70 - "Admin mcp server"
Cohesion: 0.46
Nodes (7): authorize(), handleToolCall(), isAllowedTool(), processConn(), requireEnv(), runAdminServer(), validateAdminIsolationConfig()

### Community 71 - "Ops Run scavenger real sink"
Cohesion: 0.5
Nodes (7): build_probe_bundle(), env_required(), fail(), info(), main(), make_case_dir(), write_json()

### Community 72 - "Ops Run temporal host adapter runtime"
Cohesion: 0.46
Nodes (7): allowed_response(), check(), denied_response(), fail(), main(), request_payload(), write_json()

### Community 73 - "Ops Publish riskfix pr"
Cohesion: 0.39
Nodes (5): Fail(), Publish-Branch(), Require-BranchPattern(), Require-CleanWorktree(), Require-GlobalWorktreeHygiene()

### Community 74 - "Ops Evaluate scavenger teardown alerts runtime"
Cohesion: 0.46
Nodes (7): base_summary(), check(), fail(), main(), make_case_dir(), run_eval(), write_json()

### Community 75 - "Ops Run vlm persona eval"
Cohesion: 0.39
Nodes (7): call_vlm(), load_dotenv(), load_images(), load_persona_prompt(), main(), parse_args(), Load the ASC evaluator visual persona from the prompt file.

### Community 76 - "Ops Seed phase e identity allowlist"
Cohesion: 0.5
Nodes (7): _b64url_decode(), _database_url(), _env(), _load_env_file(), main(), _resolve_subject(), _sub_from_jwt()

### Community 77 - "Ops Replay missing slack postbacks"
Cohesion: 0.46
Nodes (7): _bounded(), _env(), _extract_channel_id(), _load_env_file(), main(), _slack_post_channel(), _slack_post_response_url()

### Community 78 - "Ops Normalize ebpf reconciliation stub runtime"
Cohesion: 0.46
Nodes (7): check(), envelope(), fail(), main(), observed(), probe_input(), write_json()

### Community 79 - "Ops Run slack image processor adapter"
Cohesion: 0.57
Nodes (7): build_processor_payload(), emit(), fail(), main(), parse_input(), run_processor(), select_single_media()

### Community 80 - "Ops Serve hitl review runtime"
Cohesion: 0.46
Nodes (7): check(), fail(), get_bytes(), get_json(), get_text(), main(), reserve_port()

### Community 81 - "Ops Run adaptive compaction repo demote"
Cohesion: 0.54
Nodes (7): get(), load_dotenv(), load_latest_active_summary(), main(), pick_free_port(), post(), wait_for_server()

### Community 82 - "Ops Mint phase e machine jwts"
Cohesion: 0.54
Nodes (7): _env(), _first_nonempty(), _load_env_file(), main(), _require(), _sign_in(), _upsert_env_values()

### Community 83 - "Ops Upload reports to supabase"
Cohesion: 0.32
Nodes (7): load_env(), main(), Minimal .env parser — no dependency on python-dotenv., Get a fresh JWT via email/password auth., Upload report JSON to Supabase Storage via REST API., refresh_jwt(), upload_report()

### Community 84 - "Ops Run gui render"
Cohesion: 0.46
Nodes (7): choose_size(), detect_png_dimensions(), main(), parse_args(), run_playwright_screenshot(), wait_for_http_ready(), write_json()

### Community 85 - "Var Benchmarks Run"
Cohesion: 0.38
Nodes (6): BaseModel, CriticOutput, Finding, main(), Run a single generation, return metrics dict., run_one()

### Community 86 - "Validate live critic"
Cohesion: 0.52
Nodes (6): _has_unified_panel_shape(), _load_json(), main(), _resolve_run_dir(), validate_critic_contract(), _validate_unified_panel()

### Community 87 - "Critic verdict gatekeeper"
Cohesion: 0.62
Nodes (6): expect_gatekeeper_failure(), expect_gatekeeper_success(), load_json(), main(), run(), write_json()

### Community 88 - "Critic api reference"
Cohesion: 0.57
Nodes (6): assert_true(), get(), main(), pick_free_port(), post(), wait_for_server()

### Community 89 - "Ops Scavenger teardown status"
Cohesion: 0.52
Nodes (6): build_parser(), build_status(), choose_path(), load_optional_json(), main(), summarize_component()

### Community 90 - "Ops Reset general loop clone"
Cohesion: 0.62
Nodes (5): fail(), main(), remove_worktree(), repo_root(), safe_clone_root()

### Community 91 - "Ops Resolve logical resource stub runtime"
Cohesion: 0.52
Nodes (6): check(), fail(), main(), mapping_payload(), request_payload(), write_json()

### Community 92 - "Ops Prepare general loop clone"
Cohesion: 0.71
Nodes (6): current_head(), fail(), main(), parse_json_list(), read_registry(), resolve_active_session()

### Community 93 - "Ops Send slack notification"
Cohesion: 0.52
Nodes (6): _env(), _load_env_file(), main(), _post(), _split_for_slack(), _strip_codex_session_noise()

### Community 94 - "Ops Prune scavenger teardown object store stub runtime"
Cohesion: 0.57
Nodes (6): check(), fail(), load_module(), main(), make_case_dir(), touch_file()

### Community 95 - "Ops Run temporal verification activity stub"
Cohesion: 0.52
Nodes (6): atomic_write_json(), build_parser(), build_signal(), load_json(), main(), required_str()

### Community 96 - "Ops Session lock"
Cohesion: 0.33
Nodes (2): run(), run_with_env()

### Community 97 - "Ops Clone promotion boundary runtime"
Cohesion: 0.52
Nodes (6): check(), fail(), main(), read_json(), run_cmd(), write_registry()

### Community 98 - "Ops Run temporal verification activity stub runtime"
Cohesion: 0.52
Nodes (6): allowed_response(), check(), denied_response(), fail(), main(), write_json()

### Community 99 - "Ops Verify delegated authorization stub runtime"
Cohesion: 0.52
Nodes (6): check(), fail(), main(), request_payload(), token_payload(), write_json()

### Community 100 - "Ops Run general loop clone integration runtime"
Cohesion: 0.52
Nodes (6): check(), fail(), main(), read_json(), run(), write_registry()

### Community 101 - "Ops Hp training doc"
Cohesion: 0.52
Nodes (6): both(), build_doc(), bullets(), img(), Add screenshot if it exists. Tries name-viewport.png then name.png., steps()

### Community 102 - "Ops Prune scavenger teardown telemetry runtime"
Cohesion: 0.57
Nodes (6): check(), fail(), load_module(), main(), make_case_dir(), touch_file()

### Community 103 - "Ops Gui repair request runtime"
Cohesion: 0.52
Nodes (6): check(), fail(), main(), rejected_verdict(), render_manifest(), write_json()

### Community 104 - "Ops Temporal remediation signal stub"
Cohesion: 0.52
Nodes (6): atomic_write_json(), build_parser(), build_signal(), load_json(), main(), validate_verification_response()

### Community 105 - "Generate stub bundle"
Cohesion: 0.6
Nodes (5): main(), now_iso(), sha256_hex(), write_json(), write_text()

### Community 106 - "Clients Ios View"
Cohesion: 0.4
Nodes (2): ContentView, View

### Community 107 - "Security Check pat hygiene"
Cohesion: 0.6
Nodes (5): fail(), gh_get(), main(), ok(), warn()

### Community 108 - "Microvm Scavenger read"
Cohesion: 0.67
Nodes (5): assert_true(), find_free_port(), http_post(), main(), wait_for_server()

### Community 109 - "Microvm Secure mcp server"
Cohesion: 0.67
Nodes (5): assert_true(), http_post(), load_audit_events(), main(), wait_for_server()

### Community 110 - "Control plane Scavenger ingest"
Cohesion: 0.6
Nodes (5): main(), parse_jsonl(), persist_discoveries(), redact_report(), stable_hash()

### Community 111 - "Ops Append learning event"
Cohesion: 0.6
Nodes (5): load_events(), main(), normalize_text(), now_iso(), recurrence_key()

### Community 112 - "Ops Evaluate gui loop runtime"
Cohesion: 0.6
Nodes (5): check(), fail(), main(), verdict(), write_json()

### Community 113 - "Ops Stale registry lock recovery"
Cohesion: 0.6
Nodes (5): check(), main(), make_lock_info(), make_registry(), make_registry_session()

### Community 114 - "Ops Export scavenger teardown telemetry runtime"
Cohesion: 0.6
Nodes (5): check(), fail(), main(), make_case_dir(), write_pair()

### Community 115 - "Ops Rotate cli bridge jwt"
Cohesion: 0.53
Nodes (4): Get-EnvValue(), Invoke-SupabaseCli(), Resolve-ProjectRef(), Sync-EdgeSecrets()

### Community 116 - "Ops Create phase g channels"
Cohesion: 0.6
Nodes (5): _env(), _load_env_file(), main(), _slack_call(), _write_env_updates()

### Community 117 - "Ops Materialize scavenger teardown bundle runtime"
Cohesion: 0.6
Nodes (5): check(), fail(), main(), make_case_dir(), write_json()

### Community 118 - "Ops Send scavenger digest"
Cohesion: 0.6
Nodes (5): _bounded(), _env(), _load_env_file(), main(), _post_slack()

### Community 119 - "Ops Scavenger teardown status runtime"
Cohesion: 0.6
Nodes (5): check(), fail(), main(), make_case_dir(), write_json()

### Community 120 - "Ops Drain microvm run storage"
Cohesion: 0.67
Nodes (5): choose_prefixes(), directory_size_bytes(), fail(), main(), parse_args()

### Community 121 - "Ops Evaluate gui loop"
Cohesion: 0.6
Nodes (5): atomic_write_json(), build_parser(), load_json(), main(), required_str()

### Community 122 - "Ops Inference comparison"
Cohesion: 0.6
Nodes (5): check(), fail(), main(), Validate comparison function with mock data., test_compare_findings_with_mock_data()

### Community 123 - "Ops Reconcile required checks"
Cohesion: 0.6
Nodes (5): fail(), gh_request(), main(), ok(), token_from_gh_cli()

### Community 124 - "Ops Report var registry gaps"
Cohesion: 0.67
Nodes (5): collect_code_vars(), collect_registry_vars(), iter_text_files(), main(), read_text()

### Community 125 - "Ops Temporal remediation signal stub runtime"
Cohesion: 0.6
Nodes (5): check(), denied_response(), fail(), main(), write_json()

### Community 126 - "Ops Run scavenger locked loop"
Cohesion: 0.6
Nodes (5): _available_memory_mb(), _env(), main(), _queue_pressure_snapshot(), run_once()

### Community 127 - "Ops Var Load"
Cohesion: 0.6
Nodes (5): check(), fail(), load_gap_report(), load_json(), main()

### Community 128 - "Ops Normalize ebpf reconciliation stub"
Cohesion: 0.6
Nodes (5): atomic_write_json(), build_parser(), load_json(), main(), required_str()

### Community 129 - "Ops Gui repair request"
Cohesion: 0.6
Nodes (5): atomic_write_json(), build_parser(), load_json(), main(), required_str()

### Community 130 - "Ops Exchange slack oauth"
Cohesion: 0.6
Nodes (5): _env(), fail(), _load_env_file(), main(), _upsert_env_values()

### Community 131 - "Slack webhook Supabase"
Cohesion: 0.7
Nodes (4): applyFailover(), includesAnyKeyword(), normalizeText(), routeRequest()

### Community 132 - "Required check workflow"
Cohesion: 0.8
Nodes (4): check(), fail(), main(), read()

### Community 133 - "Control plane Scavenger stream guard"
Cohesion: 0.6
Nodes (3): appendLog(), handlePayload(), killMicrovm()

### Community 134 - "Control plane Admin tailscale proxy"
Cohesion: 0.5
Nodes (2): forwardToAdminBridge(), handleConn()

### Community 135 - "Ops V2 metrics report"
Cohesion: 0.7
Nodes (4): fetch_metrics(), main(), now_iso(), write_outputs()

### Community 136 - "Ops Delegated execution envelope runtime"
Cohesion: 0.7
Nodes (4): check(), fail(), main(), write_json()

### Community 137 - "Ops Verify phase e migrations applied"
Cohesion: 0.7
Nodes (4): _database_url(), fail(), _load_env_file(), main()

### Community 138 - "Ops Serve temporal host adapter stdio runtime"
Cohesion: 0.7
Nodes (4): check(), fail(), main(), write_json()

### Community 139 - "Ops Verify phase g migrations applied"
Cohesion: 0.7
Nodes (4): _database_url(), fail(), _load_env_file(), main()

### Community 140 - "Ops Run remote microvm storage drain emergency"
Cohesion: 0.4
Nodes (0): 

### Community 141 - "Ops Run remote microvm storage drain"
Cohesion: 0.4
Nodes (0): 

### Community 142 - "Ops Repo learning loop start runtime"
Cohesion: 0.8
Nodes (4): check(), main(), run_case(), write()

### Community 143 - "Ops Run remote gpu runtime proof"
Cohesion: 0.4
Nodes (0): 

### Community 144 - "Ops Run scavenger remote"
Cohesion: 0.4
Nodes (0): 

### Community 145 - "Ops Run remote ollama"
Cohesion: 0.4
Nodes (0): 

### Community 146 - "Ops Run temporal host adapter worker runtime"
Cohesion: 0.7
Nodes (4): check(), fail(), main(), write_json()

### Community 147 - "Ops Reconcile thread continuity"
Cohesion: 0.7
Nodes (4): _env(), _load_env_file(), main(), _split_thread_ref()

### Community 148 - "Ops Verify phase f migrations applied"
Cohesion: 0.7
Nodes (4): _database_url(), fail(), _load_env_file(), main()

### Community 149 - "Ops Run slack image ingestion"
Cohesion: 0.4
Nodes (0): 

### Community 150 - "Ops Run remote host inference critic proof"
Cohesion: 0.4
Nodes (0): 

### Community 151 - "Ops Repo learning loop report runtime"
Cohesion: 0.8
Nodes (4): check(), fail(), main(), make_event()

### Community 152 - "Ops Validate merge readiness pack"
Cohesion: 0.8
Nodes (4): canonicalize_command(), fail(), load_json(), main()

### Community 153 - "Ops Drain microvm run storage runtime"
Cohesion: 0.7
Nodes (4): check(), fail(), main(), run()

### Community 154 - "Ops Run remote host inference"
Cohesion: 0.4
Nodes (0): 

### Community 155 - "Ops Materialize lint rule bundle"
Cohesion: 0.8
Nodes (4): fail(), main(), _safe_repo_path(), _write()

### Community 156 - "Verify control plane"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 157 - "Critic runner Check"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 158 - "Llm Validate profiles"
Cohesion: 0.83
Nodes (3): fail(), main(), ok()

### Community 159 - "Microvm Boot run"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 160 - "Microvm Run scavenger workload"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 161 - "Microvm Teardown telemetry"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 162 - "Slack webhook Check"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 163 - "Export audit chain"
Cohesion: 0.83
Nodes (3): fail(), main(), stable_json_hash()

### Community 164 - "Control plane Oracle engine"
Cohesion: 0.83
Nodes (3): handleOracleRequest(), sanitizeUntrustedLog(), validateRequest()

### Community 165 - "Ops Admin fs attack"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 166 - "Ops Amps Check"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 167 - "Ops Phase e tailscale proxy"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 168 - "Ops Sync agent"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 169 - "Ops Scavenger stale run watchdog"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 170 - "Ops Run lint warning mode"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 171 - "Ops Microvm runtime workflow"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 172 - "Ops Phase g8 mcp routing audit sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 173 - "Ops Phase f migration verifier"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 174 - "Ops Run remote host inference critic proof"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 175 - "Ops Reconcile slack postbacks"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 176 - "Ops Critic migration"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 177 - "Ops Society review loop"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 178 - "Ops Evaluate gui loop"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 179 - "Ops General self learning loop"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 180 - "Ops Scavenger orchestrator"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 181 - "Ops Run general loop clone integration"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 182 - "Ops Run general self learning loop"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 183 - "Ops Scavenger teardown status"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 184 - "Ops Temporal host runtime adapter"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 185 - "Ops Zero trust delegation"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 186 - "Ops Slack image ingestion response"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 187 - "Ops Admin mcp isolation"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 188 - "Ops Cli bridge task"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 189 - "Ops Adaptive control memory budget"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 190 - "Ops Phase g host commands sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 191 - "Ops Nightly pass rate"
Cohesion: 0.83
Nodes (3): fail(), gh_get(), main()

### Community 192 - "Ops Phase h receipt update"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 193 - "Ops Mask policy"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 194 - "Ops Zero trust runtime convergence"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 195 - "Ops Var governance gap1"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 196 - "Ops Phase e identity allowlist"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 197 - "Ops Phase g3 bridge heartbeats sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 198 - "Ops Slack image ingestion ingress"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 199 - "Ops Repo learning loop"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 200 - "Ops Delegated execution envelope"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 201 - "Ops Phase g7 bridge heartbeat webhook sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 202 - "Ops Sprint microvm task"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 203 - "Ops Scavenger real sink dev server"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 204 - "Ops Pr branch residue purge"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 205 - "Ops Lane isolation"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 206 - "Ops Preflight scavenger remote access"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 207 - "Ops Agents governance"
Cohesion: 0.67
Nodes (2): line_count(), read_text()

### Community 208 - "Ops Critic unified gate"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 209 - "Ops Slack hitl git mutation non goal"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 210 - "Ops Clean working branch governance"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 211 - "Ops Slack image ingestion media fetch"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 212 - "Ops Phase g4 slack postback audit sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 213 - "Ops Runtime resolver activity"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 214 - "Ops Run scavenger remote"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 215 - "Ops Slack image ingestion enablement"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 216 - "Ops Temporal remediation signal stub"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 217 - "Ops Bridge health watchdog"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 218 - "Ops Phase f ast lint sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 219 - "Ops Survey calibration hitl review"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 220 - "Ops Phase h microvm isolation"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 221 - "Ops Prune scavenger teardown object store stub"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 222 - "Ops Scavenger real sink"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 223 - "Ops Phase g6 host command media sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 224 - "Ops Adaptive control sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 225 - "Ops Adaptive control package"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 226 - "Ops Run remote gpu host remediation"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 227 - "Ops Materialize scavenger teardown bundle"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 228 - "Ops Verify delegated authorization stub"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 229 - "Ops Supervisor max loop"
Cohesion: 0.83
Nodes (3): check(), main(), parse_max_loops()

### Community 230 - "Ops Phase h host telemetry observer"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 231 - "Ops Knowledge integrator schema"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 232 - "Ops Slack image processor adapter runtime"
Cohesion: 1.0
Nodes (3): check(), fail(), main()

### Community 233 - "Ops Gpu wrapper enforcement"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 234 - "Ops Validate lint rule bundle"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 235 - "Ops Phase g migration verifier"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 236 - "Ops Run remote gpu host remediation"
Cohesion: 0.5
Nodes (0): 

### Community 237 - "Ops Rotate cli bridge jwt"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 238 - "Ops Agent architecture manifest convergence"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 239 - "Ops Phase e runtime readiness"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 240 - "Ops Normalize ebpf reconciliation stub"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 241 - "Ops Github update"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 242 - "Ops Agent listener"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 243 - "Ops Zero trust runtime convergence proof"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 244 - "Ops Oracle bridge lifecycle"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 245 - "Ops Phase g2 slack ingress sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 246 - "Ops Inference Check"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 247 - "Ops Survey calibration hitl review runtime"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 248 - "Ops Resolve logical resource stub"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 249 - "Ops Phase h5 host command resume link sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 250 - "Ops Oracle engine"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 251 - "Ops Run slack image ingestion"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 252 - "Ops Phase f scavenger sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 253 - "Ops Promote lint rule bundle"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 254 - "Ops Drain microvm run storage"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 255 - "Ops Phase h hitl"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 256 - "Ops Run remote host inference"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 257 - "Ops Purge archived branch family"
Cohesion: 0.83
Nodes (3): is_safe_dead_candidate(), main(), run()

### Community 258 - "Ops Publish riskfix pr"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 259 - "Ops Merge readiness pack"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 260 - "Ops Clone promotion boundary"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 261 - "Ops Run temporal verification activity stub"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 262 - "Ops Slack image ingestion prereqs"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 263 - "Ops Prune scavenger teardown telemetry"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 264 - "Ops Zero trust runtime wiring"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 265 - "Ops Worktree hygiene preflight"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 266 - "Ops Agent sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 267 - "Ops Reconcile required checks"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 268 - "Ops Start repo learning loop"
Cohesion: 0.83
Nodes (3): default_run_id(), main(), run()

### Community 269 - "Ops Pr routing Check"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 270 - "Ops Slack bot rotation task"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 271 - "Ops Upload scavenger teardown bundles"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 272 - "Ops Inference runtime"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 273 - "Ops Phase g Check"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 274 - "Ops Local wifi gateway"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 275 - "Ops Branch residue classification"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 276 - "Ops Windows host inference tuning"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 277 - "Ops Run temporal host adapter"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 278 - "Ops Phase g5 thread continuity sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 279 - "Ops Phase h2 slack receipt audit sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 280 - "Ops Run hp crawl"
Cohesion: 0.83
Nodes (3): load_dotenv(), main(), run_crawl()

### Community 281 - "Ops Run sprint microvm"
Cohesion: 0.5
Nodes (0): 

### Community 282 - "Ops Slack hitl transaction capability"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 283 - "Ops Phase h4 host command hitl pause sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 284 - "Ops Adaptive control projection"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 285 - "Ops Slack image processor adapter"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 286 - "Ops Evaluate scavenger teardown alerts"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 287 - "Ops Sprint microvm runner"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 288 - "Ops Phase h3 capability delegation sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 289 - "Ops Runtime envelope"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 290 - "Ops Scavenger ingest"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 291 - "Ops Slack hitl capability closeout"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 292 - "Ops Replay missing slack postbacks"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 293 - "Ops Microsase hyperv gpu enablement"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 294 - "Ops Branch residue governance"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 295 - "Ops Materialize lint rule bundle"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 296 - "Ops Run remote ollama"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 297 - "Ops Adaptive control runtime"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 298 - "Ops Run remote microvm storage drain emergency"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 299 - "Ops Phase h6 cli bridge transaction insert sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 300 - "Ops Windows host inference integration"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 301 - "Ops Slack temporal branch residue purge"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 302 - "Ops Run scavenger"
Cohesion: 0.5
Nodes (0): 

### Community 303 - "Ops Final merge hygiene"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 304 - "Ops Run gui visual loop"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 305 - "Ops Scavenger stream guard"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 306 - "Ops Phase e checkpoint kill"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 307 - "Ops Runtime reconciliation"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 308 - "Ops Report var registry gaps"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 309 - "Ops Phase h safe apply"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 310 - "Ops Work branch residue purge"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 311 - "Ops Phase i pwsh scoped"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 312 - "Ops Phase h sprint backlog sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 313 - "Ops Scavenger lock loop"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 314 - "Ops Knowledge integrator runner"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 315 - "Ops Phase h hitl workflow"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 316 - "Ops Phase h1 slack hitl audit sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 317 - "Ops Phase g cli bridge"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 318 - "Ops Gpu upgrade"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 319 - "Ops Serve temporal host adapter stdio"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 320 - "Ops Run remote microvm storage drain"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 321 - "Ops Final sprint runbooks"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 322 - "Ops Repo learning loop start"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 323 - "Ops Learning capture governance"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 324 - "Ops Zero trust runtime resolver consumption"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 325 - "Ops Slack rotation task"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 326 - "Ops Zero trust runtime resolver shape"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 327 - "Ops Bridge watchdog task"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 328 - "Ops Repo learning loop report"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 329 - "Ops Phase e migration verifier"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 330 - "Ops Issue0 branch residue purge"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 331 - "Ops Seed phase g channel routes"
Cohesion: 0.83
Nodes (3): _env(), _load_env_file(), main()

### Community 332 - "Ops Scavenger task"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 333 - "Ops Queue cleanup governance"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 334 - "Ops Phase e hitl sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 335 - "Ops Send scavenger digest"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 336 - "Ops Lint rule bundle schema"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 337 - "Ops Execution capability mode switch"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 338 - "Ops Reconcile thread continuity"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 339 - "Ops Phase g channel routes sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 340 - "Ops Run temporal host adapter worker"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 341 - "Ops Run gui render"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 342 - "Ops Microvm runtime proof"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 343 - "Ops Gui repair request"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 344 - "Ops Fail fast governance"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 345 - "Ops Phase h mrp gatekeeper"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 346 - "Ops Github branch residue purge"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 347 - "Ops Windows host inference fallback"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 348 - "Ops Phase e redaction airlock"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 349 - "Ops Temporal sdk dropin gate"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 350 - "Ops Supabase jwt rotation task"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 351 - "Ops Run remote gpu runtime proof"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 352 - "Ops Zero trust runtime convergence proof runtime"
Cohesion: 1.0
Nodes (3): check(), fail(), main()

### Community 353 - "Ops Phase h schema"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 354 - "Ops Completion slack"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 355 - "Ops Phase h pending actions sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 356 - "Ops Local wifi iphone client"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 357 - "Ops Adaptive control ingestion"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 358 - "Ops Gui visual pipeline"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 359 - "Ops Export scavenger teardown telemetry"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 360 - "Ops Phase g response url sql"
Cohesion: 0.83
Nodes (3): check(), fail(), main()

### Community 361 - "Ops Reconcile slack postbacks"
Cohesion: 0.83
Nodes (3): _env(), _load_env_file(), main()

### Community 362 - "Clients Ios Local"
Cohesion: 0.67
Nodes (2): App, LocalWiFiImageClientApp

### Community 363 - "Runtime parity Assert"
Cohesion: 1.0
Nodes (2): assert_true(), main()

### Community 364 - "Bootstrap episodic memory"
Cohesion: 0.67
Nodes (0): 

### Community 365 - "Critic api postgres"
Cohesion: 1.0
Nodes (2): assert_true(), main()

### Community 366 - "Supabase critic runtime"
Cohesion: 1.0
Nodes (2): assert_true(), main()

### Community 367 - "Ops Hp suite Check"
Cohesion: 1.0
Nodes (2): check(), main()

### Community 368 - "Ops Host telemetry observer"
Cohesion: 1.0
Nodes (2): main(), sha256_text()

### Community 369 - "Ops Validate learning pr body"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 370 - "Ops Run phase g media"
Cohesion: 0.67
Nodes (0): 

### Community 371 - "Ops Classify branch residue actions"
Cohesion: 1.0
Nodes (2): classify_action(), main()

### Community 372 - "Ops Run cli bridge"
Cohesion: 0.67
Nodes (0): 

### Community 373 - "Ops Promote lint rule bundle"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 374 - "Ops Set tailscale bind ip"
Cohesion: 1.0
Nodes (2): main(), _upsert_env()

### Community 375 - "Ops Capture hp training screenshots"
Cohesion: 1.0
Nodes (2): load_dotenv(), main()

### Community 376 - "Ops Prestudy Check"
Cohesion: 1.0
Nodes (2): check(), main()

### Community 377 - "Ops Run local wifi gateway processor"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 378 - "Ops Run lint warning mode"
Cohesion: 1.0
Nodes (2): main(), parse_fixture_file()

### Community 379 - "Ops Reconciliation transport"
Cohesion: 1.0
Nodes (2): check(), main()

### Community 380 - "Ops Simulate survey walkthrough"
Cohesion: 1.0
Nodes (2): load_dotenv(), main()

### Community 381 - "Ops Validate lint rule bundle"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 382 - "Ops Adaptive kill switch trip"
Cohesion: 1.0
Nodes (2): check(), main()

### Community 383 - "Ops Slack temporal handoff worker"
Cohesion: 1.0
Nodes (2): check(), main()

### Community 384 - "Ops Run zero trust runtime convergence proof"
Cohesion: 1.0
Nodes (2): main(), writeJson()

### Community 385 - "Ops Verify general loop clone promotion"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 386 - "Ops Capture hp surveyor walkthrough"
Cohesion: 1.0
Nodes (2): load_dotenv(), main()

### Community 387 - "Ops Audit retention check"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 388 - "Ops Slack temporal handoff convergence"
Cohesion: 1.0
Nodes (2): check(), main()

### Community 389 - "Workflows Runtime reconciliation"
Cohesion: 0.67
Nodes (0): 

### Community 390 - "Workflows Durable adapter"
Cohesion: 0.67
Nodes (0): 

### Community 391 - "Custom lint rules No swallowed errors"
Cohesion: 1.0
Nodes (0): 

### Community 392 - "Ops Install slack rotation task"
Cohesion: 1.0
Nodes (0): 

### Community 393 - "Ops Append learning record"
Cohesion: 1.0
Nodes (0): 

### Community 394 - "Ops Run bridge watchdog"
Cohesion: 1.0
Nodes (0): 

### Community 395 - "Ops Set execution capability mode"
Cohesion: 1.0
Nodes (0): 

### Community 396 - "Ops Pinecroft findings"
Cohesion: 1.0
Nodes (1): Pinecroft E2E survey test data — 27 Phase 1 findings + 16 TJC RFIs + facility me

### Community 397 - "Ops Install slack bot rotation task"
Cohesion: 1.0
Nodes (0): 

### Community 398 - "Workflows Runtime resolver activity"
Cohesion: 1.0
Nodes (0): 

### Community 399 - "Orchestrator Native orchestrator Base"
Cohesion: 1.0
Nodes (0): 

### Community 400 - "Custom lint rules No swallowed errors"
Cohesion: 1.0
Nodes (0): 

### Community 401 - "Slack webhook Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 402 - "Slack webhook Slack signature Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 403 - "Control plane Execution capability"
Cohesion: 1.0
Nodes (0): 

### Community 404 - "Ops Install bridge watchdog task"
Cohesion: 1.0
Nodes (0): 

### Community 405 - "Ops Install scavenger task"
Cohesion: 1.0
Nodes (0): 

### Community 406 - "Ops Install supabase jwt rotation task"
Cohesion: 1.0
Nodes (0): 

### Community 407 - "Ops Install sprint microvm task"
Cohesion: 1.0
Nodes (0): 

### Community 408 - "Ops Install cli bridge task"
Cohesion: 1.0
Nodes (0): 

### Community 409 - "Ops Scoped Status"
Cohesion: 1.0
Nodes (0): 

### Community 410 - "Ops Scoped Run"
Cohesion: 1.0
Nodes (0): 

### Community 411 - "Ops Scoped Restart"
Cohesion: 1.0
Nodes (0): 

### Community 412 - "Ops Scoped Disk"
Cohesion: 1.0
Nodes (0): 

### Community 413 - "Ops Scoped Gpu"
Cohesion: 1.0
Nodes (0): 

### Community 414 - "Types Adaptation artifact"
Cohesion: 1.0
Nodes (0): 

### Community 415 - "Workflows Resolver gate"
Cohesion: 1.0
Nodes (0): 

### Community 416 - "Workflows Runtime envelope"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **166 isolated node(s):** `invalidURL`, `invalidPort`, `invalidResponse`, `requestNeverCompleted`, `Configuration` (+161 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Custom lint rules No swallowed errors`** (2 nodes): `no-swallowed-errors.ts`, `noSwallowedErrors()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Install slack rotation task`** (2 nodes): `install_slack_config_rotation_task.ps1`, `Resolve-RefreshToken()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Append learning record`** (2 nodes): `append_learning_record.py`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Run bridge watchdog`** (2 nodes): `run_bridge_watchdog.ps1`, `Import-DotEnv()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Set execution capability mode`** (2 nodes): `set_execution_capability_mode.ps1`, `Set-DotEnvKey()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Pinecroft findings`** (2 nodes): `pinecroft_findings_data.py`, `Pinecroft E2E survey test data — 27 Phase 1 findings + 16 TJC RFIs + facility me`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Install slack bot rotation task`** (2 nodes): `install_slack_bot_rotation_task.ps1`, `Resolve-RefreshToken()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Workflows Runtime resolver activity`** (2 nodes): `runtime_resolver_activity_test.ts`, `writeJson()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Orchestrator Native orchestrator Base`** (2 nodes): `native_orchestrator_test.ts`, `baseInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Custom lint rules No swallowed errors`** (1 nodes): `no-swallowed-errors.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Slack webhook Supabase`** (1 nodes): `router_test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Slack webhook Slack signature Supabase`** (1 nodes): `slack_signature_test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Control plane Execution capability`** (1 nodes): `execution_capability_test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Install bridge watchdog task`** (1 nodes): `install_bridge_watchdog_task.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Install scavenger task`** (1 nodes): `install_scavenger_task.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Install supabase jwt rotation task`** (1 nodes): `install_supabase_jwt_rotation_task.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Install sprint microvm task`** (1 nodes): `install_sprint_microvm_task.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Install cli bridge task`** (1 nodes): `install_cli_bridge_task.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Scoped Status`** (1 nodes): `get_service_status.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Scoped Run`** (1 nodes): `get_run_log.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Scoped Restart`** (1 nodes): `restart_ollama.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Scoped Disk`** (1 nodes): `get_disk_usage.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ops Scoped Gpu`** (1 nodes): `get_gpu_status.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Types Adaptation artifact`** (1 nodes): `adaptation_artifact.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Workflows Resolver gate`** (1 nodes): `resolver_gate_test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Workflows Runtime envelope`** (1 nodes): `runtime_envelope_test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Handler` connect `Critic api postgres` to `Ops Run local wifi gateway`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Why does `CriticAPIHandler` connect `Critic api reference` to `Ops Run local wifi gateway`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Are the 51 inferred relationships involving `handleSlackWebhook()` (e.g. with `json()` and `requireEnv()`) actually correct?**
  _`handleSlackWebhook()` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `tick()` (e.g. with `heartbeatIfDue()` and `failStaleExecuting()`) actually correct?**
  _`tick()` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `run()` (e.g. with `fail()` and `env_required()`) actually correct?**
  _`run()` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `json()` (e.g. with `mcpReadCircuitState()` and `proxyJson()`) actually correct?**
  _`json()` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `invalidURL`, `invalidPort`, `invalidResponse` to the rest of the system?**
  _166 weakly-connected nodes found - possible documentation gaps or missing edges._