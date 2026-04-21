#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_JSON = REPO_ROOT / "metrics" / "self-learning" / "latest.json"
DEFAULT_REPORT_MD = REPO_ROOT / "metrics" / "self-learning" / "latest.md"
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is",
    "it", "of", "on", "or", "that", "the", "this", "to", "with", "without",
}


@dataclass(frozen=True)
class LearningEntry:
    entry_id: str
    source_path: str
    title: str
    summary: str
    evidence_paths: list[str]
    date: str | None
    kind: str
    tokens: list[str]


@dataclass(frozen=True)
class LearningMatch:
    title: str
    summary: str
    source_path: str
    evidence_paths: list[str]
    score: int
    repeat_count: int


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9_-]{2,}", text.lower())
        if token not in STOP_WORDS
    }


def _rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _entry_id(source_path: str, title: str) -> str:
    return hashlib.sha256(f"{source_path}\n{title}".encode("utf-8")).hexdigest()[:16]


def _date_from_text(text: str) -> str | None:
    match = re.search(r"\b20\d{2}-\d{2}-\d{2}\b", text)
    return match.group(0) if match else None


def _markdown_table_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw in body.splitlines():
        line = raw.strip()
        if not line.startswith("|") or "---" in line or "Field" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        key = re.sub(r"[^a-z0-9]+", "_", cells[0].lower()).strip("_")
        if key:
            fields[key] = cells[1]
    return fields


def load_fail_fast(root: Path) -> list[LearningEntry]:
    path = root / "docs" / "FAIL_FAST_LOG.md"
    if not path.exists():
        return []
    entries: list[LearningEntry] = []
    source = _rel(root, path)
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("|") or "---" in line or "Error | Root Cause" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        title, root_cause, resolution, date = cells[:4]
        if not title or title.lower() == "error":
            continue
        summary = f"Root cause: {root_cause}. Resolution: {resolution}"
        text = " ".join([title, root_cause, resolution])
        entries.append(
            LearningEntry(
                entry_id=_entry_id(source, title),
                source_path=source,
                title=title,
                summary=summary,
                evidence_paths=[source],
                date=date or _date_from_text(text),
                kind="fail_fast",
                tokens=sorted(tokenize(text)),
            )
        )
    return entries


def load_error_patterns(root: Path) -> list[LearningEntry]:
    path = root / "docs" / "ERROR_PATTERNS.md"
    if not path.exists():
        return []
    source = _rel(root, path)
    text = path.read_text(encoding="utf-8")
    entries: list[LearningEntry] = []
    for match in re.finditer(r"^## Pattern:\s*(.+)$", text, re.MULTILINE):
        title = match.group(1).strip()
        start = match.end()
        next_match = re.search(r"^##\s+", text[start:], re.MULTILINE)
        body = text[start : start + next_match.start()] if next_match else text[start:]
        if "stub" in title.lower():
            continue
        summary = " ".join(body.strip().split())[:500]
        entries.append(
            LearningEntry(
                entry_id=_entry_id(source, title),
                source_path=source,
                title=title,
                summary=summary,
                evidence_paths=[source],
                date=_date_from_text(body),
                kind="error_pattern",
                tokens=sorted(tokenize(f"{title} {body}")),
            )
        )
    return entries


def load_session_error_patterns(root: Path) -> list[LearningEntry]:
    path = root / "docs" / "runbooks" / "session-error-patterns.md"
    if not path.exists():
        return []
    source = _rel(root, path)
    text = path.read_text(encoding="utf-8")
    entries: list[LearningEntry] = []
    for match in re.finditer(r"^## Pattern:\s*(.+)$", text, re.MULTILINE):
        title = match.group(1).strip()
        start = match.end()
        next_match = re.search(r"^##\s+", text[start:], re.MULTILINE)
        body = text[start : start + next_match.start()] if next_match else text[start:]
        body_text = " ".join(body.strip().split())
        if not body_text:
            continue
        fields = _markdown_table_fields(body)
        summary_parts = [
            f"Signature: {fields['signature']}" if fields.get("signature") else "",
            f"Correction: {fields['correction']}" if fields.get("correction") else "",
            f"Guardrail: {fields['guardrail']}" if fields.get("guardrail") else "",
            f"Validation: {fields['validation']}" if fields.get("validation") else "",
        ]
        summary = " ".join(part for part in summary_parts if part) or body_text
        entries.append(
            LearningEntry(
                entry_id=_entry_id(source, title),
                source_path=source,
                title=title,
                summary=summary[:500],
                evidence_paths=[source],
                date=_date_from_text(body),
                kind="session_error_pattern",
                tokens=sorted(tokenize(f"{title} {body}")),
            )
        )
    return entries


def _section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^##\s+", text[start:], re.MULTILINE)
    body = text[start : start + next_match.start()] if next_match else text[start:]
    return " ".join(body.strip().split())


