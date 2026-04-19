# Issue #351 - Qwen3.6-35B-A3B MLX Benchmark PDCA/R

## Plan

Download and benchmark `mlx-community/Qwen3.6-35B-A3B-4bit` on the Mac M5 Pro local MLX lane without promoting it into active routing.

Acceptance criteria from issue #351:

- Model download completes or exact blocker is captured.
- Benchmark uses only no-PII synthetic prompts.
- Runtime evidence includes model ID, command, prompt class, timing, token count or estimate, and memory/headroom observations.
- No routing order, PII policy, or active model promotion is changed.
- PDCA/R and validation artifacts record Plan, Do, Check, Adjust, and Review.
- E2E local validation passes after artifacts are written.

## Do

- Created issue #351 as the issue-backed follow-up to #347.
- Downloaded `mlx-community/Qwen3.6-35B-A3B-4bit` through `huggingface_hub.snapshot_download`.
- Ran the first smoke probe with system `python3` and captured the `qwen3_5_moe` unsupported-runtime blocker.
- Installed the benchmark runtime on Homebrew Python 3.11 with `mlx-lm==0.31.2`, `mlx==0.31.1`, and `huggingface_hub==1.11.0`.
- Reran no-PII smoke generation and a no-PII coding prompt.
- Ran the built-in `mlx_lm benchmark` with 128 prompt tokens, 128 generation tokens, and 3 trials.
- Recorded metrics and validation evidence under `metrics/runtime-benchmarks/` and `raw/validation/`.

## Check

| Check | Result |
|---|---|
| Download `mlx-community/Qwen3.6-35B-A3B-4bit` | PASS - 17 files, 19.026 GiB, 592.683 seconds |
| System Python 3.9 smoke generation | EXPECTED BLOCKER - `mlx-lm 0.29.1` does not support `model_type=qwen3_5_moe` |
| Python 3.11 runtime install | PASS - installed `mlx-lm 0.31.2`, `mlx 0.31.1`, `huggingface_hub 1.11.0` |
| Python 3.11 smoke generation, 16 tokens | PASS - 106.959 generation tok/s, 19.632 GB peak MLX memory |
| Python 3.11 no-PII coding prompt, 128 tokens | PASS - 98.816 generation tok/s, 19.670 GB peak MLX memory |
| `mlx_lm benchmark`, 128/128, 3 trials | PASS - avg prompt 654.101 tok/s, avg generation 103.018 tok/s, 19.797 GB peak MLX memory |
| PII/routing policy | PASS - no routing-order, cloud fallback, Windows placement, or PII policy changes |

## Adjust

The 24 GB roster budget from #347 remains acceptable for the Mac M5 Pro 48 GB lane. The benchmark showed peak MLX memory below 20 GB on 128/128 synthetic runs. The practical adjustment is operational: Qwen3.6 requires the Python 3.11 MLX stack with `mlx-lm >= 0.31.2`; the existing system Python 3.9 `mlx-lm 0.29.1` fails before load because `qwen3_5_moe` is unsupported there.

## Review

Review status is local benchmark validation plus repo gates. This slice does not promote the model into active routing and does not modify `STANDARDS.md`, so architecture/standards cross-review is not required.
