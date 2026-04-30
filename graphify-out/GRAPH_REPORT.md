# Graph Report - .  (2026-04-30)

## Corpus Check
- Large corpus: 3502 files · ~1,285,614 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 2196 nodes · 5577 edges · 54 communities detected
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 1079 edges (avg confidence: 0.75)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Windows ollama Submit Audit|Windows ollama Submit Audit]]
- [[_COMMUNITY_Overlord Validate structured agent cycle plan|Overlord Validate structured agent cycle plan]]
- [[_COMMUNITY_Orchestrator Read only observer Overlord|Orchestrator Read only observer Overlord]]
- [[_COMMUNITY_Orchestrator Hitl relay queue|Orchestrator Hitl relay queue]]
- [[_COMMUNITY_Packet Validate Schema|Packet Validate Schema]]
- [[_COMMUNITY_Som client Som client Mcp|Som client Som client Mcp]]
- [[_COMMUNITY_Deploy Deploy gate Run|Deploy Deploy gate Run]]
- [[_COMMUNITY_Packages Hldpro sim|Packages Hldpro sim]]
- [[_COMMUNITY_Overlord Deploy governance tooling|Overlord Deploy governance tooling]]
- [[_COMMUNITY_Local ci gate Local ci gate Profile|Local ci gate Local ci gate Profile]]
- [[_COMMUNITY_Cli session supervisor Overlord|Cli session supervisor Overlord]]
- [[_COMMUNITY_Knowledge base Graphify|Knowledge base Graphify]]
- [[_COMMUNITY_Overlord Deploy governance tooling|Overlord Deploy governance tooling]]
- [[_COMMUNITY_Deploy Deploy verifier Domain|Deploy Deploy verifier Domain]]
- [[_COMMUNITY_Overlord Assert execution scope|Overlord Assert execution scope]]
- [[_COMMUNITY_Knowledge base Measure graphify usage|Knowledge base Measure graphify usage]]
- [[_COMMUNITY_Overlord Verify governance consumer|Overlord Verify governance consumer]]
- [[_COMMUNITY_Session bootstrap Check|Session bootstrap Check]]
- [[_COMMUNITY_Orchestrator Self learning|Orchestrator Self learning]]
- [[_COMMUNITY_Overlord Assert execution scope|Overlord Assert execution scope]]
- [[_COMMUNITY_Overlord Verify governance consumer|Overlord Verify governance consumer]]
- [[_COMMUNITY_Overlord Codex ingestion|Overlord Codex ingestion]]
- [[_COMMUNITY_Orchestrator Packet queue|Orchestrator Packet queue]]
- [[_COMMUNITY_Overlord Validate handoff package|Overlord Validate handoff package]]
- [[_COMMUNITY_Overlord Check stage6 closeout|Overlord Check stage6 closeout]]
- [[_COMMUNITY_Overlord Check governance issue branch parity|Overlord Check governance issue branch parity]]
- [[_COMMUNITY_Lam Runtime inventory|Lam Runtime inventory]]
- [[_COMMUNITY_Overlord Validate structured agent cycle plan|Overlord Validate structured agent cycle plan]]
- [[_COMMUNITY_Overlord Report governance consumer status|Overlord Report governance consumer status]]
- [[_COMMUNITY_Overlord Validate closeout|Overlord Validate closeout]]
- [[_COMMUNITY_Overlord Validate sql schema|Overlord Validate sql schema]]
- [[_COMMUNITY_Overlord Local ci gate workflow|Overlord Local ci gate workflow]]
- [[_COMMUNITY_Overlord Validate session error patterns|Overlord Validate session error patterns]]
- [[_COMMUNITY_Overlord Validate handoff package|Overlord Validate handoff package]]
- [[_COMMUNITY_Overlord Org governance compendium|Overlord Org governance compendium]]
- [[_COMMUNITY_Orchestrator Delegation gate|Orchestrator Delegation gate]]
- [[_COMMUNITY_Overlord Workflow local coverage|Overlord Workflow local coverage]]
- [[_COMMUNITY_Overlord Check plan preflight|Overlord Check plan preflight]]
- [[_COMMUNITY_Overlord Check worker handoff route|Overlord Check worker handoff route]]
- [[_COMMUNITY_Packet Validate hitl relay|Packet Validate hitl relay]]
- [[_COMMUNITY_Remote mcp Monitor alert|Remote mcp Monitor alert]]
- [[_COMMUNITY_Deploy Inventory direct upload projects|Deploy Inventory direct upload projects]]
- [[_COMMUNITY_Overlord Validate provisioning evidence|Overlord Validate provisioning evidence]]
- [[_COMMUNITY_Overlord Check execution environment|Overlord Check execution environment]]
- [[_COMMUNITY_Overlord Check org repo inventory|Overlord Check org repo inventory]]
- [[_COMMUNITY_Overlord Validate provisioning evidence|Overlord Validate provisioning evidence]]
- [[_COMMUNITY_Overlord Lane bootstrap|Overlord Lane bootstrap]]
- [[_COMMUNITY_Overlord Lane bootstrap|Overlord Lane bootstrap]]
- [[_COMMUNITY_Overlord Validate backlog gh sync|Overlord Validate backlog gh sync]]
- [[_COMMUNITY_Windows ollama Init|Windows ollama Init]]
- [[_COMMUNITY_Deploy Init|Deploy Init]]
- [[_COMMUNITY_Deploy Init|Deploy Init]]
- [[_COMMUNITY_Som client Som client From|Som client Som client From]]
- [[_COMMUNITY_Packages Hldpro sim Personas|Packages Hldpro sim Personas]]