def load_closeouts(root: Path) -> list[LearningEntry]:
    entries: list[LearningEntry] = []
    for path in sorted((root / "raw" / "closeouts").glob("*.md")):
        if path.name == "TEMPLATE.md":
            continue
        text = path.read_text(encoding="utf-8")
        decision = _section(text, "Decision Made")
        pattern = _section(text, "Pattern Identified")
        risks = _section(text, "Residual Risks / Follow-Up")
        title = decision[:120] or path.stem
        summary = " ".join(part for part in [pattern, risks] if part)[:500]
        source = _rel(root, path)
        entries.append(
            LearningEntry(
                entry_id=_entry_id(source, title),
                source_path=source,
                title=title,
                summary=summary or decision[:500],
                evidence_paths=[source],
                date=_date_from_text(text),
                kind="closeout",
                tokens=sorted(tokenize(f"{title} {summary}")),
            )
        )
    return entries


def load_operator_context(root: Path) -> list[LearningEntry]:
    entries: list[LearningEntry] = []
    for path in sorted((root / "raw" / "operator-context").rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else path.stem
        summary = " ".join(text.split())[:500]
        source = _rel(root, path)
        entries.append(
            LearningEntry(
                entry_id=_entry_id(source, title),
                source_path=source,
                title=title,
                summary=summary,
                evidence_paths=[source],
                date=_date_from_text(text),
                kind="operator_context",
                tokens=sorted(tokenize(text)),
            )
        )
    return entries


def load_compendium_attention(root: Path) -> set[str]:
    path = root / "docs" / "ORG_GOVERNANCE_COMPENDIUM.md"
    if not path.exists():
        return set()
    return tokenize(path.read_text(encoding="utf-8"))


def load_graph_attention(root: Path) -> set[str]:
    path = root / "graphify-out" / "hldpro-governance" / "GRAPH_REPORT.md"
    if not path.exists():
        return set()
    return tokenize(path.read_text(encoding="utf-8"))


def load_entries(root: Path = REPO_ROOT) -> list[LearningEntry]:
    return (
        load_fail_fast(root)
        + load_error_patterns(root)
        + load_session_error_patterns(root)
        + load_closeouts(root)
        + load_operator_context(root)
    )


def duplicate_counts(entries: list[LearningEntry]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in entries:
        key_tokens = [token for token in entry.tokens if len(token) >= 5][:8]
        key = " ".join(key_tokens) or entry.title.lower()
        counts[key] = counts.get(key, 0) + 1
    return counts


def lookup_patterns(query: str, *, root: Path = REPO_ROOT, limit: int = 5) -> list[LearningMatch]:
    entries = load_entries(root)
    query_tokens = tokenize(query)
    attention = load_compendium_attention(root) | load_graph_attention(root)
    dupes = duplicate_counts(entries)
    matches: list[LearningMatch] = []
    for entry in entries:
        entry_tokens = set(entry.tokens)
        overlap = query_tokens & entry_tokens
        if not overlap:
            continue
        attention_bonus = 1 if overlap & attention else 0
        score = len(overlap) * 10 + attention_bonus
        key_tokens = [token for token in entry.tokens if len(token) >= 5][:8]
        repeat_count = dupes.get(" ".join(key_tokens) or entry.title.lower(), 1)
        matches.append(
            LearningMatch(
                title=entry.title,
                summary=entry.summary,
                source_path=entry.source_path,
                evidence_paths=entry.evidence_paths,
                score=score,
                repeat_count=repeat_count,
            )
        )
    return sorted(matches, key=lambda item: (-item.score, item.source_path, item.title))[:limit]


def query_from_packet(packet: dict[str, Any]) -> str:
    parts: list[str] = []
    parts.extend(str(item) for item in packet.get("artifacts", []) if item)
    governance = packet.get("governance") or {}
    for key in ("structured_plan_ref", "execution_scope_ref"):
        if governance.get(key):
            parts.append(str(governance[key]))
    metadata = packet.get("metadata")
    if isinstance(metadata, dict):
        parts.extend(str(value) for value in metadata.values())
    return " ".join(parts)


def enrich_packet(packet: dict[str, Any], *, root: Path = REPO_ROOT, limit: int = 5) -> dict[str, Any]:
    enriched = json.loads(json.dumps(packet))
    governance = enriched.setdefault("governance", {})
    matches = lookup_patterns(query_from_packet(enriched), root=root, limit=limit)
    governance["known_failure_context"] = [
        {
            "title": match.title,
            "summary": match.summary,
            "source_path": match.source_path,
            "evidence_paths": match.evidence_paths,
            "repeat_count": match.repeat_count,
        }
        for match in matches
    ]
    return enriched


def atomic_write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{datetime.now(timezone.utc).timestamp()}.tmp")
    tmp.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    tmp.replace(path)


def record_failure(
    *,
    root: Path,
    issue_number: int,
    title: str,
    summary: str,
    evidence_path: str,
    follow_up: str,
) -> Path:
    if issue_number <= 0 or issue_number > 999999:
        raise ValueError("issue_number must be between 1 and 999999")
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60] or "failure"
    output_dir = root / "raw" / "operator-context" / "self-learning"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{date}-issue-{issue_number}-{slug}.md"
    counter = 2
    while path.exists():
        path = output_dir / f"{date}-issue-{issue_number}-{slug}-{counter}.md"
        counter += 1
    body = (
        f"# {title}\n\n"
        f"Date: {utc_now()}\n"
        f"Issue: #{issue_number}\n"
        f"Evidence: {evidence_path}\n"
        f"Follow-up: {follow_up}\n\n"
        f"## Summary\n\n{summary}\n"
    )
    path.write_text(body, encoding="utf-8")
    return path


def build_report(root: Path = REPO_ROOT) -> dict[str, Any]:
    entries = load_entries(root)
    dupes = {key: count for key, count in duplicate_counts(entries).items() if count > 1}
    today = datetime.now(timezone.utc).date()
    stale: list[dict[str, str]] = []
    for entry in entries:
        if not entry.date:
            continue
        try:
            age = (today - datetime.fromisoformat(entry.date).date()).days
        except ValueError:
            continue
        if age > 90:
            stale.append({"source_path": entry.source_path, "title": entry.title, "age_days": str(age)})
    return {
        "generated_at": utc_now(),
        "entry_count": len(entries),
        "duplicate_groups": dupes,
        "stale_entries": stale,
        "sources": sorted({entry.kind for entry in entries}),
        "session_error_patterns": [
            {
                "title": entry.title,
                "source_path": entry.source_path,
                "summary": entry.summary,
            }
            for entry in entries
            if entry.kind == "session_error_pattern"
        ],
        "graphify_attention_only": True,
    }


def report_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Self-Learning Knowledge Report",
        "",
        f"Generated: {report['generated_at']}",
        f"Entries indexed: {report['entry_count']}",
        f"Duplicate groups: {len(report['duplicate_groups'])}",
        f"Stale entries: {len(report['stale_entries'])}",
        f"Sources: {', '.join(report['sources'])}",
        "",
        "Graphify inference is used for routing attention only; direct source files validate claims.",
    ]
    if report["duplicate_groups"]:
        lines.extend(["", "## Duplicate Groups"])
        for key, count in sorted(report["duplicate_groups"].items()):
            lines.append(f"- {key}: {count}")
    if report["session_error_patterns"]:
        lines.extend(["", "## Session Error Patterns"])
        for entry in report["session_error_patterns"]:
            lines.append(f"- {entry['title']} ({entry['source_path']}): {entry['summary']}")
    if report["stale_entries"]:
        lines.extend(["", "## Stale Entries"])
        for entry in report["stale_entries"][:25]:
            lines.append(f"- {entry['source_path']}: {entry['title']} ({entry['age_days']} days)")
    return "\n".join(lines) + "\n"


