from pydantic import BaseModel

from hldprosim.aggregator import BaseAggregator


class ScholarExtraction(BaseModel):
    perspective_id: str
    extraction_type: str
    identified_structures: list[str]
    caveats: list[str]


class ScholarOutcome(BaseModel):
    persona_id: str
    capability_id: str
    contract_version: str
    selected_perspectives: list[str]
    technical_summary: str
    perspective_extractions: list[ScholarExtraction]
    input_quality_flags: list[str]


class ScholarAggregator(BaseAggregator):
    def aggregate(self, outcomes: list[dict]) -> dict:
        parsed = [ScholarOutcome(**outcome) for outcome in outcomes]
        unique_perspectives = sorted(
            {
                perspective_id
                for outcome in parsed
                for perspective_id in outcome.selected_perspectives
            }
        )
        all_flags = sorted(
            {
                flag
                for outcome in parsed
                for flag in outcome.input_quality_flags
            }
        )
        return {
            "run_count": len(parsed),
            "perspective_count": len(unique_perspectives),
            "selected_perspectives": unique_perspectives,
            "input_quality_flags": all_flags,
        }
