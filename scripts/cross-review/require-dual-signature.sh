#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "::error::[require-dual-signature] expected exactly one argument: <cross-review-file>"
  exit 1
fi

FILE="$1"
if [ ! -f "${FILE}" ]; then
  echo "::error file=${FILE}::[require-dual-signature] cross-review file not found"
  exit 1
fi

export PY_DATA
PY_DATA="$(python3 -c "import yaml,sys,json; doc=open(sys.argv[1]).read(); fm=doc.split('---')[1]; data=yaml.safe_load(fm); print(json.dumps(data, default=str))" "${FILE}")"
if [ -z "${PY_DATA}" ] || [ "${PY_DATA}" = "null" ]; then
  echo "::error file=${FILE},line=1::[require-dual-signature] failed to parse YAML frontmatter"
  exit 1
fi

python3 - "$FILE" "$PY_DATA" <<'PY'
import json
import sys

path = sys.argv[1]
text = sys.argv[2]
data = json.loads(text) if text else {}

required = {
    "pr_number",
    "pr_scope",
    "drafter",
    "reviewer",
    "invariants_checked",
}

if not isinstance(data, dict):
    print(f"::error file={path},line=1::[require-dual-signature] frontmatter must be a mapping")
    sys.exit(1)

missing = sorted(required - set(data.keys()))
if missing:
    print(f"::error file={path},line=1::[require-dual-signature] missing required keys: {', '.join(missing)}")
    sys.exit(1)

drafter = data.get("drafter") or {}
reviewer = data.get("reviewer") or {}
if not isinstance(drafter, dict) or not isinstance(reviewer, dict):
    print(f"::error file={path},line=1::[require-dual-signature] drafter and reviewer must be objects")
    sys.exit(1)

drafter_required = {"role", "model_id", "model_family", "signature_date"}
reviewer_required = {"role", "model_id", "model_family", "signature_date", "verdict"}
missing_drafter = sorted(drafter_required - set(drafter.keys()))
missing_reviewer = sorted(reviewer_required - set(reviewer.keys()))
if missing_drafter:
    print(f"::error file={path},line=1::[require-dual-signature] missing drafter fields: {', '.join(missing_drafter)}")
    sys.exit(1)
if missing_reviewer:
    print(f"::error file={path},line=1::[require-dual-signature] missing reviewer fields: {', '.join(missing_reviewer)}")
    sys.exit(1)

if drafter.get("model_id") == reviewer.get("model_id"):
    print(f"::error file={path},line=1::[require-dual-signature] drafter.model_id must differ from reviewer.model_id")
    sys.exit(1)
if drafter.get("model_family") == reviewer.get("model_family"):
    print(f"::error file={path},line=1::[require-dual-signature] drafter.model_family must differ from reviewer.model_family")
    sys.exit(1)

verdict = (reviewer.get("verdict") or "").upper()
if verdict not in {"APPROVED", "APPROVED_WITH_CHANGES"}:
    print(
        f"::error file={path},line=1::[require-dual-signature] verdict must be APPROVED or APPROVED_WITH_CHANGES"
    )
    sys.exit(1)

inv = data.get("invariants_checked")
if not isinstance(inv, dict):
    print(f"::error file={path},line=1::[require-dual-signature] invariants_checked must be an object")
    sys.exit(1)

for key, value in inv.items():
    if value is not True:
        print(f"::error file={path},line=1::[require-dual-signature] invariant '{key}' must be true")
        sys.exit(1)

print(f"[require-dual-signature] {path} passed validation")
PY
