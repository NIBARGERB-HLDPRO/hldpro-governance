#!/usr/bin/env python3
"""
Windows-Ollama Submission Path — SoM Tier-2 Worker

Authoritative entry point for routing inference requests to the Windows-Ollama endpoint
at 172.17.227.49:11434. Enforces PII detection, model allowlist, and failover
PII-preservation rules per STANDARDS.md invariant #8.

Usage:
    submit.py <model> <prompt> [--json]

    Or as a Python module:
        from submit import WindowsOllamaSubmitter
        s = WindowsOllamaSubmitter()
        result = s.submit(model="qwen2.5-coder:7b", prompt="...", has_pii=False)

Exit codes:
    0 — submission successful, response returned
    1 — PII detected or model not allowed (hard block)
    2 — endpoint unreachable or other recoverable error
    3 — malformed request or invalid arguments

Environment variables:
    WINDOWS_OLLAMA_URL (default: http://172.17.227.49:11434)
    WINDOWS_OLLAMA_TIMEOUT (default: 30)
    WINDOWS_OLLAMA_CONFIG_DIR (default: scripts/windows-ollama/)

Last updated: 2026-04-15
"""

__all__ = [
    "WindowsOllamaSubmitter",
    "PiiDetectionError",
    "ModelNotAllowedError",
    "EndpointUnreachableError",
]

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.error import URLError
from urllib.request import Request, urlopen

try:
    import requests
except ImportError:
    requests = None

# Import audit writer
from audit import AuditWriter


