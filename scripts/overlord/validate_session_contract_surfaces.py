#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_FILES = (
    Path("AGENT_REGISTRY.md"),
    Path("CODEX.md"),
    Path("CLAUDE.md"),
    Path("STANDARDS.md"),
    Path("docs/EXTERNAL_SERVICES_RUNBOOK.md"),
    Path("docs/hldpro-sim-consumer-pull-state.json"),
    Path("docs/schemas/governance-specialist-output.schema.json"),
    Path("agents/gov-specialist-planner.md"),
    Path("agents/gov-specialist-auditor.md"),
    Path("agents/gov-specialist-qa.md"),
    Path("agents/gov-specialist-local-repo-researcher.md"),
    Path("agents/gov-specialist-web-researcher.md"),
    Path("hooks/pre-session-context.sh"),
    Path(".claude/hooks/pre-session-context.sh"),
    Path(".claude/settings.json"),
    Path("scripts/packet/run_specialist_packet.py"),
    Path("scripts/session_bootstrap_contract.py"),
)
HOOK_HELPER_NEEDLE = 'python3 "$REPO_ROOT/scripts/session_bootstrap_contract.py" --emit-hook-note'
RUNBOOK_HOOK_NOTE = "python3 scripts/session_bootstrap_contract.py --emit-hook-note"
RUNBOOK_BOOTSTRAP_COMMAND = "bash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh <repo>"
CODEX_ROUTE_NEEDLE = "neither side may absorb the other side's pinned role"
CLAUDE_ROUTE_NEEDLE = "Every governed code/doc/config change must end with a distinct pinned auditor or QA specialist review before merge or closeout."
STANDARDS_ROUTE_NEEDLE = "Primary-session dispatch is hard-gated in both directions."
RUNBOOK_PACKET_NEEDLE = "bash scripts/codex-review.sh claude <packet-file>"
RUNBOOK_SPECIALIST_NEEDLE = "python3 scripts/packet/run_specialist_packet.py --packet <packet-file> --persona-id <persona-id>"
STANDARDS_SPECIALIST_NEEDLE = "Governance specialist planner, auditor, QA, local-repo researcher, and web/external researcher lanes must run through `python3 scripts/packet/run_specialist_packet.py --packet <packet-file> --persona-id <persona-id>`."
CODEX_SPECIALIST_NEEDLE = "Declared Codex-side governance specialist lanes are packet-backed only"
AGENT_REGISTRY_NEEDLES = (
    "| gov-specialist-planner | hldpro-governance |",
    "| gov-specialist-auditor | hldpro-governance |",
    "| gov-specialist-qa | hldpro-governance |",
    "| gov-specialist-local-repo-researcher | hldpro-governance |",
    "| gov-specialist-web-researcher | hldpro-governance |",
)
SIM_PULL_STATE_NEEDLES = (
    "gov-specialist-planner.json",
    "gov-specialist-auditor.json",
    "gov-specialist-qa.json",
    "gov-specialist-local-repo-researcher.json",
    "gov-specialist-web-researcher.json",
)
RUNNER_NEEDLES = (
    "OUTPUT_SCHEMA_PATH",
    "PersonaLoader.from_package",
    "emit_dispatch_packet",
)


def _normalized(text: str) -> str:
    return " ".join(text.split())


def _find_hook_command(entries: object, matcher: str | None, needle: str) -> bool:
    if not isinstance(entries, list):
        return False
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if matcher is not None and entry.get("matcher") != matcher:
            continue
        hooks = entry.get("hooks")
        if not isinstance(hooks, list):
            continue
        for hook in hooks:
            if not isinstance(hook, dict):
                continue
            command = hook.get("command")
            if isinstance(command, str) and needle in command:
                return True
    return False


