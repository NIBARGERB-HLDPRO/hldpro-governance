# Graph Report - hldpro-governance  (2026-04-16)

## Corpus Check
- Large corpus: 1298 files · ~242,409 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 390 nodes · 760 edges · 31 communities detected
- Extraction: 49% EXTRACTED · 51% INFERRED · 0% AMBIGUOUS · INFERRED: 388 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `WindowsOllamaSubmitter` - 48 edges
2. `PiiDetectionError` - 44 edges
3. `ModelNotAllowedError` - 44 edges
4. `EndpointUnreachableError` - 44 edges
5. `AuditWriter` - 28 edges
6. `_tier1_packet()` - 17 edges
7. `graphify_results()` - 13 edges
8. `cmd_generate()` - 11 edges
9. `TestAuditIntegration` - 11 edges
10. `TestPiiDetection` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Raised when PII is detected or explicitly marked.` --uses--> `AuditWriter`  [INFERRED]
  hldpro-governance/scripts/windows-ollama/submit.py → hldpro-governance/scripts/windows-ollama/audit.py
- `Return structured error dict for JSON output.` --uses--> `AuditWriter`  [INFERRED]
  hldpro-governance/scripts/windows-ollama/submit.py → hldpro-governance/scripts/windows-ollama/audit.py
- `Raised when model is not in allowlist.` --uses--> `AuditWriter`  [INFERRED]
  hldpro-governance/scripts/windows-ollama/submit.py → hldpro-governance/scripts/windows-ollama/audit.py
- `Return structured error dict for JSON output.` --uses--> `AuditWriter`  [INFERRED]
  hldpro-governance/scripts/windows-ollama/submit.py → hldpro-governance/scripts/windows-ollama/audit.py
- `Raised when Windows-Ollama endpoint is unreachable.` --uses--> `AuditWriter`  [INFERRED]
  hldpro-governance/scripts/windows-ollama/submit.py → hldpro-governance/scripts/windows-ollama/audit.py

## Communities

### Community 0 - "Overlord Codex ingestion"
Cohesion: 0.1
Nodes (34): append_fail_fast_block_entry(), append_fail_fast_candidate(), append_fail_fast_table_entry(), append_progress_candidate(), bounded_text(), build_parser(), build_review_context(), build_schema_file() (+26 more)

### Community 1 - "Packet Validate Pii"
Cohesion: 0.09
Nodes (15): _make_parent_packet(), anthropic + openai is fine., Parent file absent → warn, don't refuse., Same model_id appearing as both planner and reviewer in the chain., Sanity: the patterns file should be present in this worktree., Non-LAM role with PII artifact path must be refused., worker-lam role is allowed to handle PII artifacts., When pii-patterns.yml is absent, validator must refuse (not silently pass). (+7 more)

### Community 2 - "Windows ollama Audit"
Cohesion: 0.07
Nodes (26): Modify first_hash in manifest and verify fails., Test that truncated file (missing last line) breaks manifest., Delete last line and verify detects entry_count mismatch., Test that duplicate line (replay) breaks seq monotonicity., Duplicate a line and verify detects non-monotonic seq., Test that tampering with a line breaks the chain., Tamper with line N and verify fails at line N+1., Test that replacing entry_hmac with wrong value fails verification. (+18 more)

### Community 3 - "Knowledge base Measure graphify usage"
Cohesion: 0.16
Nodes (28): aggregate_file_scores(), augment_workflow_doc_candidates(), baseline_results(), build_summary(), build_trace(), emit_usage_events(), estimate_tokens(), evaluate_relevance() (+20 more)

### Community 4 - "Windows ollama Submit"
Cohesion: 0.15
Nodes (13): AuditWriter, Append-only audit log writer with hash-chain and daily manifest., main(), Scan text for PII patterns.          Returns: pattern name if detected, None oth, Verify model is in allowlist for the specified role., Submit a request to Windows-Ollama.          Args:             model: Model name, POST to /api/generate and return response., Return structured error dict for JSON output. (+5 more)

### Community 5 - "Windows ollama Audit"
Cohesion: 0.13
Nodes (13): canonical_json(), compute_entry_hmac(), compute_sha256(), Write an audit entry. Returns True if successful, False otherwise.          Args, Return canonical JSON for HMAC computation., Write or update today's manifest., Compute SHA256 hash of bytes., Compute HMAC-SHA256 over canonical JSON of entry (without entry_hmac field). (+5 more)

### Community 6 - "Packet Validate Pii"
Cohesion: 0.16
Nodes (18): _find_packet_file(), _load_packet(), load_pii_patterns(), Enforce cross-family independence for tier-1 dual-planner packets.      When pri, Refuse if any consecutive pair in the parent chain shares model_id across differ, Refuse tier-1 packets whose model is below the planning floor., Refuse if PII artifacts appear outside LAM-role packets, or if the pattern file, Run all validators against a packet dict.      Returns (all_passed, list_of_fail (+10 more)

### Community 7 - "Overlord Check progress github issue staleness"
Cohesion: 0.23
Nodes (12): backlog_issues(), build_summary(), collect_active_issue_refs(), current_repo_slug(), fail(), gh_json(), IssueRef, main() (+4 more)

### Community 8 - "Windows ollama Submit"
Cohesion: 0.19
Nodes (9): EndpointUnreachableError, Raised when Windows-Ollama endpoint is unreachable., Verify that all submission paths write exactly one audit entry., Test that successful submission writes one audit entry., Test that PII detection writes one audit entry with status='rejected'., Test that explicit PII flag writes one audit entry., Test that model rejection writes one audit entry., Test that endpoint unreachability writes one audit entry. (+1 more)

### Community 9 - "Windows ollama Submit"
Cohesion: 0.19
Nodes (9): Exception, PiiDetectionError, Raised when PII is detected or explicitly marked., Return structured error dict for JSON output., Negative test: unreachable endpoint., Test that unreachable endpoint raises appropriate error., Test that endpoint timeout is handled., Test that reachable endpoint succeeds. (+1 more)

### Community 10 - "Windows ollama Submit"
Cohesion: 0.21
Nodes (8): ModelNotAllowedError, Raised when model is not in allowlist., Return structured error dict for JSON output., Negative test: non-allowlisted model., Test that non-allowlisted model is rejected., Test that allowlisted model passes allowlist check., Temporary audit directory for testing., TestModelAllowlist

### Community 11 - "Knowledge base Graph"
Cohesion: 0.38
Nodes (10): build_graph(), _community_label(), _derive_path_phrase(), _derive_path_tokens(), infer_community_labels(), main(), _normalize_phrase(), _sanitize_markdown_artifacts() (+2 more)

### Community 12 - "Overlord Validate backlog gh sync"
Cohesion: 0.29
Nodes (9): check_github_issue(), find_planned_table(), main(), parse_columns(), Return (header_line_index, list_of_data_lines) for the ## Planned table., Split a markdown table row into a dict keyed by header column names.     Returns, Extract a #NNN from the cell value.     Returns the integer issue number, or Non, Call GitHub API to verify issue exists and is open.     Returns (ok: bool, title (+1 more)

### Community 13 - "Windows ollama Submit"
Cohesion: 0.2
Nodes (6): Test that clean prompt passes PII detection., Negative test: PII detection., Test that SSN pattern is detected., Test that email pattern is detected., Test that explicit has_pii=True triggers pii_halt., TestPiiDetection

### Community 14 - "Windows ollama Submit"
Cohesion: 0.2
Nodes (6): Negative test: empty rationale from model., Test that response with missing 'response' field is handled gracefully., Test response with empty 'response' field., Create a submitter with test config., submitter(), TestEmptyRationale

### Community 15 - "Knowledge base Graphify targets"
Cohesion: 0.38
Nodes (9): filtered_targets(), find_target(), load_manifest(), main(), print_json(), print_shell(), print_stage_paths(), print_tsv() (+1 more)

### Community 16 - "Overlord Memory integrity"
Cohesion: 0.42
Nodes (7): check_memory_exists(), inspect_repo(), load_memory_lines(), main(), memory_dir_for_repo(), parse_pointer_filenames(), validate_frontmatter()

### Community 17 - "Knowledge base Graphify usage logging"
Cohesion: 0.61
Nodes (8): check(), main(), run_command(), test_logger_backwards_compatible(), test_logger_query_trace_fields(), test_measurement_falls_back_from_stale_governance_repo_path(), test_measurement_outputs_query_traces(), test_schema_shape()

### Community 18 - "Overlord Effectiveness metrics"
Cohesion: 0.46
Nodes (7): collect_repo_metrics(), main(), parse_iso(), pct(), render_markdown(), RepoMetrics, run()

### Community 19 - "Windows ollama Submit"
Cohesion: 0.25
Nodes (5): Verify error structures for JSON output., Test that PII errors have correct JSON structure., Test that model-not-allowed errors have correct JSON structure., Test that endpoint-unreachable errors have correct JSON structure., TestErrorStructure

### Community 20 - "Overlord Validate structured agent cycle plan"
Cohesion: 0.6
Nodes (5): _find_plan_files(), _load_json(), main(), _require(), _validate_file()

### Community 21 - "Overlord Check overlord backlog github alignment"
Cohesion: 0.67
Nodes (5): collect_section_lines(), fail(), has_issue_ref(), main(), parse_markdown_row()

### Community 22 - "Windows ollama Submit Response"
Cohesion: 0.33
Nodes (4): Negative test: malformed /api/generate response., Test that invalid JSON response is rejected., Test that empty response is handled., TestMalformedResponse

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
- **50 isolated node(s):** `Return (header_line_index, list_of_data_lines) for the ## Planned table.`, `Split a markdown table row into a dict keyed by header column names.     Returns`, `Extract a #NNN from the cell value.     Returns the integer issue number, or Non`, `Call GitHub API to verify issue exists and is open.     Returns (ok: bool, title`, `Return canonical JSON for HMAC computation.` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Windows ollama Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AuditWriter` connect `Windows ollama Submit` to `Windows ollama Submit`, `Windows ollama Submit`, `Windows ollama Submit`, `Windows ollama Audit`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `WindowsOllamaSubmitter` connect `Windows ollama Submit` to `Windows ollama Submit`, `Windows ollama Submit`, `Windows ollama Submit`, `Windows ollama Submit`, `Windows ollama Submit`, `Windows ollama Submit`, `Windows ollama Submit Response`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `PiiDetectionError` connect `Windows ollama Submit` to `Windows ollama Submit`, `Windows ollama Submit`, `Windows ollama Submit`, `Windows ollama Submit`, `Windows ollama Submit`, `Windows ollama Submit`, `Windows ollama Submit Response`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `WindowsOllamaSubmitter` (e.g. with `main()` and `AuditWriter`) actually correct?**
  _`WindowsOllamaSubmitter` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `PiiDetectionError` (e.g. with `.submit()` and `AuditWriter`) actually correct?**
  _`PiiDetectionError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `ModelNotAllowedError` (e.g. with `.submit()` and `AuditWriter`) actually correct?**
  _`ModelNotAllowedError` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `EndpointUnreachableError` (e.g. with `.submit()` and `AuditWriter`) actually correct?**
  _`EndpointUnreachableError` has 39 INFERRED edges - model-reasoned connections that need verification._