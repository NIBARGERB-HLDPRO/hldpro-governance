import os
import subprocess
import textwrap
import time
from pathlib import Path
from typing import Optional


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "codex-fire.sh"
REVIEW_TEMPLATE = REPO_ROOT / "scripts" / "codex-review-template.sh"


def write_fake_codex(tmp_path: Path, body: str) -> Path:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_codex = fake_bin / "codex"
    fake_codex.write_text(
        "#!/usr/bin/env bash\n"
        "set -uo pipefail\n"
        + body,
        encoding="utf-8",
    )
    fake_codex.chmod(0o755)
    return fake_bin


def run_fire(tmp_path: Path, fake_bin: Path, extra_env: Optional[dict[str, str]] = None) -> subprocess.CompletedProcess[str]:
    brief = tmp_path / "brief.txt"
    brief.write_text("do the work\n", encoding="utf-8")
    log_file = tmp_path / "fail-fast-log.md"
    env = os.environ.copy()
    env.update(
        {
            "PATH": f"{fake_bin}{os.pathsep}{env.get('PATH', '')}",
            "CODEX_FIRE_LOG": str(log_file),
            "CODEX_FIRE_TIMEOUT_SECONDS": "1",
        }
    )
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [
            "bash",
            str(SCRIPT),
            "-m",
            "bad-model",
            "-e",
            "high",
            "-w",
            str(tmp_path),
            "-b",
            str(brief),
        ],
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )


def test_preflight_failure_logs_and_exits_fast(tmp_path: Path) -> None:
    fake_bin = write_fake_codex(
        tmp_path,
        textwrap.dedent(
            """
            echo "400: model not supported with ChatGPT account" >&2
            exit 42
            """
        ),
    )

    started = time.monotonic()
    result = run_fire(tmp_path, fake_bin)
    elapsed = time.monotonic() - started

    assert result.returncode == 1
    assert elapsed < 5
    assert "CODEX_FAIL: model=bad-model exit=1" in result.stdout
    log = (tmp_path / "fail-fast-log.md").read_text(encoding="utf-8")
    assert "| codex-exec | bad-model | preflight failed: 400: model not supported with ChatGPT account |" in log


def test_preflight_timeout_logs_and_exits_fast(tmp_path: Path) -> None:
    fake_bin = write_fake_codex(
        tmp_path,
        textwrap.dedent(
            """
            sleep 3
            echo ok
            """
        ),
    )

    started = time.monotonic()
    result = run_fire(tmp_path, fake_bin)
    elapsed = time.monotonic() - started

    assert result.returncode == 1
    assert elapsed < 5
    assert "CODEX_FAIL: model=bad-model exit=1" in result.stdout
    log = (tmp_path / "fail-fast-log.md").read_text(encoding="utf-8")
    assert "preflight failed: preflight timed out after 1s" in log


def test_exec_failure_after_successful_preflight_logs_and_signals(tmp_path: Path) -> None:
    counter = tmp_path / "counter"
    fake_bin = write_fake_codex(
        tmp_path,
        textwrap.dedent(
            f"""
            counter="{counter}"
            count=0
            if [ -f "$counter" ]; then
              count="$(cat "$counter")"
            fi
            count=$((count + 1))
            printf '%s' "$count" >"$counter"
            if [ "$count" -eq 1 ]; then
              echo ok
              exit 0
            fi
            echo "runtime model failure" >&2
            exit 7
            """
        ),
    )

    result = run_fire(tmp_path, fake_bin)

    assert result.returncode == 1
    assert "runtime model failure" in result.stdout
    assert "CODEX_FAIL: model=bad-model exit=1" in result.stdout
    log = (tmp_path / "fail-fast-log.md").read_text(encoding="utf-8")
    assert "| codex-exec | bad-model | exec failed: runtime model failure |" in log


def test_success_does_not_write_failure_log(tmp_path: Path) -> None:
    fake_bin = write_fake_codex(
        tmp_path,
        textwrap.dedent(
            """
            echo ok
            exit 0
            """
        ),
    )

    result = run_fire(tmp_path, fake_bin)

    assert result.returncode == 0
    assert result.stdout.count("ok") == 1
    assert not (tmp_path / "fail-fast-log.md").exists()


def test_review_template_propagates_wrapper_failure(tmp_path: Path) -> None:
    counter = tmp_path / "counter"
    fake_bin = write_fake_codex(
        tmp_path,
        textwrap.dedent(
            f"""
            counter="{counter}"
            count=0
            if [ -f "$counter" ]; then
              count="$(cat "$counter")"
            fi
            count=$((count + 1))
            printf '%s' "$count" >"$counter"
            if [ "$count" -eq 1 ]; then
              echo ok
              exit 0
            fi
            echo "template routed failure" >&2
            exit 9
            """
        ),
    )
    env = os.environ.copy()
    env.update(
        {
            "PATH": f"{fake_bin}{os.pathsep}{env.get('PATH', '')}",
            "CODEX_FIRE_LOG": str(tmp_path / "template-log.md"),
            "CODEX_FIRE_TIMEOUT_SECONDS": "1",
        }
    )

    result = subprocess.run(
        [
            "bash",
            str(REVIEW_TEMPLATE),
            "audit",
            "scripts",
        ],
        text=True,
        capture_output=True,
        env=env,
        cwd=REPO_ROOT,
        check=False,
    )

    assert result.returncode == 1
    assert "CODEX_FAIL: model=gpt-5.4 exit=1" in result.stdout
    assert "Audit saved to:" not in result.stdout
    assert "Audit failed; see CODEX_FAIL output above." in result.stderr
    assert "Codex brief retained at:" in result.stderr


def test_review_template_persona_override_reaches_wrapper(tmp_path: Path) -> None:
    counter = tmp_path / "counter"
    captured_prompt = tmp_path / "captured-prompt.txt"
    fake_bin = write_fake_codex(
        tmp_path,
        textwrap.dedent(
            f"""
            counter="{counter}"
            count=0
            if [ -f "$counter" ]; then
              count="$(cat "$counter")"
            fi
            count=$((count + 1))
            printf '%s' "$count" >"$counter"
            if [ "$count" -eq 1 ]; then
              cat >/dev/null
              echo ok
              exit 0
            fi
            cat >"{captured_prompt}"
            echo ok
            exit 0
            """
        ),
    )
    override_persona = tmp_path / "codex-reviewer.md"
    override_persona.write_text("OVERRIDE PERSONA MARKER\n", encoding="utf-8")
    env = os.environ.copy()
    env.update(
        {
            "PATH": f"{fake_bin}{os.pathsep}{env.get('PATH', '')}",
            "CODEX_FIRE_LOG": str(tmp_path / "template-log.md"),
            "CODEX_FIRE_TIMEOUT_SECONDS": "1",
            "CODEX_REVIEW_PERSONA": str(override_persona),
        }
    )

    result = subprocess.run(
        [
            "bash",
            str(REVIEW_TEMPLATE),
            "audit",
            "scripts",
        ],
        text=True,
        capture_output=True,
        env=env,
        cwd=REPO_ROOT,
        check=False,
    )

    assert result.returncode == 0
    assert "Audit saved to:" in result.stdout
    assert "OVERRIDE PERSONA MARKER" in captured_prompt.read_text(encoding="utf-8")
    assert not (tmp_path / "template-log.md").exists()
