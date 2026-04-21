#!/usr/bin/env python3
"""Repo-specific issue lane bootstrap planner and validator."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


POLICY_PATH = Path("docs/lane_policies.json")


@dataclass(frozen=True)
class LanePolicy:
    name: str
    branch_pattern: str
    worktree_basename_pattern: str
    branch_template: str
    worktree_template: str
    cleanup_policy: str


def load_policy(root: Path, repo_slug: str) -> LanePolicy:
    payload = json.loads((root / POLICY_PATH).read_text(encoding="utf-8"))
    policy_name = payload.get("repo_policies", {}).get(repo_slug, payload.get("default_policy", "standard"))
    policy_payload = payload["policies"][policy_name]
    return LanePolicy(
        name=policy_name,
        branch_pattern=policy_payload["branch_pattern"],
        worktree_basename_pattern=policy_payload["worktree_basename_pattern"],
        branch_template=policy_payload["branch_template"],
        worktree_template=policy_payload["worktree_template"],
        cleanup_policy=policy_payload["cleanup_policy"],
    )


def normalize_slug(scope: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", scope.lower()).strip("-")
    if not slug:
        raise ValueError("scope slug must contain at least one alphanumeric character")
    return slug


def _match(pattern: str, value: str) -> re.Match[str] | None:
    return re.match(pattern, value)


def validate_lane(policy: LanePolicy, *, branch_name: str, worktree_path: str, issue_number: int) -> dict[str, Any]:
    branch_match = _match(policy.branch_pattern, branch_name)
    if not branch_match:
        return {
            "decision": "block",
            "reason": f"invalid branch pattern for policy {policy.name}",
            "expected_branch_pattern": policy.branch_pattern,
        }
    worktree_name = Path(worktree_path).name
    worktree_match = _match(policy.worktree_basename_pattern, worktree_name)
    if not worktree_match:
        return {
            "decision": "block",
            "reason": f"invalid worktree path pattern for policy {policy.name}",
            "expected_worktree_basename_pattern": policy.worktree_basename_pattern,
        }
    branch_issue = int(branch_match.group("issue"))
    worktree_issue = int(worktree_match.group("issue"))
    branch_scope = branch_match.group("scope")
    worktree_scope = worktree_match.group("scope")
    if branch_issue != issue_number:
        return {"decision": "block", "reason": "branch issue mismatch", "branch_issue": branch_issue}
    if worktree_issue != issue_number:
        return {"decision": "block", "reason": "worktree issue mismatch", "worktree_issue": worktree_issue}
    if branch_scope != worktree_scope:
        return {
            "decision": "block",
            "reason": "branch/worktree scope mismatch",
            "branch_scope": branch_scope,
            "worktree_scope": worktree_scope,
        }
    return {
        "decision": "allow",
        "reason": "lane_policy_matched",
        "policy": policy.name,
        "issue_number": issue_number,
        "scope_slug": branch_scope,
    }


def plan_lane(
    policy: LanePolicy,
    *,
    repo_slug: str,
    issue_number: int,
    scope_slug: str,
    worktree_root: str,
    base_ref: str,
) -> dict[str, Any]:
    scope = normalize_slug(scope_slug)
    branch_name = policy.branch_template.format(issue=issue_number, scope=scope)
    worktree_name = policy.worktree_template.format(issue=issue_number, scope=scope)
    worktree_path = str(Path(worktree_root) / worktree_name)
    return {
        "decision": "allow",
        "policy": policy.name,
        "branch_name": branch_name,
        "worktree_path": worktree_path,
        "command": f"HLDPRO_REPO_SLUG={repo_slug} HLDPRO_LANE_CLAIM_BOOTSTRAP=1 git worktree add -b {branch_name} {worktree_path} {base_ref}",
    }


def cleanup_advice(*, dirty: bool) -> dict[str, Any]:
    if dirty:
        return {
            "decision": "block",
            "reason": "dirty invalid lane cleanup refused",
            "next_action": "operator_review_required",
        }
    return {
        "decision": "allow",
        "reason": "clean invalid lane can be removed before implementation",
        "next_action": "remove clean worktree and recreate with lane bootstrap helper",
    }


def infer_repo_slug(cwd: Path) -> str:
    env_slug = ""
    try:
        env_slug = sys.argv[sys.argv.index("--repo-slug") + 1]
    except (ValueError, IndexError):
        env_slug = ""
    if env_slug:
        return env_slug
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=cwd, text=True).strip()
        return Path(root).name
    except Exception:
        return cwd.resolve().name


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--repo-slug")
    parser.add_argument("--json", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan")
    plan.add_argument("--issue-number", type=int, required=True)
    plan.add_argument("--scope-slug", required=True)
    plan.add_argument("--worktree-root", default="var/worktrees")
    plan.add_argument("--base-ref", default="origin/main")

    validate = subparsers.add_parser("validate")
    validate.add_argument("--branch-name", required=True)
    validate.add_argument("--worktree-path", required=True)
    validate.add_argument("--issue-number", type=int, required=True)

    cleanup = subparsers.add_parser("cleanup-advice")
    cleanup.add_argument("--dirty", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = Path(args.repo_root).resolve()
    repo_slug = args.repo_slug or infer_repo_slug(Path.cwd())
    policy = load_policy(root, repo_slug)

    if args.command == "plan":
        payload = plan_lane(
            policy,
            repo_slug=repo_slug,
            issue_number=args.issue_number,
            scope_slug=args.scope_slug,
            worktree_root=args.worktree_root,
            base_ref=args.base_ref,
        )
    elif args.command == "validate":
        payload = validate_lane(
            policy,
            branch_name=args.branch_name,
            worktree_path=args.worktree_path,
            issue_number=args.issue_number,
        )
    else:
        payload = cleanup_advice(dirty=args.dirty)

    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        print(payload["reason"] if "reason" in payload else payload["command"])
    return 0 if payload["decision"] == "allow" else 1


if __name__ == "__main__":
    raise SystemExit(main())
