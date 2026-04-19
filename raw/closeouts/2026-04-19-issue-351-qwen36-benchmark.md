# Stage 6 Closeout
Date: 2026-04-19
Repo: hldpro-governance
Task ID: GitHub issue #351
Six-Stage Cycle: Stage 6 / Audit + Closeout
Completed By: Codex

## Decision Made
`mlx-community/Qwen3.6-35B-A3B-4bit` downloaded and benchmarked successfully on the Mac M5 Pro 48 GB lane using Python 3.11 with `mlx-lm 0.31.2`; it remains an on-demand candidate only.

## Pattern Identified
New MLX MoE models need a runtime-version probe in addition to a model-size/memory probe; older MLX-LM releases can fail before memory pressure appears.

## Contradicts Existing
No contradiction. This validates the #347 24 GB candidate budget and adds the operational requirement to use the Python 3.11 MLX runtime for Qwen3.6.

## Files Changed
- `docs/plans/issue-351-qwen36-benchmark-pdcar.md`
- `docs/plans/issue-351-structured-agent-cycle-plan.json`
- `metrics/runtime-benchmarks/2026-04-19-qwen36-35b-a3b-mlx.json`
- `metrics/runtime-benchmarks/2026-04-19-qwen36-35b-a3b-mlx.md`
- `raw/execution-scopes/2026-04-19-issue-351-qwen36-benchmark-implementation.json`
- `raw/validation/2026-04-19-issue-351-qwen36-benchmark.md`
- `OVERLORD_BACKLOG.md`
- `docs/PROGRESS.md`

## Issue Links
- Parent epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/224
- Roster issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/347
- Benchmark issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/351
- Source model: https://huggingface.co/Qwen/Qwen3.6-35B-A3B
- MLX model package: https://huggingface.co/mlx-community/Qwen3.6-35B-A3B-4bit

## Schema / Artifact Version
Structured agent cycle plan schema: `docs/schemas/structured-agent-cycle-plan.schema.json`.
Runtime benchmark evidence stored as JSON and Markdown under `metrics/runtime-benchmarks/`.

## Model Identity
- Planner/implementer: Codex, `gpt-5.4`, OpenAI, reasoning effort medium in this session.
- Benchmark runtime: Python 3.11, `mlx-lm 0.31.2`, `mlx 0.31.1`.
- Blocked runtime: system Python 3.9, `mlx-lm 0.29.1`.

## Review And Gate Identity
Review is local validation and GitHub CI for the benchmark evidence PR. No architecture/standards cross-review is required because no routing, PII, or `STANDARDS.md` policy changed.

## Wired Checks Run
- Model download.
- Python 3.9 negative-control smoke generation.
- Python 3.11 smoke generation.
- Python 3.11 no-PII coding generation.
- Built-in `mlx_lm benchmark`.
- Structured plan validator.
- Execution-scope assertion.
- Local CI Gate.
- Stage 6 closeout hook.

## Execution Scope / Write Boundary
Execution scope: `raw/execution-scopes/2026-04-19-issue-351-qwen36-benchmark-implementation.json`.

## Validation Commands
- `huggingface_hub.snapshot_download("mlx-community/Qwen3.6-35B-A3B-4bit")` - PASS
- `python3 -m mlx_lm generate --model <snapshot> --max-tokens 16` - EXPECTED BLOCKER
- `python3.11 -m pip install --user mlx-lm==0.31.2 huggingface_hub` - PASS
- `python3.11 -m mlx_lm generate --model <snapshot> --max-tokens 16` - PASS
- `python3.11 -m mlx_lm generate --model <snapshot> --max-tokens 128` - PASS
- `python3.11 -m mlx_lm benchmark --model <snapshot> --prompt-tokens 128 --generation-tokens 128 --num-trials 3` - PASS
- `tools/local-ci-gate/bin/hldpro-local-ci --profile hldpro-governance --json` - PASS
- `hooks/closeout-hook.sh raw/closeouts/2026-04-19-issue-351-qwen36-benchmark.md` - PASS

## Tier Evidence Used
No architecture/standards cross-review artifact required. This benchmark does not change routing order, fallback authority, PII policy, or `STANDARDS.md`.

## Residual Risks / Follow-Up
Active routing promotion remains out of scope. Open a separate promotion issue if Qwen3.6 should become an active Worker-LAM lane.

## Wiki Pages Updated
Stage 6 graph/wiki artifacts should refresh `wiki/hldpro/` through the closeout hook.

## operator_context Written
[ ] Yes - row ID: N/A
[x] No - reason: Benchmark evidence is recorded in repository metrics, validation, and issue artifacts.

## Links To
- `metrics/runtime-benchmarks/2026-04-19-qwen36-35b-a3b-mlx.md`
- `raw/validation/2026-04-19-issue-351-qwen36-benchmark.md`
