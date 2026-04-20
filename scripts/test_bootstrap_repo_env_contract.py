#!/usr/bin/env python3
"""Static contract for governance SSOT bootstrap propagation."""

from __future__ import annotations

import os
import shutil
import subprocess
import textwrap
from pathlib import Path


SCRIPT = Path("scripts/bootstrap-repo-env.sh").read_text(encoding="utf-8")
REGISTRY = Path("docs/ENV_REGISTRY.md").read_text(encoding="utf-8")


def check(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"[FAIL] {message}")


def main() -> int:
    check("shlex.quote" in SCRIPT, "bootstrap must quote vault values before exporting")
    check("source \"$SHARED_ENV\"" not in SCRIPT, "bootstrap must not execute .env.shared as shell")
    check("<redacted>" in SCRIPT, "dry-run output must redact assignment values")

    for key in [
        "SOM_MCP_URL",
        "SOM_REMOTE_MCP_AUTH_HMAC_KEY",
        "CF_ACCESS_CLIENT_ID",
        "SOM_OPERATOR_INBOUND_QUEUE_ROOT",
        "SLACK_BOT_USER_OAUTH_TOKEN",
        "SLACK_CODEX_CHANNEL_ID",
        "SLACK_CHANNEL_ID",
        "SLACK_E2E_CHANNEL_ID",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "TWILIO_FROM_NUMBER",
        "TWILIO_SMS_FROM",
        "SOM_TWILIO_FROM_NUMBER",
        "TWILIO_TEST_CONSUMER_NUMBER",
        "OPERATOR_SMS_PHONE",
        "SOM_OPERATOR_SMS_PHONE",
    ]:
        check(f"{key}=" in SCRIPT, f"lam bootstrap missing {key}")
        check(key in REGISTRY, f"ENV registry missing local-ai-machine mapping for {key}")

    run_synthetic_lam_bootstrap()
    run_sibling_worktree_lam_bootstrap()

    print("[PASS] bootstrap repo env contract checks passed")
    return 0


