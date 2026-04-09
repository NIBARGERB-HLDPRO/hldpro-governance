# Issue #43 — Effectiveness Engine Baseline Metrics PDCA/R

## Plan
- verify what the weekly sweep already computes live
- replace report-only metrics with a reproducible governance-hosted baseline in `metrics/effectiveness-baseline/`
- keep the implementation deterministic and avoid creating a second audit path

## Do
- add `scripts/overlord/build_effectiveness_metrics.py`
- seed the first dated baseline snapshot plus `latest.*`
- wire the weekly sweep to refresh the stored metrics artifacts

## Check
- run the metrics builder locally against the current governed repos
- verify JSON and markdown snapshots are written consistently
- verify the weekly sweep stages the metrics artifacts for commit

## Adjust
- if another repo-specific metric turns out to be too noisy or conditional for baseline use, keep it out of the first stored baseline and record it as follow-up instead of forcing it into the current slice

## Review
- issue `#43` is complete when bug rate, revert rate, and CI pass rate are reproducibly stored in governance and refreshed by the sweep
- any further metric expansion should be opened as a separate issue instead of bloating the baseline slice
