# Graph Report - hldpro-governance  (2026-04-18)

## Corpus Check
- Large corpus: 1462 files · ~344,476 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 887 nodes · 1668 edges · 47 communities detected
- Extraction: 51% EXTRACTED · 49% INFERRED · 0% AMBIGUOUS · INFERRED: 815 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `_tier1_packet()` - 29 edges
2. `TestAssertExecutionScope` - 28 edges
3. `RepoFixture` - 25 edges
4. `TestGovernanceSurfacePlanGate` - 21 edges
5. `TestLocalCiGate` - 19 edges
6. `TestDeployGovernanceTooling` - 19 edges
7. `TestDeployLocalCIGate` - 16 edges
8. `TestPacketQueue` - 15 edges
9. `describe_file()` - 14 edges
10. `build_plan()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `GateError` --inherits--> `RuntimeError`  [EXTRACTED]
  tools/local-ci-gate/local_ci_gate.py →   _Bridges community 4 → community 21_
- `GovernanceDeployError` --inherits--> `RuntimeError`  [EXTRACTED]
  scripts/overlord/deploy_governance_tooling.py →   _Bridges community 21 → community 10_
- `HelperError` --inherits--> `RuntimeError`  [EXTRACTED]
  scripts/knowledge_base/graphify_hook_helper.py →   _Bridges community 21 → community 8_

## Communities

### Community 0 - "Windows ollama Submit"
Cohesion: 0.03
Nodes (37): Test that clean prompt passes PII detection., Negative test: non-allowlisted model., Test that non-allowlisted model is rejected., Test that allowlisted model passes allowlist check., Negative test: unreachable endpoint., Test that unreachable endpoint raises appropriate error., Test that endpoint timeout is handled., Test that reachable endpoint succeeds. (+29 more)

### Community 1 - "Packet Validate Passes"
Cohesion: 0.07
Nodes (19): _make_parent_packet(), Cross-family independence violated: both planners are anthropic., anthropic + openai is fine., Parent file absent → warn, don't refuse., Sanity: the patterns file should be present in this worktree., Non-LAM role with PII artifact path must be refused., worker-lam role is allowed to handle PII artifacts., When pii-patterns.yml is absent, validator must refuse (not silently pass). (+11 more)

### Community 2 - "Overlord Codex ingestion"
Cohesion: 0.1
Nodes (34): append_fail_fast_block_entry(), append_fail_fast_candidate(), append_fail_fast_table_entry(), append_progress_candidate(), bounded_text(), build_parser(), build_review_context(), build_schema_file() (+26 more)

### Community 3 - "Windows ollama Submit"
Cohesion: 0.07
Nodes (25): Exception, detect_pii(), _iter_patterns(), load_pii_patterns(), Load and validate pii patterns from pii_patterns.yml., Scan text for PII patterns from YAML patterns.      Falls back to the previous b, EndpointUnreachableError, main() (+17 more)

### Community 4 - "Local ci gate Local ci gate Report"
Cohesion: 0.12
Nodes (37): _branch_issue_number(), build_argument_parser(), _build_summary(), _changed_files_from_git(), ChangedFiles, _check_exit_code(), _check_matches_changed_files(), CheckResult (+29 more)

### Community 5 - "Overlord Assert execution scope"
Cohesion: 0.23
Nodes (4): _git(), RepoFixture, TestAssertExecutionScope, _working_directory()

### Community 6 - "Windows ollama Audit"
Cohesion: 0.07
Nodes (26): Modify first_hash in manifest and verify fails., Test that truncated file (missing last line) breaks manifest., Delete last line and verify detects entry_count mismatch., Test that duplicate line (replay) breaks seq monotonicity., Duplicate a line and verify detects non-monotonic seq., Test that tampering with a line breaks the chain., Tamper with line N and verify fails at line N+1., Test that replacing entry_hmac with wrong value fails verification. (+18 more)

### Community 7 - "Orchestrator Self learning"
Cohesion: 0.15
Nodes (26): atomic_write_yaml(), build_report(), _date_from_text(), duplicate_counts(), enrich_packet(), _entry_id(), LearningEntry, LearningMatch (+18 more)

### Community 8 - "Knowledge base Graphify"
Cohesion: 0.13
Nodes (19): add_common_args(), build_plan(), build_refresh_command(), execute_refresh(), find_target(), git_hook_paths(), HelperError, HookPlan (+11 more)

### Community 9 - "Packet Validate Load"
Cohesion: 0.1
Nodes (30): _find_packet_file(), _load_packet(), load_pii_patterns(), _load_schema(), Load and compile PII patterns from pii-patterns.yml., Enforce cross-family independence for tier-1 dual-planner packets.      When pri, Refuse if any consecutive pair in the parent chain shares model_id across differ, Enforce expected handoff sequence with no tier jumps. (+22 more)

### Community 10 - "Overlord Deploy governance tooling"
Cohesion: 0.18
Nodes (24): add_common_args(), apply(), _build_local_ci_plan(), build_plan(), _consumer_record(), _consumer_record_relpath(), _ensure_relative_to(), _fail() (+16 more)

### Community 11 - "Knowledge base Measure graphify usage"
Cohesion: 0.16
Nodes (28): aggregate_file_scores(), augment_workflow_doc_candidates(), baseline_results(), build_summary(), build_trace(), emit_usage_events(), estimate_tokens(), evaluate_relevance() (+20 more)

### Community 12 - "Overlord Check local ci gate workflow"
Cohesion: 0.11
Nodes (14): _all_executable_lines(), _all_run_commands(), check_contract(), _contains_main_branch(), _executable_lines(), _failures_for_text(), _has_executable_line_starting_with(), _load_workflow() (+6 more)

### Community 13 - "Overlord Assert execution scope"
Cohesion: 0.17
Nodes (22): _changed_paths(), _changed_paths_from_file(), check_scope(), _current_branch(), ExecutionScope, _format_path(), _git_root(), HandoffEvidence (+14 more)

### Community 14 - "Windows ollama Audit"
Cohesion: 0.14
Nodes (15): AuditWriter, canonical_json(), compute_entry_hmac(), compute_sha256(), Write an audit entry. Returns True if successful, False otherwise.          Args, Return canonical JSON for HMAC computation., Write or update today's manifest., Compute SHA256 hash of bytes. (+7 more)

### Community 15 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.18
Nodes (2): _plan(), TestGovernanceSurfacePlanGate

### Community 16 - "Overlord Org governance compendium"
Cohesion: 0.19
Nodes (21): build(), category_for(), describe_file(), esc(), FileInfo, first_comment(), first_heading(), frontmatter_field() (+13 more)

### Community 17 - "Overlord Workflow local coverage"
Cohesion: 0.21
Nodes (12): _actual_workflows(), check_inventory(), _command_file_candidates(), _load_inventory(), main(), _normalize_path(), _validate_coverage(), _validate_required_snippets() (+4 more)

### Community 18 - "Orchestrator Packet queue"
Cohesion: 0.2
Nodes (18): append_audit(), _audit_path(), ensure_queue(), load_packet(), _load_plan(), QueueDecision, Replay audit events into logical latest states.      `latest_states` includes ac, replay_audit() (+10 more)

### Community 19 - "Local ci gate Local ci gate Profile"
Cohesion: 0.1
Nodes (1): TestLocalCiGate

### Community 20 - "Overlord Deploy governance tooling"
Cohesion: 0.32
Nodes (1): TestDeployGovernanceTooling

### Community 21 - "Overlord Deploy local ci gate"
Cohesion: 0.25
Nodes (15): add_common_args(), build_plan(), _common_preview_payload(), DeployError, DeployPlan, _existing_shim_state(), _fail(), _is_relative_to() (+7 more)

### Community 22 - "Orchestrator Read only observer"
Cohesion: 0.22
Nodes (17): _artifact(), ArtifactStatus, build_reports(), _count_open_issue_metadata(), _daemon_readiness(), _git_commit(), _latest_raw_issue_file(), main() (+9 more)

### Community 23 - "Overlord Deploy local ci gate"
Cohesion: 0.27
Nodes (1): TestDeployLocalCIGate

### Community 24 - "Orchestrator Packet queue"
Cohesion: 0.3
Nodes (2): _packet(), TestPacketQueue

### Community 25 - "Overlord Check progress github issue staleness"
Cohesion: 0.23
Nodes (12): backlog_issues(), build_summary(), collect_active_issue_refs(), current_repo_slug(), fail(), gh_json(), IssueRef, main() (+4 more)

### Community 26 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.35
Nodes (12): _branch_issue_number(), _find_plan_files(), _is_governance_surface(), _load_json(), main(), _matching_execution_scopes(), _matching_plan_payloads(), _read_changed_files() (+4 more)

### Community 27 - "Lam Runtime inventory"
Cohesion: 0.18
Nodes (2): FakeResponse, TestRuntimeInventory

### Community 28 - "Knowledge base Graph"
Cohesion: 0.38
Nodes (10): build_graph(), _community_label(), _derive_path_phrase(), _derive_path_tokens(), infer_community_labels(), main(), _normalize_phrase(), _sanitize_markdown_artifacts() (+2 more)

### Community 29 - "Overlord Validate backlog gh sync"
Cohesion: 0.29
Nodes (9): check_github_issue(), find_planned_table(), main(), parse_columns(), Return (header_line_index, list_of_data_lines) for the ## Planned table., Split a markdown table row into a dict keyed by header column names.     Returns, Extract a #NNN from the cell value.     Returns the integer issue number, or Non, Call GitHub API to verify issue exists and is open.     Returns (ok: bool, title (+1 more)

### Community 30 - "Lam Runtime inventory"
Cohesion: 0.4
Nodes (9): build_inventory(), import_available(), local_runtime(), mac_hardware(), main(), memory_budget(), pii_guardrail(), _run() (+1 more)

### Community 31 - "Knowledge base Graphify targets"
Cohesion: 0.38
Nodes (9): filtered_targets(), find_target(), load_manifest(), main(), print_json(), print_shell(), print_stage_paths(), print_tsv() (+1 more)

### Community 32 - "Overlord Governed repos"
Cohesion: 0.42
Nodes (7): _expand_home(), governed_repos(), GovernedRepo, load_registry(), repo_names_enabled_for(), repos_enabled_for(), repos_root()

### Community 33 - "Overlord Memory integrity"
Cohesion: 0.42
Nodes (7): check_memory_exists(), inspect_repo(), load_memory_lines(), main(), memory_dir_for_repo(), parse_pointer_filenames(), validate_frontmatter()

### Community 34 - "Knowledge base Graphify usage logging"
Cohesion: 0.61
Nodes (8): check(), main(), run_command(), test_logger_backwards_compatible(), test_logger_query_trace_fields(), test_measurement_falls_back_from_stale_governance_repo_path(), test_measurement_outputs_query_traces(), test_schema_shape()

### Community 35 - "Overlord Effectiveness metrics"
Cohesion: 0.46
Nodes (7): collect_repo_metrics(), main(), parse_iso(), pct(), render_markdown(), RepoMetrics, run()

### Community 36 - "Overlord Validate governed repos"
Cohesion: 0.67
Nodes (6): check(), fail(), load_json(), main(), validate_graphify_reconciliation(), validate_registry_shape()

### Community 37 - "Orchestrator Read only observer"
Cohesion: 0.48
Nodes (2): _copy_fixture(), TestReadOnlyObserver

### Community 38 - "Overlord Check overlord backlog github alignment"
Cohesion: 0.67
Nodes (5): collect_section_lines(), fail(), has_issue_ref(), main(), parse_markdown_row()

### Community 39 - "Knowledge base Log graphify usage"
Cohesion: 0.7
Nodes (4): append_event(), build_event(), main(), parse_args()

### Community 40 - "Knowledge base Graphify governance"
Cohesion: 0.83
Nodes (3): check(), is_ignored(), main()

### Community 41 - "Knowledge base Update knowledge"
Cohesion: 0.83
Nodes (3): main(), replace_section(), summary_line()

### Community 42 - "Packet Emit Yaml"
Cohesion: 0.67
Nodes (3): emit_packet(), main(), Emit a packet YAML file.     Returns: path to written file

### Community 43 - "Overlord Render github issue feed"
Cohesion: 1.0
Nodes (2): main(), render_issue()

### Community 44 - "Knowledge base Push graph to neo4j"
Cohesion: 1.0
Nodes (2): build_scoped_graph(), main()

### Community 45 - "Windows ollama Init"
Cohesion: 1.0
Nodes (0): 

### Community 46 - "Windows ollama Submit Temporary"
Cohesion: 1.0
Nodes (1): Temporary audit directory for testing.

## Knowledge Gaps
- **100 isolated node(s):** `Return (header_line_index, list_of_data_lines) for the ## Planned table.`, `Split a markdown table row into a dict keyed by header column names.     Returns`, `Extract a #NNN from the cell value.     Returns the integer issue number, or Non`, `Call GitHub API to verify issue exists and is open.     Returns (ok: bool, title`, `Submit requests to Windows-Ollama endpoint with PII detection and allowlist enfo` (+95 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Windows ollama Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Windows ollama Submit Temporary`** (1 nodes): `Temporary audit directory for testing.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GateError` connect `Local ci gate Local ci gate Report` to `Overlord Deploy local ci gate`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Why does `HelperError` connect `Knowledge base Graphify` to `Overlord Deploy local ci gate`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **Why does `GovernanceDeployError` connect `Overlord Deploy governance tooling` to `Overlord Deploy local ci gate`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Are the 28 inferred relationships involving `_tier1_packet()` (e.g. with `.test_tier1_without_parent_passes()` and `.test_same_family_dual_planner_refused()`) actually correct?**
  _`_tier1_packet()` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `RepoFixture` (e.g. with `.test_allows_changes_in_allowed_paths_dirty_tree_mode()` and `.test_planning_only_diff_inside_allowed_paths_passes()`) actually correct?**
  _`RepoFixture` has 22 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Return (header_line_index, list_of_data_lines) for the ## Planned table.`, `Split a markdown table row into a dict keyed by header column names.     Returns`, `Extract a #NNN from the cell value.     Returns the integer issue number, or Non` to the rest of the system?**
  _100 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Windows ollama Submit` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._