# Issue 65 PDCA/R — Graphify Adoption And Measurement

Date: 2026-04-09
Issue: [#65](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/65)
Owner: nibargerb

## Plan

- build a deterministic graphify-vs-baseline retrieval harness using real fail-fast scenarios
- add an auditable append-only graphify usage-event path
- persist quality and token-footprint estimates in tracked governance metrics

## Do

- defined a scenario corpus from the live fail-fast issues
- built a local measurement harness for graphify-guided retrieval vs baseline repo search
- added a JSONL event logger and schema for graphify usage events
- persisted tracked metrics and a Markdown summary under `metrics/graphify-evals/`

## Check

Verification target:
- at least one repeatable graphify-vs-baseline run exists on real governance scenarios
- usage logging has a documented path and append-only event file
- measured results are tracked in governance and can inform issue #66

## Adjust

If the harness shows graphify underperforming baseline retrieval on the fail-fast corpus, keep issue #66 as the quality-improvement follow-up rather than burying the gap.

## Review

This slice does not claim graphify is already better. It closes the instrumentation and repeatability gap so graphify usage, quality, and estimated token footprint can be measured instead of assumed.
