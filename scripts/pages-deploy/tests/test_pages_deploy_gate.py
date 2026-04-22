from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from unittest import mock

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "pages_deploy_gate.py"
SPEC = importlib.util.spec_from_file_location("pages_deploy_gate", MODULE_PATH)
gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


class FakeCompleted:
    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = ""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def write_config(tmp_path: Path, **overrides: object) -> Path:
    config = {
        "project_name": "hldpro-test",
        "app_root": str(tmp_path),
        "build_command": "npm run build",
        "output_dir": "dist",
        "branch": "main",
        "pages_alias": "https://hldpro-test.pages.dev",
        "required_env": ["CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID"],
    }
    config.update(overrides)
    path = tmp_path / "pages-deploy.config.json"
    path.write_text(__import__("json").dumps(config), encoding="utf-8")
    return path


def default_env() -> dict[str, str]:
    return {
        "PATH": os.environ.get("PATH", ""),
        "CLOUDFLARE_API_TOKEN": "secret-token",
        "CLOUDFLARE_ACCOUNT_ID": "secret-account",
        "PAGES_DEPLOY_APPROVED": "1",
    }


def make_runner(tmp_path: Path, *, pre_code: int = 0, build_code: int = 0, deploy_code: int = 0):
    calls: list[tuple[object, dict[str, object]]] = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        if command == ["wrangler", "--version"]:
            return FakeCompleted(stdout="wrangler 3.100.0\n")
        if command == ["git", "rev-parse", "HEAD"]:
            return FakeCompleted(stdout="abc123\n")
        if isinstance(command, str) and command == "preflight":
            return FakeCompleted(returncode=pre_code, stderr="pre failed\n" if pre_code else "")
        if isinstance(command, str) and command == "npm run build":
            if build_code == 0:
                dist = tmp_path / "dist"
                dist.mkdir(exist_ok=True)
                (dist / "index.html").write_text("ok", encoding="utf-8")
                os.utime(dist, None)
            return FakeCompleted(returncode=build_code, stderr="build failed\n" if build_code else "")
        if isinstance(command, list) and command[:3] == ["wrangler", "pages", "deploy"]:
            signed_query = "X-Amz-" + "Signature=abc"
            auth_header = "Authorization:" + " Bearer secret-token"
            return FakeCompleted(
                returncode=deploy_code,
                stdout=(f"Published https://deploy.pages.dev?{signed_query} {auth_header}\n"),
            )
        return FakeCompleted()

    return calls, fake_run


def run_gate(config_path: Path, tmp_path: Path, *, env: dict[str, str] | None = None, dry_run: bool = False, **runner_kwargs):
    calls, fake_run = make_runner(tmp_path, **runner_kwargs)
    with mock.patch.object(gate.shutil, "which", return_value="/usr/bin/tool"), mock.patch.object(
        gate.subprocess, "run", side_effect=fake_run
    ), mock.patch.object(gate, "branch_binding_preflight"), mock.patch.object(
        gate, "_run_post_deploy_verification"
    ):
        code = gate.run_gate(config_path, dry_run=dry_run, env=env or default_env())
    return code, calls


def run_gate_expect_error(
    config_path: Path,
    tmp_path: Path,
    *,
    env: dict[str, str] | None = None,
    dry_run: bool = False,
    which_return: str | None = "/usr/bin/tool",
    **runner_kwargs,
):
    calls, fake_run = make_runner(tmp_path, **runner_kwargs)
    with mock.patch.object(gate.shutil, "which", return_value=which_return), mock.patch.object(
        gate.subprocess, "run", side_effect=fake_run
    ), mock.patch.object(gate, "branch_binding_preflight"), mock.patch.object(
        gate, "_run_post_deploy_verification"
    ):
        with pytest.raises(gate.GateError) as exc:
            gate.run_gate(config_path, dry_run=dry_run, env=env or default_env())
    return str(exc.value), calls


def deploy_calls(calls):
    return [call for call in calls if isinstance(call[0], list) and call[0][:3] == ["wrangler", "pages", "deploy"]]


