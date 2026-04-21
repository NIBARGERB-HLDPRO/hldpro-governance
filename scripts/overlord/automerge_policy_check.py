#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SUCCESS_CONCLUSIONS = {"success"}
PENDING_STATUSES = {"pending", "queued", "requested", "waiting", "in_progress", "in-progress"}
GITHUB_NATIVE_MERGE_SOURCES = {"github", "github_api", "origin/main", "origin_main"}
BLOCKING_LABELS = {
    "do-not-merge",
    "hold",
    "manual-merge-required",
    "security-review-required",
}
OPT_IN_LABELS = {"automerge", "merge-when-green"}


def _labels(payload: dict[str, Any]) -> set[str]:
    return {str(label).strip().lower() for label in payload.get("labels", []) if str(label).strip()}


def _check_required_checks(payload: dict[str, Any]) -> tuple[list[str], list[str]]:
    blockers: list[str] = []
    pending: list[str] = []
    for check in payload.get("checks", []):
        if not isinstance(check, dict) or not check.get("required", False):
            continue
        name = str(check.get("name") or "(unnamed check)")
        status = str(check.get("status") or "").lower()
        conclusion = str(check.get("conclusion") or "").lower()
        if status != "completed":
            if status in PENDING_STATUSES or not status:
                pending.append(f"required check pending: {name}")
            else:
                blockers.append(f"required check in unexpected state: {name} ({status})")
            continue
        if conclusion not in SUCCESS_CONCLUSIONS:
            blockers.append(f"required check not successful: {name} ({conclusion or 'missing conclusion'})")
    return blockers, pending


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    pending: list[str] = []
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

    check_blockers, check_pending = _check_required_checks(payload)
    blockers.extend(check_blockers)
    pending.extend(check_pending)

    merge_probe = payload.get("mergeability_probe", {})
    if not isinstance(merge_probe, dict):
        merge_probe = {}
    probe_source = str(merge_probe.get("source") or "").lower()
    if merge_probe.get("uses_local_main", False):
        blockers.append("mergeability probe must not use local main; use GitHub state or origin/main")
    elif probe_source and probe_source not in GITHUB_NATIVE_MERGE_SOURCES:
        warnings.append(f"mergeability probe source is not GitHub-native/origin-main: {probe_source}")

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

    state = "eligible" if not blockers and not pending else "pending" if pending and not blockers else "blocked"

    return {
        "eligible": state == "eligible",
        "state": state,
        "blockers": blockers,
        "pending": pending,
        "warnings": warnings,
        "merge_guidance": [
            "wait for required checks to complete before making a final merge decision",
            "if GitHub reports the branch is behind, run gh pr update-branch <pr> instead of merging local main",
            "after checks pass, use GitHub-native merge/automerge: gh pr merge <pr> --merge --delete-branch or gh pr merge <pr> --auto",
        ],
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
    parser.add_argument("--allow-pending", action="store_true", help="Return success for expected pending required checks.")
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("input JSON must be an object")

    result = evaluate(payload)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.json_output:
        args.json_output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if result["eligible"]:
        return 0
    if result["state"] == "pending":
        return 0 if args.allow_pending else 3
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
