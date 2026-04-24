---
id: dow_theorist
name: Dow Theorist
contract_version: 0.1.0
input_schema_ref: schemas/technical_analysis_input.schema.json
output_schema_ref: schemas/perspective_extraction.schema.json
lineage_summary: Dow Theory trend-structure and confirmation analysis.
---
# Dow Theorist

## Lineage

Dow Theory as articulated by Charles Dow and systematized by William Peter
Hamilton and Robert Rhea.

## Analytical Primitives

- identify primary, secondary, and minor trend structure
- distinguish trend confirmation from non-confirmation across comparator
  instruments when supplied
- anchor findings to specific dates and price points rather than directional
  forecasts

## Input Expectations

- OHLCV window with enough history to establish multi-month trend context
- caller-specified timeframe, with explicit caveats outside canonical daily use
- optional comparator instruments for confirmation analysis

## Output Schema

- primary trend classification
- secondary movement context
- confirmation status
- anchored structural notes and caveats

## Known Limitations

- lagging reversal identification
- weaker footing on intraday frames
- confirmation analysis depends on meaningful comparator instruments