def test_two_phase_order_pre_deploy_success(tmp_path):
    config = write_config(tmp_path, pre_deploy={"command": "preflight"})
    code, calls = run_gate(config, tmp_path)

    assert code == 0
    commands = [call[0] for call in calls]
    assert commands.index("preflight") < commands.index("npm run build")
    assert deploy_calls(calls)


def test_two_phase_order_pre_deploy_failure(tmp_path):
    config = write_config(tmp_path, pre_deploy={"command": "preflight"})
    error, calls = run_gate_expect_error(config, tmp_path, pre_code=1)

    assert "PRE_DEPLOY_FAIL: preflight exited 1" in error
    assert not deploy_calls(calls)


def test_missing_cloudflare_api_token(tmp_path):
    config = write_config(tmp_path)
    env = default_env()
    missing_value = env.pop("CLOUDFLARE_API_TOKEN")

    error, calls = run_gate_expect_error(config, tmp_path, env=env)
    assert error == "MISSING_ENV: CLOUDFLARE_API_TOKEN"
    assert not deploy_calls(calls)
    assert missing_value not in error


def test_missing_cloudflare_api_token_public_message_is_name_only(tmp_path, capsys):
    config = write_config(tmp_path)
    env = default_env()
    missing_value = env.pop("CLOUDFLARE_API_TOKEN")

    error, _calls = run_gate_expect_error(config, tmp_path, env=env)
    with pytest.raises(SystemExit):
        try:
            gate.preflight_env(["CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID"], env, dry_run=False)
        except gate.GateError as exc:
            gate.fail_error(exc, env)

    out = capsys.readouterr().out
    assert error == "MISSING_ENV: CLOUDFLARE_API_TOKEN"
    assert "Missing required secret variables: CLOUDFLARE_API_TOKEN." in out
    assert "hldpro-governance/.env.shared plus bootstrap" in out
    assert "GitHub Actions secrets" in out
    assert "Values are intentionally not accepted" in out
    assert missing_value not in out
    assert "secret-account" not in out
    assert "export " not in out
    assert "<your-token>" not in out


def test_missing_cloudflare_account_id(tmp_path):
    config = write_config(tmp_path)
    env = default_env()
    missing_value = env.pop("CLOUDFLARE_ACCOUNT_ID")

    error, calls = run_gate_expect_error(config, tmp_path, env=env)

    assert error == "MISSING_ENV: CLOUDFLARE_ACCOUNT_ID"
    assert not deploy_calls(calls)
    assert missing_value not in error


def test_missing_cloudflare_account_id_public_message_is_name_only(capsys):
    env = default_env()
    missing_value = env.pop("CLOUDFLARE_ACCOUNT_ID")

    with pytest.raises(SystemExit):
        try:
            gate.preflight_env(["CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID"], env, dry_run=False)
        except gate.GateError as exc:
            gate.fail_error(exc, env)

    out = capsys.readouterr().out
    assert "Missing required secret variables: CLOUDFLARE_ACCOUNT_ID." in out
    assert "hldpro-governance/.env.shared plus bootstrap" in out
    assert "GitHub Actions secrets" in out
    assert missing_value not in out
    assert "secret-token" not in out
    assert "export " not in out
    assert "<your-token>" not in out


def test_missing_both_cloudflare_env_vars_lists_names_only(capsys):
    env = default_env()
    missing_token = env.pop("CLOUDFLARE_API_TOKEN")
    missing_account = env.pop("CLOUDFLARE_ACCOUNT_ID")

    with pytest.raises(SystemExit):
        try:
            gate.preflight_env(["CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID"], env, dry_run=False)
        except gate.GateError as exc:
            gate.fail_error(exc, env)

    out = capsys.readouterr().out
    assert "Missing required secret variables: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID." in out
    assert missing_token not in out
    assert missing_account not in out
    assert "export " not in out
    assert "<your-token>" not in out


def test_deploy_requires_approved_flag(tmp_path):
    config = write_config(tmp_path)
    env = default_env()
    env.pop("PAGES_DEPLOY_APPROVED")

    error, calls = run_gate_expect_error(config, tmp_path, env=env)

    assert "PREFLIGHT_FAIL: PAGES_DEPLOY_APPROVED must be 1" in error
    assert not deploy_calls(calls)