## God Nodes (most connected - your core abstractions)
1. `read_text()` - 173 edges
2. `parse_args()` - 57 edges
3. `TestVerifyGovernanceConsumer` - 49 edges
4. `WindowsOllamaSubmitter` - 49 edges
5. `TestActiveIssueBranchContract` - 44 edges
6. `PiiDetectionError` - 44 edges
7. `ModelNotAllowedError` - 44 edges
8. `EndpointUnreachableError` - 44 edges
9. `TestAssertExecutionScope` - 42 edges
10. `RepoFixture` - 37 edges

## Surprising Connections (you probably didn't know these)
- `_write_output_from_call()` --calls--> `read_text()`  [INFERRED]
  ./packages/hldpro-sim/tests/test_providers.py → ./scripts/overlord/validate_registry_surfaces.py
- `test_evidence_scan_rejects_sensitive_material()` --calls--> `_scan_evidence_dir()`  [INFERRED]
  ./scripts/remote-mcp/tests/test_live_health_monitor.py → ./scripts/remote-mcp/live_health_monitor.py
- `_load_yaml()` --calls--> `read_text()`  [INFERRED]
  ./tools/local-ci-gate/local_ci_gate.py → ./scripts/overlord/validate_registry_surfaces.py
- `_read_changed_files_file()` --calls--> `read_text()`  [INFERRED]
  ./tools/local-ci-gate/local_ci_gate.py → ./scripts/overlord/validate_registry_surfaces.py
- `_scope_lane_claim_issue()` --calls--> `read_text()`  [INFERRED]
  ./tools/local-ci-gate/local_ci_gate.py → ./scripts/overlord/validate_registry_surfaces.py

## Communities

### Community 0 - "Windows ollama Submit Audit"
Cohesion: 0.03
Nodes (122): AuditWriter, canonical_json(), compute_entry_hmac(), compute_sha256(), Write an audit entry. Returns True if successful, False otherwise.          Args, Return canonical JSON for HMAC computation., Write or update today's manifest., Compute SHA256 hash of bytes. (+114 more)

### Community 1 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.03
Nodes (52): check(), main(), Exercise worktree invocation while still resolving the canonical governance root, Exercise failure when the canonical governance root is absent., Exercise Seek/Ponder bootstrap aliases without leaking synthetic values., Exercise Stampede bootstrap with production Tradier mapping and redaction., Exercise lam bootstrap with command-like vault values and missing optional keys., run_canonical_root_worktree_lam_bootstrap() (+44 more)

### Community 2 - "Orchestrator Read only observer Overlord"
Cohesion: 0.05
Nodes (70): compare_inventory(), _default_branch_name(), _inventory_rows_from_payload(), InventoryDrift, load_inventory_file(), _load_json(), load_live_inventory(), main() (+62 more)

### Community 3 - "Orchestrator Hitl relay queue"
Cohesion: 0.06
Nodes (82): append_audit(), atomic_write_json(), _base_packet(), _build_decision_packet(), _build_instruction_packet(), build_request(), _build_response_packet(), _build_resume_packet() (+74 more)

