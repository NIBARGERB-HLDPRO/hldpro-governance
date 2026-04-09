# Graph Report - hldpro-governance  (2026-04-09)

## Corpus Check
- Large corpus: 1127 files · ~172,448 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 140 nodes · 253 edges · 18 communities detected
- Extraction: 50% EXTRACTED · 50% INFERRED · 0% AMBIGUOUS · INFERRED: 126 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `graphify_results()` - 12 edges
2. `cmd_generate()` - 11 edges
3. `cmd_qualify()` - 9 edges
4. `main()` - 9 edges
5. `cmd_promote()` - 7 edges
6. `augment_workflow_doc_candidates()` - 7 edges
7. `baseline_results()` - 7 edges
8. `main()` - 7 edges
9. `collect_repo_metrics()` - 6 edges
10. `main()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `ValidateLocationTests` --uses--> `Finding`  [INFERRED]
  hldpro-governance/tests/test_codex_ingestion.py → hldpro-governance/scripts/overlord/codex_ingestion.py

## Communities

### Community 0 - "Knowledge base Measure graphify usage"
Cohesion: 0.17
Nodes (25): aggregate_file_scores(), augment_workflow_doc_candidates(), baseline_results(), build_summary(), estimate_tokens(), evaluate_relevance(), GraphData, graphify_results() (+17 more)

### Community 1 - "Overlord Check progress github issue staleness"
Cohesion: 0.23
Nodes (12): backlog_issues(), build_summary(), collect_active_issue_refs(), current_repo_slug(), fail(), gh_json(), IssueRef, main() (+4 more)

### Community 2 - "Knowledge base Graph"
Cohesion: 0.38
Nodes (10): build_graph(), _community_label(), _derive_path_phrase(), _derive_path_tokens(), infer_community_labels(), main(), _normalize_phrase(), _sanitize_markdown_artifacts() (+2 more)

### Community 3 - "Overlord Codex ingestion"
Cohesion: 0.27
Nodes (10): bounded_text(), build_review_context(), build_schema_file(), cmd_generate(), extract_json_from_stdout(), git_lines(), normalize_review(), run() (+2 more)

### Community 4 - "Knowledge base Graphify targets"
Cohesion: 0.38
Nodes (9): filtered_targets(), find_target(), load_manifest(), main(), print_json(), print_shell(), print_stage_paths(), print_tsv() (+1 more)

### Community 5 - "Overlord Codex ingestion"
Cohesion: 0.33
Nodes (5): context_matches_anchors(), extract_claim_anchors(), looks_like_camel_identifier(), read_context_window(), validate_location()

### Community 6 - "Overlord Effectiveness metrics"
Cohesion: 0.46
Nodes (7): collect_repo_metrics(), main(), parse_iso(), pct(), render_markdown(), RepoMetrics, run()

### Community 7 - "Overlord Codex ingestion"
Cohesion: 0.29
Nodes (8): append_progress_candidate(), classify_finding(), cmd_promote(), cmd_qualify(), detect_duplicate(), Finding, load_json(), write_json()

### Community 8 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.6
Nodes (5): _find_plan_files(), _load_json(), main(), _require(), _validate_file()

### Community 9 - "Overlord Check overlord backlog github alignment"
Cohesion: 0.67
Nodes (5): collect_section_lines(), fail(), has_issue_ref(), main(), parse_markdown_row()

### Community 10 - "Overlord Codex ingestion"
Cohesion: 0.4
Nodes (5): build_parser(), cmd_status(), list_backlog_files(), main(), today_string()

### Community 11 - "Overlord Codex ingestion"
Cohesion: 0.5
Nodes (5): append_fail_fast_block_entry(), append_fail_fast_candidate(), append_fail_fast_table_entry(), find_section_span(), markdown_escape()

### Community 12 - "Codex ingestion Anchor"
Cohesion: 0.5
Nodes (1): ValidateLocationTests

### Community 13 - "Knowledge base Update knowledge"
Cohesion: 0.83
Nodes (3): main(), replace_section(), summary_line()

### Community 14 - "Overlord Render github issue feed"
Cohesion: 1.0
Nodes (2): main(), render_issue()

### Community 15 - "Knowledge base Graphify governance"
Cohesion: 1.0
Nodes (2): check(), main()

### Community 16 - "Knowledge base Log graphify usage"
Cohesion: 1.0
Nodes (2): main(), parse_args()

### Community 17 - "Knowledge base Push graph to neo4j"
Cohesion: 1.0
Nodes (2): build_scoped_graph(), main()

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ValidateLocationTests` connect `Codex ingestion Anchor` to `Overlord Codex ingestion`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **Why does `Finding` connect `Overlord Codex ingestion` to `Codex ingestion Anchor`, `Overlord Codex ingestion`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `graphify_results()` (e.g. with `load_graph()` and `normalize_tokens()`) actually correct?**
  _`graphify_results()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `cmd_generate()` (e.g. with `git_lines()` and `write_json()`) actually correct?**
  _`cmd_generate()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `cmd_qualify()` (e.g. with `load_json()` and `write_json()`) actually correct?**
  _`cmd_qualify()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `main()` (e.g. with `load_manifest()` and `target_rows()`) actually correct?**
  _`main()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `cmd_promote()` (e.g. with `load_json()` and `Finding`) actually correct?**
  _`cmd_promote()` has 6 INFERRED edges - model-reasoned connections that need verification._