def validate(root: Path) -> list[str]:
    failures: list[str] = []
    missing = [path.as_posix() for path in REQUIRED_FILES if not (root / path).is_file()]
    if missing:
        failures.append(
            "governance session-contract surfaces missing: " + ", ".join(missing)
        )
        return failures

    try:
        payload = json.loads((root / ".claude/settings.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f".claude/settings.json could not be parsed as JSON: {exc}"]

    hooks = payload.get("hooks", {})
    if not isinstance(hooks, dict):
        return [".claude/settings.json must expose a top-level `hooks` object"]

    if not _find_hook_command(
        hooks.get("UserPromptSubmit"),
        None,
        "hooks/pre-session-context.sh",
    ):
        failures.append(
            ".claude/settings.json must expose a UserPromptSubmit command that invokes hooks/pre-session-context.sh"
        )

    if not _find_hook_command(
        hooks.get("PostToolUse"),
        "*",
        "hooks/check-errors.sh",
    ):
        failures.append(
            ".claude/settings.json must expose PostToolUse matcher '*' with a command invoking hooks/check-errors.sh"
        )

    for rel_path in ("hooks/pre-session-context.sh", ".claude/hooks/pre-session-context.sh"):
        content = (root / rel_path).read_text(encoding="utf-8")
        if HOOK_HELPER_NEEDLE not in content:
            failures.append(f"{rel_path} must invoke scripts/session_bootstrap_contract.py with --emit-hook-note")

    runbook_text = (root / "docs/EXTERNAL_SERVICES_RUNBOOK.md").read_text(encoding="utf-8")
    runbook_norm = _normalized(runbook_text)
    if RUNBOOK_HOOK_NOTE not in runbook_text:
        failures.append("docs/EXTERNAL_SERVICES_RUNBOOK.md must document the canonical session bootstrap hook note path")
    if RUNBOOK_BOOTSTRAP_COMMAND not in runbook_text:
        failures.append("docs/EXTERNAL_SERVICES_RUNBOOK.md must document the canonical bootstrap command")
    if _normalized(RUNBOOK_PACKET_NEEDLE) not in runbook_norm:
        failures.append("docs/EXTERNAL_SERVICES_RUNBOOK.md must document the file-backed Claude packet review path")
    if _normalized(RUNBOOK_SPECIALIST_NEEDLE) not in runbook_norm:
        failures.append("docs/EXTERNAL_SERVICES_RUNBOOK.md must document the specialist packet runner path")

    codex_text = (root / "CODEX.md").read_text(encoding="utf-8")
    codex_norm = _normalized(codex_text)
    if _normalized(CODEX_ROUTE_NEEDLE) not in codex_norm:
        failures.append("CODEX.md must hard-gate bidirectional Codex <> Claude role dispatch")
    if _normalized(CODEX_SPECIALIST_NEEDLE) not in codex_norm:
        failures.append("CODEX.md must require packet-backed Codex-side governance specialist lanes")

    claude_text = (root / "CLAUDE.md").read_text(encoding="utf-8")
    claude_norm = _normalized(claude_text)
    if _normalized(CLAUDE_ROUTE_NEEDLE) not in claude_norm:
        failures.append("CLAUDE.md must require end-of-change pinned auditor or QA specialist review")

    standards_text = (root / "STANDARDS.md").read_text(encoding="utf-8")
    standards_norm = _normalized(standards_text)
    if _normalized(STANDARDS_ROUTE_NEEDLE) not in standards_norm:
        failures.append("STANDARDS.md must declare primary-session dispatch as a hard gate")
    if _normalized(STANDARDS_SPECIALIST_NEEDLE) not in standards_norm:
        failures.append("STANDARDS.md must declare the packet-backed governance specialist runner contract")

    registry_text = (root / "AGENT_REGISTRY.md").read_text(encoding="utf-8")
    for needle in AGENT_REGISTRY_NEEDLES:
        if needle not in registry_text:
            failures.append("AGENT_REGISTRY.md must register the governance specialist packet lanes")
            break

    sim_pull_state_text = (root / "docs/hldpro-sim-consumer-pull-state.json").read_text(encoding="utf-8")
    for needle in SIM_PULL_STATE_NEEDLES:
        if needle not in sim_pull_state_text:
            failures.append("docs/hldpro-sim-consumer-pull-state.json must expose governance specialist personas")
            break

    runner_text = (root / "scripts/packet/run_specialist_packet.py").read_text(encoding="utf-8")
    for needle in RUNNER_NEEDLES:
        if needle not in runner_text:
            failures.append("scripts/packet/run_specialist_packet.py must preserve the tracked packet runner contract")
            break

    helper_text = (root / "scripts/session_bootstrap_contract.py").read_text(encoding="utf-8")
    for needle in ('parser.add_argument("--emit-hook-note"', "docs/EXTERNAL_SERVICES_RUNBOOK.md", "docs/FAIL_FAST_LOG.md"):
        if needle not in helper_text:
            failures.append(f"scripts/session_bootstrap_contract.py must include `{needle}` in the canonical session contract")

    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate tracked governance session-contract surfaces.")
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    failures = validate(root)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print("PASS governance session contract surfaces present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
