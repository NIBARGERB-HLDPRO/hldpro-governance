from typing import Any, Callable

from .personas import PersonaLoader
from .providers import BaseProvider


class SimulationEngine:
    def __init__(
        self,
        provider: BaseProvider,
        persona_loader: PersonaLoader,
        prompt_template: Callable[[dict, dict], tuple[str, str]],
        outcome_schema: dict,
    ):
        self.provider = provider
        self.persona_loader = persona_loader
        self.prompt_template = prompt_template
        self.outcome_schema = outcome_schema

    def run(self, event: dict, persona_id: str) -> dict:
        persona = self.persona_loader.load(persona_id)
        system, user = self.prompt_template(event, persona)
        result = self.provider.complete(system, user, self.outcome_schema)
        return result
