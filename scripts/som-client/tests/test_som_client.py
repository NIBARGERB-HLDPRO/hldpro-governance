#!/usr/bin/env python3
"""
Targeted tests for the Remote MCP thin client.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from som_client import SomClient, SomClientConfig, SomClientError


def _build_success_response(payload: Dict[str, Any]) -> SimpleNamespace:
    body = json.dumps(payload).encode("utf-8")
    return SimpleNamespace(
        __enter__=lambda self: self,
        __exit__=lambda self, exc_type, exc, tb: False,
        read=lambda: body,
    )


def _build_http_error(
    code: int,
    payload: Optional[Dict[str, Any]] = None,
) -> urllib.error.HTTPError:
    body = json.dumps(payload or {}).encode("utf-8")
    return urllib.error.HTTPError(
        url="https://example.com/mcp",
        code=code,
        msg="error",
        hdrs=None,
        fp=BytesIO(body),
    )


def test_som_client_sends_cf_and_bearer_headers(monkeypatch) -> None:
    seen_headers: Dict[str, str] = {}

    def fake_urlopen(request: urllib.request.Request, timeout: float = 0.0):
        seen_headers.update({k.lower(): v for k, v in request.header_items()})
        return _build_success_response({"result": {"ok": True}})

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setenv("SOM_MCP_URL", "https://mcp.example.com")
    monkeypatch.setenv("SOM_MCP_TOKEN", "bearer-token")
    monkeypatch.setenv("CF_ACCESS_CLIENT_ID", "cf-id")
    monkeypatch.setenv("CF_ACCESS_CLIENT_SECRET", "cf-secret")
    monkeypatch.setenv("SOM_REMOTE_MCP_AUDIT_HMAC_KEY", "unused")

    client = SomClient.from_env()
    client.ping()

    assert seen_headers["authorization"] == "Bearer bearer-token"
    assert seen_headers["cf-access-client-id"] == "cf-id"
    assert seen_headers["cf-access-client-secret"] == "cf-secret"


def test_som_client_retries_on_429(monkeypatch) -> None:
    calls = {"count": 0}
    sleeps: List[float] = []

    def fake_urlopen(request: urllib.request.Request, timeout: float = 0.0):
        calls["count"] += 1
        if calls["count"] == 1:
            raise _build_http_error(429, {"error": "rate limited"})
        return _build_success_response({"result": {"ok": True}})

    def fake_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr("som_client.time.sleep", fake_sleep)
    monkeypatch.setenv("SOM_MCP_TOKEN", "bearer-token")

    client = SomClient(
        SomClientConfig(
            base_url="https://mcp.example.com",
            bearer_token="bearer-token",
            max_retries=1,
            backoff_base_sec=0.5,
        )
    )
    result = client.ping()

    assert calls["count"] == 2
    assert result == {"ok": True}
    assert sleeps == [0.5]


def test_som_client_payload_safe_errors(monkeypatch) -> None:
    def fake_urlopen(request: urllib.request.Request, timeout: float = 0.0):
        raise _build_http_error(
            400,
            {"error": "bad request", "payload": {"secret": "do-not-leak-abc123"}},
        )

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setenv("SOM_MCP_TOKEN", "bearer-token")
    client = SomClient(
        SomClientConfig(
            base_url="https://mcp.example.com",
            bearer_token="bearer-token",
            max_retries=0,
        )
    )

    with pytest.raises(SomClientError) as exc:
        client.ping()
    message = str(exc.value)
    assert "do-not-leak-abc123" not in message
    assert "remote service returned an error" in message
