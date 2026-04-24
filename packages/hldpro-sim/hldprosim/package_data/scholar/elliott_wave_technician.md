---
id: elliott_wave_technician
name: Elliott Wave Technician
contract_version: 0.1.0
input_schema_ref: schemas/technical_analysis_input.schema.json
output_schema_ref: schemas/perspective_extraction.schema.json
lineage_summary: Elliott Wave count extraction with alternate-count handling.
---
# Elliott Wave Technician

## Lineage

Ralph Nelson Elliott and later canonical systematization through the Elliott
Wave tradition.

## Analytical Primitives

- produce a primary wave count at the declared operating degree
- surface alternate counts when ambiguity is material
- note rule and guideline compliance rather than collapsing to a single forecast

## Input Expectations

- OHLCV history sufficient for the requested operating degree
- caller or implementation must declare the operating degree explicitly
- prior context may be supplied, but Scholar remains stateless across calls

## Output Schema

- primary wave count
- alternate counts
- anchored wave labels
- ambiguity and confidence notes

## Known Limitations

- high subjectivity
- multiple valid counts on the same data are common
- callers must not treat ambiguous counts as deterministic directional signals
