#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError


MODULE_PATH = Path(__file__).with_name("runtime_inventory.py")
SPEC = importlib.util.spec_from_file_location("runtime_inventory", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
runtime_inventory = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runtime_inventory
SPEC.loader.exec_module(runtime_inventory)


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self) -> bytes:
        return self.payload


class TestRuntimeInventory(unittest.TestCase):
    def test_windows_timeout_reports_unreachable_without_payloads(self) -> None:
        with patch("runtime_inventory.urlopen", side_effect=URLError("timed out")):
            payload = runtime_inventory.windows_ollama("http://example.invalid:11434", 0.01)
        self.assertEqual(payload["reachable"], False)
        self.assertEqual(payload["probe_payloads_sent"], False)
        self.assertEqual(payload["models"], [])
        self.assertIn("unverified", payload["role"])

    def test_windows_tags_lists_models_without_payloads(self) -> None:
        response = FakeResponse({"models": [{"name": "qwen2.5-coder:7b"}, {"name": "llama3.1:8b"}]})
        with patch("runtime_inventory.urlopen", return_value=response):
            payload = runtime_inventory.windows_ollama("http://example.invalid:11434", 0.01)
        self.assertEqual(payload["reachable"], True)
        self.assertEqual(payload["probe_payloads_sent"], False)
        self.assertEqual(payload["models"], ["llama3.1:8b", "qwen2.5-coder:7b"])
        self.assertEqual(payload["role"], "lan_only_fallback_batch_health_unverified")

    def test_pii_guardrail_missing_patterns_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            payload = runtime_inventory.pii_guardrail(Path(raw) / "missing.yml")
        self.assertEqual(payload["ready"], False)
        self.assertEqual(payload["fail_closed"], True)

    def test_pii_guardrail_happy_path_detects_email_and_allows_clean_probe(self) -> None:
        payload = runtime_inventory.pii_guardrail()
        self.assertEqual(payload["ready"], True)
        self.assertEqual(payload["fail_closed"], False)
        self.assertEqual(payload["email_probe_detected"], True)
        self.assertEqual(payload["clean_probe_detected"], False)

    def test_inventory_has_no_payload_routing(self) -> None:
        with patch("runtime_inventory.windows_ollama") as windows:
            windows.return_value = {
                "endpoint": "http://example.invalid:11434",
                "reachable": False,
                "models": [],
                "probe_payloads_sent": False,
                "role": "lan_only_fallback_batch_health_unverified",
            }
            payload = runtime_inventory.build_inventory("http://example.invalid:11434", 0.01)
        self.assertEqual(payload["probe_payloads_sent"], False)
        self.assertEqual(payload["routing_boundaries"]["pii_to_cloud_allowed"], False)
        self.assertEqual(payload["routing_boundaries"]["pii_to_windows_allowed"], False)
        self.assertEqual(payload["routing_boundaries"]["patterns_missing_behavior"], "halt")
        self.assertEqual(payload["routing_boundaries"]["windows_role"], "lan_only_fallback_batch_health_unverified")


if __name__ == "__main__":
    unittest.main(verbosity=2)
