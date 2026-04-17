#!/usr/bin/env python3
"""Build the org-level governance rules compendium.

The compendium is intentionally deterministic and heuristic. It indexes the
governance/rules surface from the canonical governed repos without requiring an
LLM during weekly sweep.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_REPOS_ROOT = Path(os.environ.get("HLDPRO_REPOS_ROOT", str(Path.home() / "Developer" / "HLDPRO")))
DEFAULT_OUTPUT = Path("docs/ORG_GOVERNANCE_COMPENDIUM.md")

REPOS = [
    ("hldpro-governance", "hldpro-governance", "Governance standards, reusable CI, agents, and cross-repo audit tooling"),
    ("ai-integration-services", "ai-integration-services", "AIS SaaS platform governance, CI, hooks, and specialist agents"),
    ("HealthcarePlatform", "healthcareplatform", "HIPAA platform governance, CI, hooks, and specialist agents"),
    ("local-ai-machine", "local-ai-machine", "Local AI runtime governance, packet controls, lane rules, and schemas"),
    ("knocktracker", "knocktracker", "Field app governance, issue controls, security/privacy agents, and CI"),
    ("ASC-Evaluator", "asc-evaluator", "Knowledge/evaluation repo with limited governance and graph coverage"),
]

ROOT_RULE_FILES = {
    "AGENT_REGISTRY.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CODEX.md",
    "DEPENDENCIES.md",
    "GITHUB_ENTERPRISE_ADOPTION_PLAN.md",
    "GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md",
    "GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md",
    "GITHUB_ENTERPRISE_RULESET_RECOMMENDATIONS.md",
    "GITHUB_ENTERPRISE_SPRINT1_TASKS.md",
    "OVERLORD_BACKLOG.md",
    "README.md",
    "STANDARDS.md",
}

DOC_RULE_FILES = {
    "docs/COMPENDIUM.md",
    "docs/COMPENDIUM_INDEX.md",
    "docs/DATA_DICTIONARY.md",
    "docs/ENV_REGISTRY.md",
    "docs/ERROR_PATTERNS.md",
    "docs/EXTERNAL_SERVICES_RUNBOOK.md",
    "docs/FAIL_FAST_LOG.md",
    "docs/FEATURE_REGISTRY.md",
    "docs/PROGRESS.md",
    "docs/SERVICE_REGISTRY.md",
    "docs/exception-register.md",
    "docs/graphify_targets.json",
}

PATH_PREFIXES = (
    ".agents/",
    ".claude/agents/",
    ".claude/commands/",
    ".claude/hooks/",
    ".claude/plans/",
    ".claude/skills/",
    ".github/workflows/",
    "agents/",
    "backend/.agents/",
    "backend/docs/schemas/",
    "backend/schemas/",
    "docs/agents/",
    "docs/plans/",
    "docs/runbooks/",
    "docs/schemas/",
    "schemas/",
    "scripts/lam/",
    "scripts/overlord/",
    "scripts/packet/",
    "scripts/windows-ollama/",
)

PATH_SUFFIXES = (
    ".schema.json",
    ".schema.md",
    ".schema.yml",
)


@dataclass(frozen=True)
class RepoInfo:
    name: str
    graph_slug: str
    purpose: str
    path: Path


@dataclass(frozen=True)
class FileInfo:
    path: str
    category: str
    description: str
    logic: str
    interactions: str


def run(cmd: list[str], cwd: Path) -> str:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed in {cwd}: {proc.stderr.strip()}")
    return proc.stdout


def tracked_files(repo_path: Path) -> list[str]:
    if not (repo_path / ".git").exists():
        return []
    out = run(["git", "ls-files"], repo_path)
    return sorted(line.strip() for line in out.splitlines() if line.strip())


def is_rule_file(path: str, repo_name: str) -> bool:
    if path in ROOT_RULE_FILES or path in DOC_RULE_FILES:
        return True
    if repo_name == "hldpro-governance" and path.startswith("hooks/"):
        return True
    if "/" not in path and path.endswith(".md"):
        return True
    if path.endswith(PATH_SUFFIXES):
        return True
    return any(path.startswith(prefix) for prefix in PATH_PREFIXES)


def read_text(path: Path, limit: int = 40000) -> str:
    try:
        return path.read_text(errors="ignore")[:limit]
    except OSError:
        return ""


def category_for(path: str) -> str:
    if path.startswith(".github/workflows/"):
        return "workflow"
    if path.endswith("settings.json"):
        return "settings"
    if "/hooks/" in path or path.startswith("hooks/"):
        return "hook"
    if "/agents/" in path or path.startswith("agents/") or path.startswith(".agents/") or path.startswith("backend/.agents/"):
        return "agent"
    if path.endswith(PATH_SUFFIXES) or path.startswith("schemas/") or path.startswith("docs/schemas/"):
        return "schema"
    if path.startswith("scripts/"):
        return "script"
    if path.startswith("docs/plans/"):
        return "pdcar-plan"
    if path.endswith(".md"):
        return "policy-doc"
    return "governance-file"


def first_heading(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return ""


def frontmatter_field(text: str, field: str) -> str:
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    if len(parts) < 3:
        return ""
    for line in parts[1].splitlines():
        if line.startswith(f"{field}:"):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def first_comment(text: str) -> str:
    for line in text.splitlines()[:30]:
        stripped = line.strip()
        if stripped.startswith("#") and not stripped.startswith("#!"):
            return stripped.lstrip("#").strip()
        if stripped.startswith('"""') and stripped.strip('"'):
            return stripped.strip('"').strip()
        if stripped.startswith("//"):
            return stripped.lstrip("/").strip()
    return ""


