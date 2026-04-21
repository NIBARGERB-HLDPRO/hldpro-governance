# Stage 6 Closeout
Date: 2026-04-20
Repo: Stampede
Task ID: Stampede GitHub issue #76
Six-Stage Cycle: Stage 6 / Audit + Closeout
Completed By: Benji

## Decision Made
Implemented `AnthropicApiProvider` with `temperature=0.0` + `max_tokens=1024` and wired a `--provider anthropic` flag into `run_slice6_simulation.py`; seed stability re-run confirmed mean std dev collapsed from 28.9 bps to 4.6 bps with 0 direction-unstable events.

## Pattern Identified
Sampling variance from non-zero temperature dominated prediction noise for weak-signal events. Setting `temperature=0` is now standard for all Stampede Phase 0 production inference paths; `ClaudeCliProvider` follows the same convention via `--temperature 0` in its subprocess invocation.

## Contradicts Existing
None. Extends `hldpro-sim` provider contract — all providers must now support deterministic (temperature=0) mode for bakeoff comparability.

## Files Changed
- `hldpro-sim/hldprosim/providers.py` — `AnthropicApiProvider.complete()` added with `temperature=0, max_tokens=1024`
- `scripts/run_slice6_simulation.py` — `--provider [codex|anthropic|claude-cli]` flag added; `AnthropicApiProvider` wired as production path

## Issue Links
- Stampede issue [#76](https://github.com/NIBARGERB-HLDPRO/Stampede/issues/76) — CLOSED
- Stampede issue [#64](https://github.com/NIBARGERB-HLDPRO/Stampede/issues/64) — CLOSED (seed stability baseline, predecessor to #76)
- Stampede issue [#78](https://github.com/NIBARGERB-HLDPRO/Stampede/issues/78) — OPEN (live forward validation; unblocked by #76)

## Schema / Artifact Version
- `hldprosim` provider protocol: `BaseProvider.complete(system, user, outcome_schema) -> dict`
- Model output schema: `schemas/model_output_v0_1.schema.json`

## Model Identity
- Production inference: `claude-sonnet-4-6` via `AnthropicApiProvider`, `temperature=0.0`, `max_tokens=1024`
- Dispatch / planning: Claude Sonnet 4.6 (`claude-sonnet-4-6`)

## Review And Gate Identity
- No formal cross-review required (implementation-only slice, not an architecture or standards change)
- Acceptance criteria validated by seed stability re-run (3 seeds × 13 events): mean std dev = 4.6 bps, direction-unstable events = 0

## Wired Checks Run
- `python scripts/run_slice6_simulation.py --provider anthropic --allow-model-calls` (fixture-safe path via FixtureProvider confirmed; live path confirmed with AnthropicApiProvider)
- Seed stability re-run: 3-seed sweep over all 13 candidate events, results logged to `cache/sim-runs/`
- `python -m py_compile hldpro-sim/hldprosim/providers.py` — PASS

## Execution Scope / Write Boundary
- Work performed in Stampede repo worktree on branch `issue-76-temperature-determinism-*`
- Governance repo unchanged by this slice (no governance surface writes)

## Validation Commands
- Seed stability re-run: PASS (mean std dev 4.6 bps, 0 direction-unstable)
- `run_slice6_simulation.py --provider anthropic` CLI flag: PASS
- `AnthropicApiProvider` schema validation: PASS

## Tier Evidence Used
- Not applicable (no architecture or standards scope).

## Residual Risks / Follow-Up
- `ClaudeCliProvider` temperature pin relies on subprocess flag rather than API parameter — lower enforcement confidence; tracked as a known divergence, not an active risk for Phase 0.
- Forward validation (issue #78) is the first live consumer of this determinism guarantee.

## Wiki Pages Updated
- None created; Stampede graph (363 nodes, 555 edges, 59 communities) already committed to `graphify-out/stampede/` and `wiki/stampede/` in governance HEAD as of 2026-04-20.

## operator_context Written
[ ] No — governance-level Stampede closeouts do not currently write operator_context rows; Stampede is tracked as an experimental repo outside the operator_context write boundary.

## Links To
- [Society of Minds Model Routing Charter](../../wiki/decisions/2026-04-14-society-of-minds-charter.md)
- Stampede graphify summary: `wiki/stampede/`
