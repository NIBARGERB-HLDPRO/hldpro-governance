#!/usr/bin/env python3
"""Reusable Cloudflare Pages Direct Upload deploy gate."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_CONFIG_KEYS = (
    "project_name",
    "app_root",
    "build_command",
    "output_dir",
    "branch",
    "pages_alias",
    "required_env",
)

DEFAULT_LIMITS = {
    "max_files": 20000,
    "max_file_size_mb": 25,
    "max_build_size_mb": 25,
}

SENSITIVE_ENV_NAMES = ("CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID")
SIGNED_URL_RE = re.compile(r"([?&](?:X-Amz-|X-Goog-|Expires=|Signature=)[^\s\"]+)", re.IGNORECASE)
AUTH_HEADER_RE = re.compile(r"(Authorization:\s*)(Bearer\s+)?[^\s\"]+", re.IGNORECASE)


class GateError(Exception):
    """Expected gate failure with deterministic operator output."""

    def __init__(self, message: str, public_message: str | None = None):
        super().__init__(message)
        self.public_message = public_message or message


@dataclass
class ArtifactStats:
    file_count: int
    total_size: int
    largest_file: Path | None
    largest_size: int


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def redact(text: str, env: dict[str, str] | None = None) -> str:
    redacted = text
    source_env = env if env is not None else os.environ
    for name in SENSITIVE_ENV_NAMES:
        value = source_env.get(name) or os.environ.get(name, "")
        if value:
            redacted = redacted.replace(value, "[REDACTED]")
    redacted = AUTH_HEADER_RE.sub(r"\1[REDACTED]", redacted)
    redacted = SIGNED_URL_RE.sub("[REDACTED]", redacted)
    return redacted


def log(message: str, env: dict[str, str] | None = None) -> None:
    print(redact(str(message), env), flush=True)


def fail(message: str, env: dict[str, str] | None = None) -> None:
    log(message, env)
    sys.exit(1)


def fail_error(error: GateError, env: dict[str, str] | None = None) -> None:
    fail(error.public_message, env)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GateError(f"CONFIG_INVALID_JSON: {path}: {exc}") from exc
    except OSError as exc:
        raise GateError(f"CONFIG_READ_FAILED: {path}: {exc}") from exc


def json_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    return True


def validate_with_schema(config: Any, schema: dict[str, Any]) -> None:
    def validate(value: Any, subschema: dict[str, Any], path: str) -> None:
        expected_type = subschema.get("type")
        if expected_type and not json_type_matches(value, expected_type):
            raise GateError(f"CONFIG_SCHEMA_ERROR: {path} expected {expected_type}")

        if expected_type == "object":
            if not isinstance(value, dict):
                raise GateError(f"CONFIG_SCHEMA_ERROR: {path} expected object")
            properties = subschema.get("properties", {})
            required = subschema.get("required", [])
            for key in required:
                if key not in value:
                    raise GateError(f"CONFIG_SCHEMA_ERROR: missing required property {path}.{key}")
            if subschema.get("additionalProperties") is False:
                allowed = set(properties)
                for key in value:
                    if key not in allowed:
                        raise GateError(f"CONFIG_SCHEMA_ERROR: unexpected property {path}.{key}")
            for key, child in properties.items():
                if key in value:
                    validate(value[key], child, f"{path}.{key}")

        if expected_type == "array":
            item_schema = subschema.get("items", {})
            for index, item in enumerate(value):
                validate(item, item_schema, f"{path}[{index}]")

    validate(config, schema, "config")


def _validate_config_or_raise(config: Any) -> None:
    if not isinstance(config, dict):
        raise GateError("CONFIG_INVALID: config must be an object")
    for key in REQUIRED_CONFIG_KEYS:
        if key not in config:
            raise GateError(f"CONFIG_INVALID: missing required key: {key}")


def validate_config(config: Any) -> None:
    """Public test-facing config validator."""

    try:
        _validate_config_or_raise(config)
    except GateError as exc:
        fail_error(exc)


def validate_schema(config: dict[str, Any]) -> str:
    schema_path = repo_root() / "docs/schemas/pages-deploy-consumer.schema.json"
    schema = load_json(schema_path)
    try:
        import jsonschema  # type: ignore
    except ImportError:
        validate_with_schema(config, schema)
        return "passed: fallback validator"

    try:
        jsonschema.validate(instance=config, schema=schema)
    except jsonschema.ValidationError as exc:
        raise GateError(f"CONFIG_SCHEMA_ERROR: {exc.message}") from exc
    return "passed: jsonschema"


def load_config(config_path: Path) -> tuple[dict[str, Any], str]:
    config = load_json(config_path)
    _validate_config_or_raise(config)
    schema_result = validate_schema(config)
    return config, schema_result


def resolve_app_root(config: dict[str, Any], config_path: Path) -> Path:
    app_root = Path(config["app_root"])
    if app_root.is_absolute():
        return app_root
    return (config_path.parent / app_root).resolve()


def resolve_output_dir(config: dict[str, Any], app_root: Path) -> Path:
    output_dir = Path(config["output_dir"])
    if output_dir.is_absolute():
        return output_dir
    return (app_root / output_dir).resolve()


def run_command(
    command: str | list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    shell: bool = False,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        env=env,
        shell=shell,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = (getattr(result, "stdout", "") or "") + (getattr(result, "stderr", "") or "")
    if output.strip():
        log(output.rstrip(), env)
    return result


def preflight_env(required_env: list[str], env: dict[str, str], dry_run: bool) -> None:
    missing = [name for name in required_env if not env.get(name)]
    if missing:
        missing_names = ", ".join(missing)
        raise GateError(
            f"MISSING_ENV: {missing_names}",
            "\n".join(
                [
                    f"Missing required secret variables: {missing_names}.",
                    (
                        "Provision them through hldpro-governance/.env.shared plus bootstrap for local runs, "
                        "or through GitHub Actions secrets for CI."
                    ),
                    "Values are intentionally not accepted in this prompt or printed in logs.",
                    "No deploy was attempted. Configure the approved provisioning surface, then rerun the preflight.",
                ]
            ),
        )
    if not dry_run and env.get("PAGES_DEPLOY_APPROVED") != "1":
        raise GateError(
            "DEPLOY_NOT_APPROVED: PREFLIGHT_FAIL: PAGES_DEPLOY_APPROVED must be 1",
            "PREFLIGHT_FAIL: PAGES_DEPLOY_APPROVED must be 1",
        )


def preflight_tools() -> None:
    if shutil.which("node") is None:
        raise GateError("PREFLIGHT_FAIL: node not found on PATH")
    if shutil.which("wrangler") is None:
        raise GateError("PREFLIGHT_FAIL: wrangler not found on PATH")


def get_wrangler_version(env: dict[str, str]) -> str:
    result = run_command(["wrangler", "--version"], env=env)
    if result.returncode != 0:
        raise GateError(f"PREFLIGHT_FAIL: wrangler --version exited {result.returncode}")
    version = ((result.stdout or "") + (result.stderr or "")).strip() or "unknown"
    log(f"wrangler_version: {version}", env)
    return version


def run_pre_deploy(config: dict[str, Any], app_root: Path, env: dict[str, str]) -> None:
    pre_deploy = config.get("pre_deploy")
    if not pre_deploy:
        return
    command = pre_deploy["command"]
    result = run_command(command, cwd=app_root, env=env, shell=True)
    if result.returncode != 0:
        raise GateError(
            f"PRE_DEPLOY_FAILED: PRE_DEPLOY_FAIL: {command} exited {result.returncode}",
            f"PRE_DEPLOY_FAIL: {command} exited {result.returncode}",
        )


def count_files(output_dir: Path) -> int:
    return sum(1 for path in output_dir.rglob("*") if path.is_file())


def run_build(config: dict[str, Any], app_root: Path, output_dir: Path, env: dict[str, str]) -> tuple[float, float, int]:
    build_start = time.time()
    log(f"build_start: {build_start:.6f}", env)
    result = run_command(config["build_command"], cwd=app_root, env=env, shell=True)
    build_end = time.time()

    if result.returncode != 0:
        raise GateError(
            f"BUILD_FAILED: BUILD_FAIL: {config['build_command']} exited {result.returncode}",
            f"BUILD_FAIL: {config['build_command']} exited {result.returncode}",
        )
    if not output_dir.exists() or not output_dir.is_dir():
        raise GateError(
            "OUTPUT_DIR_MISSING: BUILD_FAIL: output_dir does not exist",
            "BUILD_FAIL: output_dir does not exist",
        )
    file_count = count_files(output_dir)
    if file_count == 0:
        raise GateError("OUTPUT_DIR_EMPTY: BUILD_FAIL: output_dir is empty", "BUILD_FAIL: output_dir is empty")
    if output_dir.stat().st_mtime < build_start:
        raise GateError("STALE_ARTIFACT: BUILD_FAIL: output_dir is stale", "BUILD_FAIL: output_dir is stale")

    log(f"build_end: {build_end:.6f}", env)
    log(f"artifact_count: {file_count}", env)
    return build_start, build_end, file_count


def _inspect_files(files: list[Path]) -> ArtifactStats:
    file_count = 0
    total_size = 0
    largest_file: Path | None = None
    largest_size = 0
    for path in files:
        if not path.is_file():
            continue
        size = path.stat().st_size
        file_count += 1
        total_size += size
        if size > largest_size:
            largest_size = size
            largest_file = path
    return ArtifactStats(file_count, total_size, largest_file, largest_size)


def _check_pages_limits(config: dict[str, Any], files: list[Path]) -> ArtifactStats:
    limits = dict(DEFAULT_LIMITS)
    limits.update(config.get("pages_limits", {}))
    stats = _inspect_files(files)

    if stats.file_count > int(limits["max_files"]):
        message = f"PAGES_LIMIT_FAIL: file count {stats.file_count} exceeds {limits['max_files']}"
        raise GateError(f"PAGES_LIMIT_FILE_COUNT: {message}", message)

    max_file_size = float(limits["max_file_size_mb"]) * 1024 * 1024
    if stats.largest_size > max_file_size:
        largest = stats.largest_file or Path("<unknown>")
        message = f"PAGES_LIMIT_FAIL: file exceeds max_file_size_mb: {largest}"
        raise GateError(f"PAGES_LIMIT_FILE_SIZE: {message}", message)

    max_build_size = float(limits["max_build_size_mb"]) * 1024 * 1024
    if stats.total_size > max_build_size:
        message = f"PAGES_LIMIT_FAIL: total build size exceeds max_build_size_mb: {stats.total_size}"
        raise GateError(f"PAGES_LIMIT_BUILD_SIZE: {message}", message)

    return stats


def enforce_pages_limits(config: dict[str, Any], files: list[Path]) -> ArtifactStats:
    """Public test-facing Pages limits checker."""

    try:
        return _check_pages_limits(config, files)
    except GateError as exc:
        fail_error(exc)


def git_head() -> str:
    try:
        output = subprocess.check_output(["git", "rev-parse", "HEAD"])
    except subprocess.CalledProcessError as exc:
        raise GateError("GIT_HEAD_FAILED") from exc
    except OSError as exc:
        raise GateError("GIT_HEAD_FAILED") from exc
    if isinstance(output, str):
        return output.strip()
    return output.decode().strip()


def deploy(config: dict[str, Any], output_dir: Path, source_sha: str, env: dict[str, str]) -> str:
    child_env = dict(env)
    child_env["CI"] = "true"
    command = [
        "wrangler",
        "pages",
        "deploy",
        str(output_dir.resolve()),
        "--project-name",
        config["project_name"],
        "--branch",
        config["branch"],
        "--commit-hash",
        source_sha,
        "--non-interactive",
    ]
    result = run_command(command, env=child_env)
    if result.returncode != 0:
        raise GateError(f"DEPLOY_FAIL: wrangler pages deploy exited {result.returncode}")
    output = (result.stdout or "") + (result.stderr or "")
    deployment_url = extract_deployment_url(output) or "unknown"
    log(f"deployment_url: {deployment_url}", child_env)
    return deployment_url


def extract_deployment_url(output: str) -> str | None:
    match = re.search(r"https://[^\s\"]+\.pages\.dev[^\s\"]*", output)
    if match:
        return match.group(0).rstrip(".,)")
    match = re.search(r"https://[^\s\"]+", output)
    if match:
        return match.group(0).rstrip(".,)")
    return None


def emit_evidence(
    *,
    deployment_url: str,
    source_sha: str,
    config: dict[str, Any],
    wrangler_version: str,
    build_start: float | None,
    build_end: float | None,
    artifact_count: int,
    env: dict[str, str],
) -> None:
    evidence = {
        "deployment_url": deployment_url,
        "source_sha": source_sha,
        "project_name": config["project_name"],
        "branch": config["branch"],
        "wrangler_version": wrangler_version,
        "build_start_ts": build_start,
        "build_end_ts": build_end,
        "artifact_count": artifact_count,
    }
    log(json.dumps(evidence, sort_keys=True), env)


def run_gate(config_path: Path, *, dry_run: bool = False, env: dict[str, str] | None = None) -> int:
    gate_env = dict(os.environ if env is None else env)
    config_path = config_path.resolve()
    config, schema_result = load_config(config_path)
    log(f"schema_validation: {schema_result}", gate_env)
    app_root = resolve_app_root(config, config_path)
    output_dir = resolve_output_dir(config, app_root)

    preflight_tools()
    preflight_env(config["required_env"], gate_env, dry_run=dry_run)
    wrangler_version = get_wrangler_version(gate_env)
    run_pre_deploy(config, app_root, gate_env)

    if dry_run:
        emit_evidence(
            deployment_url="unknown",
            source_sha="dry-run",
            config=config,
            wrangler_version=wrangler_version,
            build_start=None,
            build_end=None,
            artifact_count=0,
            env=gate_env,
        )
        return 0

    build_start, build_end, artifact_count = run_build(config, app_root, output_dir, gate_env)
    _check_pages_limits(config, list(output_dir.rglob("*")))
    source_sha = git_head()
    deployment_url = deploy(config, output_dir, source_sha, gate_env)

    emit_evidence(
        deployment_url=deployment_url,
        source_sha=source_sha,
        config=config,
        wrangler_version=wrangler_version,
        build_start=build_start,
        build_end=build_end,
        artifact_count=artifact_count,
        env=gate_env,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cloudflare Pages Direct Upload deploy gate")
    parser.add_argument("--config", required=True, help="Path to consumer config JSON")
    parser.add_argument("--dry-run", action="store_true", help="Validate only; skip build and deploy")
    args = parser.parse_args(argv)

    try:
        return run_gate(Path(args.config), dry_run=args.dry_run)
    except GateError as exc:
        fail_error(exc)


if __name__ == "__main__":
    sys.exit(main())