def workflow_logic(text: str) -> tuple[str, str]:
    name = ""
    jobs: list[str] = []
    uses: list[str] = []
    events: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("name:") and not name:
            name = stripped.split(":", 1)[1].strip()
        if re.match(r"^[A-Za-z0-9_-]+:\s*$", line) and line.startswith("  "):
            key = stripped[:-1]
            if key not in {"steps", "with", "env", "permissions", "outputs"}:
                jobs.append(key)
        if stripped.startswith("uses:"):
            uses.append(stripped.split(":", 1)[1].strip())
        if stripped in {"pull_request:", "push:", "workflow_call:", "workflow_dispatch:", "schedule:"}:
            events.append(stripped.rstrip(":"))
    logic = f"Workflow {name or 'unnamed'}"
    if events:
        logic += f"; triggers: {', '.join(sorted(set(events)))}"
    if jobs:
        logic += f"; jobs: {', '.join(sorted(set(jobs))[:8])}"
    interactions = f"Uses {', '.join(sorted(set(uses))[:8])}" if uses else "Runs local shell/Python governance checks"
    return logic, interactions


def settings_logic(text: str) -> tuple[str, str]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return "Claude settings file; JSON parse failed", "Hook interactions unavailable"
    commands: list[str] = []
    hooks = data.get("hooks", {})
    if isinstance(hooks, dict):
        for phase, entries in hooks.items():
            if not isinstance(entries, list):
                continue
            for entry in entries:
                matcher = entry.get("matcher", "*") if isinstance(entry, dict) else "*"
                for hook in entry.get("hooks", []) if isinstance(entry, dict) else []:
                    if isinstance(hook, dict) and hook.get("command"):
                        commands.append(f"{phase}:{matcher} -> {hook['command']}")
    logic = f"Claude settings wiring {len(commands)} hook command(s)"
    interactions = "; ".join(commands[:6]) if commands else "No hook commands detected"
    return logic, interactions


def script_logic(path: str, text: str) -> tuple[str, str]:
    funcs = re.findall(r"^(?:def|function)\s+([A-Za-z0-9_ -]+)|^([A-Za-z0-9_:-]+)\(\)\s*\{", text, re.M)
    names = [a or b for a, b in funcs if a or b]
    refs = sorted(set(re.findall(r"[\w./-]+(?:\.md|\.yml|\.yaml|\.json|\.sh|\.py)", text)))
    logic = f"Executable {Path(path).name}"
    if names:
        logic += f"; functions: {', '.join(names[:8])}"
    interactions = f"References {', '.join(refs[:8])}" if refs else "No explicit file references detected"
    return logic, interactions


def markdown_logic(text: str) -> tuple[str, str]:
    headings = [line.lstrip("#").strip() for line in text.splitlines() if line.startswith("## ")]
    refs = sorted(set(re.findall(r"`([^`]+(?:\.md|\.yml|\.yaml|\.json|\.sh|\.py))`", text)))
    logic = f"Sections: {', '.join(headings[:6])}" if headings else "Markdown policy or agent instruction document"
    interactions = f"References {', '.join(refs[:8])}" if refs else "No explicit file references detected"
    return logic, interactions


