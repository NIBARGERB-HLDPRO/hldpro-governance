#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


ARTIFACT_ISSUE_NUMBER = 503
ARTIFACT_ISSUE_URL = "https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/503"
ARTIFACT_SCOPE_PATH = (
    "raw/execution-scopes/2026-04-21-issue-503-overlord-sweep-generated-artifacts-implementation.json"
)
ARTIFACT_PLAN_PATH = "docs/plans/issue-503-overlord-sweep-generated-artifacts-structured-agent-cycle-plan.json"
CLAIMED_AT = "2026-04-21T19:00:00Z"


def artifact_branch(date: str, run_id: str) -> str:
    if not date:
        raise ValueError("date is required")
    if not run_id:
        raise ValueError("run_id is required")
    return f"automation/issue-{ARTIFACT_ISSUE_NUMBER}-overlord-sweep-{date}-{run_id}"


def artifact_scope(branch: str, run_id: str, server_url: str, repository: str) -> dict[str, object]:
    if not branch:
        raise ValueError("branch is required")
    if not run_id:
        raise ValueError("run_id is required")
    if not server_url:
        raise ValueError("server_url is required")
    if not repository:
        raise ValueError("repository is required")

    run_url = f"{server_url.rstrip('/')}/{repository}/actions/runs/{run_id}"
    return {
        "expected_execution_root": "{repo_root}",
        "expected_branch": branch,
        "allowed_write_paths": [
            "docs/ORG_GOVERNANCE_COMPENDIUM.md",
            "graphify-out/",
            "metrics/effectiveness-baseline/",
            "metrics/pentagi/",
            "metrics/self-learning/",
            ARTIFACT_SCOPE_PATH,
            "wiki/",
        ],
        "forbidden_roots": [],
        "execution_mode": "implementation_ready",
        "lane_claim": {
            "issue_number": ARTIFACT_ISSUE_NUMBER,
            "claim_ref": ARTIFACT_ISSUE_URL,
            "claimed_by": "overlord-sweep-workflow",
            "claimed_at": CLAIMED_AT,
        },
        "handoff_evidence": {
            "status": "accepted",
            "planner_model": "operator-directive",
            "implementer_model": "overlord-sweep-workflow",
            "accepted_at": CLAIMED_AT,
            "evidence_paths": [
                ARTIFACT_PLAN_PATH,
                run_url,
                ARTIFACT_ISSUE_URL,
            ],
            "active_exception_ref": None,
            "active_exception_expires_at": None,
        },
    }


def write_scope(path: Path, scope: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Overlord Sweep generated artifact PR metadata.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    branch_parser = subparsers.add_parser("branch")
    branch_parser.add_argument("--date", required=True)
    branch_parser.add_argument("--run-id", required=True)

    subparsers.add_parser("scope-path")

    write_parser = subparsers.add_parser("write-scope")
    write_parser.add_argument("--branch", required=True)
    write_parser.add_argument("--run-id", required=True)
    write_parser.add_argument("--server-url", required=True)
    write_parser.add_argument("--repository", required=True)
    write_parser.add_argument("--path", default=ARTIFACT_SCOPE_PATH)

    args = parser.parse_args()
    if args.command == "branch":
        print(artifact_branch(args.date, args.run_id))
    elif args.command == "scope-path":
        print(ARTIFACT_SCOPE_PATH)
    elif args.command == "write-scope":
        scope = artifact_scope(args.branch, args.run_id, args.server_url, args.repository)
        write_scope(Path(args.path), scope)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
