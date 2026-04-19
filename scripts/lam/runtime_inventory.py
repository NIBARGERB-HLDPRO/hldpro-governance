#!/usr/bin/env python3
"""No-payload local model runtime and guardrail inventory."""

from __future__ import annotations

import argparse
import json
import importlib.util
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import urlopen


REPO_ROOT = Path(__file__).resolve().parents[2]
WINDOWS_OLLAMA_URL = "http://172.17.227.49:11434"
DEFAULT_TIMEOUT = 2.0
WINDOWS_ROLE_UNVERIFIED = "lan_only_fallback_batch_health_unverified"


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=False, capture_output=True, text=True)


def mac_hardware() -> dict[str, Any]:
    result = _run(["system_profiler", "SPHardwareDataType"])
    payload: dict[str, Any] = {"available": result.returncode == 0}
    if result.returncode != 0:
        payload["error"] = result.stderr.strip() or result.stdout.strip()
        return payload
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("Model Identifier:"):
            payload["model_identifier"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("Chip:"):
            payload["chip"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("Total Number of Cores:"):
            payload["cores"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("Memory:"):
            payload["memory"] = stripped.split(":", 1)[1].strip()
    return payload


def import_available(module_name: str) -> bool:
    result = _run([sys.executable, "-c", f"import {module_name}"])
    return result.returncode == 0


def local_runtime() -> dict[str, Any]:
    return {
        "mlx_lm_importable": import_available("mlx_lm"),
        "mlx_lm_server_path": shutil.which("mlx_lm.server"),
        "ollama_cli_path": shutil.which("ollama"),
        "probe_payloads_sent": False,
    }


def windows_ollama(endpoint: str = WINDOWS_OLLAMA_URL, timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    url = endpoint.rstrip("/") + "/api/tags"
    try:
        with urlopen(url, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except (OSError, URLError, TimeoutError) as exc:
        return {
            "endpoint": endpoint,
            "reachable": False,
            "error": str(exc),
            "models": [],
            "probe_payloads_sent": False,
            "role": WINDOWS_ROLE_UNVERIFIED,
        }
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        return {
            "endpoint": endpoint,
            "reachable": False,
            "error": f"invalid JSON from /api/tags: {exc}",
            "models": [],
            "probe_payloads_sent": False,
            "role": WINDOWS_ROLE_UNVERIFIED,
        }
    models = [str(row.get("name")) for row in parsed.get("models", []) if isinstance(row, dict) and row.get("name")]
    return {
        "endpoint": endpoint,
        "reachable": True,
        "models": sorted(models),
        "probe_payloads_sent": False,
        "role": WINDOWS_ROLE_UNVERIFIED,
    }


def pii_guardrail(patterns_path: Path | None = None) -> dict[str, Any]:
    patterns = patterns_path or (REPO_ROOT / "scripts" / "windows-ollama" / "pii_patterns.yml")
    try:
        module_path = REPO_ROOT / "scripts" / "windows-ollama" / "_pii.py"
        spec = importlib.util.spec_from_file_location("windows_ollama_pii", module_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"could not load {module_path}")
        pii_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pii_module)
        loaded = pii_module.load_pii_patterns(str(patterns))
        email_detected = pii_module.detect_pii("contact jane@example.com", loaded) is not None
        clean_detected = pii_module.detect_pii("write a function that adds two integers", loaded) is not None
    except Exception as exc:
        return {
            "patterns_path": patterns.as_posix(),
            "ready": False,
            "fail_closed": True,
            "error": str(exc),
        }
    return {
        "patterns_path": patterns.as_posix(),
        "ready": bool(email_detected and not clean_detected),
        "fail_closed": not bool(email_detected and not clean_detected),
        "email_probe_detected": bool(email_detected),
        "clean_probe_detected": bool(clean_detected),
        "probe_payloads_sent": False,
    }


def memory_budget(total_memory_gb: int = 48) -> dict[str, Any]:
    return {
        "mac_total_memory_gb": total_memory_gb,
        "steady_state": {
            "guardrail_lam": {"model": "mlx-community/Qwen3-8B-4bit", "budget_gb": 4.67, "resident": True},
            "mcp_intent": {"model": "mlx-community/Qwen3-1.7B-4bit", "budget_gb": 1.5, "resident": "warm_evictable"},
        },
        "on_demand": {
            "worker_lam": {"model": "mlx-community/Qwen3-14B-4bit", "budget_gb": 10, "resident": False},
            "worker_lam_large": {
                "model": "mlx-community/Qwen3.6-35B-A3B-4bit",
                "budget_gb": 24,
                "resident": False,
                "runtime": "mlx",
                "placement": "mac_m5_pro_48gb_on_demand_only",
            },
            "critic_lam": {"model": "mlx-community/gemma-4-26b-a4b-4bit", "budget_gb": 18, "resident": False},
            "qwen_coder_fallback": {"model": "mlx-community/Qwen2.5-Coder-7B-Instruct-4bit", "budget_gb": 6, "resident": False},
        },
        "policy": "keep guardrail resident; load one large on-demand model at a time; unload on completion or memory pressure",
    }


def build_inventory(endpoint: str = WINDOWS_OLLAMA_URL, timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    hardware = mac_hardware()
    memory_raw = str(hardware.get("memory") or "48 GB")
    try:
        total_memory_gb = int(memory_raw.split()[0])
    except (ValueError, IndexError):
        total_memory_gb = 48
    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "probe_payloads_sent": False,
        "mac_hardware": hardware,
        "local_runtime": local_runtime(),
        "windows_ollama": windows_ollama(endpoint, timeout),
        "pii_guardrail": pii_guardrail(),
        "memory_budget": memory_budget(total_memory_gb),
        "routing_boundaries": {
            "pii_to_cloud_allowed": False,
            "pii_to_windows_allowed": False,
            "patterns_missing_behavior": "halt",
            "local_guardrail_unavailable_behavior": "halt_for_pii_arch_standards",
            "windows_role": WINDOWS_ROLE_UNVERIFIED,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory local model runtimes without sending prompt payloads.")
    parser.add_argument("--endpoint", default=WINDOWS_OLLAMA_URL, help="Windows Ollama endpoint base URL.")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Metadata probe timeout in seconds.")
    parser.add_argument("--output", type=Path, help="Optional JSON output path.")
    args = parser.parse_args()

    payload = build_inventory(args.endpoint, args.timeout)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