def _run_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lookup and write back self-learning governance context")
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)

    lookup = sub.add_parser("lookup")
    lookup.add_argument("--query", required=True)
    lookup.add_argument("--limit", type=int, default=5)

    enrich = sub.add_parser("enrich-packet")
    enrich.add_argument("--packet", type=Path, required=True)
    enrich.add_argument("--output", type=Path, required=True)
    enrich.add_argument("--limit", type=int, default=5)

    record = sub.add_parser("record-failure")
    record.add_argument("--issue", type=int, required=True)
    record.add_argument("--title", required=True)
    record.add_argument("--summary", required=True)
    record.add_argument("--evidence-path", required=True)
    record.add_argument("--follow-up", required=True)

    report = sub.add_parser("report")
    report.add_argument("--output-json", type=Path, default=DEFAULT_REPORT_JSON)
    report.add_argument("--output-md", type=Path, default=DEFAULT_REPORT_MD)

    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.command == "lookup":
        print(json.dumps([asdict(match) for match in lookup_patterns(args.query, root=root, limit=args.limit)], indent=2))
        return 0
    if args.command == "enrich-packet":
        packet = yaml.safe_load(args.packet.read_text(encoding="utf-8"))
        if not isinstance(packet, dict):
            raise SystemExit("packet must be a YAML object")
        atomic_write_yaml(args.output, enrich_packet(packet, root=root, limit=args.limit))
        return 0
    if args.command == "record-failure":
        path = record_failure(
            root=root,
            issue_number=args.issue,
            title=args.title,
            summary=args.summary,
            evidence_path=args.evidence_path,
            follow_up=args.follow_up,
        )
        print(path)
        return 0
    if args.command == "report":
        built = build_report(root)
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(built, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        args.output_md.write_text(report_markdown(built), encoding="utf-8")
        print(args.output_json)
        print(args.output_md)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(_run_cli())