def run_synthetic_lam_bootstrap() -> None:
    """Exercise lam bootstrap with command-like vault values and missing optional keys."""
    import tempfile

    required_vault = """
    CLAUDE_CODE_OAUTH_TOKEN=synthetic-claude-secret
    CLOUDFLARE_MASTER_OPS_TOKEN=synthetic-cloudflare-secret
    CLOUDFLARE_ACCOUNT_ID=synthetic-account
    CLOUDFLARE_ZONE_ID=synthetic-zone
    CLOUDFLARE_TUNNEL_ID=synthetic-tunnel
    CF_TEAM_DOMAIN=synthetic-team
    CF_ACCESS_AUD_TAG=synthetic-aud
    SOM_REMOTE_MCP_STDIO_PROOF_COMMAND=/tmp/synthetic proof command
    SOM_MCP_URL=https://remote-mcp.example.test
    SOM_REMOTE_MCP_AUTH_HMAC_KEY=synthetic-hmac-secret
    CF_ACCESS_CLIENT_ID=synthetic-client-id
    SOM_OPERATOR_INBOUND_QUEUE_ROOT=/tmp/synthetic queue root
    TWILIO_ACCOUNT_SID=synthetic-twilio-sid
    TWILIO_AUTH_TOKEN=synthetic-twilio-secret
    TWILIO_FROM_NUMBER=+15557654321
    TWILIO_SMS_FROM=+15557654321
    SOM_TWILIO_FROM_NUMBER=+15557654321
    TWILIO_TEST_CONSUMER_NUMBER=+15551234567
    OPERATOR_SMS_PHONE=+15551234567
    SOM_OPERATOR_SMS_PHONE=+15551234567
    """

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        script_dir = root / "scripts"
        script_dir.mkdir()
        script_path = script_dir / "bootstrap-repo-env.sh"
        shutil.copy2("scripts/bootstrap-repo-env.sh", script_path)
        script_path.chmod(0o755)
        (root / ".env.shared").write_text(textwrap.dedent(required_vault).strip() + "\n", encoding="utf-8")

        env = os.environ.copy()
        env["DRY_RUN"] = "1"
        result = subprocess.run(
            ["bash", str(script_path), "lam", str(root / "local-ai-machine" / ".env")],
            cwd=root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        check(result.returncode == 0, f"synthetic lam dry-run failed: {result.stderr.strip()}")
        output = result.stdout
        for key in [
            "SOM_MCP_URL",
            "SOM_REMOTE_MCP_AUTH_HMAC_KEY",
            "CF_ACCESS_CLIENT_ID",
            "SOM_OPERATOR_INBOUND_QUEUE_ROOT",
            "SLACK_BOT_USER_OAUTH_TOKEN",
            "TWILIO_ACCOUNT_SID",
            "TWILIO_AUTH_TOKEN",
            "TWILIO_FROM_NUMBER",
            "TWILIO_SMS_FROM",
            "SOM_TWILIO_FROM_NUMBER",
            "TWILIO_TEST_CONSUMER_NUMBER",
            "OPERATOR_SMS_PHONE",
            "SOM_OPERATOR_SMS_PHONE",
        ]:
            check(f"{key}=" in output, f"synthetic lam dry-run missing {key}")
        for secret_value in [
            "synthetic-claude-secret",
            "synthetic-cloudflare-secret",
            "synthetic-hmac-secret",
            "synthetic-twilio-secret",
            "+15557654321",
            "+15551234567",
        ]:
            check(secret_value not in output, f"dry-run leaked synthetic value {secret_value}")


def run_sibling_worktree_lam_bootstrap() -> None:
    """Exercise vault discovery from sibling governance worktrees."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        hldpro_root = Path(tmp) / "HLDPRO"
        primary_root = hldpro_root / "hldpro-governance"
        sibling_root = hldpro_root / "hldpro-governance-sibling-worktree"
        primary_root.mkdir(parents=True)
        (sibling_root / "scripts").mkdir(parents=True)
        script_path = sibling_root / "scripts" / "bootstrap-repo-env.sh"
        shutil.copy2("scripts/bootstrap-repo-env.sh", script_path)
        script_path.chmod(0o755)
        (primary_root / ".env.shared").write_text(
            textwrap.dedent(
                """
                CLAUDE_CODE_OAUTH_TOKEN=synthetic-claude-secret
                CLOUDFLARE_MASTER_OPS_TOKEN=synthetic-cloudflare-secret
                CLOUDFLARE_ACCOUNT_ID=synthetic-account
                CLOUDFLARE_ZONE_ID=synthetic-zone
                CLOUDFLARE_TUNNEL_ID=synthetic-tunnel
                CF_TEAM_DOMAIN=synthetic-team
                CF_ACCESS_AUD_TAG=synthetic-aud
                TWILIO_TEST_CONSUMER_NUMBER=+15551234567
                TWILIO_FROM_NUMBER=+15557654321
                TWILIO_SMS_FROM=+15557654321
                SOM_TWILIO_FROM_NUMBER=+15557654321
                OPERATOR_SMS_PHONE=+15551234567
                SOM_OPERATOR_SMS_PHONE=+15551234567
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        env = os.environ.copy()
        env["DRY_RUN"] = "1"
        result = subprocess.run(
            ["bash", str(script_path), "lam", str(hldpro_root / "local-ai-machine" / ".env")],
            cwd=sibling_root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        check(result.returncode == 0, f"sibling worktree lam dry-run failed: {result.stderr.strip()}")
        check("OPERATOR_SMS_PHONE=<redacted>" in result.stdout, "sibling worktree dry-run missed operator phone")
        check("SOM_TWILIO_FROM_NUMBER=<redacted>" in result.stdout, "sibling worktree dry-run missed SoM sender")


if __name__ == "__main__":
    raise SystemExit(main())
