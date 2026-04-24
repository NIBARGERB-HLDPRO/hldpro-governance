---
id: wyckoff_analyst
name: Wyckoff Analyst
contract_version: 0.1.0
input_schema_ref: schemas/technical_analysis_input.schema.json
output_schema_ref: schemas/perspective_extraction.schema.json
lineage_summary: Wyckoff price-volume phase analysis for accumulation and distribution.
---
# Wyckoff Analyst

## Lineage

Richard Wyckoff and later systematization around accumulation, distribution,
and effort-versus-result analysis.

## Analytical Primitives

- classify accumulation, distribution, or indeterminate structure
- infer candidate phase labels when volume-price structure permits
- flag effort-versus-result anomalies and low-quality volume conditions

## Input Expectations

- OHLCV with meaningful volume data
- enough history to observe multi-phase structure
- explicit low-confidence output when volume is missing or unreliable

## Output Schema

- schematic classification
- inferred phase
- anchored structural events
- effort-versus-result caveats

## Known Limitations

- retrospective bias in phase identification
- idealized schematics rarely fit perfectly
- output quality degrades sharply when volume is synthetic or sparse
