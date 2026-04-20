#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SUCCESS_CONCLUSIONS = {"success"}
BLOCKING_LABELS = {
    "do-not-merge",
    "hold",
    "manual-merge-required",
    "security-review-required",
}
OPT_IN_LABELS = {"automerge", "merge-when-green"}


def _labels(payload: dict[str, Any]) -> set[str]:
    return {str(label).strip().lower() for label in payload.get("labels", []) if str(label).strip()}


def _check_required_checks(payload: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    for check in payload.get("checks", []):
        if not isinstance(check, dict) or not check.get("required", False):
            continue
        name = str(check.get("name") or "(unnamed check)")
        status = str(check.get("status") or "").lower()
        conclusion = str(check.get("conclusion") or "").lower()
        if status != "completed":
            blockers.append(f"required check pending: {name}")
            continue
        if conclusion not in SUCCESS_CONCLUSIONS:
            blockers.append(f"required check not successful: {name} ({conclusion or 'missing conclusion'})")
    return blockers


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
    labels = _labels(payload)

    repo = payload.get("repo", {})
    if not isinstance(repo, dict):
        repo = {}
    if not repo.get("allow_auto_merge", False):
        blockers.append("repository auto-merge is disabled")

    if payload.get("is_draft", False):
        blockers.append("pull request is draft")
    if not payload.get("protected_target", False):
        blockers.append("target branch is not covered by a protected ruleset or branch protection")

    mergeable_state = str(payload.get("mergeable_state") or "").lower()
    if mergeable_state != "clean":
        blockers.append(f"pull request is not cleanly mergeable: {mergeable_state or 'unknown'}")

    blockers.extend(_check_required_checks(payload))

    reviews = payload.get("reviews", {})
    if not isinstance(reviews, dict):
        reviews = {}
    required_approvals = int(reviews.get("required_approvals") or 0)
    approvals = int(reviews.get("approvals") or 0)
    if approvals < required_approvals:
        blockers.append(f"required approvals missing: {approvals}/{required_approvals}")
    if reviews.get("code_owner_review_required", False) and not reviews.get("code_owner_approved", False):
        blockers.append("code owner review required but not approved")
    if reviews.get("review_thread_resolution_required", False) and not reviews.get("review_threads_resolved", False):
        blockers.append("review threads are not resolved")

    blocking_labels = sorted(labels & BLOCKING_LABELS)
    if blocking_labels:
        blockers.append("blocking label present: " + ", ".join(blocking_labels))

    if payload.get("explicit_opt_in_required", True) and not labels.intersection(OPT_IN_LABELS):
        blockers.append("explicit automerge opt-in label missing")

    for artifact in payload.get("governance_artifacts", []):
        if not isinstance(artifact, dict) or not artifact.get("required", False):
            continue
        name = str(artifact.get("name") or "(unnamed artifact)")
        if not artifact.get("present", False):
            blockers.append(f"required governance artifact missing: {name}")

    if not payload.get("required_checks_configured", False):
        warnings.append("required checks are not configured as a merge gate for this target")
    if not payload.get("review_requirements_configured", False):
        warnings.append("review requirements are not configured as a merge gate for this target")

    return {
        "eligible": not blockers,
        "blockers": blockers,
        "warnings": warnings,
        "rollback": [
            "remove the automerge or merge-when-green label from the PR",
            "disable the repository auto-merge setting",
            "disable or remove the automerge workflow entrypoint",
            "restore the previous ruleset or branch-protection snapshot if a rollout changed enforcement",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run HLD Pro governed automerge eligibility.")
    parser.add_argument("--input", required=True, type=Path, help="JSON fixture describing PR, repo, and gate state.")
    parser.add_argument("--json-output", type=Path, help="Optional path to write the evaluation JSON.")
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("input JSON must be an object")

    result = evaluate(payload)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.json_output:
        args.json_output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["eligible"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
