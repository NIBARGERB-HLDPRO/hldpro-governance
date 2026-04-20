from hldprosim.engine import SimulationEngine
from hldprosim.personas import PersonaLoader


def test_engine_passes_template_results_to_provider():
    outcome = {
        "persona_id": "trader-momentum",
        "result": "sell",
    }

    provider = type("MockProvider", (), {"complete": lambda self, system, user, schema: dict(outcome)})()
    persona_loader = PersonaLoader(local_dir=None, shared_dir=None)
    persona_loader.load = lambda _: {"name": "Trader Momentum"}

    engine = SimulationEngine(
        provider=provider,
        persona_loader=persona_loader,
        prompt_template=lambda event, persona: ("System prompt", f"Event: {event}. Persona: {persona['name']}"),
        outcome_schema={"type": "object"},
    )

    result = engine.run({"headline": "AAPL beats"}, "trader-momentum")
    assert result == outcome
