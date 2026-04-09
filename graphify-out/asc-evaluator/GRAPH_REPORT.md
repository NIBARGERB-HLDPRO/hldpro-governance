# Graph Report - asc-evaluator  (2026-04-09)

## Corpus Check
- 20 files · ~73,955 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 35 nodes · 42 edges · 4 communities detected
- Extraction: 74% EXTRACTED · 26% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `annotate()` - 6 edges
2. `annotate()` - 6 edges
3. `annotate()` - 5 edges
4. `draw_arrow()` - 3 edges
5. `draw_highlight()` - 3 edges
6. `draw_arrow()` - 3 edges
7. `draw_label()` - 3 edges
8. `draw_circle()` - 3 edges
9. `draw_arrow()` - 3 edges
10. `px()` - 3 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Processed Pinecroft the woodlands tx 20260114 Annotate"
Cohesion: 0.29
Nodes (9): annotate(), draw_arrow(), draw_circle(), draw_highlight(), get_color(), Annotate ALL 43 facility images — arrows and highlight zones ONLY (no text on im, Draw a thick arrow with filled arrowhead., Draw semi-transparent rectangle highlight. (+1 more)

### Community 1 - "Processed Pinecroft the woodlands tx 20260114 Annotate"
Cohesion: 0.27
Nodes (9): annotate(), draw_arrow(), draw_circle(), draw_label(), Annotate facility images with arrows, crop zones, and labels for findings. Produ, Draw an arrow from start to end point., Draw a label with semi-transparent background., Draw a circle highlight. (+1 more)

### Community 2 - "Processed Pinecroft the woodlands tx 20260114 Annotate"
Cohesion: 0.29
Nodes (9): annotate(), draw_arrow(), draw_circle(), get_color(), px(), Annotate ALL 43 facility images — arrows and circles ONLY (no text on images). V, Draw a thick arrow with filled arrowhead., Convert proportional coordinate (0.0-1.0) to pixel. (+1 more)

### Community 3 - "Processed Pinecroft the woodlands tx 20260114 Generate"
Cohesion: 0.4
Nodes (1): Generate Final Report for Pinecroft Cycle 1 as a professional Word document.

## Knowledge Gaps
- **14 isolated node(s):** `Annotate ALL 43 facility images — arrows and highlight zones ONLY (no text on im`, `Draw a thick arrow with filled arrowhead.`, `Draw semi-transparent rectangle highlight.`, `annotations: list of dicts:       - arrow: ((from_x, from_y), (to_x, to_y))`, `Annotate facility images with arrows, crop zones, and labels for findings. Produ` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 4 inferred relationships involving `annotate()` (e.g. with `get_color()` and `draw_highlight()`) actually correct?**
  _`annotate()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `annotate()` (e.g. with `get_color()` and `draw_circle()`) actually correct?**
  _`annotate()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `annotate()` (e.g. with `draw_circle()` and `draw_arrow()`) actually correct?**
  _`annotate()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Annotate ALL 43 facility images — arrows and highlight zones ONLY (no text on im`, `Draw a thick arrow with filled arrowhead.`, `Draw semi-transparent rectangle highlight.` to the rest of the system?**
  _14 weakly-connected nodes found - possible documentation gaps or missing edges._