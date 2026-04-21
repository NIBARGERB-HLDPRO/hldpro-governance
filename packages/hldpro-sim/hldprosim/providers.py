import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class BaseProvider(Protocol):
    def complete(self, system: str, user: str, outcome_schema: dict) -> dict: ...


class CodexCliProvider:
    """Subprocess-backed provider using codex exec --ephemeral."""

    def __init__(self, model: str = "gpt-5.4", effort: str = "medium"):
        self.model = model
        self.effort = effort

    def complete(self, system: str, user: str, outcome_schema: dict) -> dict:
        schema = dict(outcome_schema)
        schema["additionalProperties"] = False

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as sf:
            json.dump(schema, sf)
            schema_path = sf.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as of:
            output_path = of.name

        try:
            prompt = f"{system}\n\n{user}" if system else user
            result = subprocess.run(
                [
                    "codex",
                    "exec",
                    "--ephemeral",
                    "--skip-git-repo-check",
                    "--sandbox",
                    "read-only",
                    "-m",
                    self.model,
                    "-c",
                    f"model_reasoning_effort={self.effort}",
                    "--output-schema",
                    schema_path,
                    "-o",
                    output_path,
                    prompt,
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode != 0:
                raise RuntimeError(f"codex exec failed (exit {result.returncode}): {result.stderr[:400]}")

            output = Path(output_path).read_text().strip()
            if not output:
                raise RuntimeError("codex exec produced no output")
            return json.loads(output)
        finally:
            os.unlink(schema_path)
            try:
                os.unlink(output_path)
            except FileNotFoundError:
                pass


class AnthropicApiProvider:
    """Cloud stub — not implemented until API keys are provisioned."""

    def complete(self, system: str, user: str, outcome_schema: dict) -> dict:
        raise NotImplementedError("Cloud stub — set ANTHROPIC_API_KEY and implement")
