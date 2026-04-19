# Local Model Runtime Runbook

## Current Mac Inventory

Verified on 2026-04-17 with `system_profiler SPHardwareDataType`:

- Machine: MacBook Pro
- Model identifier: Mac17,8
- Chip: Apple M5 Pro
- CPU cores: 18
- Unified memory: 48 GB

Runtime checks from the governance shell:

- `mlx_lm` Python package: importable
- `mlx_lm.server`: not required for this slice; `runtime_inventory.py` reports path when present
- `ollama` CLI on Mac: not present in this shell unless `runtime_inventory.py` reports otherwise

## Memory Budget

The Mac is the primary local runtime for PII, guardrails, and offline/bulk work.

| Lane | Model | Residency | Budget |
|---|---|---:|---:|
| Guardrail-LAM | `mlx-community/Qwen3-8B-4bit` | always resident | 4.67 GB |
| MCP intent | `mlx-community/Qwen3-1.7B-4bit` | warm, evictable | 1.5 GB |
| Worker-LAM | `mlx-community/Qwen3-14B-4bit` | on demand | 10 GB |
| Worker-LAM large | `mlx-community/Qwen3.6-35B-A3B-4bit` | on demand | 24 GB |
| Critic-LAM | `mlx-community/gemma-4-26b-a4b-4bit` | on demand | 18 GB |
| Qwen-Coder fallback | `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` | on demand | 6 GB |

Operating rule: keep guardrail resident, keep MCP intent warm when memory allows, and run only one large on-demand worker/critic model at a time. Unload on completion or memory pressure.

`mlx-community/Qwen3.6-35B-A3B-4bit` is the Mac-equivalent local entry for `Qwen/Qwen3.6-35B-A3B`. The BF16 MLX package is too large for this 48 GB lane, and the 8-bit package is too tight once guardrail and intent residency are considered. This entry is not always-warm and does not change PII routing authority.

## Health Probe

Run:

```bash
python3 scripts/lam/runtime_inventory.py
```

The probe:

- Reads Mac hardware metadata.
- Checks local runtime availability.
- Queries Windows Ollama metadata with `/api/tags` only.
- Loads local PII patterns and verifies a local email probe is detected.
- Does not send prompt payloads to Windows, cloud, or local model endpoints.

Write a report to a reviewed path:

```bash
python3 scripts/lam/runtime_inventory.py --output metrics/runtime-inventory/latest.json
```

## PII Boundary

- PII to cloud: never allowed.
- PII to Windows Ollama: never allowed.
- Missing or malformed PII patterns: halt.
- Local guardrail unavailable: halt for PII, architecture, and standards work.
- Clean implementation work may degrade only through the documented fallback ladder and fallback logging.

## No Authority Change

This runbook and probe do not grant autonomous write authority, packet dispatch authority, or model installation authority.