### Community 4 - "Packet Validate Schema"
Cohesion: 0.04
Nodes (54): _dispatch_packet(), _make_parent_packet(), Cross-family independence violated: both planners are anthropic., anthropic + openai is fine., Parent file absent → warn, don't refuse., Sanity: the patterns file should be present in this worktree., Non-LAM role with PII artifact path must be refused., worker-lam role is allowed to handle PII artifacts. (+46 more)

### Community 5 - "Som client Som client Mcp"
Cohesion: 0.05
Nodes (59): BaseHTTPRequestHandler, build_parser(), _env_has_live_markers(), main(), _run_fixture(), _run_live(), _scan_evidence_dir(), _stage_d_args() (+51 more)

### Community 6 - "Deploy Deploy gate Run"
Cohesion: 0.08
Nodes (71): ArtifactStats, branch_binding_preflight(), _check_pages_limits(), count_files(), deploy(), emit_evidence(), enforce_pages_limits(), extract_deployment_url() (+63 more)

### Community 7 - "Packages Hldpro sim"
Cohesion: 0.05
Nodes (43): ABC, BaseAggregator, ArtifactWriter, RunManifest, BaseAggregator, BaseModel, _load_workflow(), SimulationEngine (+35 more)

### Community 8 - "Overlord Deploy governance tooling"
Cohesion: 0.07
Nodes (25): GovernanceDeployError, build_governance(), emit_dispatch_packet(), emit_packet(), main(), Emit a dispatch-ready packet that includes a complete governance block., Emit a minimal or dispatch-ready packet YAML file. Returns path to written file., Build a governance block dict for inclusion in a dispatch-ready packet. (+17 more)

### Community 9 - "Local ci gate Local ci gate Profile"
Cohesion: 0.08
Nodes (39): _branch_issue_number(), build_argument_parser(), _build_summary(), _changed_files_from_git(), ChangedFiles, _check_exit_code(), _check_matches_changed_files(), CheckResult (+31 more)

### Community 10 - "Cli session supervisor Overlord"
Cohesion: 0.06
Nodes (49): _check_required_checks(), evaluate(), _labels(), main(), collect_repo_metrics(), main(), parse_iso(), pct() (+41 more)

### Community 11 - "Knowledge base Graphify"
Cohesion: 0.07
Nodes (45): build_graph(), _community_label(), _derive_path_phrase(), _derive_path_tokens(), infer_community_labels(), main(), _normalize_phrase(), _sanitize_markdown_artifacts() (+37 more)

### Community 12 - "Overlord Deploy governance tooling"
Cohesion: 0.1
Nodes (47): add_common_args(), apply(), _build_local_ci_plan(), build_plan(), _consumer_record(), _consumer_record_relpath(), _ensure_relative_to(), _ensure_remote_reachable_governance_ref() (+39 more)

### Community 13 - "Deploy Deploy verifier Domain"
Cohesion: 0.1
Nodes (50): _branch(), build_report(), _cname_note(), _deployment_url(), _domain_label(), _domain_result(), _domains(), emit_summary() (+42 more)

### Community 14 - "Overlord Assert execution scope"
Cohesion: 0.09
Nodes (48): _branch_issue_number(), _changed_paths(), _changed_paths_from_file(), check_scope(), _current_branch(), ExecutionScope, _format_path(), _git_root() (+40 more)

### Community 15 - "Knowledge base Measure graphify usage"
Cohesion: 0.08
Nodes (43): backlog_issues(), build_summary(), collect_active_issue_refs(), current_repo_slug(), fail(), gh_json(), IssueRef, main() (+35 more)

### Community 16 - "Overlord Verify governance consumer"
Cohesion: 0.17
Nodes (1): TestVerifyGovernanceConsumer

### Community 17 - "Session bootstrap Check"
Cohesion: 0.08
Nodes (44): build_parser(), _changed_files(), check_publish_gate(), _fail(), _git_root(), main(), _package_has_file_index_check(), print_json() (+36 more)

### Community 18 - "Orchestrator Self learning"
Cohesion: 0.11
Nodes (30): atomic_write_yaml(), build_report(), _date_from_text(), duplicate_counts(), enrich_packet(), _entry_id(), LearningEntry, LearningMatch (+22 more)

