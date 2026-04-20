#!/usr/bin/env python3
"""
Thin Remote MCP client for the hldpro-governance thin runner.

This client is intentionally conservative:
- stdlib-only transport
- Cloudflare Access headers
- bearer auth support
- small in-memory JWT refresh/cache path
- conservative retry with exponential backoff on 429
- payload-safe error reporting
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence


DEFAULT_BASE_URL = "http://localhost:8080"


class SomClientError(RuntimeError):
    """Error raised for client-side protocol and transport failures."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        tool: Optional[str] = None,
        attempts: Optional[int] = None,
    ) -> None:
        self.status_code = status_code
        self.tool = tool
        self.attempts = attempts
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": "som_client_error",
            "status_code": self.status_code,
            "tool": self.tool,
            "attempts": self.attempts,
        }


def _decode_jwt_payload(jwt_token: str) -> Optional[Dict[str, Any]]:
    """Decode JWT payload without verifying signature."""
    if jwt_token.count(".") != 2:
        return None

    try:
        _, payload_b64, _ = jwt_token.split(".")
        padding = "=" * ((4 - (len(payload_b64) % 4)) % 4)
        raw_payload = base64.urlsafe_b64decode(payload_b64 + padding)
        return json.loads(raw_payload.decode("utf-8"))
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return None


def _unix_now() -> int:
    return int(time.time())


@dataclass
class SomClientConfig:
    base_url: str
    bearer_token: Optional[str] = None
    cf_access_client_id: Optional[str] = None
    cf_access_client_secret: Optional[str] = None
    token_refresher: Optional[Callable[[], str]] = None
    timeout_sec: float = 8.0
    max_retries: int = 3
    backoff_base_sec: float = 0.25
    user_agent: Optional[str] = None
    headers: Optional[Dict[str, str]] = None


class SomClient:
    """Minimal HTTP client for Remote MCP Bridge tools."""

    def __init__(self, config: SomClientConfig) -> None:
        self._config = config
        self._cached_token = config.bearer_token

    @classmethod
    def from_env(cls) -> "SomClient":
        """Build a client from well-known environment variables."""
        base_url = os.environ.get("SOM_MCP_URL", DEFAULT_BASE_URL).rstrip("/")
        token = os.environ.get("SOM_MCP_TOKEN") or os.environ.get("SOM_REMOTE_MCP_JWT")
        return cls(
            SomClientConfig(
                base_url=base_url,
                bearer_token=token,
                cf_access_client_id=os.environ.get("CF_ACCESS_CLIENT_ID"),
                cf_access_client_secret=os.environ.get("CF_ACCESS_CLIENT_SECRET"),
                user_agent=os.environ.get("SOM_MCP_USER_AGENT"),
            )
        )

    def _current_token(self) -> str:
        if not self._cached_token:
            raise SomClientError("authorization token is not configured")

        payload = _decode_jwt_payload(self._cached_token)
        exp = payload.get("exp") if isinstance(payload, dict) else None
        if not isinstance(exp, int):
            return self._cached_token

        # Refresh if expiring within window.
        if exp - _unix_now() <= 60:
            if not self._config.token_refresher:
                # Conservative: don't send near-expired tokens when we can't refresh.
                raise SomClientError("authorization token is expired or near expiry")
            self._cached_token = self._config.token_refresher()

        return self._cached_token

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self._config.user_agent:
            headers["User-Agent"] = self._config.user_agent

        token = self._current_token()
        headers["Authorization"] = f"Bearer {token}"

        if self._config.cf_access_client_id and self._config.cf_access_client_secret:
            headers["Cf-Access-Client-Id"] = self._config.cf_access_client_id
            headers["Cf-Access-Client-Secret"] = self._config.cf_access_client_secret

        if self._config.headers:
            headers.update(self._config.headers)

        return headers

    def _request(
        self,
        path: str,
        method: str,
        body: Dict[str, Any],
        *,
        tool: Optional[str] = None,
        allow_retry: bool = True,
    ) -> Dict[str, Any]:
        payload = json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        url = f"{self._config.base_url}/{path.lstrip('/')}"
        last_error: Optional[SomClientError] = None

        for attempt in range(self._config.max_retries + 1):
            request = urllib.request.Request(
                url=url,
                data=payload,
                headers=self._headers(),
                method=method,
            )
            try:
                response = urllib.request.urlopen(request, timeout=self._config.timeout_sec)
                try:
                    raw = response.read()
                finally:
                    close = getattr(response, "close", None)
                    if close is not None:
                        close()

                result = json.loads(raw.decode("utf-8"))
                if "error" in result:
                    raise SomClientError(
                        "remote tool returned an error",
                        status_code=200,
                        tool=tool,
                        attempts=attempt + 1,
                    )
                return result
            except urllib.error.HTTPError as error:
                if error.code == 429 and allow_retry and attempt < self._config.max_retries:
                    last_error = SomClientError(
                        "temporary service throttling",
                        status_code=error.code,
                        tool=tool,
                        attempts=attempt + 1,
                    )
                    time.sleep(self._config.backoff_base_sec * (2**attempt))
                    continue
                raise SomClientError(
                    "remote service returned an error",
                    status_code=error.code,
                    tool=tool,
                    attempts=attempt + 1,
                ) from error
            except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
                raise SomClientError(
                    "failed to decode remote response",
                    status_code=None,
                    tool=tool,
                    attempts=attempt + 1,
                ) from error

        if last_error is not None:
            raise last_error

        raise SomClientError("request could not be completed", tool=tool, attempts=self._config.max_retries + 1)

    def _call_tool(self, name: str, args: Dict[str, Any], *, method: str = "POST") -> Dict[str, Any]:
        body = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools.call",
            "params": {
                "name": name,
                "arguments": args,
            },
        }
        response = self._request("mcp", method, body, tool=name)
        if "result" not in response:
            raise SomClientError("malformed remote response", tool=name)
        if isinstance(response["result"], dict):
            return response["result"]
        return {"result": response["result"]}

    def ping(self) -> Dict[str, Any]:
        return self._call_tool("som.ping", {})

    def handoff(
        self,
        *,
        prior: Dict[str, Any],
        next_tier: int,
        artifacts: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        args: Dict[str, Any] = {"prior": prior, "next_tier": next_tier}
        if artifacts is not None:
            args["artifacts"] = artifacts
        return self._call_tool("som.handoff", args)

    def chain(self, *, packet_id: str) -> Dict[str, Any]:
        return self._call_tool("som.chain", {"packet_id": packet_id})

    def log_fallback(self, *, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._call_tool("som.log_fallback", payload)

    def lam_probe(self) -> Dict[str, Any]:
        return self._call_tool("lam.probe", {})

    def lam_embed(self, *, text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        args: Dict[str, Any] = {"text": text}
        if metadata is not None:
            args["metadata"] = metadata
        return self._call_tool("lam.embed", args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Remote MCP thin client")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    parser.parse_args(list(argv) if argv is not None else None)
    SomClient.from_env().ping()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
