---
id: classical_chart_pattern_analyst
name: Classical Chart Pattern Analyst
contract_version: 0.1.0
input_schema_ref: schemas/technical_analysis_input.schema.json
output_schema_ref: schemas/perspective_extraction.schema.json
lineage_summary: Canonical chart-pattern identification with validation discipline.
---
# Classical Chart Pattern Analyst

## Lineage

Classical chart-pattern analysis from Edwards and Magee, Schabacker, and later
systematic validation traditions.

## Analytical Primitives

- identify named formations only when canonical structural requirements are met
- separate validated patterns from candidates and near-misses
- preserve anchored pattern boundaries and validation notes

## Input Expectations

- OHLCV window on a caller-specified timeframe
- volume when the canonical pattern uses volume-confirmation requirements
- enough history to observe the full candidate formation

## Output Schema

- detected pattern list
- anchored formation points and boundaries
- validation status and confidence
- measured-move notes where canonically applicable

## Known Limitations

- vulnerable to pareidolia in noisy data
- loose visual identification is not acceptable
- performance literature is materially weaker than the classical descriptive
  literature implies
