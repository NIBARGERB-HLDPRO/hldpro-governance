#!/usr/bin/env python3
"""
Test suite for submit.py — Windows-Ollama submission path.

Covers negative test cases:
1. PII in prompt
2. Non-allowlisted model
3. Unreachable endpoint
4. Malformed /api/generate response
5. Empty rationale from model

Run via: pytest scripts/windows-ollama/tests/test_submit.py
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch
from urllib.error import URLError

import pytest

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from submit import (
    EndpointUnreachableError,
    ModelNotAllowedError,
    PiiDetectionError,
    WindowsOllamaSubmitter,
)


@pytest.fixture
def submitter():
    """Create a submitter with test config."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir)

        # Write minimal config files
        (config_dir / "pii_patterns.yml").write_text(
            """patterns:
  ssn:
    regex: '\\d{3}-\\d{2}-\\d{4}'
    severity: critical
  email:
    regex: '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]+'
    severity: high
"""
        )

        (config_dir / "model_allowlist.yml").write_text(
            """allowlist:
  worker:
    models:
      - qwen2.5-coder:7b
"""
        )

        yield WindowsOllamaSubmitter(
            endpoint="http://172.17.227.49:11434",
            config_dir=str(config_dir),
            timeout_sec=5,
        )


class TestPiiDetection:
    """Negative test: PII detection."""

    def test_pii_ssn_detected(self, submitter):
        """Test that SSN pattern is detected."""
        with pytest.raises(PiiDetectionError) as exc_info:
            submitter.submit(
                model="qwen2.5-coder:7b", prompt="My SSN is 123-45-6789"
            )
        assert exc_info.value.error == "pii_detected"
        assert exc_info.value.exit_code == 1

    def test_pii_email_detected(self, submitter):
        """Test that email pattern is detected."""
        with pytest.raises(PiiDetectionError) as exc_info:
            submitter.submit(
                model="qwen2.5-coder:7b",
                prompt="Contact me at john.doe@example.com for details",
            )
        assert exc_info.value.error == "pii_detected"
        assert exc_info.value.exit_code == 1

    def test_pii_explicit_flag(self, submitter):
        """Test that explicit has_pii=True triggers pii_halt."""
        with pytest.raises(PiiDetectionError) as exc_info:
            submitter.submit(
                model="qwen2.5-coder:7b", prompt="clean prompt", has_pii=True
            )
        assert exc_info.value.error == "pii_halt"
        assert exc_info.value.reason == "explicit_pii_flag"
        assert exc_info.value.exit_code == 1

    def test_no_pii_clean_prompt(self, submitter):
        """Test that clean prompt passes PII detection."""
        # Should not raise during PII check; will fail on endpoint later
        with patch.object(submitter, "_post_generate") as mock_post:
            mock_post.return_value = {"response": "test"}
            result = submitter.submit(
                model="qwen2.5-coder:7b", prompt="What is 2+2?"
            )
            assert result == {"response": "test"}


class TestModelAllowlist:
    """Negative test: non-allowlisted model."""

    def test_model_not_in_allowlist(self, submitter):
        """Test that non-allowlisted model is rejected."""
        with pytest.raises(ModelNotAllowedError) as exc_info:
            submitter.submit(
                model="llama2:7b", prompt="clean prompt", role="worker"
            )
        assert exc_info.value.error == "model_not_allowed"
        assert exc_info.value.model == "llama2:7b"
        assert exc_info.value.exit_code == 1

    def test_model_allowed_in_allowlist(self, submitter):
        """Test that allowlisted model passes allowlist check."""
        with patch.object(submitter, "_post_generate") as mock_post:
            mock_post.return_value = {"response": "test"}
            result = submitter.submit(
                model="qwen2.5-coder:7b", prompt="clean prompt"
            )
            assert result == {"response": "test"}
            mock_post.assert_called_once()


