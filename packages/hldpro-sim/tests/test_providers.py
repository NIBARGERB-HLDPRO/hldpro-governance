import json
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from hldprosim.personas import PersonaLoader
from hldprosim.providers import AnthropicApiProvider, CodexCliProvider



_captured_schema: dict = {}


def _write_output_from_call(cmd, **kwargs):
    schema_path = Path(cmd[cmd.index("--output-schema") + 1])
    _captured_schema.update(json.loads(schema_path.read_text()))
    output_path = Path(cmd[cmd.index("-o") + 1])
    output_path.write_text(json.dumps({"persona_id": "trader-momentum", "result": "ok"}))
    return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")


def test_codex_provider_builds_expected_subprocess_args():
    provider = CodexCliProvider()
    schema = {"type": "object"}
    _captured_schema.clear()

    with patch("hldprosim.providers.subprocess.run") as mock_run:
        mock_run.side_effect = _write_output_from_call
        provider.complete("system prompt", "user prompt", schema)

    called_cmd = mock_run.call_args.args[0]
    assert called_cmd[0] == "codex"
    assert called_cmd[1] == "exec"
    assert called_cmd[2] == "--ephemeral"
    assert called_cmd[3] == "--skip-git-repo-check"
    assert called_cmd[4:7] == ["--sandbox", "read-only", "-m"]
    assert called_cmd[7] == provider.model
    assert called_cmd[8:10] == ["-c", f"model_reasoning_effort={provider.effort}"]
    assert "--output-schema" in called_cmd
    assert _captured_schema["additionalProperties"] is False
    assert called_cmd[-1] == "system prompt\n\nuser prompt"


def test_codex_provider_injects_additional_properties_false_when_missing():
    provider = CodexCliProvider()
    schema = {"type": "object", "properties": {"x": {"type": "string"}}}
    _captured_schema.clear()

    with patch("hldprosim.providers.subprocess.run") as mock_run:
        mock_run.side_effect = _write_output_from_call
        provider.complete("", "hello", schema)

    assert _captured_schema["additionalProperties"] is False


def test_codex_provider_passes_prompt_as_positional_arg_only():
    provider = CodexCliProvider()
    with patch("hldprosim.providers.subprocess.run") as mock_run:
        mock_run.side_effect = _write_output_from_call
        provider.complete("system", "user", {})

    call_kwargs = mock_run.call_args.kwargs
    assert "input" not in call_kwargs or call_kwargs["input"] is None


def test_anthropic_provider_complete_calls_api():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "dummy-test-key"}):
        provider = AnthropicApiProvider()
    mock_block = MagicMock()
    mock_block.type = "tool_use"
    mock_block.name = "structured_output"
    mock_block.input = {"result": "ok"}
    mock_response = MagicMock()
    mock_response.content = [mock_block]
    with patch.object(provider, "_get_client") as mock_client:
        mock_client.return_value.messages.create.return_value = mock_response
        result = provider.complete("sys", "usr", {"type": "object", "properties": {}})
    assert result == {"result": "ok"}
    call_kwargs = mock_client.return_value.messages.create.call_args[1]
    assert call_kwargs["thinking"]["type"] == "enabled"
    assert call_kwargs["tool_choice"] == {"type": "tool", "name": "structured_output"}


def test_codex_provider_raises_on_nonzero_exit_code():
    provider = CodexCliProvider()
    with patch("hldprosim.providers.subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess([], 1, stdout="", stderr="failed")
        try:
            provider.complete("system", "user", {})
        except RuntimeError as err:
            assert "codex exec failed" in str(err)
        else:
            assert False, "expected RuntimeError"


def test_persona_loader_prefers_local_file():
    with tempfile.TemporaryDirectory() as local_dir, tempfile.TemporaryDirectory() as shared_dir:
        local_path = Path(local_dir) / "trader-momentum.json"
        shared_path = Path(shared_dir) / "trader-momentum.json"
        shared_path.write_text(json.dumps({"source": "shared"}))
        local_path.write_text(json.dumps({"source": "local"}))

        loader = PersonaLoader(local_dir=Path(local_dir), shared_dir=Path(shared_dir))
        persona = loader.load("trader-momentum")
        assert persona == {"source": "local"}


def test_persona_loader_falls_back_to_shared_file():
    with tempfile.TemporaryDirectory() as local_dir, tempfile.TemporaryDirectory() as shared_dir:
        shared_path = Path(shared_dir) / "trader-momentum.json"
        shared_path.write_text(json.dumps({"source": "shared"}))

        loader = PersonaLoader(local_dir=Path(local_dir), shared_dir=Path(shared_dir))
        persona = loader.load("trader-momentum")
        assert persona == {"source": "shared"}


def test_persona_loader_raises_when_missing():
    with tempfile.TemporaryDirectory() as local_dir, tempfile.TemporaryDirectory() as shared_dir:
        loader = PersonaLoader(local_dir=Path(local_dir), shared_dir=Path(shared_dir))
        try:
            loader.load("trader-momentum")
        except FileNotFoundError as err:
            assert "trader-momentum" in str(err)
        else:
            assert False, "expected FileNotFoundError"
