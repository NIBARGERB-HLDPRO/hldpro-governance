import json
from pathlib import Path
from typing import Any

_PACKAGE_ROOT = Path(__file__).parent.parent


class PersonaLoader:
    """Load persona JSON files. Resolves process-agents/ first, then local, then personas/ shared."""

    def __init__(
        self,
        local_dir: Path | None = None,
        shared_dir: Path | None = None,
        process_agents_dir: Path | None = None,
    ):
        self.local_dir = local_dir
        self.shared_dir = shared_dir if shared_dir is not None else _PACKAGE_ROOT / "personas"
        self.process_agents_dir = (
            process_agents_dir if process_agents_dir is not None
            else _PACKAGE_ROOT / "process-agents"
        )

    def load(self, persona_id: str) -> dict[str, Any]:
        for search_dir in [self.process_agents_dir, self.local_dir, self.shared_dir]:
            if search_dir is None:
                continue
            candidate = Path(search_dir) / f"{persona_id}.json"
            if candidate.exists():
                return json.loads(candidate.read_text())
        raise FileNotFoundError(f"Persona '{persona_id}' not found in process-agents, local, or shared dirs")

    @classmethod
    def from_package(cls, local_dir: Path | None = None) -> "PersonaLoader":
        """Convenience: prefer process-agents/ with bundled personas/ fallback."""
        return cls(local_dir=local_dir, shared_dir=_PACKAGE_ROOT / "personas")
