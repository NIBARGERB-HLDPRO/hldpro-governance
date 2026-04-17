# Graph Report - hldpro-governance  (2026-04-17)

## Corpus Check
- Large corpus: 1340 files · ~279,463 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 527 nodes · 1026 edges · 31 communities detected
- Extraction: 49% EXTRACTED · 51% INFERRED · 0% AMBIGUOUS · INFERRED: 525 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `WindowsOllamaSubmitter` - 48 edges
2. `PiiDetectionError` - 44 edges
3. `ModelNotAllowedError` - 44 edges
4. `EndpointUnreachableError` - 44 edges
5. `_tier1_packet()` - 29 edges
6. `AuditWriter` - 28 edges
7. `describe_file()` - 14 edges
8. `TestGovernanceSurfacePlanGate` - 13 edges
9. `graphify_results()` - 13 edges
10. `cmd_generate()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Submit requests to Windows-Ollama endpoint with PII detection and allowlist enfo` --uses--> `AuditWriter`  [INFERRED]
  hldpro-governance/scripts/windows-ollama/submit.py → hldpro-governance/scripts/windows-ollama/audit.py
- `Raised when PII is detected or explicitly marked.` --uses--> `AuditWriter`  [INFERRED]
  hldpro-governance/scripts/windows-ollama/submit.py → hldpro-governance/scripts/windows-ollama/audit.py
- `Raised when model is not in allowlist.` --uses--> `AuditWriter`  [INFERRED]
  hldpro-governance/scripts/windows-ollama/submit.py → hldpro-governance/scripts/windows-ollama/audit.py
- `Raised when Windows-Ollama endpoint is unreachable.` --uses--> `AuditWriter`  [INFERRED]
  hldpro-governance/scripts/windows-ollama/submit.py → hldpro-governance/scripts/windows-ollama/audit.py
- `Return structured error dict for JSON output.` --uses--> `AuditWriter`  [INFERRED]
  hldpro-governance/scripts/windows-ollama/submit.py → hldpro-governance/scripts/windows-ollama/audit.py

## Communities

### Community 0 - "Windows ollama Submit"
Cohesion: 0.08
Nodes (49): Exception, EndpointUnreachableError, main(), ModelNotAllowedError, PiiDetectionError, Raised when PII is detected or explicitly marked., Raised when model is not in allowlist., Raised when Windows-Ollama endpoint is unreachable. (+41 more)

### Community 1 - "Packet Validate Passes"
Cohesion: 0.07
Nodes (19): _make_parent_packet(), Cross-family independence violated: both planners are anthropic., anthropic + openai is fine., Parent file absent → warn, don't refuse., Sanity: the patterns file should be present in this worktree., Non-LAM role with PII artifact path must be refused., worker-lam role is allowed to handle PII artifacts., When pii-patterns.yml is absent, validator must refuse (not silently pass). (+11 more)

### Community 2 - "Windows ollama Audit"
Cohesion: 0.07
Nodes (24): AuditWriter, canonical_json(), compute_entry_hmac(), compute_sha256(), Write an audit entry. Returns True if successful, False otherwise.          Args, Return canonical JSON for HMAC computation., Write or update today's manifest., Compute SHA256 hash of bytes. (+16 more)

### Community 3 - "Overlord Codex ingestion"
Cohesion: 0.1
Nodes (34): append_fail_fast_block_entry(), append_fail_fast_candidate(), append_fail_fast_table_entry(), append_progress_candidate(), bounded_text(), build_parser(), build_review_context(), build_schema_file() (+26 more)

### Community 4 - "Windows ollama Audit"
Cohesion: 0.07
Nodes (26): Modify first_hash in manifest and verify fails., Test that truncated file (missing last line) breaks manifest., Delete last line and verify detects entry_count mismatch., Test that duplicate line (replay) breaks seq monotonicity., Duplicate a line and verify detects non-monotonic seq., Test that tampering with a line breaks the chain., Tamper with line N and verify fails at line N+1., Test that replacing entry_hmac with wrong value fails verification. (+18 more)

### Community 5 - "Packet Validate Load"
Cohesion: 0.1
Nodes (30): _find_packet_file(), _load_packet(), load_pii_patterns(), _load_schema(), Load and compile PII patterns from pii-patterns.yml., Enforce cross-family independence for tier-1 dual-planner packets.      When pri, Refuse if any consecutive pair in the parent chain shares model_id across differ, Enforce expected handoff sequence with no tier jumps. (+22 more)

### Community 6 - "Knowledge base Measure graphify usage"
Cohesion: 0.16
Nodes (28): aggregate_file_scores(), augment_workflow_doc_candidates(), baseline_results(), build_summary(), build_trace(), emit_usage_events(), estimate_tokens(), evaluate_relevance() (+20 more)

### Community 7 - "Orchestrator Read only observer"
Cohesion: 0.15
Nodes (24): _expand_home(), governed_repos(), GovernedRepo, load_registry(), repo_names_enabled_for(), repos_enabled_for(), repos_root(), _artifact() (+16 more)

### Community 8 - "Overlord Org governance compendium"
Cohesion: 0.19
Nodes (21): build(), category_for(), describe_file(), esc(), FileInfo, first_comment(), first_heading(), frontmatter_field() (+13 more)

### Community 9 - "Overlord Check progress github issue staleness"
Cohesion: 0.23
Nodes (12): backlog_issues(), build_summary(), collect_active_issue_refs(), current_repo_slug(), fail(), gh_json(), IssueRef, main() (+4 more)