class WindowsOllamaSubmitter:
    """Submit requests to Windows-Ollama endpoint with PII detection and allowlist enforcement."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        config_dir: Optional[str] = None,
        timeout_sec: int = 30,
    ):
        """
        Initialize the submitter.

        Args:
            endpoint: Windows-Ollama endpoint URL (default: WINDOWS_OLLAMA_URL env or hardcoded)
            config_dir: Directory containing pii_patterns.yml and model_allowlist.yml
            timeout_sec: Request timeout in seconds
        """
        self.endpoint = endpoint or os.environ.get(
            "WINDOWS_OLLAMA_URL", "http://172.17.227.49:11434"
        )
        self.timeout_sec = timeout_sec
        self.config_dir = Path(
            config_dir or os.environ.get("WINDOWS_OLLAMA_CONFIG_DIR", "scripts/windows-ollama/")
        )

        self.pii_patterns = self._load_pii_patterns()
        self.allowlist = self._load_allowlist()

    def _load_pii_patterns(self) -> Dict[str, Any]:
        """Load PII patterns from pii_patterns.yml."""
        patterns_file = self.config_dir / "pii_patterns.yml"
        if not patterns_file.exists():
            raise FileNotFoundError(f"pii_patterns.yml not found at {patterns_file}")

        # Simple YAML parser for our specific format (no external deps)
        patterns = {}
        current_pattern = None
        try:
            with open(patterns_file) as f:
                for line in f:
                    line = line.rstrip()
                    if line.startswith("  ") and ":" in line:
                        key, val = line.strip().split(":", 1)
                        key, val = key.strip(), val.strip().strip("'\"")
                        if current_pattern:
                            patterns[current_pattern][key] = val
                    elif line and not line.startswith("#") and not line.startswith(" "):
                        if ":" in line:
                            name, _ = line.split(":", 1)
                            current_pattern = name.strip()
                            patterns[current_pattern] = {}
        except Exception as e:
            raise ValueError(f"Failed to parse pii_patterns.yml: {e}")

        return patterns

    def _load_allowlist(self) -> Dict[str, Any]:
        """Load model allowlist from model_allowlist.yml."""
        allowlist_file = self.config_dir / "model_allowlist.yml"
        if not allowlist_file.exists():
            raise FileNotFoundError(f"model_allowlist.yml not found at {allowlist_file}")

        allowlist = {"worker": []}
        try:
            with open(allowlist_file) as f:
                in_worker = False
                for line in f:
                    line = line.rstrip()
                    if "worker:" in line:
                        in_worker = True
                    elif "models:" in line and in_worker:
                        # Next lines are models
                        pass
                    elif in_worker and line.startswith("      - "):
                        model = line.split("-", 1)[1].strip()
                        allowlist["worker"].append(model)
                    elif line and not line.startswith("#") and not line.startswith(" "):
                        in_worker = False
        except Exception as e:
            raise ValueError(f"Failed to parse model_allowlist.yml: {e}")

        return allowlist

    def detect_pii(self, text: str) -> Optional[str]:
        """
        Scan text for PII patterns.

        Returns: pattern name if detected, None otherwise
        """
        if not text:
            return None

        # Built-in patterns (fallback if YAML load fails)
        builtin_patterns = {
            "ssn": r"(?:\d{3}-\d{2}-\d{4}|\d{9})",
            "phone": r"(?:\+\d{1,3}[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "dob": r"(?:0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])[-/](19|20)\d{2}",
            "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
            "field_marker": r"(?:ssn|social|phone|dob|date.?of.?birth|credit|password|api.?key)\s*[:=]",
        }

        for pattern_name, regex in builtin_patterns.items():
            try:
                if re.search(regex, text, re.IGNORECASE):
                    return pattern_name
            except re.error:
                pass

        return None

    def check_allowlist(self, model: str, role: str = "worker") -> bool:
        """Verify model is in allowlist for the specified role."""
        allowed = self.allowlist.get(role, [])
        return model in allowed

    def submit(
        self,
        model: str,
        prompt: str,
        has_pii: bool = False,
        role: str = "worker",
        principal: str = "anonymous",
        session_jti: str = "local",
    ) -> Dict[str, Any]:
        """
        Submit a request to Windows-Ollama.

        Args:
            model: Model name (must be in allowlist)
            prompt: Prompt text
            has_pii: Whether the prompt contains marked PII (hard block)
            role: Role for allowlist check (default: "worker")
            principal: Principal identifier for audit logging
            session_jti: Session JTI for audit logging

        Returns:
            Response dict from /api/generate

        Raises:
            PiiDetectionError: if PII detected or has_pii=True
            ModelNotAllowedError: if model not in allowlist
            EndpointUnreachableError: if endpoint unreachable
        """
        # Initialize audit writer
        audit = AuditWriter()

        # Check explicit PII flag (invariant #8)
        if has_pii:
            audit.write_entry(
                principal=principal,
                session_jti=session_jti,
                tool="windows-ollama.submit",
                args_dict={"model": model, "prompt": "[REDACTED]"},
                status="rejected",
                reject_reason="explicit_pii_flag",
                latency_ms=0
            )
            raise PiiDetectionError(
                error="pii_halt",
                reason="explicit_pii_flag",
                message="Request marked as containing PII; cannot submit to Windows endpoint",
                exit_code=1,
            )

        # Scan for PII patterns
        detected = self.detect_pii(prompt)
        if detected:
            audit.write_entry(
                principal=principal,
                session_jti=session_jti,
                tool="windows-ollama.submit",
                args_dict={"model": model, "prompt": "[REDACTED]"},
                status="rejected",
                reject_reason="pii_detected",
                latency_ms=0
            )
            raise PiiDetectionError(
                error="pii_detected",
                reason=detected,
                message=f"PII pattern detected ({detected}); rejecting submission",
                exit_code=1,
            )

        # Check allowlist
        if not self.check_allowlist(model, role):
            audit.write_entry(
                principal=principal,
                session_jti=session_jti,
                tool="windows-ollama.submit",
                args_dict={"model": model, "prompt": "[REDACTED]"},
                status="rejected",
                reject_reason="model_not_allowed",
                latency_ms=0
            )
            raise ModelNotAllowedError(
                error="model_not_allowed",
                model=model,
                role=role,
                allowed=self.allowlist.get(role, []),
                exit_code=1,
            )

        # Submit to /api/generate
        start_time = time.time()
        try:
            result = self._post_generate(model, prompt)
            latency_ms = int((time.time() - start_time) * 1000)
            audit.write_entry(
                principal=principal,
                session_jti=session_jti,
                tool="windows-ollama.submit",
                args_dict={"model": model, "prompt": "[REDACTED]"},
                status="ok",
                reject_reason=None,
                latency_ms=latency_ms
            )
            return result
        except URLError as e:
            latency_ms = int((time.time() - start_time) * 1000)
            audit.write_entry(
                principal=principal,
                session_jti=session_jti,
                tool="windows-ollama.submit",
                args_dict={"model": model, "prompt": "[REDACTED]"},
                status="error",
                reject_reason="endpoint_unreachable",
                latency_ms=latency_ms
            )
            raise EndpointUnreachableError(
                error="endpoint_unreachable",
                endpoint=self.endpoint,
                reason=str(e),
                exit_code=2,
            )

    def _post_generate(self, model: str, prompt: str) -> Dict[str, Any]:
        """POST to /api/generate and return response."""
        url = f"{self.endpoint}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }

        headers = {"Content-Type": "application/json"}

        # Use requests if available, fall back to urllib
        if requests:
            try:
                resp = requests.post(
                    url, json=payload, headers=headers, timeout=self.timeout_sec
                )
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as e:
                if requests.exceptions.ConnectionError in type(e).__mro__:
                    raise URLError(str(e))
                raise
        else:
            req = Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
            )
            with urlopen(req, timeout=self.timeout_sec) as response:
                data = response.read().decode("utf-8")
                return json.loads(data)


class PiiDetectionError(Exception):
    """Raised when PII is detected or explicitly marked."""

    def __init__(
        self,
        error: str,
        reason: str,
        message: str,
        exit_code: int = 1,
    ):
        self.error = error
        self.reason = reason
        self.message = message
        self.exit_code = exit_code
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        """Return structured error dict for JSON output."""
        return {
            "error": self.error,
            "reason": self.reason,
            "exit_code": self.exit_code,
        }


class ModelNotAllowedError(Exception):
    """Raised when model is not in allowlist."""

    def __init__(
        self,
        error: str,
        model: str,
        role: str,
        allowed: list,
        exit_code: int = 1,
    ):
        self.error = error
        self.model = model
        self.role = role
        self.allowed = allowed
        self.exit_code = exit_code
        super().__init__(f"Model '{model}' not allowed for role '{role}'")

    def to_dict(self) -> Dict[str, Any]:
        """Return structured error dict for JSON output."""
        return {
            "error": self.error,
            "model": self.model,
            "role": self.role,
            "allowed_models": self.allowed,
            "exit_code": self.exit_code,
        }


class EndpointUnreachableError(Exception):
    """Raised when Windows-Ollama endpoint is unreachable."""

    def __init__(
        self,
        error: str,
        endpoint: str,
        reason: str,
        exit_code: int = 2,
    ):
        self.error = error
        self.endpoint = endpoint
        self.reason = reason
        self.exit_code = exit_code
        super().__init__(f"Endpoint unreachable: {endpoint} ({reason})")

    def to_dict(self) -> Dict[str, Any]:
        """Return structured error dict for JSON output."""
        return {
            "error": self.error,
            "endpoint": self.endpoint,
            "reason": self.reason,
            "exit_code": self.exit_code,
        }


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 3:
        print("usage: submit.py <model> <prompt> [--json]", file=sys.stderr)
        return 3

    model = sys.argv[1]
    prompt = sys.argv[2]
    output_json = "--json" in sys.argv

    try:
        submitter = WindowsOllamaSubmitter()
        result = submitter.submit(model=model, prompt=prompt)
        if output_json:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(result, indent=2))
        return 0
    except PiiDetectionError as e:
        if output_json:
            print(json.dumps(e.to_dict()), file=sys.stderr)
        else:
            print(f"ERROR: {e.message}", file=sys.stderr)
        return e.exit_code
    except ModelNotAllowedError as e:
        if output_json:
            print(json.dumps(e.to_dict()), file=sys.stderr)
        else:
            print(f"ERROR: {e}", file=sys.stderr)
        return e.exit_code
    except EndpointUnreachableError as e:
        if output_json:
            print(json.dumps(e.to_dict()), file=sys.stderr)
        else:
            print(f"ERROR: {e}", file=sys.stderr)
        return e.exit_code
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