### Community 19 - "Overlord Assert execution scope"
Cohesion: 0.18
Nodes (4): _git(), RepoFixture, TestAssertExecutionScope, _working_directory()

### Community 20 - "Overlord Verify governance consumer"
Cohesion: 0.1
Nodes (43): build_parser(), _consumer_record_relpath(), ConsumerRecord, ConsumerVerifyError, _contains_negated_forbidden_action(), _ensure_remote_reachable_governance_ref(), _expected_checksum(), _expected_entry_failures() (+35 more)

### Community 21 - "Overlord Codex ingestion"
Cohesion: 0.1
Nodes (36): append_fail_fast_block_entry(), append_fail_fast_candidate(), append_fail_fast_table_entry(), append_progress_candidate(), bounded_text(), build_parser(), build_review_context(), build_schema_file() (+28 more)

### Community 22 - "Orchestrator Packet queue"
Cohesion: 0.14
Nodes (18): append_audit(), _audit_path(), ensure_queue(), load_packet(), _load_plan(), QueueDecision, _repo_relative_path(), _run_cli() (+10 more)

### Community 23 - "Overlord Validate handoff package"
Cohesion: 0.23
Nodes (8): _consumer_scope(), _dispatch_contract(), _handoff(), _plan(), _scope(), TestValidateHandoffPackage, _write_json(), _write_supporting_files()

### Community 24 - "Overlord Check stage6 closeout"
Cohesion: 0.13
Nodes (15): build_parser(), CloseoutDecision, evaluate(), _is_governance_surface(), _is_planning_only(), _issue_number(), main(), _matching_closeouts() (+7 more)

### Community 25 - "Overlord Check governance issue branch parity"
Cohesion: 0.14
Nodes (19): active_governance_issue_numbers(), branch_issue_number(), check_branch_parity(), current_branch(), fail(), main(), parse_args(), check_github_issue_open() (+11 more)

### Community 26 - "Lam Runtime inventory"
Cohesion: 0.1
Nodes (18): detect_pii(), _iter_patterns(), load_pii_patterns(), Load and validate pii patterns from pii_patterns.yml., Scan text for PII patterns from YAML patterns.      Falls back to the previous b, build_inventory(), import_available(), local_runtime() (+10 more)

### Community 27 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.16
Nodes (29): _agent_registry_has_agent(), _agent_surface_exists(), _alternate_review_identity_gate_applies(), _branch_issue_number(), _display_path(), _find_plan_files(), _is_governance_surface(), _is_planning_evidence_surface() (+21 more)

### Community 28 - "Overlord Report governance consumer status"
Cohesion: 0.13
Nodes (21): build_parser(), build_report(), _count_or_none(), inspect_repo(), _load_json(), _load_record(), main(), _managed_paths() (+13 more)

### Community 29 - "Overlord Validate closeout"
Cohesion: 0.17
Nodes (15): _json(), TestValidateCloseout, _write(), build_parser(), _execution_scope_refs(), _extract_repo_refs(), _load_json(), main() (+7 more)

### Community 30 - "Overlord Validate sql schema"
Cohesion: 0.17
Nodes (17): TestValidateSqlSchemaProbeContract, valid_contract(), build_parser(), _column_key(), _contract_paths(), _display(), _fixture_columns(), _load_contract() (+9 more)

### Community 31 - "Overlord Local ci gate workflow"
Cohesion: 0.14
Nodes (13): _all_executable_lines(), _all_run_commands(), check_contract(), _contains_main_branch(), _executable_lines(), _failures_for_text(), _has_executable_line_starting_with(), main() (+5 more)

### Community 32 - "Overlord Validate session error patterns"
Cohesion: 0.21
Nodes (10): _settings(), ValidateSessionContractSurfacesTests, _write(), TestValidateSessionErrorPatterns, _write_runbook(), _field_key(), _fields(), _pattern_sections() (+2 more)

### Community 33 - "Overlord Validate handoff package"
Cohesion: 0.22
Nodes (22): _agent_registry_has_agent(), _agent_surface_exists(), _consumer_managed_paths(), _consumer_verifier_acceptance_gate_applies(), _criteria_verification_refs(), _discover_package_files(), _dispatch_contract_gate_applies(), _evidence_ref_gate_applies() (+14 more)

### Community 34 - "Overlord Org governance compendium"
Cohesion: 0.19
Nodes (21): build(), category_for(), describe_file(), esc(), FileInfo, first_comment(), first_heading(), frontmatter_field() (+13 more)

