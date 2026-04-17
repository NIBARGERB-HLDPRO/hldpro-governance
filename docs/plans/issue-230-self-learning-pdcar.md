# Issue #230 — Self-Learning and Self-Healing Loop PDCA/R

## Plan

Issue #230 makes documented mistakes available before packet dispatch. The implementation must cite direct evidence paths, halt repeated known failures, capture novel failures append-only, and surface stale or duplicate learning entries in the weekly sweep.

## Do

- Added `scripts/orchestrator/self_learning.py`.
- Added `scripts/orchestrator/test_self_learning.py`.
- Extended packet governance metadata with optional `known_failure_context`.
- Updated `scripts/orchestrator/packet_queue.py` to halt repeated known failures.
- Added weekly self-learning report generation to `overlord-sweep.yml`.
- Extended governance-surface classification for self-learning outputs.
- Updated registries and data dictionary.

## Check

Planned validation:

- `python3 scripts/orchestrator/test_self_learning.py`
- `python3 scripts/orchestrator/test_packet_queue.py`
- `python3 scripts/packet/test_validate.py`
- `python3 scripts/overlord/test_validate_structured_agent_cycle_plan.py`
- `python3 scripts/orchestrator/self_learning.py report --output-json metrics/self-learning/latest.json --output-md metrics/self-learning/latest.md`
- governance-surface changed-file validation with `--enforce-governance-surface`
- issue-branch plan validation with `--require-if-issue-branch`
- py_compile, model pin checks, graphify contract, and compendium freshness check

## Adjust

The learning loop stays deterministic and local. Graphify and compendium text contribute attention tokens, while injected packet context cites direct files such as fail-fast logs, error patterns, closeouts, and operator-context records.

## Review

Alternate-family review is recorded in `raw/cross-review/2026-04-17-self-learning.md`.
