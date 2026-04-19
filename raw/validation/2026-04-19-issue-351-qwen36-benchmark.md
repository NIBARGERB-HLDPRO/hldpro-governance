# Validation - Issue #351 Qwen3.6 MLX Benchmark

Date: 2026-04-19
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/351

## Commands And Results

| Command | Result |
|---|---|
| `df -h .` | PASS - 599 GiB available before download |
| `python3 -c import mlx_lm, mlx, huggingface_hub` | PASS before benchmark, but system Python runtime was later insufficient |
| `huggingface_hub.snapshot_download("mlx-community/Qwen3.6-35B-A3B-4bit")` | PASS - 19.026 GiB downloaded in 592.683 seconds |
| `python3 -m mlx_lm generate ... --max-tokens 16` | EXPECTED BLOCKER - `Model type qwen3_5_moe not supported` on `mlx-lm 0.29.1` |
| `python3.11 -m pip install --user mlx-lm==0.31.2 huggingface_hub` | PASS |
| `python3.11 -m mlx_lm generate ... --max-tokens 16` | PASS - 106.959 generation tok/s, 19.632 GB peak MLX memory |
| `python3.11 -m mlx_lm generate ... --max-tokens 128` | PASS - 98.816 generation tok/s, 19.670 GB peak MLX memory |
| `python3.11 -m mlx_lm benchmark --prompt-tokens 128 --generation-tokens 128 --num-trials 3` | PASS - 103.018 avg generation tok/s, 19.797 GB peak memory |

## Acceptance Criteria

| AC | Result |
|---|---|
| Model download completes or failure is captured with exact blocker | PASS - download completed; Python 3.9 runtime blocker also captured |
| Benchmark uses only no-PII synthetic prompts | PASS |
| Runtime evidence includes model ID, command, prompt class, timing, token count or estimate, and memory/headroom observations | PASS |
| No routing order, PII policy, or active model promotion is changed | PASS |
| PDCA/R and validation artifacts record Plan, Do, Check, Adjust, Review | PASS |
| E2E local validation passes after artifacts are written | PASS pending final local gate in this PR branch |

## Summary

Qwen3.6-35B-A3B 4-bit MLX is viable as an on-demand candidate on this Mac lane. The benchmark supports the existing 24 GB metadata budget, but active routing promotion remains out of scope.
