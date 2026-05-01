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

python3 - "$FILE" <<'PY'
import re
import sys
import yaml


path = sys.argv[1]

with open(path, "r", encoding="utf-8", errors="replace") as handle:
    raw = handle.read()

if not raw.startswith("---"):
    print(f"::error file={path},line=1::[require-dual-signature] missing YAML frontmatter")
    sys.exit(1)

parts = re.split(r"^---\s*$", raw, maxsplit=2, flags=re.M)
if len(parts) < 3:
    print(f"::error file={path},line=1::[require-dual-signature] malformed YAML frontmatter")
    sys.exit(1)

try:
    data = yaml.safe_load(parts[1]) or {}
except Exception as exc:
    print(f"::error file={path},line=1::[require-dual-signature] failed to parse YAML frontmatter: {exc}")
    sys.exit(1)

if not isinstance(data, dict):
    print(f"::error file={path},line=1::[require-dual-signature] frontmatter must be a mapping")
    sys.exit(1)


def parse_schema_version(value):
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"v(\d+)(?:\.\d+)?", value.strip(), flags=re.I)
    if not match:
        return None
    return int(match.group(1))


schema_version = data.get("schema_version")
schema_version_num = parse_schema_version(schema_version)
if schema_version_num is None:
    print(
        f"::error file={path},line=1::[require-dual-signature] schema_version missing/invalid; historical artifacts must set schema_version: v1 and new artifacts must set v2+"
    )
    sys.exit(1)

required_v1 = {"pr_number", "pr_scope", "drafter", "reviewer", "invariants_checked"}
required_v2 = required_v1 | {"gate_identity"}

if schema_version_num == 1:
    required = required_v1
else:
    required = required_v2

missing = sorted(required - set(data.keys()))
if missing:
    print(
        f"::error file={path},line=1::[require-dual-signature] missing required keys for schema_version {schema_version}: {', '.join(missing)}"
    )
    sys.exit(1)


def validate_identity(entity_path, payload, *, require_verdict=False):
    if not isinstance(payload, dict):
        print(f"::error file={path},line=1::[require-dual-signature] {entity_path} must be an object")
        sys.exit(1)

    required_fields = {"role", "model_id", "model_family", "signature_date"}
    if require_verdict:
        required_fields.add("verdict")

    missing_fields = sorted(required_fields - set(payload.keys()))
    if missing_fields:
        print(
            f"::error file={path},line=1::[require-dual-signature] {entity_path} missing fields: {', '.join(missing_fields)}"
        )
        sys.exit(1)

    verdict = (payload.get("verdict") or "").upper()
    if require_verdict and verdict not in {"APPROVED", "APPROVED_WITH_CHANGES"}:
        print(
            f"::error file={path},line=1::[require-dual-signature] {entity_path}.verdict must be APPROVED or APPROVED_WITH_CHANGES"
        )
        sys.exit(1)

    signature_date = payload.get("signature_date")
    if signature_date is None:
        print(
            f"::error file={path},line=1::[require-dual-signature] {entity_path}.signature_date must be a non-empty string"
        )
        sys.exit(1)
    if isinstance(signature_date, str) and not signature_date.strip():
        print(
            f"::error file={path},line=1::[require-dual-signature] {entity_path}.signature_date must not be empty"
        )
        sys.exit(1)

    model_id = payload.get("model_id")
    if model_id is None:
        print(
            f"::error file={path},line=1::[require-dual-signature] {entity_path}.model_id must be a non-empty string"
        )
        sys.exit(1)

    if isinstance(model_id, str) and not model_id.strip():
        print(
            f"::error file={path},line=1::[require-dual-signature] {entity_path}.model_id must not be empty"
        )
        sys.exit(1)

    model_family = payload.get("model_family")
    if model_family is None:
        print(
            f"::error file={path},line=1::[require-dual-signature] {entity_path}.model_family must be a non-empty string"
        )
        sys.exit(1)

    if isinstance(model_family, str) and not model_family.strip():
        print(
            f"::error file={path},line=1::[require-dual-signature] {entity_path}.model_family must not be empty"
        )
        sys.exit(1)


drafter = data.get("drafter")
reviewer = data.get("reviewer")
validate_identity("drafter", drafter)
validate_identity("reviewer", reviewer, require_verdict=True)

# AC8: same-login check — drafter and reviewer GitHub login strings must differ
drafter_login = str(drafter.get("github_login", drafter.get("login", "")) or "").strip().lower()
reviewer_login = str(reviewer.get("github_login", reviewer.get("login", "")) or "").strip().lower()
if drafter_login and reviewer_login and drafter_login == reviewer_login:
    print(
        f"::error file={path},line=1::[require-dual-signature] drafter and reviewer must be different GitHub logins; both are '{drafter_login}'"
    )
    sys.exit(1)

gate_identity = data.get("gate_identity")
if schema_version_num >= 2:
    validate_identity("gate_identity", gate_identity)
elif "gate_identity" in data:
    validate_identity("gate_identity", gate_identity)

model_ids = [drafter.get("model_id"), reviewer.get("model_id")]

if drafter.get("model_id") == reviewer.get("model_id"):
    print(
        f"::error file={path},line=1::[require-dual-signature] drafter.model_id must differ from reviewer.model_id"
    )
    sys.exit(1)

if drafter.get("model_family") == reviewer.get("model_family"):
    print(
        f"::error file={path},line=1::[require-dual-signature] drafter.model_family must differ from reviewer.model_family"
    )
    sys.exit(1)

if schema_version_num >= 2:
    model_ids.append(gate_identity.get("model_id"))

if len(set(model_ids)) != len(model_ids):
    print(
        f"::error file={path},line=1::[require-dual-signature] drafter/reviewer/gate model_id values must be distinct"
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
