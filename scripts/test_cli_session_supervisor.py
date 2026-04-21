import json
import subprocess
import sys
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUPERVISOR = ROOT / "scripts" / "cli_session_supervisor.py"


def write_fake(tmp_path: Path, body: str) -> Path:
    fake = tmp_path / "fake_cli.py"
    fake.write_text(textwrap.dedent(body), encoding="utf-8")
    return fake


def run_supervisor(tmp_path: Path, fake: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    prompt = tmp_path / "prompt.txt"
    prompt.write_text("do work\n", encoding="utf-8")
    event_root = tmp_path / "events"
    return subprocess.run(
        [
            sys.executable,
            str(SUPERVISOR),
            "--tool",
            "claude",
            "--role",
            "worker",
            "--model",
            "claude-sonnet-4-6",
            "--cwd",
            str(tmp_path),
            "--prompt-file",
            str(prompt),
            "--scope-slug",
            "test-scope",
            "--event-root",
            str(event_root),
            "--wall-timeout-sec",
            "0.7",
            "--silence-timeout-sec",
            "0.25",
            "--terminate-grace-sec",
            "0.05",
            *extra,
            "--command",
            "--",
            sys.executable,
            str(fake),
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def events(tmp_path: Path) -> list[dict]:
    jsonl = next((tmp_path / "events").glob("*.jsonl"))
    return [json.loads(line) for line in jsonl.read_text(encoding="utf-8").splitlines()]


def test_success_event_captures_stdout_and_schema_fields(tmp_path):
    fake = write_fake(
        tmp_path,
        """
        import sys
        print("ok")
        print("warn", file=sys.stderr)
        """,
    )

    result = run_supervisor(tmp_path, fake)

    assert result.returncode == 0
    assert "ok" in result.stdout
    [event] = events(tmp_path)
    assert event["termination_reason"] == "succeeded"
    assert event["exit_code"] == 0
    assert event["handoff_package_ref"] is None
    assert event["prompt_sha256"]
    assert Path(event["stdout_path"]).read_text(encoding="utf-8").strip() == "ok"
    assert Path(event["stderr_path"]).read_text(encoding="utf-8").strip() == "warn"


def test_nonzero_failure_is_recorded_without_retry(tmp_path):
    fake = write_fake(
        tmp_path,
        """
        import sys
        print("bad")
        raise SystemExit(7)
        """,
    )

    result = run_supervisor(tmp_path, fake)

    assert result.returncode == 7
    [event] = events(tmp_path)
    assert event["termination_reason"] == "failed_nonzero"
    assert event["exit_code"] == 7


def test_silent_stall_hits_idle_timeout_and_kills_process(tmp_path):
    fake = write_fake(
        tmp_path,
        """
        import time
        time.sleep(5)
        """,
    )

    result = run_supervisor(tmp_path, fake)

    assert result.returncode == 124
    assert "idle_timeout" in result.stderr
    [event] = events(tmp_path)
    assert event["termination_reason"] == "idle_timeout"


def test_intermittent_output_avoids_idle_timeout(tmp_path):
    fake = write_fake(
        tmp_path,
        """
        import sys, time
        for idx in range(3):
            print(f"tick-{idx}", flush=True)
            time.sleep(0.1)
        """,
    )

    result = run_supervisor(tmp_path, fake)

    assert result.returncode == 0
    [event] = events(tmp_path)
    assert event["termination_reason"] == "succeeded"
    assert event["last_output_at"] is not None


def test_total_timeout_overrides_active_output(tmp_path):
    fake = write_fake(
        tmp_path,
        """
        import time
        while True:
            print("still working", flush=True)
            time.sleep(0.05)
        """,
    )

    result = run_supervisor(tmp_path, fake)

    assert result.returncode == 124
    assert "total_timeout" in result.stderr
    [event] = events(tmp_path)
    assert event["termination_reason"] == "total_timeout"


def test_retry_once_can_recover_from_timeout(tmp_path):
    fake = write_fake(
        tmp_path,
        """
        from pathlib import Path
        import time
        state = Path("state.txt")
        if state.exists():
            print("retry ok")
        else:
            state.write_text("seen", encoding="utf-8")
            time.sleep(5)
        """,
    )
    retry_prompt = tmp_path / "retry.txt"
    retry_prompt.write_text("do smaller work\n", encoding="utf-8")

    result = run_supervisor(
        tmp_path,
        fake,
        "--retry-prompt-file",
        str(retry_prompt),
        "--scope-reduction-summary",
        "smaller retry",
    )

    assert result.returncode == 0
    first, second = events(tmp_path)
    assert first["termination_reason"] == "idle_timeout"
    assert second["termination_reason"] == "succeeded"
    assert second["retry_of"] == first["session_event_id"]
    assert second["retry_count"] == 1
    assert second["scope_reduction_summary"] == "smaller retry"


def test_retry_halts_after_one_additional_timeout(tmp_path):
    fake = write_fake(
        tmp_path,
        """
        import time
        time.sleep(5)
        """,
    )
    retry_prompt = tmp_path / "retry.txt"
    retry_prompt.write_text("do smaller work\n", encoding="utf-8")

    result = run_supervisor(
        tmp_path,
        fake,
        "--retry-prompt-file",
        str(retry_prompt),
        "--scope-reduction-summary",
        "smaller retry",
    )

    assert result.returncode == 124
    first, second = events(tmp_path)
    assert first["termination_reason"] == "idle_timeout"
    assert second["termination_reason"] == "idle_timeout"
    assert second["retry_count"] == 1