def describe_file(repo_path: Path, rel: str) -> FileInfo:
    text = read_text(repo_path / rel)
    category = category_for(rel)
    description = (
        frontmatter_field(text, "description")
        or first_heading(text)
        or first_comment(text)
        or f"{category} file"
    )
    if category == "workflow":
        logic, interactions = workflow_logic(text)
    elif category == "settings":
        logic, interactions = settings_logic(text)
    elif category in {"hook", "script"}:
        logic, interactions = script_logic(rel, text)
    elif category in {"policy-doc", "agent", "pdcar-plan"}:
        logic, interactions = markdown_logic(text)
    elif category == "schema":
        logic, interactions = schema_logic(text)
    else:
        logic, interactions = "Governance support artifact", "No explicit interactions detected"
    return FileInfo(rel, category, one_line(description), one_line(logic), one_line(interactions))


def schema_logic(text: str) -> tuple[str, str]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return "Schema document or non-JSON schema", "Validates governed artifact shape"
    title = data.get("title") or data.get("$id") or "JSON schema"
    required = data.get("required", [])
    props = data.get("properties", {})
    logic = f"{title}; required: {', '.join(required[:8]) if isinstance(required, list) else 'n/a'}"
    interactions = f"Defines properties: {', '.join(list(props)[:10])}" if isinstance(props, dict) else "Defines schema contract"
    return logic, interactions


def one_line(value: str) -> str:
    cleaned = re.sub(r"\s+", " ", value or "").strip()
    cleaned = cleaned.replace(str(Path.home()), "~")
    return cleaned[:240] if len(cleaned) > 240 else cleaned


