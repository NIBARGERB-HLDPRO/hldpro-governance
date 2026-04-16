# Ops Supervisor max loop enforcer

> 19 nodes · cohesion 0.13

## Key Concepts

- **SupervisorMaxLoopEnforcer** (7 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **supervisor_max_loop_enforcer.py** (4 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **discover_agents()** (4 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **parse_agent_max_loops()** (3 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **.manifest()** (3 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **.write_manifest()** (3 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **test_supervisor_max_loop_runtime.py** (3 connections) — `local-ai-machine/scripts/ops/test_supervisor_max_loop_runtime.py`
- **.can_invoke()** (2 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **.__init__()** (2 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **.record_invocation()** (2 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **check()** (2 connections) — `local-ai-machine/scripts/ops/test_supervisor_max_loop_runtime.py`
- **main()** (2 connections) — `local-ai-machine/scripts/ops/test_supervisor_max_loop_runtime.py`
- **Extract max-loops value from agent YAML frontmatter.** (1 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **Discover all agents with max-loops declarations.      Returns a dict keyed by ag** (1 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **Tracks agent invocations and enforces max-loops at runtime.** (1 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **Check if an agent is allowed another invocation.** (1 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **Record an agent invocation. Raises if max-loops exceeded.** (1 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **Return the full invocation manifest for artifact emission.** (1 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **Write the invocation manifest to a JSON file.** (1 connections) — `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- `local-ai-machine/scripts/ops/test_supervisor_max_loop_runtime.py`

## Audit Trail

- EXTRACTED: 36 (82%)
- INFERRED: 8 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*