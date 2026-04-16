# Issue 76 PDCA/R — Cited Code Path Validation

Date: 2026-04-09
Issue: [#76](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/76)
Owner: nibargerb

## Plan

- make `validate_location()` read code context around the cited line
- reject findings whose cited line does not match strong claim anchors
- add a regression test for hallucinated-line rejection

## Do

- added strong-anchor extraction for identifiers and backticked code terms
- read a small context window around the cited line during qualification
- reject drifted findings when the cited code window does not contain the claim anchors
- added unittest coverage for both rejection and acceptance paths

## Check

Verification target:
- qualification rejects a valid-file/valid-line finding whose cited code does not match the claim
- valid cited identifiers still qualify
- the helper remains bounded and does not attempt full semantic review

## Adjust

If review shows more semantic validation is needed than a strong-anchor check can safely provide, create a follow-up issue rather than overloading this helper.

## Review

This closes the most obvious qualification trust gap: a finding can no longer survive solely because it points at a real file and in-range line. When the claim names concrete code anchors, the cited line now has to match them.
