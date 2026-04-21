# Qwen-Coder MLX Driver — Runbook

Version: 2026-04-21
Worker tier: local bounded micro-worker

## When to use
- Issue-backed execution scope explicitly routes a tiny local implementation chunk to Qwen-Coder.
- Task can tolerate <=10-15s per file of latency.
- Output fits within model's reliable ceiling (see limits below).
- Downstream Codex QA and deterministic gate remain required.

Do not use this model for planning, authoritative review, gate verification, security-sensitive code, broad refactors, or unbounded full-file rewrites.

## Model
- `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` (~4.5 GB RAM peak)
- MLX runtime, Apple Silicon only

## Driver location
`/tmp/qwen-coder-mlx-driver.py` — create from template if absent
(Template lives alongside `/tmp/stage2-driver-v2.py`, shares pattern)

## Invocation
`python3 /tmp/qwen-coder-mlx-driver.py <tasks.json> [audit_dir]`

Task JSON shape:
```json
[{"slug": "...", "target_file": "abs/path", "system_prompt": "...", "user_prompt": "...", "max_tokens": 2000}]
```

## Known limitations (2026-04-14)

### Full-file regeneration of >200 lines is unreliable
Model emits stubs with `# Existing logic...` placeholders instead of complete file contents. Bug tracked in issue [#105](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/105).

**Workarounds:**
1. Break full-file tasks into smaller per-function prompts (each <150 lines output)
2. Use unified-diff format: provide current file inline + diff patch, ask model to apply and emit final
3. Raise `max_tokens` to 4000-6000 and retry (partially effective)
4. If all else fails: escalate intentionally to `mlx-community/Qwen3-14B-4bit`, `mlx-community/Qwen3.6-35B-A3B-4bit`, or `claude-sonnet-4-6` based on the approved execution scope.

### Tokenizer artifacts
Model sometimes appends `<|im_end|>` or leaves code fences in output. Driver includes a cleanup pass, but verify before writing to disk.

### Cold load is slow
First call takes ~50s (model load). Keep-warm across multiple tasks saves time — driver loads once per invocation, so batch all pending tasks into a single JSON list.

## Always-warm pattern (future)

Planned `services/som-worker/` daemon (Stage 5+ architecture) may keep Qwen-Coder loaded continuously for bounded local-worker packets. The current waterfall remains: Codex orchestrates, Opus plans, GPT-5.4 high reviews plans, Sonnet or bounded local Qwen workers implement, Codex QA reviews, and deterministic gates verify. See backlog entry.

## Memory interaction
- Qwen-Coder (4.5 GB) + M7 always-resident (4.67 GB) = 9.2 GB baseline
- Leaves headroom for M4 (8.37 GB on-demand) but NOT M6 (14.54 GB) — Qwen-Coder must evict before M6 loads
- Eviction protocol: same `_unload()` pattern as MLXRuntime

## Troubleshooting
- Driver hangs at load: check MLX Metal device (`python -c "import mlx.core as mx; print(mx.default_device())"`)
- Output truncated: raise max_tokens; split task
- Bad JSON in task file: validate with `python -m json.tool`
- Memory pressure: check `mx.get_active_memory() / 1e9` before load; must be < 4 GB free
