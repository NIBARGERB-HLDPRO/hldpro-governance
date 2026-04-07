#!/usr/bin/env python3
"""Codex ingestion helpers for weekly overlord review flow."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_INGESTION_ROOT = Path.home() / "Developer" / "hldpro" / ".codex-ingestion"
DEFAULT_REPOS = [
    "ai-integration-services",
    "HealthcarePlatform",
    "local-ai-machine",
    "knocktracker",
]
MAX_DIFFSTAT_CHARS = 12000
MAX_PATCH_CHARS = 160000
MAX_CHANGED_FILES = 200
SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
BUG_CATEGORIES = {"security", "error-handling", "testing"}
SECTION_MAPPINGS = {
    "security": ("INFRA", "SECURITY", "GOVERNANCE"),
    "error-handling": ("INFRA", "BUILD", "PIPELINE"),
    "architecture": ("INFRA", "GOVERNANCE"),
    "performance": ("PIPELINE", "INFRA", "FRONTEND"),
    "testing": ("TEST", "BUILD", "PIPELINE"),
    "docs": ("GOVERNANCE", "INFRA", "BUILD"),
}


@dataclass
class Finding:
    finding_id: str
    severity: str
    category: str
    file: str
    line: int
    title: str
    detail: str
    suggestion: str

    @property
    def priority(self) -> str:
        if self.severity in {"CRITICAL", "HIGH"}:
            return "P1"
        if self.severity == "MEDIUM":
            return "MED"
        return "LOW"

    @property
    def fail_fast_severity(self) -> str:
        if self.severity == "CRITICAL":
            return "P0"
        if self.severity == "HIGH":
            return "P1"
        if self.severity == "MEDIUM":
            return "P2"
        return "P3"

    @property
    def est_hours(self) -> str:
        if self.severity == "CRITICAL":
            return "6"
        if self.severity == "HIGH":
            return "4"
        if self.severity == "MEDIUM":
            return "2"
        if self.severity == "LOW":
            return "1"
        return "0.5"


def today_string() -> str:
    return subprocess.run(
        ["date", "+%Y-%m-%d"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def extract_json_from_stdout(stdout: str) -> dict[str, Any]:
    for line in reversed(stdout.splitlines()):
        candidate = line.strip()
        if not candidate.startswith("{"):
            continue
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    raise json.JSONDecodeError("no JSON object found in stdout", stdout, 0)


def summarize_failure_output(stderr: str, stdout: str) -> str:
    ignored_prefixes = (
        "OpenAI Codex v",
        "workdir:",
        "model:",
        "provider:",
        "approval:",
        "sandbox:",
        "reasoning effort:",
        "reasoning summaries:",
        "session id:",
        "user",
        "codex",
        "tokens used",
        "Reading additional input from stdin",
        "--------",
    )
    candidates: list[str] = []
    for stream in (stderr, stdout):
        for raw_line in stream.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if any(line.startswith(prefix) for prefix in ignored_prefixes):
                continue
            candidates.append(line)
    if candidates:
        return " | ".join(candidates[-3:])
    return (stderr.strip() or stdout.strip() or "codex exec failed").strip()


def skip_payload(repo: str, date: str, reason: str) -> dict[str, Any]:
    return {"repo": repo, "date": date, "skipped": True, "reason": reason}


def list_backlog_files(repo: str, ingestion_root: Path) -> list[Path]:
    repo_dir = ingestion_root / repo
    if not repo_dir.exists():
        return []
    return sorted(repo_dir.glob("backlog-*.md"))


def git_lines(repo_path: Path, *args: str) -> list[str]:
    output = run(["git", *args], cwd=repo_path).stdout
    return [line for line in output.splitlines() if line.strip()]


def bounded_text(value: str, limit: int) -> str:
    text = value.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n...[truncated]..."


def build_review_context(repo_path: Path, base_parent: str, head_sha: str, commit_shas: list[str]) -> str:
    commit_subjects = git_lines(repo_path, "log", "--format=%h %s", f"{base_parent}..{head_sha}")
    changed_files = git_lines(repo_path, "diff", "--name-only", f"{base_parent}..{head_sha}")
    diffstat = run(["git", "diff", "--stat", f"{base_parent}..{head_sha}"], cwd=repo_path).stdout
    patch = run(["git", "diff", "--unified=3", f"{base_parent}..{head_sha}"], cwd=repo_path).stdout

    commit_block = "\n".join(commit_subjects[:50]) if commit_subjects else "(none)"
    file_block = "\n".join(changed_files[:MAX_CHANGED_FILES]) if changed_files else "(none)"
    if len(changed_files) > MAX_CHANGED_FILES:
        file_block += f"\n...[+{len(changed_files) - MAX_CHANGED_FILES} more files]"

    sections = [
        "Review this precomputed git context instead of running git commands in the sandbox.",
        "Commit subjects:",
        commit_block,
        "",
        "Changed files:",
        file_block,
        "",
        "Diffstat:",
        bounded_text(diffstat or "(none)", MAX_DIFFSTAT_CHARS),
        "",
        "Patch excerpt:",
        bounded_text(patch or "(none)", MAX_PATCH_CHARS),
    ]
    return "\n".join(sections).strip()


def build_schema_file(temp_dir: Path) -> Path:
    schema = {
        "type": "object",
        "required": [
            "repo",
            "date",
            "model",
            "base_sha",
            "head_sha",
            "commits_reviewed",
            "findings",
        ],
        "properties": {
            "repo": {"type": "string"},
            "date": {"type": "string"},
            "model": {"type": "string"},
            "base_sha": {"type": "string"},
            "head_sha": {"type": "string"},
            "commits_reviewed": {"type": "integer", "minimum": 0},
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "severity",
                        "category",
                        "file",
                        "line",
                        "title",
                        "detail",
                        "suggestion",
                    ],
                    "properties": {
                        "severity": {
                            "type": "string",
                            "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"],
                        },
                        "category": {
                            "type": "string",
                            "enum": [
                                "security",
                                "error-handling",
                                "architecture",
                                "performance",
                                "testing",
                                "docs",
                            ],
                        },
                        "file": {"type": "string"},
                        "line": {"type": "integer", "minimum": 0},
                        "title": {"type": "string"},
                        "detail": {"type": "string"},
                        "suggestion": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
            },
        },
        "additionalProperties": False,
    }
    schema_path = temp_dir / "codex-review.schema.json"
    schema_path.write_text(json.dumps(schema))
    return schema_path


def normalize_review(payload: dict[str, Any], repo: str, date: str, model: str, base_sha: str, head_sha: str, commit_count: int) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for raw_finding in payload.get("findings", []):
        severity = str(raw_finding.get("severity", "INFO")).upper()
        if severity not in SEVERITY_ORDER:
            severity = "INFO"
        category = str(raw_finding.get("category", "docs")).lower()
        if category not in SECTION_MAPPINGS:
            category = "docs"
        findings.append(
            {
                "severity": severity,
                "category": category,
                "file": str(raw_finding.get("file", "")).strip(),
                "line": int(raw_finding.get("line", 0) or 0),
                "title": str(raw_finding.get("title", "")).strip(),
                "detail": str(raw_finding.get("detail", "")).strip(),
                "suggestion": str(raw_finding.get("suggestion", "")).strip(),
            }
        )

    findings.sort(key=lambda item: SEVERITY_ORDER.get(item["severity"], 99))
    return {
        "repo": repo,
        "date": date,
        "model": str(payload.get("model", model)).strip() or model,
        "base_sha": str(payload.get("base_sha", base_sha)).strip() or base_sha,
        "head_sha": str(payload.get("head_sha", head_sha)).strip() or head_sha,
        "commits_reviewed": int(payload.get("commits_reviewed", commit_count) or commit_count),
        "findings": findings,
    }


def classify_finding(finding: Finding) -> str:
    if finding.severity in {"CRITICAL", "HIGH"}:
        return "bug"
    if finding.category in BUG_CATEGORIES:
        return "bug"
    return "improvement"


def detect_duplicate(finding: Finding, repo_path: Path) -> str | None:
    docs = [
        repo_path / "docs" / "FAIL_FAST_LOG.md",
        repo_path / "docs" / "PROGRESS.md",
        repo_path / "docs" / "ERROR_PATTERNS.md",
    ]
    title = finding.title.casefold()
    for doc in docs:
        if not doc.exists():
            continue
        content = doc.read_text().casefold()
        if title and title in content:
            return doc.name
    return None


def validate_location(finding: Finding, repo_path: Path) -> str | None:
    relative = Path(finding.file)
    target = repo_path / relative
    if not target.exists():
        return f"missing file {finding.file}"
    if finding.line <= 0:
        return None
    try:
        lines = target.read_text().splitlines()
    except UnicodeDecodeError:
        return None
    if finding.line > len(lines):
        return f"line {finding.line} out of range"
    return None


def markdown_escape(value: str) -> str:
    return value.replace("\n", " ").replace("|", "\\|").strip()


def find_section_span(content: str, heading: str) -> tuple[int, int] | None:
    start = content.find(heading)
    if start == -1:
        return None
    next_heading = re.search(r"^##\s", content[start + len(heading) :], flags=re.MULTILINE)
    if next_heading:
        end = start + len(heading) + next_heading.start()
        return start, end
    return start, len(content)


def append_progress_candidate(progress_path: Path, row: str, repo: str) -> str:
    content = progress_path.read_text()
    if repo == "ai-integration-services":
        header = "| Plan | Status | Priority | Est. Hours | Key Deliverables | Notes |"
    else:
        header = "| Plan | Status | Priority | Est. Hours | Deliverables | Notes |"

    marker = content.find(header)
    if marker == -1:
        raise RuntimeError(f"missing plans table in {progress_path}")

    table_start = content[marker:].splitlines()
    consumed = 0
    last_table_end = marker
    for line in table_start:
        consumed += len(line) + 1
        if not line.startswith("|"):
            break
        last_table_end = marker + consumed

    prefix = content[:last_table_end]
    if not prefix.endswith("\n"):
        prefix += "\n"
    updated = prefix + row + "\n" + content[last_table_end:]
    progress_path.write_text(updated)
    return "docs/PROGRESS.md"


def append_fail_fast_candidate(fail_fast_path: Path, title: str, date: str, finding: Finding) -> str:
    content = fail_fast_path.read_text()
    if "| Date | Severity | Description | Resolution | PR |" in content:
        return append_fail_fast_table_entry(fail_fast_path, title, date, finding)
    return append_fail_fast_block_entry(fail_fast_path, title, date, finding)


def append_fail_fast_table_entry(fail_fast_path: Path, title: str, date: str, finding: Finding) -> str:
    content = fail_fast_path.read_text()
    categories = SECTION_MAPPINGS.get(finding.category, ("INFRA",))
    for category in categories:
        span = find_section_span(content, f"## {category}")
        if not span:
            continue
        start, end = span
        section = content[start:end]
        table_match = re.search(r"^\| Date \| Severity \| Description \| Resolution \| PR \|\n^\|.*\|\n", section, flags=re.MULTILINE)
        if not table_match:
            continue
        insert_at = start + table_match.end()
        row = (
            f"| {date} | {finding.fail_fast_severity} | {markdown_escape(title + ': ' + finding.detail)} | "
            f"{markdown_escape(finding.suggestion or 'Awaiting HITL resolution')} | Source: Codex review {date} |\n"
        )
        updated = content[:insert_at] + row + content[insert_at:]
        fail_fast_path.write_text(updated)
        return "docs/FAIL_FAST_LOG.md"
    raise RuntimeError(f"no compatible fail-fast table section found in {fail_fast_path}")


def append_fail_fast_block_entry(fail_fast_path: Path, title: str, date: str, finding: Finding) -> str:
    content = fail_fast_path.read_text()
    categories = SECTION_MAPPINGS.get(finding.category, ("INFRA",))
    for category in categories:
        span = find_section_span(content, f"## {category}")
        if not span:
            continue
        _, end = span
        block = (
            f"\n### {date} -- {title}\n"
            f"- **Category:** {category}\n"
            f"- **Severity:** {finding.fail_fast_severity}\n"
            f"- **Description:** {finding.detail}\n"
            f"- **Resolution:** {finding.suggestion or 'OPEN -- awaiting HITL review.'}\n"
            f"- **PR/Commit:** Source: Codex review {date} (⚠️ CODEX-FLAGGED)\n"
        )
        updated = content[:end] + block + content[end:]
        fail_fast_path.write_text(updated)
        return "docs/FAIL_FAST_LOG.md"
    raise RuntimeError(f"no compatible fail-fast section found in {fail_fast_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Codex ingestion helpers")
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo", required=True)
    common.add_argument("--repo-path", type=Path)
    common.add_argument("--date", default=today_string())
    common.add_argument("--ingestion-root", type=Path, default=DEFAULT_INGESTION_ROOT)

    status_parser = subparsers.add_parser("status", parents=[common])
    status_parser.add_argument("--latest-only", action="store_true")

    gen_parser = subparsers.add_parser("generate", parents=[common])
    gen_parser.add_argument("--since-days", type=int, default=7)
    gen_parser.add_argument("--model", default="gpt-5.4")
    gen_parser.add_argument("--timeout-seconds", type=int, default=180)

    qualify_parser = subparsers.add_parser("qualify", parents=[common])

    promote_parser = subparsers.add_parser("promote", parents=[common])
    promote_parser.add_argument("--finding-id", action="append", default=[])
    promote_parser.add_argument("--apply", action="store_true")

    return parser


def cmd_status(args: argparse.Namespace) -> int:
    backlog_files = list_backlog_files(args.repo, args.ingestion_root)
    if args.latest_only and backlog_files:
        backlog_files = [backlog_files[-1]]
    print(f"repo={args.repo}")
    print(f"pending_backlog_files={len(backlog_files)}")
    if backlog_files:
        for path in backlog_files:
            print(path)
    else:
        print("none")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    if not args.repo_path:
        raise SystemExit("--repo-path is required for generate")

    repo_path = args.repo_path.resolve()
    review_path = args.ingestion_root / args.repo / f"review-{args.date}.json"
    args.ingestion_root.mkdir(parents=True, exist_ok=True)
    review_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        commit_shas = git_lines(repo_path, "rev-list", "--reverse", f"--since={args.since_days} days ago", "HEAD")
    except subprocess.CalledProcessError as exc:
        write_json(review_path, skip_payload(args.repo, args.date, f"git rev-list failed: {exc.stderr.strip()}"))
        print(review_path)
        return 0

    if not commit_shas:
        write_json(review_path, skip_payload(args.repo, args.date, "no commits in review window"))
        print(review_path)
        return 0

    base_sha = commit_shas[0]
    head_sha = run(["git", "rev-parse", "HEAD"], cwd=repo_path).stdout.strip()
    base_parent = run(["git", "rev-parse", f"{base_sha}^"], cwd=repo_path).stdout.strip()
    commit_count = len(commit_shas)
    review_context = build_review_context(repo_path, base_parent, head_sha, commit_shas)

    with tempfile.TemporaryDirectory(prefix="codex-ingestion-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        schema_path = build_schema_file(temp_dir)
        candidate_models = [args.model]
        if args.model != "gpt-5.4":
            candidate_models.append("gpt-5.4")

        last_reason = "codex exec did not run"
        for model_name in candidate_models:
            prompt = f"""
