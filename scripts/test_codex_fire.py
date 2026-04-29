import os
import subprocess
import textwrap
import time
from pathlib import Path
from typing import Optional


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "codex-fire.sh"


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


def test_review_template_default_persona_reaches_codex_fire(tmp_path: Path) -> None:
    counter = tmp_path / "counter"
    prompt_capture = tmp_path / "prompt.txt"
    args_capture = tmp_path / "args.txt"
    fake_bin = write_fake_codex(
        tmp_path,
        textwrap.dedent(
            f"""
            counter="{counter}"
            prompt_capture="{prompt_capture}"
            args_capture="{args_capture}"
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
            printf '%s\\n' "$@" >"$args_capture"
            cat >"$prompt_capture"
            echo "audit complete"
            exit 0
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
    env.pop("CODEX_REVIEW_PERSONA", None)

    result = subprocess.run(
        [
            "bash",
            str(REPO_ROOT / "scripts" / "codex-review-template.sh"),
            "audit",
            "scripts/codex-fire.sh",
        ],
        text=True,
        capture_output=True,
        env=env,
        cwd=REPO_ROOT,
        check=False,
    )

    assert result.returncode == 0
    assert "Audit saved to:" in result.stdout
    assert "audit complete" in result.stdout
    assert "CODEX_FAIL" not in result.stdout
    assert not (tmp_path / "template-log.md").exists()

    args = args_capture.read_text(encoding="utf-8")
    prompt = prompt_capture.read_text(encoding="utf-8")
    assert "exec" in args
    assert "-m" in args
    assert "gpt-5.4" in args
    assert "model_reasoning_effort=high" in args
    assert "docs/codex-reviews" in args
    assert "Review Discipline" in prompt
    assert "Focus your security audit on: scripts/codex-fire.sh" in prompt


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
            "CODEX_REVIEW_PERSONA": str(tmp_path / "codex-reviewer.md"),
        }
    )
    (tmp_path / "codex-reviewer.md").write_text("Return concise review findings.\n", encoding="utf-8")

    result = subprocess.run(
        [
            "bash",
            str(REPO_ROOT / "scripts" / "codex-review-template.sh"),
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


def test_review_template_claude_dry_run_uses_self_contained_packet_contract(tmp_path: Path) -> None:
    persona = tmp_path / "codex-reviewer.md"
    persona.write_text("Return concise review findings.\n", encoding="utf-8")
    env = os.environ.copy()
    env.update(
        {
            "CODEX_REVIEW_DRY_RUN": "1",
            "CODEX_REVIEW_PERSONA": str(persona),
            "CLAUDE_CODE_OAUTH_TOKEN": "test-token",
            "CLAUDE_REVIEW_ENV_FILE": str(tmp_path / ".env.local"),
        }
    )

    result = subprocess.run(
        [
            "bash",
            str(REPO_ROOT / "scripts" / "codex-review-template.sh"),
            "claude",
            "Review this packet only.",
        ],
        text=True,
        capture_output=True,
        env=env,
        cwd=REPO_ROOT,
        check=False,
    )

    assert result.returncode == 0
    assert "DRY_RUN claude mode ready" in result.stdout
    assert "model=claude-opus-4-6" in result.stdout
    assert "permission_mode=bypassPermissions" in result.stdout
    assert "max_turns=8" in result.stdout
    assert "allowed_tools=none" in result.stdout
    assert "review_contract=self_contained_packet" in result.stdout
