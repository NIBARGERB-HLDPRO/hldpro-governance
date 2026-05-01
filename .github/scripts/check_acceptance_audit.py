import json
import os
import re
from json import JSONDecodeError
from pathlib import Path


head_ref = os.environ.get("HEAD_REF", "")
planning_only = os.environ.get("PLANNING_ONLY", "")

if planning_only == "true":
    print("[check-acceptance-audit] PLANNING_ONLY=true; skipping gate check.")
    raise SystemExit(0)

match = re.search(r"issue-(\d+)", head_ref, re.I)
if not match:
    print("[check-acceptance-audit] non-issue branch, skipping")
    raise SystemExit(0)

issue_number = int(match.group(1))

for audit_file in sorted(Path("raw/acceptance-audits").glob("*.json")):
    try:
        data = json.loads(audit_file.read_text())
    except JSONDecodeError:
        print(f"::warning::[check-acceptance-audit] Invalid JSON in {audit_file}")
        continue

    if data.get("issue_number") == issue_number and data.get("overall_verdict") == "PASS":
        print(f"::notice::[check-acceptance-audit] Found PASS artifact {audit_file} for issue {issue_number}.")
        raise SystemExit(0)

print(
    f"::error::[check-acceptance-audit] No functional-acceptance-auditor PASS artifact found for issue {issue_number} on branch {head_ref}."
)
raise SystemExit(1)
