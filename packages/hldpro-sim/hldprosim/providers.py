import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


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
    """Anthropic API provider with extended thinking + strict JSON schema enforcement."""

    def __init__(self, model: str = "claude-sonnet-4-6", thinking_budget_tokens: int = 2048):
        self.model = model
        self.thinking_budget_tokens = thinking_budget_tokens
        self._api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self._api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required but not set")
        self._client: Any | None = None

    def _require_api_key(self) -> str:
        if not self._api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required but not set")
        return self._api_key

    def _strict_schema(self, outcome_schema: dict) -> dict:
        schema = dict(outcome_schema)
        schema.setdefault("type", "object")
        schema["additionalProperties"] = False
        return schema

    def _get_client(self) -> Any:
        self._require_api_key()
        if self._client is not None:
            return self._client

        try:
            from anthropic import Anthropic
        except ImportError as err:
            raise RuntimeError(
                "AnthropicApiProvider requires the optional 'anthropic' package to execute completions"
            ) from err

        self._client = Anthropic(api_key=self._api_key)
        return self._client

    def complete(self, system: str, user: str, outcome_schema: dict) -> dict:
        strict_schema = self._strict_schema(outcome_schema)
        client = self._get_client()
        try:
            from anthropic import APIError

            response = client.messages.create(
                model=self.model,
                max_tokens=self.thinking_budget_tokens + 8192,
                thinking={"type": "enabled", "budget_tokens": self.thinking_budget_tokens},
                system=system,
                messages=[{"role": "user", "content": f"{user}\n\nRespond using the 'structured_output' tool only."}],
                tools=[{"name": "structured_output", "description": "Emit the result conforming to the required schema", "input_schema": strict_schema}],
                tool_choice={"type": "tool", "name": "structured_output"},
            )
        except APIError as e:
            raise RuntimeError(f"Anthropic API error: {e}") from e

        for block in response.content:
            if block.type == "tool_use" and block.name == "structured_output":
                return block.input
        raise RuntimeError("AnthropicApiProvider: no structured_output tool_use block in response")