### Community 10 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.28
Nodes (2): _plan(), TestGovernanceSurfacePlanGate

### Community 11 - "Overlord Assert execution scope"
Cohesion: 0.36
Nodes (4): _git(), RepoFixture, TestAssertExecutionScope, _working_directory()

### Community 12 - "Overlord Assert execution scope"
Cohesion: 0.36
Nodes (11): _changed_paths(), check_scope(), _current_branch(), ExecutionScope, _format_path(), _git_root(), _load_scope(), main() (+3 more)

### Community 13 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.38
Nodes (10): _branch_issue_number(), _find_plan_files(), _is_governance_surface(), _load_json(), main(), _matching_plan_payloads(), _read_changed_files(), _require() (+2 more)

### Community 14 - "Knowledge base Graph"
Cohesion: 0.38
Nodes (10): build_graph(), _community_label(), _derive_path_phrase(), _derive_path_tokens(), infer_community_labels(), main(), _normalize_phrase(), _sanitize_markdown_artifacts() (+2 more)

### Community 15 - "Overlord Validate backlog gh sync"
Cohesion: 0.29
Nodes (9): check_github_issue(), find_planned_table(), main(), parse_columns(), Return (header_line_index, list_of_data_lines) for the ## Planned table., Split a markdown table row into a dict keyed by header column names.     Returns, Extract a #NNN from the cell value.     Returns the integer issue number, or Non, Call GitHub API to verify issue exists and is open.     Returns (ok: bool, title (+1 more)

### Community 16 - "Knowledge base Graphify targets"
Cohesion: 0.38
Nodes (9): filtered_targets(), find_target(), load_manifest(), main(), print_json(), print_shell(), print_stage_paths(), print_tsv() (+1 more)

### Community 17 - "Overlord Memory integrity"
Cohesion: 0.42
Nodes (7): check_memory_exists(), inspect_repo(), load_memory_lines(), main(), memory_dir_for_repo(), parse_pointer_filenames(), validate_frontmatter()

### Community 18 - "Knowledge base Graphify usage logging"
Cohesion: 0.61
Nodes (8): check(), main(), run_command(), test_logger_backwards_compatible(), test_logger_query_trace_fields(), test_measurement_falls_back_from_stale_governance_repo_path(), test_measurement_outputs_query_traces(), test_schema_shape()

### Community 19 - "Overlord Effectiveness metrics"
Cohesion: 0.46
Nodes (7): collect_repo_metrics(), main(), parse_iso(), pct(), render_markdown(), RepoMetrics, run()

### Community 20 - "Overlord Validate governed repos"
Cohesion: 0.67
Nodes (6): check(), fail(), load_json(), main(), validate_graphify_reconciliation(), validate_registry_shape()

### Community 21 - "Orchestrator Read only observer"
Cohesion: 0.48
Nodes (2): _copy_fixture(), TestReadOnlyObserver

### Community 22 - "Overlord Check overlord backlog github alignment"
Cohesion: 0.67
Nodes (5): collect_section_lines(), fail(), has_issue_ref(), main(), parse_markdown_row()

### Community 23 - "Windows ollama Pii"
Cohesion: 0.4
Nodes (5): detect_pii(), _iter_patterns(), load_pii_patterns(), Load and validate pii patterns from pii_patterns.yml., Scan text for PII patterns from YAML patterns.      Falls back to the previous b

### Community 24 - "Knowledge base Log graphify usage"
Cohesion: 0.7
Nodes (4): append_event(), build_event(), main(), parse_args()

### Community 25 - "Knowledge base Update knowledge"
Cohesion: 0.83
Nodes (3): main(), replace_section(), summary_line()

### Community 26 - "Packet Emit Yaml"
Cohesion: 0.67
Nodes (3): emit_packet(), main(), Emit a packet YAML file.     Returns: path to written file

### Community 27 - "Overlord Render github issue feed"
Cohesion: 1.0
Nodes (2): main(), render_issue()

### Community 28 - "Knowledge base Graphify governance"
Cohesion: 1.0
Nodes (2): check(), main()

### Community 29 - "Knowledge base Push graph to neo4j"
Cohesion: 1.0
Nodes (2): build_scoped_graph(), main()

### Community 30 - "Windows ollama Init"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **55 isolated node(s):** `Return (header_line_index, list_of_data_lines) for the ## Planned table.`, `Split a markdown table row into a dict keyed by header column names.     Returns`, `Extract a #NNN from the cell value.     Returns the integer issue number, or Non`, `Call GitHub API to verify issue exists and is open.     Returns (ok: bool, title`, `Return canonical JSON for HMAC computation.` (+50 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Windows ollama Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AuditWriter` connect `Windows ollama Audit` to `Windows ollama Submit`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `WindowsOllamaSubmitter` connect `Windows ollama Submit` to `Windows ollama Audit`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Why does `PiiDetectionError` connect `Windows ollama Submit` to `Windows ollama Audit`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `WindowsOllamaSubmitter` (e.g. with `main()` and `AuditWriter`) actually correct?**
  _`WindowsOllamaSubmitter` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `PiiDetectionError` (e.g. with `.submit()` and `AuditWriter`) actually correct?**
  _`PiiDetectionError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `ModelNotAllowedError` (e.g. with `.submit()` and `AuditWriter`) actually correct?**
  _`ModelNotAllowedError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `EndpointUnreachableError` (e.g. with `.submit()` and `AuditWriter`) actually correct?**
  _`EndpointUnreachableError` has 39 INFERRED edges - model-reasoned connections that need verification._