def test_dry_run_skips_deploy(tmp_path):
    config = write_config(tmp_path)
    env = default_env()
    env.pop("PAGES_DEPLOY_APPROVED")

    code, calls = run_gate(config, tmp_path, env=env, dry_run=True)

    assert code == 0
    commands = [call[0] for call in calls]
    assert "npm run build" not in commands
    assert not deploy_calls(calls)


def test_build_failure(tmp_path):
    config = write_config(tmp_path)

    error, calls = run_gate_expect_error(config, tmp_path, build_code=1)

    assert "BUILD_FAIL" in error
    assert not deploy_calls(calls)


def test_output_dir_missing(tmp_path):
    config = write_config(tmp_path, build_command="true")

    error, calls = run_gate_expect_error(config, tmp_path)

    assert "BUILD_FAIL: output_dir does not exist" in error
    assert not deploy_calls(calls)


def test_output_dir_empty(tmp_path):
    (tmp_path / "dist").mkdir()
    config = write_config(tmp_path, build_command="true")

    error, calls = run_gate_expect_error(config, tmp_path)

    assert "BUILD_FAIL: output_dir is empty" in error
    assert not deploy_calls(calls)


def test_stale_artifact(tmp_path):
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("stale", encoding="utf-8")
    os.utime(dist, (1, 1))
    config = write_config(tmp_path, build_command="true")

    error, calls = run_gate_expect_error(config, tmp_path)

    assert "BUILD_FAIL: output_dir is stale" in error
    assert not deploy_calls(calls)


def test_pages_limit_file_count(tmp_path):
    config = write_config(tmp_path, pages_limits={"max_files": 0})

    error, calls = run_gate_expect_error(config, tmp_path)

    assert "PAGES_LIMIT_FAIL: file count 1 exceeds 0" in error
    assert not deploy_calls(calls)


def test_pages_limit_file_size(tmp_path):
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "large.bin").write_bytes(b"123456")
    config = write_config(tmp_path, pages_limits={"max_file_size_mb": 0.000001})

    error, calls = run_gate_expect_error(config, tmp_path)

    assert "PAGES_LIMIT_FAIL: file exceeds max_file_size_mb" in error
    assert not deploy_calls(calls)


def test_secret_redaction(tmp_path, capsys):
    config = write_config(tmp_path)

    run_gate(config, tmp_path)
    out = capsys.readouterr().out

    assert "secret-token" not in out
    assert "secret-account" not in out
    assert "[REDACTED]" in out


def test_wrangler_missing(tmp_path):
    config = write_config(tmp_path)
    calls, fake_run = make_runner(tmp_path)

    with mock.patch.object(gate.shutil, "which", return_value=None), mock.patch.object(
        gate.subprocess, "run", side_effect=fake_run
    ):
        with pytest.raises(gate.GateError) as exc:
            gate.run_gate(config, env=default_env())

    assert str(exc.value) == "PREFLIGHT_FAIL: node not found on PATH"

    def fake_which(name):
        if name == "node":
            return "/usr/bin/node"
        return None

    with mock.patch.object(gate.shutil, "which", side_effect=fake_which), mock.patch.object(
        gate.subprocess, "run", side_effect=fake_run
    ):
        with pytest.raises(gate.GateError) as exc:
            gate.run_gate(config, env=default_env())

    assert str(exc.value) == "PREFLIGHT_FAIL: wrangler not found on PATH"
    assert not deploy_calls(calls)


def test_wrangler_uses_ci_without_removed_noninteractive_flag(tmp_path):
    config = write_config(tmp_path)

    code, calls = run_gate(config, tmp_path)

    assert code == 0
    deploy_call = deploy_calls(calls)[0]
    command, kwargs = deploy_call
    assert "--non-interactive" not in command
    assert kwargs["env"]["CI"] == "true"


def _make_cf_response(production_branch: str) -> object:
    import json as _json
    body = _json.dumps({"result": {"production_branch": production_branch}}).encode()

    class FakeResponse:
        def __init__(self):
            self._body = body

        def read(self):
            return self._body

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    return FakeResponse()


