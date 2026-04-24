import json
import tempfile

from pathlib import Path

from hldprosim.artifacts import ArtifactWriter, RunManifest
from hldprosim.engine import SimulationEngine
from hldprosim.personas import PersonaLoader
from hldprosim.runner import Runner
from hldprosim.scholar import ScholarLoader
from tests.fixtures.stampede_consumer import NarrativeAggregator
from tests.fixtures.scholar_consumer import ScholarAggregator


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

SCHOLAR_OUTCOME = {
    "persona_id": "scholar-technical-analyst",
    "capability_id": "scholar",
    "contract_version": "0.1.0",
    "selected_perspectives": ["dow_theorist", "momentum_indicator_technician"],
    "technical_summary": "Trend remains up, but momentum shows bearish divergence.",
    "perspective_extractions": [
        {
            "perspective_id": "dow_theorist",
            "extraction_type": "trend_structure",
            "identified_structures": ["primary uptrend", "secondary pullback"],
            "caveats": ["no comparator instrument provided"],
        },
        {
            "perspective_id": "momentum_indicator_technician",
            "extraction_type": "indicator_signal",
            "identified_structures": ["bearish RSI divergence"],
            "caveats": ["warm-up history near minimum"],
        },
    ],
    "input_quality_flags": ["limited_comparator_context"],
}

SCHOLAR_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "persona_id": {"type": "string"},
        "capability_id": {"type": "string"},
        "contract_version": {"type": "string"},
        "selected_perspectives": {"type": "array", "items": {"type": "string"}},
        "technical_summary": {"type": "string"},
        "perspective_extractions": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "perspective_id": {"type": "string"},
                    "extraction_type": {"type": "string"},
                    "identified_structures": {"type": "array", "items": {"type": "string"}},
                    "caveats": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["perspective_id", "extraction_type", "identified_structures", "caveats"]
            }
        },
        "input_quality_flags": {"type": "array", "items": {"type": "string"}}
    },
    "required": [
        "persona_id",
        "capability_id",
        "contract_version",
        "selected_perspectives",
        "technical_summary",
        "perspective_extractions",
        "input_quality_flags"
    ]
}


class MockProvider:
    def complete(self, system, user, schema):
        if schema == SCHOLAR_SCHEMA:
            return dict(SCHOLAR_OUTCOME)
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


def test_scholar_consumer_proof():
    loader = PersonaLoader.from_package()
    scholar = ScholarLoader.from_package().load()
    invocation_context = scholar.build_invocation_context(
        perspective_ids=["dow_theorist", "momentum_indicator_technician"]
    )

    engine = SimulationEngine(
        provider=MockProvider(),
        persona_loader=loader,
        prompt_template=lambda event, persona: (
            "You are Scholar, a technical-analysis specialty agent.",
            (
                f"Event: {event}. Persona: {persona['name']}. "
                f"Capability: {invocation_context['capability_id']} "
                f"v{invocation_context['version']}. "
                f"Perspectives: {[p['id'] for p in invocation_context['selected_perspectives']]}."
            ),
        ),
        outcome_schema=SCHOLAR_SCHEMA,
    )
    runner = Runner()
    outcomes = runner.run_n(
        engine,
        {"ticker": "AAPL", "headline": "Apple trends higher on mixed breadth"},
        "scholar-technical-analyst",
        n=2,
    )

    agg = ScholarAggregator()
    result = agg.aggregate(outcomes)
    assert result["run_count"] == 2
    assert result["perspective_count"] == 2
    assert result["selected_perspectives"] == [
        "dow_theorist",
        "momentum_indicator_technician",
    ]

    with tempfile.TemporaryDirectory() as tmp:
        writer = ArtifactWriter(base_dir=Path(tmp))
        manifest = RunManifest(
            run_id="scholar-test-001",
            persona_id="scholar-technical-analyst",
            n_runs=2,
        )
        run_dir = writer.write(manifest, outcomes)
        assert (run_dir / "run_manifest.json").exists()
        assert (run_dir / "outcomes.jsonl").exists()
