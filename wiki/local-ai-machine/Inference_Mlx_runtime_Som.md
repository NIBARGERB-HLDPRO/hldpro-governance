# Inference Mlx runtime Som

> 60 nodes · cohesion 0.05

## Key Concepts

- **MLXRuntime** (10 connections) — `local-ai-machine/src/inference/mlx_runtime.py`
- **adapt_critic_output()** (9 connections) — `local-ai-machine/src/inference/mlx_runtime.py`
- **get_active_model_status()** (8 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/config.py`
- **_process_task()** (8 connections) — `local-ai-machine/services/som-worker/src/som_worker/daemon.py`
- **mlx_runtime.py** (7 connections) — `local-ai-machine/src/inference/mlx_runtime.py`
- **.critic()** (7 connections) — `local-ai-machine/src/inference/mlx_runtime.py`
- **generate()** (7 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/model_loader.py`
- **TestAdaptCriticOutput** (7 connections) — `local-ai-machine/tests/test_mlx_runtime.py`
- **get_active_model_id()** (5 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/config.py`
- **_get_config_path()** (5 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/config.py`
- **daemon.py** (5 connections) — `local-ai-machine/services/som-worker/src/som_worker/daemon.py`
- **_unload()** (5 connections) — `local-ai-machine/src/inference/mlx_runtime.py`
- **load_model()** (5 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/model_loader.py`
- **config.py** (4 connections) — `local-ai-machine/services/som-mcp/src/som_mcp/config.py`
- **test_mlx_runtime.py** (4 connections) — `local-ai-machine/tests/test_mlx_runtime.py`
- **_check_memory()** (4 connections) — `local-ai-machine/src/inference/mlx_runtime.py`
- **.executor()** (4 connections) — `local-ai-machine/src/inference/mlx_runtime.py`
- **._load_executor()** (4 connections) — `local-ai-machine/src/inference/mlx_runtime.py`
- **validate_runtime()** (4 connections) — `local-ai-machine/src/inference/mlx_runtime.py`
- **test_lam_config_env_override()** (4 connections) — `local-ai-machine/services/som-mcp/tests/test_config.py`
- **_clean_output()** (3 connections) — `local-ai-machine/services/som-worker/src/som_worker/daemon.py`
- **test_config.py** (3 connections) — `local-ai-machine/services/som-mcp/tests/test_config.py`
- **.__enter__()** (3 connections) — `local-ai-machine/src/inference/mlx_runtime.py`
- **.guardrail()** (3 connections) — `local-ai-machine/src/inference/mlx_runtime.py`
- **._unload_executor()** (3 connections) — `local-ai-machine/src/inference/mlx_runtime.py`
- *... and 35 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `local-ai-machine/services/som-mcp/src/som_mcp/config.py`
- `local-ai-machine/services/som-mcp/src/som_mcp/model_loader.py`
- `local-ai-machine/services/som-mcp/tests/test_config.py`
- `local-ai-machine/services/som-mcp/tests/test_server_config_startup.py`
- `local-ai-machine/services/som-worker/src/som_worker/daemon.py`
- `local-ai-machine/src/inference/mlx_runtime.py`
- `local-ai-machine/tests/test_mlx_runtime.py`

## Audit Trail

- EXTRACTED: 143 (76%)
- INFERRED: 46 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*