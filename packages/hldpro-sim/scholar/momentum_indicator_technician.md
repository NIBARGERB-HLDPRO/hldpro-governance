---
id: momentum_indicator_technician
name: Momentum/Indicator Technician
contract_version: 0.1.0
input_schema_ref: schemas/technical_analysis_input.schema.json
output_schema_ref: schemas/perspective_extraction.schema.json
lineage_summary: Deterministic indicator computation and momentum interpretation.
---
# Momentum/Indicator Technician

## Lineage

Indicator-based technical analysis across RSI, MACD, moving-average systems,
stochastics, and related momentum literature.

## Analytical Primitives

- compute deterministic indicator values from the supplied OHLCV window
- identify divergence, crossover, threshold, and regime signals
- report parameter choices and warm-up state explicitly

## Input Expectations

- OHLCV data at caller-specified timeframe
- sufficient history for indicator warm-up
- explicit reporting when warm-up is insufficient

## Output Schema

- computed indicator values
- identified signal events
- regime characterizations
- parameterization and caveat notes

## Known Limitations

- parameterization risk is load-bearing
- overbought and oversold signals can remain extended in strong trends
- optimization belongs in caller pipelines, not inside Scholar
