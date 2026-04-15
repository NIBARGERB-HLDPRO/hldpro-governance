# Graph Report - hldpro-governance  (2026-04-14)

## Corpus Check
- Large corpus: 1203 files · ~189,258 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 212 nodes · 372 edges · 17 communities detected
- Extraction: 53% EXTRACTED · 47% INFERRED · 0% AMBIGUOUS · INFERRED: 176 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `_tier1_packet()` - 17 edges
2. `graphify_results()` - 13 edges
3. `cmd_generate()` - 11 edges
4. `cmd_qualify()` - 9 edges
5. `main()` - 9 edges
6. `main()` - 9 edges
7. `baseline_results()` - 8 edges
8. `cmd_promote()` - 7 edges
9. `augment_workflow_doc_candidates()` - 7 edges
10. `collect_repo_metrics()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `ValidateLocationTests` --uses--> `Finding`  [INFERRED]
  hldpro-governance/tests/test_codex_ingestion.py → hldpro-governance/scripts/overlord/codex_ingestion.py

## Communities

### Community 0 - "Overlord Codex ingestion"
Cohesion: 0.1
Nodes (34): append_fail_fast_block_entry(), append_fail_fast_candidate(), append_fail_fast_table_entry(), append_progress_candidate(), bounded_text(), build_parser(), build_review_context(), build_schema_file() (+26 more)

### Community 1 - "Packet Validate Pii"
Cohesion: 0.09
Nodes (15): _make_parent_packet(), anthropic + openai is fine., Parent file absent → warn, don't refuse., Same model_id appearing as both planner and reviewer in the chain., Sanity: the patterns file should be present in this worktree., Non-LAM role with PII artifact path must be refused., worker-lam role is allowed to handle PII artifacts., When pii-patterns.yml is absent, validator must refuse (not silently pass). (+7 more)

### Community 2 - "Knowledge base Measure graphify usage"
Cohesion: 0.16
Nodes (28): aggregate_file_scores(), augment_workflow_doc_candidates(), baseline_results(), build_summary(), build_trace(), emit_usage_events(), estimate_tokens(), evaluate_relevance() (+20 more)

### Community 3 - "Packet Validate Pii"
Cohesion: 0.16
Nodes (18): _find_packet_file(), _load_packet(), load_pii_patterns(), Enforce cross-family independence for tier-1 dual-planner packets.      When pri, Refuse if any consecutive pair in the parent chain shares model_id across differ, Refuse tier-1 packets whose model is below the planning floor., Refuse if PII artifacts appear outside LAM-role packets, or if the pattern file, Run all validators against a packet dict.      Returns (all_passed, list_of_fail (+10 more)

### Community 4 - "Overlord Check progress github issue staleness"
Cohesion: 0.23
Nodes (12): backlog_issues(), build_summary(), collect_active_issue_refs(), current_repo_slug(), fail(), gh_json(), IssueRef, main() (+4 more)

### Community 5 - "Knowledge base Graph"
Cohesion: 0.38
Nodes (10): build_graph(), _community_label(), _derive_path_phrase(), _derive_path_tokens(), infer_community_labels(), main(), _normalize_phrase(), _sanitize_markdown_artifacts() (+2 more)

### Community 6 - "Knowledge base Graphify targets"
Cohesion: 0.38
Nodes (9): filtered_targets(), find_target(), load_manifest(), main(), print_json(), print_shell(), print_stage_paths(), print_tsv() (+1 more)

### Community 7 - "Knowledge base Graphify usage logging"
Cohesion: 0.61
Nodes (8): check(), main(), run_command(), test_logger_backwards_compatible(), test_logger_query_trace_fields(), test_measurement_falls_back_from_stale_governance_repo_path(), test_measurement_outputs_query_traces(), test_schema_shape()

### Community 8 - "Overlord Effectiveness metrics"
Cohesion: 0.46
Nodes (7): collect_repo_metrics(), main(), parse_iso(), pct(), render_markdown(), RepoMetrics, run()

### Community 9 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.6
Nodes (5): _find_plan_files(), _load_json(), main(), _require(), _validate_file()

### Community 10 - "Overlord Check overlord backlog github alignment"
Cohesion: 0.67
Nodes (5): collect_section_lines(), fail(), has_issue_ref(), main(), parse_markdown_row()

### Community 11 - "Knowledge base Log graphify usage"
Cohesion: 0.7
Nodes (4): append_event(), build_event(), main(), parse_args()

### Community 12 - "Knowledge base Update knowledge"
Cohesion: 0.83
Nodes (3): main(), replace_section(), summary_line()

### Community 13 - "Packet Emit Yaml"
Cohesion: 0.67
Nodes (3): emit_packet(), main(), Emit a packet YAML file.     Returns: path to written file

### Community 14 - "Overlord Render github issue feed"
Cohesion: 1.0
Nodes (2): main(), render_issue()

### Community 15 - "Knowledge base Graphify governance"
Cohesion: 1.0
Nodes (2): check(), main()

### Community 16 - "Knowledge base Push graph to neo4j"
Cohesion: 1.0
Nodes (2): build_scoped_graph(), main()

## Knowledge Gaps
- **18 isolated node(s):** `Load a YAML packet; return None if missing or malformed.`, `Locate a packet file by ID (supports YYYY-MM-DD-<id>.yml naming).`, `Walk parent_packet_id links backwards; return ordered list [packet, parent, ...]`, `Load and compile PII patterns from pii-patterns.yml.`, `Enforce cross-family independence for tier-1 dual-planner packets.      When pri` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 16 inferred relationships involving `_tier1_packet()` (e.g. with `.test_tier1_without_parent_passes()` and `.test_same_family_dual_planner_refused()`) actually correct?**
  _`_tier1_packet()` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `graphify_results()` (e.g. with `resolve_repo_root()` and `load_graph()`) actually correct?**
  _`graphify_results()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `cmd_generate()` (e.g. with `git_lines()` and `write_json()`) actually correct?**
  _`cmd_generate()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `cmd_qualify()` (e.g. with `load_json()` and `write_json()`) actually correct?**
  _`cmd_qualify()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `main()` (e.g. with `parse_args()` and `load_scenarios()`) actually correct?**
  _`main()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Load a YAML packet; return None if missing or malformed.`, `Locate a packet file by ID (supports YYYY-MM-DD-<id>.yml naming).`, `Walk parent_packet_id links backwards; return ordered list [packet, parent, ...]` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Overlord Codex ingestion` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._