### Community 35 - "Orchestrator Delegation gate"
Cohesion: 0.18
Nodes (19): apply_policy(), classifier_match(), _contains_term(), decide(), deterministic_match(), GateDecision, _load_classifier(), load_rules() (+11 more)

### Community 36 - "Overlord Workflow local coverage"
Cohesion: 0.24
Nodes (12): _actual_workflows(), check_inventory(), _command_file_candidates(), _load_inventory(), main(), _normalize_path(), _validate_coverage(), _validate_required_snippets() (+4 more)

### Community 37 - "Overlord Check plan preflight"
Cohesion: 0.19
Nodes (2): _run(), TestPlanPreflight

### Community 38 - "Overlord Check worker handoff route"
Cohesion: 0.37
Nodes (4): _git(), RepoFixture, _scope(), TestWorkerHandoffRoute

### Community 39 - "Packet Validate hitl relay"
Cohesion: 0.25
Nodes (16): _correlation(), _decision(), _instruction(), load_packet(), _operator_reply(), _packet_type(), _policy(), _run_cli() (+8 more)

### Community 40 - "Remote mcp Monitor alert"
Cohesion: 0.24
Nodes (14): build_alert(), build_parser(), _contains_sensitive(), _load_payload(), main(), _now(), render_markdown(), _safe_text() (+6 more)

### Community 41 - "Deploy Inventory direct upload projects"
Cohesion: 0.23
Nodes (14): _api_get_projects(), _deployment_metadata(), _domains(), _git_provider_status(), inventory(), _latest_deployment(), _load_json(), main() (+6 more)

### Community 42 - "Overlord Validate provisioning evidence"
Cohesion: 0.32
Nodes (1): ValidateProvisioningEvidenceTest

### Community 43 - "Overlord Check execution environment"
Cohesion: 0.42
Nodes (8): CheckExecutionEnvironmentTests, _git(), _make_repo(), _run(), _write(), _write_handoff(), _write_plan(), _write_scope()

### Community 44 - "Overlord Check org repo inventory"
Cohesion: 0.51
Nodes (1): TestOrgRepoInventory

### Community 45 - "Overlord Validate provisioning evidence"
Cohesion: 0.36
Nodes (11): _default_paths(), _expand_scan_paths(), Finding, _is_env_file(), _is_scan_candidate(), main(), _normalize_repo_path(), _read_changed_files() (+3 more)

### Community 46 - "Overlord Lane bootstrap"
Cohesion: 0.3
Nodes (2): run_helper(), TestLaneBootstrap

### Community 47 - "Overlord Lane bootstrap"
Cohesion: 0.35
Nodes (10): cleanup_advice(), infer_repo_slug(), LanePolicy, load_policy(), main(), _match(), normalize_slug(), parse_args() (+2 more)

### Community 48 - "Overlord Validate backlog gh sync"
Cohesion: 1.0
Nodes (0): 

### Community 49 - "Windows ollama Init"
Cohesion: 1.0
Nodes (0): 

### Community 50 - "Deploy Init"
Cohesion: 1.0
Nodes (0): 

### Community 51 - "Deploy Init"
Cohesion: 1.0
Nodes (0): 

### Community 52 - "Som client Som client From"
Cohesion: 1.0
Nodes (1): Build a client from well-known environment variables.

### Community 53 - "Packages Hldpro sim Personas"
Cohesion: 1.0
Nodes (1): Convenience: load shared dir from bundled package personas/.

