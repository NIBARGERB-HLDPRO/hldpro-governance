# PersonaLoader

> God node · 18 connections · `stampede/hldpro-sim/hldprosim/personas.py`

## Connections by Relation

### calls
- [[cmd_predict()]] `INFERRED`
- [[test_stampede_e2e()]] `INFERRED`
- [[run_simulation()]] `INFERRED`
- [[test_engine_passes_template_results_to_provider()]] `INFERRED`
- [[test_persona_loader_prefers_local_file()]] `INFERRED`
- [[test_persona_loader_falls_back_to_shared_file()]] `INFERRED`
- [[test_persona_loader_raises_when_missing()]] `INFERRED`

### contains
- [[personas.py]] `EXTRACTED`

### method
- [[.load()]] `EXTRACTED`
- [[.__init__()]] `EXTRACTED`

### rationale_for
- [[Load persona JSON files. Resolves local-first, shared fallback.]] `EXTRACTED`

### uses
- [[SimulationEngine]] `INFERRED`
- [[StampedeAggregator]] `INFERRED`
- [[FixtureProvider]] `INFERRED`
- [[MockProvider]] `INFERRED`
- [[SimpleAggregator]] `INFERRED`
- [[Slice 6 fixture-safe simulation runner for hldpro-sim Phase 0 bakeoff.]] `INFERRED`
- [[Live forward validation runner for Stampede Phase 0, issue #78.]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*