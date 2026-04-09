#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
LOGGER = REPO_ROOT / "scripts" / "knowledge_base" / "log_graphify_usage.py"
MEASURE = REPO_ROOT / "scripts" / "knowledge_base" / "measure_graphify_usage.py"
SCHEMA = REPO_ROOT / "docs" / "schemas" / "graphify-usage-event.schema.json"
GRAPH_ROOT = REPO_ROOT / "graphify-out"

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        print(f"[PASS] {message}")
    else:
        print(f"[FAIL] {message}")
        failures.append(message)


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, capture_output=True)


def test_schema_shape() -> None:
    payload = json.loads(SCHEMA.read_text(encoding="utf-8"))
    properties = payload.get("properties", {})
    check("experiment_id" in properties, "schema exposes experiment_id")
    check("session_id" in properties, "schema exposes session_id")
    check("prompt" in properties, "schema exposes prompt")
    check("query_terms" in properties, "schema exposes query_terms")
    check("top_candidates" in properties, "schema exposes top_candidates")
    check(payload.get("additionalProperties") is False, "schema remains closed to unexpected keys")


def test_logger_backwards_compatible() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        result = run_command(
            [
                "python3",
                str(LOGGER),
                "--output-dir",
                str(output_dir),
                "--repo",
                "hldpro-governance",
                "--task-id",
                "compat-smoke",
                "--task-type",
                "architecture_retrieval",
                "--strategy",
                "graphify",
                "--artifact",
                "wiki/index.md",
                "--estimated-tokens",
                "42",
                "--notes",
                "compatibility check",
            ]
        )
        event_path = Path(result.stdout.strip())
        event = json.loads(event_path.read_text(encoding="utf-8").strip().splitlines()[-1])
        check(event["task_id"] == "compat-smoke", "logger still writes legacy task_id events")
        check("prompt" not in event, "legacy logger usage does not force prompt")
        check("query_terms" not in event, "legacy logger usage does not force query terms")


def test_logger_query_trace_fields() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        result = run_command(
            [
                "python3",
                str(LOGGER),
                "--output-dir",
                str(output_dir),
                "--repo",
                "hldpro-governance",
                "--task-id",
                "ab-run-1",
                "--experiment-id",
                "ab-2026-04-09",
                "--session-id",
                "current-work",
                "--task-type",
                "architecture_retrieval",
                "--strategy",
                "graphify",
                "--prompt",
                "Find graphify measurement ownership files.",
                "--query-term",
                "graphify",
                "--query-term",
                "measurement",
                "--top-candidate",
                "scripts/knowledge_base/measure_graphify_usage.py",
                "--top-candidate",
                "metrics/graphify-usage/README.md",
                "--artifact",
                "graphify-out/hldpro-governance/GRAPH_REPORT.md",
                "--estimated-tokens",
                "88",
                "--notes",
                "ab test trace",
            ]
        )
        event_path = Path(result.stdout.strip())
        event = json.loads(event_path.read_text(encoding="utf-8").strip().splitlines()[-1])
        check(event["experiment_id"] == "ab-2026-04-09", "logger writes experiment_id")
        check(event["session_id"] == "current-work", "logger writes session_id")
        check(event["prompt"] == "Find graphify measurement ownership files.", "logger writes prompt")
        check(event["query_terms"] == ["graphify", "measurement"], "logger writes query terms")
        check(
            event["top_candidates"] == [
                "scripts/knowledge_base/measure_graphify_usage.py",
                "metrics/graphify-usage/README.md",
            ],
            "logger writes top candidates",
        )


def test_measurement_outputs_query_traces() -> None:
    scenario_payload = {
        "date": "2026-04-09",
        "scenarios": [
            {
                "id": "live-query-trace-smoke",
                "issue_number": 999,
                "repo": "hldpro-governance",
                "repo_path": str(REPO_ROOT),
                "graph_key": "hldpro-governance",
                "task_type": "architecture_retrieval",
                "prompt": "Find the graphify measurement logging path.",
                "query_terms": ["graphify", "usage", "logging"],
                "expected_files": [
                    "scripts/knowledge_base/log_graphify_usage.py",
                    "metrics/graphify-usage/README.md",
                ],
                "expected_terms": ["query_terms", "top_candidates", "graphify-usage"],
            }
        ],
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir = Path(tmpdir)
        scenario_file = temp_dir / "scenario.json"
        output_dir = temp_dir / "output"
        usage_dir = temp_dir / "usage-events"
        scenario_file.write_text(json.dumps(scenario_payload, indent=2) + "\n", encoding="utf-8")
        run_command(
            [
                "python3",
                str(MEASURE),
                "--repos-root",
                str(REPO_ROOT.parent),
                "--graph-root",
                str(GRAPH_ROOT),
                "--scenario-file",
                str(scenario_file),
                "--output-dir",
                str(output_dir),
                "--usage-event-dir",
                str(usage_dir),
                "--date",
                "2026-04-09",
            ]
        )
        json_path = output_dir / "2026-04-09-graphify-vs-search.json"
        md_path = output_dir / "2026-04-09-graphify-vs-search.md"
        usage_path = usage_dir / "2026-04-09.jsonl"
        results = json.loads(json_path.read_text(encoding="utf-8"))
        scenario = results["scenarios"][0]
        trace = scenario["trace"]
        check(trace["prompt"] == "Find the graphify measurement logging path.", "measurement JSON includes prompt trace")
        check(trace["query_terms"] == ["graphify", "usage", "logging"], "measurement JSON includes query terms trace")
        check(isinstance(trace["graphify_candidates"], list), "measurement JSON includes graphify candidate list")
        check(isinstance(trace["baseline_candidates"], list), "measurement JSON includes baseline candidate list")
        markdown = md_path.read_text(encoding="utf-8")
        check("## Query Traces" in markdown, "measurement markdown includes query trace section")
        check("Find the graphify measurement logging path." in markdown, "measurement markdown includes prompt text")
        events = [json.loads(line) for line in usage_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        check(len(events) == 2, "measurement run emits graphify and baseline usage events by default")
        strategies = {event["strategy"] for event in events}
        check(strategies == {"graphify", "repo-search"}, "measurement usage events preserve graphify and baseline strategies")
        check(all(event.get("experiment_id") == "graphify-ab-2026-04-09" for event in events), "measurement usage events share experiment id")
        check(all(event.get("prompt") == "Find the graphify measurement logging path." for event in events), "measurement usage events include prompt trace")


def main() -> int:
    test_schema_shape()
    test_logger_backwards_compatible()
    test_logger_query_trace_fields()
    test_measurement_outputs_query_traces()

    if failures:
        print(f"FAILED: {len(failures)} graphify usage logging contract checks failed")
        return 1

    print("[PASS] graphify usage logging contract checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
