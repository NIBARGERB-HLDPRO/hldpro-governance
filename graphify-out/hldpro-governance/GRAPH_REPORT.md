# Graph Report - /Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85  (2026-04-09)

## Corpus Check
- Large corpus: 1119 files · ~167,766 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 104 nodes · 195 edges · 14 communities detected
- Extraction: 49% EXTRACTED · 51% INFERRED · 0% AMBIGUOUS · INFERRED: 100 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `cmd_generate()` - 11 edges
2. `graphify_results()` - 11 edges
3. `cmd_qualify()` - 9 edges
4. `cmd_promote()` - 7 edges
5. `augment_workflow_doc_candidates()` - 7 edges
6. `baseline_results()` - 7 edges
7. `main()` - 7 edges
8. `collect_repo_metrics()` - 6 edges
9. `main()` - 6 edges
10. `main()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `ValidateLocationTests` --uses--> `Finding`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85/tests/test_codex_ingestion.py → /Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-85/scripts/overlord/codex_ingestion.py

## Communities

### Community 0 - "Knowledge base Measure graphify usage"
Cohesion: 0.18
Nodes (24): aggregate_file_scores(), augment_workflow_doc_candidates(), baseline_results(), build_summary(), estimate_tokens(), evaluate_relevance(), GraphData, graphify_results() (+16 more)

### Community 1 - "Overlord Codex ingestion"
Cohesion: 0.24
Nodes (8): classify_finding(), cmd_status(), context_matches_anchors(), extract_claim_anchors(), list_backlog_files(), looks_like_camel_identifier(), read_context_window(), validate_location()

### Community 2 - "Overlord Codex ingestion"
Cohesion: 0.24
Nodes (11): bounded_text(), build_review_context(), build_schema_file(), cmd_generate(), extract_json_from_stdout(), git_lines(), normalize_review(), run() (+3 more)

### Community 3 - "Knowledge base Graph"
Cohesion: 0.47
Nodes (8): build_graph(), _community_label(), _derive_path_phrase(), _derive_path_tokens(), infer_community_labels(), main(), _normalize_phrase(), _split_words()

### Community 4 - "Overlord Effectiveness metrics"
Cohesion: 0.46
Nodes (7): collect_repo_metrics(), main(), parse_iso(), pct(), render_markdown(), RepoMetrics, run()

### Community 5 - "Overlord Codex ingestion"
Cohesion: 0.36
Nodes (8): append_progress_candidate(), cmd_promote(), cmd_qualify(), detect_duplicate(), Finding, load_json(), main(), markdown_escape()

### Community 6 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.6
Nodes (5): _find_plan_files(), _load_json(), main(), _require(), _validate_file()

### Community 7 - "Overlord Check overlord backlog github alignment"
Cohesion: 0.67
Nodes (5): collect_section_lines(), fail(), has_issue_ref(), main(), parse_markdown_row()

### Community 8 - "Codex ingestion Anchor"
Cohesion: 0.5
Nodes (1): ValidateLocationTests

### Community 9 - "Overlord Codex ingestion"
Cohesion: 0.67
Nodes (4): append_fail_fast_block_entry(), append_fail_fast_candidate(), append_fail_fast_table_entry(), find_section_span()

### Community 10 - "Overlord Render github issue feed"
Cohesion: 1.0
Nodes (2): main(), render_issue()

### Community 11 - "Knowledge base Log graphify usage"
Cohesion: 1.0
Nodes (2): main(), parse_args()

### Community 12 - "Knowledge base Push graph to neo4j"
Cohesion: 1.0
Nodes (2): build_scoped_graph(), main()

### Community 13 - "Overlord Codex ingestion"
Cohesion: 1.0
Nodes (2): build_parser(), today_string()

## Knowledge Gaps
- **Thin community `Overlord Codex ingestion`** (2 nodes): `build_parser()`, `today_string()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ValidateLocationTests` connect `Codex ingestion Anchor` to `Overlord Codex ingestion`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `Finding` connect `Overlord Codex ingestion` to `Codex ingestion Anchor`, `Overlord Codex ingestion`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Why does `cmd_generate()` connect `Overlord Codex ingestion` to `Overlord Codex ingestion`, `Overlord Codex ingestion`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `cmd_generate()` (e.g. with `git_lines()` and `write_json()`) actually correct?**
  _`cmd_generate()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `graphify_results()` (e.g. with `load_graph()` and `normalize_tokens()`) actually correct?**
  _`graphify_results()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `cmd_qualify()` (e.g. with `load_json()` and `write_json()`) actually correct?**
  _`cmd_qualify()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `cmd_promote()` (e.g. with `load_json()` and `Finding`) actually correct?**
  _`cmd_promote()` has 6 INFERRED edges - model-reasoned connections that need verification._