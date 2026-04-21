# Graph Report - asc-evaluator  (2026-04-21)

## Corpus Check
- 42 files · ~115,586 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 101 nodes · 184 edges · 13 communities detected
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Generate existing info report Reviews|Generate existing info report Reviews]]
- [[_COMMUNITY_Generate docx from markdown Cycle|Generate docx from markdown Cycle]]
- [[_COMMUNITY_Xlsx text extract|Xlsx text extract]]
- [[_COMMUNITY_Processed Pinecroft the woodlands tx 20260114 Annotate|Processed Pinecroft the woodlands tx 20260114 Annotate]]
- [[_COMMUNITY_Processed Pinecroft the woodlands tx 20260114 Annotate|Processed Pinecroft the woodlands tx 20260114 Annotate]]
- [[_COMMUNITY_Processed Pinecroft the woodlands tx 20260114 Annotate|Processed Pinecroft the woodlands tx 20260114 Annotate]]
- [[_COMMUNITY_Generate existing info report|Generate existing info report]]
- [[_COMMUNITY_Generate existing info report Reviews|Generate existing info report Reviews]]
- [[_COMMUNITY_Generate existing info report Reviews|Generate existing info report Reviews]]
- [[_COMMUNITY_Extract xlsx images|Extract xlsx images]]
- [[_COMMUNITY_Generate existing info report Add|Generate existing info report Add]]
- [[_COMMUNITY_Generate existing info report Add|Generate existing info report Add]]
- [[_COMMUNITY_Generate existing info report Add|Generate existing info report Add]]

