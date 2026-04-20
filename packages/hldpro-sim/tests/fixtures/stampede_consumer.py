from collections import Counter

from hldprosim.aggregator import BaseAggregator
from pydantic import BaseModel
from typing import Literal


class NarrativeOutcome(BaseModel):
    persona_id: str
    action_type: Literal["buy", "sell", "hold", "rebalance"]
    confidence: float
    narrative_rationale: str
    key_catalysts: list[str]
    risk_flags: list[str]


class NarrativeAggregator(BaseAggregator):
    def aggregate(self, outcomes: list[dict]) -> dict:
        parsed = [NarrativeOutcome(**o) for o in outcomes]
        action_counts = Counter(o.action_type for o in parsed)
        all_catalysts = [c for o in parsed for c in o.key_catalysts]
        top_catalysts = [c for c, _ in Counter(all_catalysts).most_common(5)]
        avg_confidence = sum(o.confidence for o in parsed) / len(parsed) if parsed else 0.0
        return {
            "sentiment_distribution": dict(action_counts),
            "top_catalysts": top_catalysts,
            "avg_confidence": round(avg_confidence, 3),
        }
