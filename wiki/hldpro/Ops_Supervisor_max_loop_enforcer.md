# Ops Supervisor max loop enforcer

> 19 nodes · cohesion 0.16

## Key Concepts

- **main()** (12 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/test_supervisor_max_loop_runtime.py`
- **SupervisorMaxLoopEnforcer** (8 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **parse_agent_max_loops()** (6 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **.record_invocation()** (6 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **discover_agents()** (5 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **.manifest()** (4 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **.write_manifest()** (4 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **supervisor_max_loop_enforcer.py** (3 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **.can_invoke()** (3 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **test_supervisor_max_loop_runtime.py** (2 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/test_supervisor_max_loop_runtime.py`
- **.__init__()** (2 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **check()** (2 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/test_supervisor_max_loop_runtime.py`
- **Extract max-loops value from agent YAML frontmatter.** (1 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **Discover all agents with max-loops declarations.      Returns a dict keyed by ag** (1 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **Tracks agent invocations and enforces max-loops at runtime.** (1 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **Check if an agent is allowed another invocation.** (1 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **Record an agent invocation. Raises if max-loops exceeded.** (1 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **Return the full invocation manifest for artifact emission.** (1 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- **Write the invocation manifest to a JSON file.** (1 connections) — `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `hldpro-governance/repos/local-ai-machine/scripts/ops/supervisor_max_loop_enforcer.py`
- `hldpro-governance/repos/local-ai-machine/scripts/ops/test_supervisor_max_loop_runtime.py`

## Audit Trail

- EXTRACTED: 42 (66%)
- INFERRED: 22 (34%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*