## Knowledge Gaps
- **82 isolated node(s):** `Exercise lam bootstrap with command-like vault values and missing optional keys.`, `Exercise worktree invocation while still resolving the canonical governance root`, `Exercise failure when the canonical governance root is absent.`, `Exercise Seek/Ponder bootstrap aliases without leaking synthetic values.`, `Exercise Stampede bootstrap with production Tradier mapping and redaction.` (+77 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Overlord Validate backlog gh sync`** (2 nodes): `validate_backlog_gh_sync.py`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Windows ollama Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Deploy Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Deploy Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Som client Som client From`** (1 nodes): `Build a client from well-known environment variables.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Packages Hldpro sim Personas`** (1 nodes): `Convenience: load shared dir from bundled package personas/.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `read_text()` connect `Orchestrator Hitl relay queue` to `Windows ollama Submit Audit`, `Overlord Validate structured agent cycle plan`, `Orchestrator Read only observer Overlord`, `Packet Validate Schema`, `Som client Som client Mcp`, `Deploy Deploy gate Run`, `Packages Hldpro sim`, `Overlord Deploy governance tooling`, `Local ci gate Local ci gate Profile`, `Cli session supervisor Overlord`, `Knowledge base Graphify`, `Overlord Deploy governance tooling`, `Deploy Deploy verifier Domain`, `Overlord Assert execution scope`, `Knowledge base Measure graphify usage`, `Overlord Verify governance consumer`, `Session bootstrap Check`, `Orchestrator Self learning`, `Overlord Verify governance consumer`, `Overlord Codex ingestion`, `Orchestrator Packet queue`, `Overlord Check stage6 closeout`, `Overlord Check governance issue branch parity`, `Lam Runtime inventory`, `Overlord Validate structured agent cycle plan`, `Overlord Report governance consumer status`, `Overlord Validate closeout`, `Overlord Validate sql schema`, `Overlord Local ci gate workflow`, `Overlord Validate session error patterns`, `Overlord Validate handoff package`, `Orchestrator Delegation gate`, `Overlord Workflow local coverage`, `Packet Validate hitl relay`, `Remote mcp Monitor alert`, `Deploy Inventory direct upload projects`, `Overlord Validate provisioning evidence`, `Overlord Lane bootstrap`?**
  _High betweenness centrality (0.491) - this node is a cross-community bridge._
- **Why does `parse_args()` connect `Cli session supervisor Overlord` to `Orchestrator Read only observer Overlord`, `Orchestrator Hitl relay queue`, `Packet Validate Schema`, `Som client Som client Mcp`, `Deploy Deploy gate Run`, `Packages Hldpro sim`, `Overlord Deploy governance tooling`, `Local ci gate Local ci gate Profile`, `Knowledge base Graphify`, `Overlord Deploy governance tooling`, `Deploy Deploy verifier Domain`, `Overlord Assert execution scope`, `Knowledge base Measure graphify usage`, `Session bootstrap Check`, `Orchestrator Self learning`, `Overlord Verify governance consumer`, `Overlord Codex ingestion`, `Orchestrator Packet queue`, `Overlord Check stage6 closeout`, `Lam Runtime inventory`, `Overlord Validate structured agent cycle plan`, `Overlord Report governance consumer status`, `Overlord Validate closeout`, `Overlord Validate sql schema`, `Overlord Local ci gate workflow`, `Overlord Validate session error patterns`, `Overlord Validate handoff package`, `Overlord Org governance compendium`, `Orchestrator Delegation gate`, `Overlord Workflow local coverage`, `Packet Validate hitl relay`, `Remote mcp Monitor alert`, `Deploy Inventory direct upload projects`, `Overlord Validate provisioning evidence`?**
  _High betweenness centrality (0.172) - this node is a cross-community bridge._
- **Why does `main()` connect `Overlord Deploy governance tooling` to `Overlord Validate structured agent cycle plan`, `Som client Som client Mcp`, `Deploy Inventory direct upload projects`, `Overlord Validate provisioning evidence`, `Cli session supervisor Overlord`, `Overlord Check org repo inventory`, `Deploy Deploy verifier Domain`, `Overlord Verify governance consumer`, `Overlord Assert execution scope`, `Overlord Validate handoff package`, `Overlord Local ci gate workflow`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Are the 169 inferred relationships involving `read_text()` (e.g. with `_load_yaml()` and `_read_changed_files_file()`) actually correct?**
  _`read_text()` has 169 INFERRED edges - model-reasoned connections that need verification._
- **Are the 55 inferred relationships involving `parse_args()` (e.g. with `main()` and `test_claude_stream_json_native_argv_adds_verbose()`) actually correct?**
  _`parse_args()` has 55 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `WindowsOllamaSubmitter` (e.g. with `AuditWriter` and `TestPiiDetection`) actually correct?**
  _`WindowsOllamaSubmitter` has 39 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Exercise lam bootstrap with command-like vault values and missing optional keys.`, `Exercise worktree invocation while still resolving the canonical governance root`, `Exercise failure when the canonical governance root is absent.` to the rest of the system?**
  _82 weakly-connected nodes found - possible documentation gaps or missing edges._