## God Nodes (most connected - your core abstractions)
1. `write_docx()` - 16 edges
2. `convert()` - 9 edges
3. `main()` - 8 edges
4. `extract_workbook()` - 8 edges
5. `annotate()` - 7 edges
6. `annotate()` - 7 edges
7. `clean_display_text()` - 7 edges
8. `annotate()` - 6 edges
9. `sheet_rows()` - 6 edges
10. `parse_main_findings()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `add_heading_styled()` --calls--> `add_heading()`  [INFERRED]
  asc-evaluator/Processed/Pinecroft_TheWoodlands_TX_20260114/generate_final_report.py → asc-evaluator/Reviews/Cycle_1_MHSC_Richmond_20250513/scripts/generate_existing_info_report.py
- `annotate()` --calls--> `convert()`  [INFERRED]
  asc-evaluator/Processed/Pinecroft_TheWoodlands_TX_20260114/annotate_images_v3.py → asc-evaluator/Reviews/Cycle_1_MHSC_Richmond_20250513/scripts/generate_docx_from_markdown.py
- `annotate()` --calls--> `convert()`  [INFERRED]
  asc-evaluator/Processed/Pinecroft_TheWoodlands_TX_20260114/annotate_images.py → asc-evaluator/Reviews/Cycle_1_MHSC_Richmond_20250513/scripts/generate_docx_from_markdown.py
- `annotate()` --calls--> `convert()`  [INFERRED]
  asc-evaluator/Processed/Pinecroft_TheWoodlands_TX_20260114/annotate_images_v2.py → asc-evaluator/Reviews/Cycle_1_MHSC_Richmond_20250513/scripts/generate_docx_from_markdown.py
- `convert()` --calls--> `add_heading()`  [INFERRED]
  asc-evaluator/Reviews/Cycle_1_MHSC_Richmond_20250513/scripts/generate_docx_from_markdown.py → asc-evaluator/Reviews/Cycle_1_MHSC_Richmond_20250513/scripts/generate_existing_info_report.py

## Communities

### Community 0 - "Generate existing info report Reviews"
Cohesion: 0.18
Nodes (12): AppendixImage, cell_ref_parts(), cell_text(), col_to_num(), drawing_image_anchors(), image_output_lookup(), load_shared_strings(), nearby_issue_text() (+4 more)

### Community 1 - "Generate docx from markdown Cycle"
Cohesion: 0.23
Nodes (9): add_markdown_table(), convert(), flush_paragraph(), main(), style_heading(), add_table(), add_heading_styled(), make_table() (+1 more)

### Community 2 - "Xlsx text extract"
Cohesion: 0.33
Nodes (8): cell_ref_parts(), cell_text(), col_to_num(), extract_workbook(), load_shared_strings(), main(), _MarkdownCsvAdapter, workbook_sheets()

### Community 3 - "Processed Pinecroft the woodlands tx 20260114 Annotate"
Cohesion: 0.29
Nodes (9): annotate(), draw_arrow(), draw_circle(), get_color(), px(), Annotate ALL 43 facility images — arrows and circles ONLY (no text on images). V, Draw a thick arrow with filled arrowhead., Convert proportional coordinate (0.0-1.0) to pixel. (+1 more)

### Community 4 - "Processed Pinecroft the woodlands tx 20260114 Annotate"
Cohesion: 0.27
Nodes (9): annotate(), draw_arrow(), draw_circle(), draw_label(), Annotate facility images with arrows, crop zones, and labels for findings. Produ, Draw an arrow from start to end point., Draw a label with semi-transparent background., Draw a circle highlight. (+1 more)

### Community 5 - "Processed Pinecroft the woodlands tx 20260114 Annotate"
Cohesion: 0.29
Nodes (9): annotate(), draw_arrow(), draw_circle(), draw_highlight(), get_color(), Annotate ALL 43 facility images — arrows and highlight zones ONLY (no text on im, Draw a thick arrow with filled arrowhead., Draw semi-transparent rectangle highlight. (+1 more)

### Community 6 - "Generate existing info report"
Cohesion: 0.38
Nodes (8): clean_display_text(), domain_from_section(), excel_date(), Finding, main(), parse_hr_notes(), parse_main_findings(), parse_photo_notes()

### Community 7 - "Generate existing info report Reviews"
Cohesion: 0.36
Nodes (9): add_finding_block(), add_heading(), add_info_row(), add_tabbed_info_row(), fit_image_size(), keep_paragraph_together(), set_document_layout(), set_update_fields_on_open() (+1 more)

### Community 8 - "Generate existing info report Reviews"
Cohesion: 0.33
Nodes (7): collect_report_strings(), executive_summary_text(), grouped_counts(), risk_from_score(), run_spell_check(), top_risk_items(), write_md()

### Community 9 - "Extract xlsx images"
Cohesion: 1.0
Nodes (2): extract_images(), main()

### Community 10 - "Generate existing info report Add"
Cohesion: 0.67
Nodes (3): add_bottom_divider(), add_horizontal_rule(), add_note_block()

### Community 11 - "Generate existing info report Add"
Cohesion: 1.0
Nodes (2): add_field(), add_footer()

### Community 12 - "Generate existing info report Add"
Cohesion: 1.0
Nodes (2): add_static_toc_line(), add_toc()

## Knowledge Gaps
- **14 isolated node(s):** `Generate Final Report for Pinecroft Cycle 1 as a professional Word document.`, `Annotate ALL 43 facility images — arrows and circles ONLY (no text on images). V`, `Draw a thick arrow with filled arrowhead.`, `Convert proportional coordinate (0.0-1.0) to pixel.`, `annotations: list of dicts with proportional coords (0.0-1.0):       - arrow: ((` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Generate existing info report Add`** (2 nodes): `add_field()`, `add_footer()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Generate existing info report Add`** (2 nodes): `add_static_toc_line()`, `add_toc()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `convert()` connect `Generate docx from markdown Cycle` to `Processed Pinecroft the woodlands tx 20260114 Annotate`, `Processed Pinecroft the woodlands tx 20260114 Annotate`, `Processed Pinecroft the woodlands tx 20260114 Annotate`, `Generate existing info report Reviews`?**
  _High betweenness centrality (0.512) - this node is a cross-community bridge._
- **Why does `add_heading()` connect `Generate existing info report Reviews` to `Generate docx from markdown Cycle`, `Generate existing info report`?**
  _High betweenness centrality (0.442) - this node is a cross-community bridge._
- **Why does `annotate()` connect `Processed Pinecroft the woodlands tx 20260114 Annotate` to `Generate docx from markdown Cycle`?**
  _High betweenness centrality (0.163) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `convert()` (e.g. with `annotate()` and `annotate()`) actually correct?**
  _`convert()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Generate Final Report for Pinecroft Cycle 1 as a professional Word document.`, `Annotate ALL 43 facility images — arrows and circles ONLY (no text on images). V`, `Draw a thick arrow with filled arrowhead.` to the rest of the system?**
  _14 weakly-connected nodes found - possible documentation gaps or missing edges._