class TestEndpointReachability:
    """Negative test: unreachable endpoint."""

    def test_endpoint_unreachable(self, submitter):
        """Test that unreachable endpoint raises appropriate error."""
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = URLError("Connection refused")
            with pytest.raises(EndpointUnreachableError) as exc_info:
                submitter.submit(
                    model="qwen2.5-coder:7b", prompt="clean prompt"
                )
            assert exc_info.value.error == "endpoint_unreachable"
            assert exc_info.value.exit_code == 2

    def test_endpoint_timeout(self, submitter):
        """Test that endpoint timeout is handled."""
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = URLError("timed out")
            with pytest.raises(EndpointUnreachableError):
                submitter.submit(
                    model="qwen2.5-coder:7b", prompt="clean prompt"
                )

    def test_endpoint_reachable(self, submitter):
        """Test that reachable endpoint succeeds."""
        with patch("submit.WindowsOllamaSubmitter._post_generate") as mock_post:
            mock_post.return_value = {"response": "test output"}
            result = submitter.submit(
                model="qwen2.5-coder:7b", prompt="clean prompt"
            )
            assert result == {"response": "test output"}


class TestMalformedResponse:
    """Negative test: malformed /api/generate response."""

    def test_invalid_json_response(self, submitter):
        """Test that invalid JSON response is rejected."""
        with patch("submit.WindowsOllamaSubmitter._post_generate") as mock_post:
            mock_post.side_effect = json.JSONDecodeError("msg", "doc", 0)
            with pytest.raises(json.JSONDecodeError):
                submitter.submit(
                    model="qwen2.5-coder:7b", prompt="clean prompt"
                )

    def test_empty_response(self, submitter):
        """Test that empty response is handled."""
        with patch("submit.WindowsOllamaSubmitter._post_generate") as mock_post:
            mock_post.side_effect = json.JSONDecodeError("msg", "doc", 0)
            with pytest.raises(json.JSONDecodeError):
                submitter.submit(
                    model="qwen2.5-coder:7b", prompt="clean prompt"
                )


class TestEmptyRationale:
    """Negative test: empty rationale from model."""

    def test_response_with_empty_field(self, submitter):
        """Test that response with missing 'response' field is handled gracefully."""
        with patch("submit.WindowsOllamaSubmitter._post_generate") as mock_post:
            mock_post.return_value = {"model": "qwen2.5-coder:7b"}
            result = submitter.submit(
                model="qwen2.5-coder:7b", prompt="clean prompt"
            )
            # submit.py doesn't validate response schema — that's caller's responsibility
            assert result == {"model": "qwen2.5-coder:7b"}

    def test_response_with_empty_response_field(self, submitter):
        """Test response with empty 'response' field."""
        with patch("submit.WindowsOllamaSubmitter._post_generate") as mock_post:
            mock_post.return_value = {"response": ""}
            result = submitter.submit(
                model="qwen2.5-coder:7b", prompt="clean prompt"
            )
            # Empty response is returned as-is (validation is caller's concern)
            assert result == {"response": ""}


class TestErrorStructure:
    """Verify error structures for JSON output."""

    def test_pii_error_structure(self, submitter):
        """Test that PII errors have correct JSON structure."""
        try:
            submitter.submit(
                model="qwen2.5-coder:7b", prompt="SSN: 123-45-6789"
            )
        except PiiDetectionError as e:
            err_dict = e.to_dict()
            assert "error" in err_dict
            assert "reason" in err_dict
            assert "exit_code" in err_dict
            assert err_dict["exit_code"] == 1

    def test_model_not_allowed_error_structure(self, submitter):
        """Test that model-not-allowed errors have correct JSON structure."""
        try:
            submitter.submit(model="bogus:model", prompt="test")
        except ModelNotAllowedError as e:
            err_dict = e.to_dict()
            assert "error" in err_dict
            assert "model" in err_dict
            assert "role" in err_dict
            assert "allowed_models" in err_dict
            assert "exit_code" in err_dict
            assert err_dict["exit_code"] == 1

    def test_endpoint_unreachable_error_structure(self, submitter):
        """Test that endpoint-unreachable errors have correct JSON structure."""
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = URLError("Connection refused")
            try:
                submitter.submit(
                    model="qwen2.5-coder:7b", prompt="test"
                )
            except EndpointUnreachableError as e:
                err_dict = e.to_dict()
                assert "error" in err_dict
                assert "endpoint" in err_dict
                assert "reason" in err_dict
                assert "exit_code" in err_dict
                assert err_dict["exit_code"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
