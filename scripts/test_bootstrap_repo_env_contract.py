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
    check("seek|seek-and-ponder|snp-staging)" in SCRIPT, "bootstrap must support seek alias")
    check("seek-local|snp-local|seek-and-ponder-local)" in SCRIPT, "bootstrap must support seek-local alias")
    check("seek-worktree|snp-worktree|seek-and-ponder-worktree)" in SCRIPT, "bootstrap must support seek-worktree alias")
    check("stampede|Stampede)" in SCRIPT, "bootstrap must support Stampede target")

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

    for key in [
        "SEEK_STAGING_SUPABASE_PROJECT_REF",
        "SEEK_STAGING_SUPABASE_URL",
        "SEEK_STAGING_SUPABASE_ANON_KEY",
        "SEEK_STAGING_SUPABASE_SERVICE_ROLE_KEY",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GOOGLE_OAUTH_CLIENT_ID",
        "GOOGLE_OAUTH_CLIENT_SECRET",
    ]:
        check(f"{key}=" in SCRIPT, f"seek bootstrap missing {key}")
        check(key in REGISTRY, f"ENV registry missing seek-and-ponder mapping for {key}")

    for key in [
        "ALPACA_API_KEY",
        "ALPACA_SECRET_KEY",
        "ALPHA_VANTAGE_API_KEY",
        "POLYGON_API_KEY",
        "MASSIVE_API_KEY",
        "MASSIVE_FLATFILES_ACCESS_KEY_ID",
        "MASSIVE_FLATFILES_SECRET_ACCESS_KEY",
        "INTRINIO_API_KEY",
        "TRADIER_API_TOKEN",
        "TRADIER_ACCOUNT_ID",
        "TRADIER_ENV",
        "TRADIER_BASE_URL",
        "X_BEARER_TOKEN",
    ]:
        check(f"{key}=" in SCRIPT, f"stampede bootstrap missing {key}")
        check(key in REGISTRY, f"ENV registry missing Stampede mapping for {key}")

    run_synthetic_lam_bootstrap()
    run_sibling_worktree_lam_bootstrap()
    run_nested_var_worktree_lam_bootstrap()
    run_synthetic_seek_bootstrap()
    run_synthetic_stampede_bootstrap()

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
    TWILIO_FROM_NUMBER=SYNTHETIC-FROM-555
    TWILIO_SMS_FROM=SYNTHETIC-FROM-555
    SOM_TWILIO_FROM_NUMBER=SYNTHETIC-FROM-555
    TWILIO_TEST_CONSUMER_NUMBER=SYNTHETIC-CONSUMER-555
    OPERATOR_SMS_PHONE=SYNTHETIC-CONSUMER-555
    SOM_OPERATOR_SMS_PHONE=SYNTHETIC-CONSUMER-555
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
            "SYNTHETIC-FROM-555",
            "SYNTHETIC-CONSUMER-555",
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
                TWILIO_TEST_CONSUMER_NUMBER=SYNTHETIC-CONSUMER-555
                TWILIO_FROM_NUMBER=SYNTHETIC-FROM-555
                TWILIO_SMS_FROM=SYNTHETIC-FROM-555
                SOM_TWILIO_FROM_NUMBER=SYNTHETIC-FROM-555
                OPERATOR_SMS_PHONE=SYNTHETIC-CONSUMER-555
                SOM_OPERATOR_SMS_PHONE=SYNTHETIC-CONSUMER-555
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


