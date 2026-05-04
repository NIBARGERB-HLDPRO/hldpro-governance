#!/usr/bin/env python3
"""Check for a functional acceptance audit PASS artifact for a PR's issue number."""
import sys
import re
import json
from pathlib import Path


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", required=True, help="Branch name (e.g., issue-659-*)")
    parser.add_argument("--audit-dir", default="raw/acceptance-audits",
                        help="Directory containing audit artifacts")
    parser.add_argument("--planning-only", action="store_true",
                        help="Exempt planning-only PRs")
    args = parser.parse_args()

    if args.planning_only:
        print("::notice::Planning-only PR exempted from acceptance audit check.")
        return 0

    # Extract issue number from branch name
    match = re.search(r"(?:^|[-_/])issue-(\d+)(?:[-_/]|$)", args.branch)
    if not match:
        print("::notice::Non-issue branch exempted from acceptance audit check.")
        return 0

    issue_number = int(match.group(1))
    audit_dir = Path(args.audit_dir)

    if not audit_dir.exists():
        print(
            f"::error::Acceptance audit directory {audit_dir} does not exist. "
            f"Create raw/acceptance-audits/ and add a PASS audit artifact for issue #{issue_number}."
        )
        return 1

    # Search for matching PASS artifact
    for audit_file in sorted(audit_dir.glob("*.json")):
        try:
            data = json.loads(audit_file.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if (data.get("issue_number") == issue_number and
                data.get("overall_verdict") == "PASS"):
            print(f"::notice::Found PASS acceptance audit artifact: {audit_file}")
            return 0

    print(
        f"::error::No acceptance audit PASS artifact found for issue #{issue_number} "
        f"in {audit_dir}/. Run the functional-acceptance-auditor agent and commit the "
        f"result before merging."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