You are reviewing a week of changes for the HLD Pro repository {args.repo}.
Review the diff from base ref {base_parent} to HEAD {head_sha}. Focus on OWASP issues,
credential leaks, broken error handling, missing input validation, architectural regressions,
untested code paths, and gaps a same-model reviewer could miss.

Return only valid JSON matching the provided schema. Use exact repo metadata:
- repo: {args.repo}
- date: {args.date}
- model: {model_name}
- base_sha: {base_sha}
- head_sha: {head_sha}
- commits_reviewed: {commit_count}

If there are no substantive issues, return an empty findings array.

{review_context}
""".strip()

            cmd = [
                "codex",
                "exec",
                "-C",
                str(repo_path),
                "--full-auto",
                "--ephemeral",
                "-m",
                model_name,
                "--output-schema",
                str(schema_path),
                "--color",
                "never",
                "--",
                "-",
            ]
            try:
                completed = subprocess.run(
                    cmd,
                    cwd=repo_path,
                    check=True,
                    capture_output=True,
                    text=True,
                    input=prompt,
                    timeout=args.timeout_seconds,
                )
                payload = extract_json_from_stdout(completed.stdout)
                normalized = normalize_review(payload, args.repo, args.date, model_name, base_sha, head_sha, commit_count)
                write_json(review_path, normalized)
                print(review_path)
                return 0
            except subprocess.TimeoutExpired as exc:
                partial = "; partial stdout captured" if exc.stdout else ""
                last_reason = f"codex exec timed out after {args.timeout_seconds}s{partial}"
                break
            except (subprocess.CalledProcessError, json.JSONDecodeError, OSError) as exc:
                reason = str(exc)
                if isinstance(exc, subprocess.CalledProcessError):
                    reason = summarize_failure_output(exc.stderr, exc.stdout)
                if isinstance(exc, json.JSONDecodeError):
                    reason = summarize_failure_output("", exc.doc)
                last_reason = reason[:240]
                if (
                    isinstance(exc, subprocess.CalledProcessError)
                    and model_name != "gpt-5.4"
                    and "not supported when using Codex with a ChatGPT account" in reason
                ):
                    continue
                break

        write_json(review_path, skip_payload(args.repo, args.date, f"codex exec failed: {last_reason}"))
    print(review_path)
    return 0


def cmd_qualify(args: argparse.Namespace) -> int:
    if not args.repo_path:
        raise SystemExit("--repo-path is required for qualify")

    repo_path = args.repo_path.resolve()
    review_path = args.ingestion_root / args.repo / f"review-{args.date}.json"
    qualified_json_path = args.ingestion_root / args.repo / f"qualified-{args.date}.json"
    backlog_path = args.ingestion_root / args.repo / f"backlog-{args.date}.md"

    payload = load_json(review_path)
    if payload.get("skipped"):
        qualified = {
            "repo": args.repo,
            "date": args.date,
            "skipped": True,
            "reason": payload.get("reason", "review skipped"),
            "candidates": [],
            "skipped_findings": [],
        }
        write_json(qualified_json_path, qualified)
        backlog_path.write_text(
            f"# Codex Backlog — {args.repo} — {args.date}\n\n"
            f"Review skipped: {payload.get('reason', 'review skipped')}.\n"
        )
        print(backlog_path)
        return 0

    candidates: list[dict[str, Any]] = []
    skipped_findings: list[dict[str, Any]] = []
    findings = []
    for index, raw in enumerate(payload.get("findings", []), start=1):
        findings.append(
            Finding(
                finding_id=f"F{index:03d}",
                severity=str(raw.get("severity", "INFO")).upper(),
                category=str(raw.get("category", "docs")).lower(),
                file=str(raw.get("file", "")).strip(),
                line=int(raw.get("line", 0) or 0),
                title=str(raw.get("title", "")).strip(),
                detail=str(raw.get("detail", "")).strip(),
                suggestion=str(raw.get("suggestion", "")).strip(),
            )
        )

    for finding in findings:
        duplicate_doc = detect_duplicate(finding, repo_path)
        if duplicate_doc:
            skipped_findings.append(
                {
                    "finding_id": finding.finding_id,
                    "title": finding.title,
                    "reason": f"already tracked in {duplicate_doc}",
                }
            )
            continue

        validation_issue = validate_location(finding, repo_path)
        if validation_issue:
            skipped_findings.append(
                {
                    "finding_id": finding.finding_id,
                    "title": finding.title,
                    "reason": f"false positive: {validation_issue}",
                }
            )
            continue

        candidate_type = classify_finding(finding)
        target = "docs/FAIL_FAST_LOG.md" if candidate_type == "bug" else "docs/PROGRESS.md"
        candidates.append(
            {
                "finding_id": finding.finding_id,
                "title": finding.title,
                "severity": finding.severity,
                "priority": finding.priority,
                "fail_fast_severity": finding.fail_fast_severity,
                "category": finding.category,
                "type": candidate_type,
                "target": target,
                "file": finding.file,
                "line": finding.line,
                "detail": finding.detail,
                "suggestion": finding.suggestion,
                "est_hours": finding.est_hours,
                "deliverables": finding.suggestion or f"Address {finding.category} issue in {finding.file}",
                "notes": f"Source: Codex review {args.date}. Awaiting HITL review.",
                "source_tag": "⚠️ CODEX-FLAGGED",
            }
        )

    qualified = {
        "repo": args.repo,
        "date": args.date,
        "review_file": str(review_path),
        "candidates": candidates,
        "skipped_findings": skipped_findings,
    }
    write_json(qualified_json_path, qualified)

    bug_candidates = [item for item in candidates if item["type"] == "bug"]
    improvements = [item for item in candidates if item["type"] == "improvement"]

    lines = [
        f"# Codex Backlog — {args.repo} — {args.date}",
        "",
        "## Summary",
        "",
        f"- Review file: `{review_path}`",
        f"- Qualified findings: {len(candidates)}",
        f"- Already tracked or invalid: {len(skipped_findings)}",
        "",
    ]

    lines.extend(
        [
            "## FAIL_FAST_LOG Candidates",
            "",
            "| ID | Severity | Category | File | Line | Title | Root Cause | Suggested Resolution | Source |",
            "|----|----------|----------|------|------|-------|------------|----------------------|--------|",
        ]
    )
    if bug_candidates:
        for item in bug_candidates:
            lines.append(
                "| {finding_id} | {fail_fast_severity} | {category} | {file} | {line} | {title} | {detail} | {suggestion} | {source_tag} |".format(
                    **{key: markdown_escape(str(value)) for key, value in item.items()}
                )
            )
    else:
        lines.append("| - | - | - | - | - | None | - | - | - |")
    lines.append("")

    deliverables_key = "Key Deliverables" if args.repo == "ai-integration-services" else "Deliverables"
    lines.extend(
        [
            "## PROGRESS Candidates",
            "",
            f"| ID | Priority | File | Line | Plan | Est. Hours | {deliverables_key} | Notes |",
            "|----|----------|------|------|------|------------|--------------------|-------|",
        ]
    )
    if improvements:
        for item in improvements:
            lines.append(
                "| {finding_id} | {priority} | {file} | {line} | {title} | {est_hours} | {deliverables} | {notes} |".format(
                    **{key: markdown_escape(str(value)) for key, value in item.items()}
                )
            )
    else:
        lines.append("| - | - | - | - | None | - | - | - |")
    lines.append("")

    lines.extend(
        [
            "## Skipped Findings",
            "",
            "| ID | Title | Reason |",
            "|----|-------|--------|",
        ]
    )
    if skipped_findings:
        for item in skipped_findings:
            lines.append(
                f"| {markdown_escape(item['finding_id'])} | {markdown_escape(item['title'])} | {markdown_escape(item['reason'])} |"
            )
    else:
        lines.append("| - | None | - |")
    lines.append("")

    backlog_path.write_text("\n".join(lines))
    print(backlog_path)
    return 0


def cmd_promote(args: argparse.Namespace) -> int:
    if not args.repo_path:
        raise SystemExit("--repo-path is required for promote")

    repo_path = args.repo_path.resolve()
    qualified_json_path = args.ingestion_root / args.repo / f"qualified-{args.date}.json"
    qualified = load_json(qualified_json_path)
    candidates = qualified.get("candidates", [])
    selected = candidates
    if args.finding_id:
        wanted = set(args.finding_id)
        selected = [item for item in candidates if item["finding_id"] in wanted]

    if not selected:
        print("No matching candidates.")
        return 0

    for item in selected:
        finding = Finding(
            finding_id=item["finding_id"],
            severity=item["severity"],
            category=item["category"],
            file=item["file"],
            line=int(item["line"]),
            title=item["title"],
            detail=item["detail"],
            suggestion=item["suggestion"],
        )
        if item["type"] == "improvement":
            deliverables_label = "Key Deliverables" if args.repo == "ai-integration-services" else "Deliverables"
            row = (
                f"| {markdown_escape(item['title'])} | INBOX | {item['priority']} | {item['est_hours']} | "
                f"{markdown_escape(item['deliverables'])} | {markdown_escape(item['notes'])} |"
            )
            if args.apply:
                target = append_progress_candidate(repo_path / "docs" / "PROGRESS.md", row, args.repo)
                print(f"APPLIED {item['finding_id']} -> {target}")
            else:
                print(f"[{item['finding_id']}] docs/PROGRESS.md")
                print(f"Header: Plan | Status | Priority | Est. Hours | {deliverables_label} | Notes |")
                print(row)
                print("")
        else:
            if args.apply:
                target = append_fail_fast_candidate(repo_path / "docs" / "FAIL_FAST_LOG.md", item["title"], args.date, finding)
                print(f"APPLIED {item['finding_id']} -> {target}")
            else:
                print(f"[{item['finding_id']}] docs/FAIL_FAST_LOG.md")
                print(f"Title: {item['title']}")
                print(f"Severity: {item['fail_fast_severity']}")
                print(f"Description: {item['detail']}")
                print(f"Resolution: {item['suggestion'] or 'OPEN -- awaiting HITL review.'}")
                print(f"Source: Codex review {args.date} (⚠️ CODEX-FLAGGED)")
                print("")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "status":
        return cmd_status(args)
    if args.command == "generate":
        return cmd_generate(args)
    if args.command == "qualify":
        return cmd_qualify(args)
    if args.command == "promote":
        return cmd_promote(args)
    raise RuntimeError(f"unsupported command {args.command}")


if __name__ == "__main__":
    sys.exit(main())