def run_nested_var_worktree_lam_bootstrap() -> None:
    """Exercise vault discovery from HLDPRO/var/worktrees/* governance worktrees."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        hldpro_root = Path(tmp) / "HLDPRO"
        primary_root = hldpro_root / "hldpro-governance"
        worktree_root = hldpro_root / "var" / "worktrees" / "hldpro-governance-issue-430"
        primary_root.mkdir(parents=True)
        (worktree_root / "scripts").mkdir(parents=True)
        script_path = worktree_root / "scripts" / "bootstrap-repo-env.sh"
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
                OPERATOR_SMS_PHONE=SYNTHETIC-CONSUMER-555
                SOM_OPERATOR_SMS_PHONE=SYNTHETIC-CONSUMER-555
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        env = os.environ.copy()
        env["DRY_RUN"] = "1"
        result = subprocess.run(
            ["bash", str(script_path), "lam", str(hldpro_root / "local-ai-machine" / ".env")],
            cwd=worktree_root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        check(result.returncode == 0, f"nested var worktree lam dry-run failed: {result.stderr.strip()}")
        check("OPERATOR_SMS_PHONE=<redacted>" in result.stdout, "nested var worktree dry-run missed operator phone")


def run_synthetic_seek_bootstrap() -> None:
    """Exercise Seek/Ponder bootstrap aliases without leaking synthetic values."""
    import tempfile

    required_vault = """
    SEEK_STAGING_SUPABASE_URL=https://seek-staging.example.test
    SEEK_STAGING_SUPABASE_ANON_KEY=synthetic-seek-anon
    SEEK_STAGING_SUPABASE_SERVICE_ROLE_KEY=synthetic-seek-service
    SEEK_STAGING_SUPABASE_PROJECT_REF=synthetic-seek-ref
    SEEK_LOCAL_SUPABASE_URL=http://127.0.0.1:54321
    SEEK_LOCAL_SUPABASE_ANON_KEY=synthetic-seek-local-anon
    SEEK_LOCAL_SUPABASE_SERVICE_ROLE_KEY=synthetic-seek-local-service
    SEEK_OPENAI_API_KEY=synthetic-openai-secret
    SEEK_ANTHROPIC_API_KEY=synthetic-anthropic-secret
    SUPABASE_ACCESS_TOKEN=synthetic-supabase-token
    STRIPE_SECRET_KEY=synthetic-stripe-secret
    STRIPE_WEBHOOK_SECRET=synthetic-webhook-secret
    RESEND_API_KEY=synthetic-resend-secret
    GOOGLE_OAUTH_CLIENT_ID=synthetic-google-client
    GOOGLE_OAUTH_CLIENT_SECRET=synthetic-google-secret
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
            ["bash", str(script_path), "seek", str(root / "seek-and-ponder" / ".env")],
            cwd=root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        check(result.returncode == 0, f"synthetic seek dry-run failed: {result.stderr.strip()}")
        for key in [
            "SUPABASE_URL",
            "SEEK_STAGING_SUPABASE_PROJECT_REF",
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GOOGLE_OAUTH_CLIENT_SECRET",
        ]:
            check(f"{key}=" in result.stdout, f"synthetic seek dry-run missing {key}")
        for secret_value in [
            "synthetic-seek-service",
            "synthetic-openai-secret",
            "synthetic-anthropic-secret",
            "synthetic-google-secret",
        ]:
            check(secret_value not in result.stdout, f"seek dry-run leaked synthetic value {secret_value}")


def run_synthetic_stampede_bootstrap() -> None:
    """Exercise Stampede bootstrap with production Tradier mapping and redaction."""
    import tempfile

    required_vault = """
    ALPACA_API_KEY=synthetic-alpaca-key
    ALPACA_SECRET_KEY=synthetic-alpaca-secret
    ALPHA_VANTAGE_API_KEY=synthetic-alpha-vantage
    MASSIVE_API_KEY=synthetic-massive-key
    MASSIVE_FLATFILES_ACCESS_KEY_ID=synthetic-massive-access
    MASSIVE_FLATFILES_SECRET_ACCESS_KEY=synthetic-massive-secret
    TRADIER_API_TOKEN=synthetic-tradier-sandbox
    TRADIER_PRODUCTION_API_TOKEN=synthetic-tradier-production
    TRADIER_ACCOUNT_ID=synthetic-tradier-account
    TRADIER_PRODUCTION_BASE_URL=https://api.tradier.example.test/v1
    X_BEARER_TOKEN=synthetic-x-bearer
    STAMPEDE_ANTHROPIC_API_KEY=synthetic-stampede-anthropic
    STAMPEDE_OPENAI_API_KEY=synthetic-stampede-openai
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
            ["bash", str(script_path), "stampede", str(root / "Stampede" / ".env")],
            cwd=root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        check(result.returncode == 0, f"synthetic stampede dry-run failed: {result.stderr.strip()}")
        for key in [
            "ALPACA_API_KEY",
            "POLYGON_API_KEY",
            "MASSIVE_FLATFILES_SECRET_ACCESS_KEY",
            "TRADIER_API_TOKEN",
            "TRADIER_ENV",
            "TRADIER_BASE_URL",
            "X_BEARER_TOKEN",
        ]:
            check(f"{key}=" in result.stdout, f"synthetic stampede dry-run missing {key}")
        for secret_value in [
            "synthetic-alpaca-secret",
            "synthetic-massive-secret",
            "synthetic-tradier-production",
            "synthetic-x-bearer",
        ]:
            check(secret_value not in result.stdout, f"stampede dry-run leaked synthetic value {secret_value}")


if __name__ == "__main__":
    raise SystemExit(main())