def test_branch_binding_preflight_passes_on_match(tmp_path):
    config = {"project_name": "my-proj", "branch": "main"}
    env = {"CLOUDFLARE_API_TOKEN": "tok", "CLOUDFLARE_ACCOUNT_ID": "acct"}

    with mock.patch.object(gate.urllib.request, "urlopen", return_value=_make_cf_response("main")):
        gate.branch_binding_preflight(config, env)


def test_branch_binding_preflight_fails_on_mismatch(tmp_path):
    config = {"project_name": "my-proj", "branch": "main"}
    env = {"CLOUDFLARE_API_TOKEN": "tok", "CLOUDFLARE_ACCOUNT_ID": "acct"}

    with mock.patch.object(gate.urllib.request, "urlopen", return_value=_make_cf_response("production")):
        with pytest.raises(gate.GateError) as exc:
            gate.branch_binding_preflight(config, env)

    assert "BRANCH_BINDING_MISMATCH" in str(exc.value)
    assert "production" in str(exc.value)


def test_branch_binding_preflight_skips_without_token(tmp_path):
    config = {"project_name": "my-proj", "branch": "main"}
    env = {}

    with mock.patch.object(gate.urllib.request, "urlopen", side_effect=AssertionError("should not be called")):
        gate.branch_binding_preflight(config, env)


def test_branch_binding_preflight_skips_via_env_flag(tmp_path):
    config = {"project_name": "my-proj", "branch": "main"}
    env = {"CLOUDFLARE_API_TOKEN": "tok", "CLOUDFLARE_ACCOUNT_ID": "acct", "PAGES_SKIP_BRANCH_PREFLIGHT": "1"}

    with mock.patch.object(gate.urllib.request, "urlopen", side_effect=AssertionError("should not be called")):
        gate.branch_binding_preflight(config, env)


def test_branch_binding_preflight_skips_on_api_error(tmp_path):
    config = {"project_name": "my-proj", "branch": "main"}
    env = {"CLOUDFLARE_API_TOKEN": "tok", "CLOUDFLARE_ACCOUNT_ID": "acct"}

    with mock.patch.object(gate.urllib.request, "urlopen", side_effect=OSError("network error")):
        gate.branch_binding_preflight(config, env)


def test_post_deploy_verify_called_with_source_sha(tmp_path):
    config = write_config(tmp_path)
    calls, fake_run = make_runner(tmp_path)
    captured: list[tuple] = []

    def fake_verify(cfg, sha, env):
        captured.append((cfg, sha, env))

    with mock.patch.object(gate.shutil, "which", return_value="/usr/bin/tool"), mock.patch.object(
        gate.subprocess, "run", side_effect=fake_run
    ), mock.patch.object(gate, "_run_post_deploy_verification", side_effect=fake_verify):
        gate.run_gate(config, env=default_env())

    assert len(captured) == 1
    _cfg, sha, _env = captured[0]
    assert sha == "abc123"


def test_post_deploy_verify_failure_propagates(tmp_path):
    config = write_config(tmp_path)
    calls, fake_run = make_runner(tmp_path)

    def fake_verify(cfg, sha, env):
        raise gate.GateError("POST_DEPLOY_VERIFY_FAIL: domain mismatch")

    with mock.patch.object(gate.shutil, "which", return_value="/usr/bin/tool"), mock.patch.object(
        gate.subprocess, "run", side_effect=fake_run
    ), mock.patch.object(gate, "_run_post_deploy_verification", side_effect=fake_verify):
        with pytest.raises(gate.GateError) as exc:
            gate.run_gate(config, env=default_env())

    assert "POST_DEPLOY_VERIFY_FAIL" in str(exc.value)


def test_post_deploy_verify_not_called_on_dry_run(tmp_path):
    config = write_config(tmp_path)
    calls, fake_run = make_runner(tmp_path)
    captured: list[tuple] = []

    def fake_verify(cfg, sha, env):
        captured.append((cfg, sha, env))

    with mock.patch.object(gate.shutil, "which", return_value="/usr/bin/tool"), mock.patch.object(
        gate.subprocess, "run", side_effect=fake_run
    ), mock.patch.object(gate, "_run_post_deploy_verification", side_effect=fake_verify):
        gate.run_gate(config, dry_run=True, env=default_env())

    assert len(captured) == 0
