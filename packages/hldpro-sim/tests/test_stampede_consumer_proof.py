import json
import tempfile

from pathlib import Path

from hldprosim.artifacts import ArtifactWriter, RunManifest
from hldprosim.engine import SimulationEngine
from hldprosim.personas import PersonaLoader
from hldprosim.runner import Runner
from tests.fixtures.stampede_consumer import NarrativeAggregator


MOCK_OUTCOME = {
    "persona_id": "trader-momentum",
    "action_type": "sell",
    "confidence": 0.78,
    "narrative_rationale": "Earnings miss triggers momentum reversal.",
    "key_catalysts": ["earnings miss", "macro headwinds"],
    "risk_flags": ["high beta", "short squeeze risk"],
}

NARRATIVE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "persona_id": {"type": "string"},
        "action_type": {"type": "string"},
        "confidence": {"type": "number"},
        "narrative_rationale": {"type": "string"},
        "key_catalysts": {"type": "array", "items": {"type": "string"}},
        "risk_flags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["persona_id", "action_type", "confidence", "narrative_rationale", "key_catalysts", "risk_flags"],
}


class MockProvider:
    def complete(self, system, user, schema):
        return dict(MOCK_OUTCOME)


def test_stampede_e2e():
    personas_dir = Path(__file__).parent.parent / "personas"
    loader = PersonaLoader(shared_dir=personas_dir)
    engine = SimulationEngine(
        provider=MockProvider(),
        persona_loader=loader,
        prompt_template=lambda event, persona: ("You are a trader.", f"Event: {event}. Persona: {persona['name']}"),
        outcome_schema=NARRATIVE_SCHEMA,
    )
    runner = Runner()
    outcomes = runner.run_n(engine, {"headline": "Tesla Q1 miss 15%"}, "trader-momentum", n=3)
    assert len(outcomes) == 3

    agg = NarrativeAggregator()
    result = agg.aggregate(outcomes)
    assert "sentiment_distribution" in result
    assert "top_catalysts" in result
    assert result["avg_confidence"] > 0

    with tempfile.TemporaryDirectory() as tmp:
        writer = ArtifactWriter(base_dir=Path(tmp))
        manifest = RunManifest(run_id="test-001", persona_id="trader-momentum", n_runs=3)
        run_dir = writer.write(manifest, outcomes)
        assert (run_dir / "run_manifest.json").exists()
        assert (run_dir / "outcomes.jsonl").exists()
        lines = (run_dir / "outcomes.jsonl").read_text().strip().split("\n")
        assert len(lines) == 3