def esc(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def graph_summary(governance_root: Path, graph_slug: str) -> dict[str, object]:
    graph_dir = governance_root / "graphify-out" / graph_slug
    graph_file = graph_dir / "graph.json"
    report_file = graph_dir / "GRAPH_REPORT.md"
    summary: dict[str, object] = {
        "nodes": 0,
        "edges": 0,
        "hyperedges": 0,
        "god_nodes": [],
        "communities": [],
        "report": f"graphify-out/{graph_slug}/GRAPH_REPORT.md" if report_file.exists() else "",
    }
    if graph_file.exists():
        try:
            data = json.loads(graph_file.read_text())
            summary["nodes"] = len(data.get("nodes", []))
            summary["edges"] = len(data.get("links", []))
            summary["hyperedges"] = len(data.get("hyperedges", []))
            degree: dict[str, int] = {}
            labels: dict[str, str] = {}
            for node in data.get("nodes", []):
                node_id = str(node.get("id") or node.get("name") or "")
                labels[node_id] = str(node.get("label") or node_id)
                degree.setdefault(node_id, 0)
            for edge in data.get("links", []):
                for key in ("source", "target"):
                    node_id = str(edge.get(key, ""))
                    degree[node_id] = degree.get(node_id, 0) + 1
            summary["god_nodes"] = [
                f"{labels.get(node_id, node_id)} ({count})"
                for node_id, count in sorted(degree.items(), key=lambda item: item[1], reverse=True)[:10]
                if node_id
            ]
        except (json.JSONDecodeError, OSError):
            pass
    if report_file.exists():
        text = read_text(report_file, 12000)
        communities = re.findall(r'^### Community \d+ - "([^"]+)"', text, re.M)
        summary["communities"] = communities[:10]
    return summary


def build(repos_root: Path, governance_root: Path, output: Path) -> str:
    today = dt.date.today().isoformat()
    repo_infos = [
        RepoInfo(
            name,
            slug,
            purpose,
            governance_root if name == "hldpro-governance" else repos_root / name,
        )
        for name, slug, purpose in REPOS
    ]
    lines: list[str] = []
    lines.append("# HLD Pro Org Governance Rules Compendium")
    lines.append("")
    lines.append(f"> Generated: {today}")
    lines.append("> Source: `scripts/overlord/build_org_governance_compendium.py`")
    lines.append("> Scope: canonical governed repos only; `_worktrees/` and issue-specific local clones are excluded.")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append("This file is the single org-level index of governance rules, enforcement files, rule logic, and graph nodes across the HLD Pro governed repository portfolio. It is designed to refresh during the weekly overlord sweep so changed repo rules become visible without manual inventory work.")
    lines.append("")
    lines.append("## Update Contract")
    lines.append("")
    lines.append("- Generator: `python3 scripts/overlord/build_org_governance_compendium.py`")
    lines.append("- Check mode: `python3 scripts/overlord/build_org_governance_compendium.py --check`")
    lines.append("- Weekly sweep should run the generator after governed repos are checked out and before graph/metrics persistence.")
    lines.append("- Generated output is committed in governance with graph and metrics refreshes.")
    lines.append("")
    lines.append("## Portfolio Index")
    lines.append("")
    lines.append("| Repo | Purpose | Rule Files | Graph Nodes | Graph Edges |")
    lines.append("|------|---------|-----------:|------------:|------------:|")
    repo_file_infos: dict[str, list[FileInfo]] = {}
    graph_infos: dict[str, dict[str, object]] = {}
    for repo in repo_infos:
        files = [path for path in tracked_files(repo.path) if is_rule_file(path, repo.name)]
        infos = [describe_file(repo.path, path) for path in files]
        repo_file_infos[repo.name] = infos
        g = graph_summary(governance_root, repo.graph_slug)
        graph_infos[repo.name] = g
        lines.append(
            f"| `{repo.name}` | {esc(repo.purpose)} | {len(infos)} | {g['nodes']} | {g['edges']} |"
        )
    lines.append("")
    lines.append("## Org-Level Rule Map")
    lines.append("")
    lines.append("| Rule Surface | Source Files | Enforcement / Interaction |")
    lines.append("|--------------|--------------|---------------------------|")
    lines.append("| Shared standards | `hldpro-governance/STANDARDS.md`, repo `CLAUDE.md`, repo `AGENTS.md` | Defines required docs, hooks, CI gates, security tiers, PDCA/R closeout, and delegation authority. |")
    lines.append("| GitHub merge gates | `.github/workflows/governance.yml`, governance reusable workflows | Repo PR workflows call governance-owned reusable gates for doc co-staging, model pins, cross-review, PII routing, fail-fast schemas, and issue/backlog sync. |")
    lines.append("| Claude/Codex runtime gates | `.claude/settings.json`, `.claude/hooks/*`, `hooks/*` | PreToolUse/UserPromptSubmit/Stop hooks enforce branch safety, scope plans, error checking, backlog-first behavior, and session context. |")
    lines.append("| Agent authority | `AGENT_REGISTRY.md`, `.claude/agents/*`, `.agents/*`, `backend/.agents/*`, `agents/*` | Defines supervisor/worker roles, model floors, write scopes, max loops, no self-approval, and repo-specific specialist coverage. |")
    lines.append("| Evidence and memory | `docs/FAIL_FAST_LOG.md`, `docs/ERROR_PATTERNS.md`, `MEMORY.md`, raw closeouts | Captures repeated failures, memory entries, operator context, and closeout evidence for future sessions. |")
    lines.append("| Graph/wiki knowledge | `graphify-out/*`, `wiki/*`, `scripts/knowledge_base/*` | Turns repo files into nodes/edges/communities and feeds the weekly knowledge-base write-back. |")
    lines.append("")
    for repo in repo_infos:
        infos = repo_file_infos[repo.name]
        graph = graph_infos[repo.name]
        lines.append(f"## `{repo.name}`")
        lines.append("")
        lines.append(repo.purpose)
        lines.append("")
        lines.append("### Graph Nodes And Communities")
        lines.append("")
        lines.append(f"- Graph report: `{graph.get('report') or 'not available'}`")
        lines.append(f"- Nodes / edges / hyperedges: `{graph.get('nodes')}` / `{graph.get('edges')}` / `{graph.get('hyperedges')}`")
        god_nodes = graph.get("god_nodes") or []
        communities = graph.get("communities") or []
        lines.append(f"- Top nodes: {', '.join(f'`{item}`' for item in god_nodes[:8]) if god_nodes else 'not available'}")
        lines.append(f"- Top communities: {', '.join(f'`{item}`' for item in communities[:8]) if communities else 'not available'}")
        lines.append("")
        lines.append("### Governance File Index")
        lines.append("")
        lines.append("| File | Category | What It Does | Logic | Interactions / Nodes |")
        lines.append("|------|----------|--------------|-------|----------------------|")
        for info in infos:
            lines.append(
                f"| `{esc(info.path)}` | {esc(info.category)} | {esc(info.description)} | {esc(info.logic)} | {esc(info.interactions)} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build org governance compendium")
    parser.add_argument("--repos-root", type=Path, default=DEFAULT_REPOS_ROOT)
    parser.add_argument(
        "--governance-root",
        type=Path,
        default=None,
        help="hldpro-governance checkout root; defaults to the current working directory",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail if output is stale")
    args = parser.parse_args()

    output = args.output
    if not output.is_absolute():
        output = Path.cwd() / output
    governance_root = args.governance_root or Path.cwd()
    if not governance_root.is_absolute():
        governance_root = Path.cwd() / governance_root
    content = build(args.repos_root, governance_root, output)
    if args.check:
        existing = output.read_text(errors="ignore") if output.exists() else ""
        if existing != content:
            print(f"{output} is stale; run build_org_governance_compendium.py", file=sys.stderr)
            return 1
        print(f"{output} is current")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
