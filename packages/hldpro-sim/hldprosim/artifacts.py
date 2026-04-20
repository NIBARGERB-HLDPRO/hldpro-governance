import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class RunManifest:
    run_id: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    provider: str = ""
    model: str = ""
    persona_id: str = ""
    n_runs: int = 0
    schema_hash: str = ""
    git_commit: str = field(default_factory=lambda: _git_commit())


def _git_commit() -> str:
    try:
        return subprocess.check_output([
            "git",
            "rev-parse",
            "--short",
            "HEAD",
        ], text=True).strip()
    except Exception:
        return "unknown"


class ArtifactWriter:
    def __init__(self, base_dir: Path | str = Path("cache/sim-runs")):
        self.base_dir = Path(base_dir)

    def write(self, manifest: RunManifest, outcomes: list[dict]) -> Path:
        run_dir = self.base_dir / manifest.run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "run_manifest.json").write_text(json.dumps(asdict(manifest), indent=2))
        with open(run_dir / "outcomes.jsonl", "w") as f:
            for outcome in outcomes:
                f.write(json.dumps(outcome) + "\n")
        return run_dir
