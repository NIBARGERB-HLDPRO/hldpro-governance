import os
import pathlib
import re
import subprocess
import yaml


def parse_schema_version(value):
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"v(\d+)(?:\.\d+)?", value.strip(), flags=re.I)
    if not match:
        return None
    return int(match.group(1))


base_sha = os.environ.get("BASE_SHA", "")
head_sha = os.environ.get("HEAD_SHA", "")
if not base_sha or not head_sha:
    print("::warning::[check-no-self-approval] Missing pull request context; skipping.")
    raise SystemExit(0)

diff = subprocess.check_output(["git", "diff", "--name-only", f"{base_sha}...{head_sha}"], text=True).splitlines()
cross_files = sorted(p for p in diff if p.startswith("raw/cross-review/") and p.endswith(".md"))
if not cross_files:
    print("[check-no-self-approval] No cross-review files in diff.")
    raise SystemExit(0)

fail = False
for path in cross_files:
    file_fail = False
    fp = pathlib.Path(path)
    if not fp.exists():
        print(f"::error file={path},line=1::[check-no-self-approval] cross-review file missing")
        fail = True
        continue

    raw = fp.read_text(encoding="utf-8", errors="replace")
    if not raw.startswith("---"):
        print(f"::error file={path},line=1::[check-no-self-approval] missing YAML frontmatter")
        fail = True
        continue

    parts = re.split(r"^---\s*$", raw, maxsplit=2, flags=re.M)
    if len(parts) < 3:
        print(f"::error file={path},line=1::[check-no-self-approval] malformed YAML frontmatter")
        fail = True
        continue

    try:
        data = yaml.safe_load(parts[1]) or {}
    except Exception as exc:
        print(f"::error file={path},line=1::[check-no-self-approval] YAML parse failed: {exc}")
        fail = True
        continue

    if not isinstance(data, dict):
        print(f"::error file={path},line=1::[check-no-self-approval] frontmatter must be a mapping")
        fail = True
        continue

    schema_version = parse_schema_version(data.get("schema_version"))
    if schema_version is None:
        print(
            f"::error file={path},line=1::[check-no-self-approval] missing schema_version; historical files must set schema_version: v1"
        )
        fail = True
        continue

    drafter = data.get("drafter")
    reviewer_data = data.get("reviewer")
    gate_data = data.get("gate_identity")

    if schema_version >= 2:
        for label, entity in (
            ("drafter", drafter),
            ("reviewer", reviewer_data),
            ("gate_identity", gate_data),
        ):
            if not isinstance(entity, dict):
                print(
                    f"::error file={path},line=1::[check-no-self-approval] {label} must be an object for v{schema_version}"
                )
                file_fail = True
                continue
            for field in ("model_id", "model_family"):
                if not isinstance(entity.get(field), str) or not entity.get(field):
                    print(
                        f"::error file={path},line=1::[check-no-self-approval] {label}.{field} must be a non-empty string for v{schema_version}"
                    )
                    file_fail = True

        if file_fail:
            fail = True
            continue

    elif gate_data is not None:
        if not isinstance(gate_data, dict):
            print(f"::error file={path},line=1::[check-no-self-approval] gate_identity must be an object when present")
            file_fail = True
        else:
            for field in ("model_id", "model_family"):
                if not isinstance(gate_data.get(field), str) or not gate_data.get(field):
                    print(
                        f"::error file={path},line=1::[check-no-self-approval] gate_identity.{field} must be a non-empty string when present"
                    )
                    file_fail = True
        if file_fail:
            fail = True
            continue

    d_id = drafter.get("model_id") if isinstance(drafter, dict) else None
    r_id = reviewer_data.get("model_id") if isinstance(reviewer_data, dict) else None
    d_family = drafter.get("model_family") if isinstance(drafter, dict) else None
    r_family = reviewer_data.get("model_family") if isinstance(reviewer_data, dict) else None

    if schema_version < 2:
        if d_id is not None and r_id is not None and d_id == r_id:
            print(
                f"::error file={path},line=1::[check-no-self-approval] drafter.model_id must not equal reviewer.model_id"
            )
            file_fail = True
        if d_family is not None and r_family is not None and d_family == r_family:
            print(
                f"::error file={path},line=1::[check-no-self-approval] drafter.model_family must not equal reviewer.model_family"
            )
            file_fail = True
        if file_fail:
            fail = True
        continue

    if d_id == r_id:
        print(f"::error file={path},line=1::[check-no-self-approval] drafter.model_id must not equal reviewer.model_id")
        file_fail = True
    if d_family == r_family:
        print(
            f"::error file={path},line=1::[check-no-self-approval] drafter.model_family must not equal reviewer.model_family"
        )
        file_fail = True

    g_id = gate_data.get("model_id") if isinstance(gate_data, dict) else None
    g_family = gate_data.get("model_family") if isinstance(gate_data, dict) else None
    if len({d_id, r_id, g_id}) != 3:
        print(
            f"::error file={path},line=1::[check-no-self-approval] drafter, reviewer, and gate model_id values must be pairwise distinct"
        )
        file_fail = True

    if file_fail:
        fail = True

if fail:
    raise SystemExit(1)
