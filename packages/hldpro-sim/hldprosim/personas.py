import json
from pathlib import Path
from typing import Any


class PersonaLoader:
    """Load persona JSON files. Resolves local-first, shared fallback."""

    def __init__(self, local_dir: Path | None = None, shared_dir: Path | None = None):
        self.local_dir = local_dir
        self.shared_dir = shared_dir

    def load(self, persona_id: str) -> dict[str, Any]:
        for search_dir in [self.local_dir, self.shared_dir]:
            if search_dir is None:
                continue
            candidate = Path(search_dir) / f"{persona_id}.json"
            if candidate.exists():
                return json.loads(candidate.read_text())
        raise FileNotFoundError(f"Persona '{persona_id}' not found in local or shared dirs")

    @classmethod
    def from_package(cls, local_dir: Path | None = None) -> "PersonaLoader":
        """Convenience: load shared dir from bundled package personas/."""
        shared = Path(__file__).parent.parent / "personas"
        return cls(local_dir=local_dir, shared_dir=shared)
