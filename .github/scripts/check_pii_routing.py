import fnmatch
import json
import os
import re
import subprocess
import sys
import yaml

base_sha = os.environ.get("BASE_SHA", "")
head_sha = os.environ.get("HEAD_SHA", "")
if not base_sha or not head_sha:
    print("::warning::[check-pii-routing] Missing pull request context; skipping.")
    raise SystemExit(0)

with open(os.environ["GITHUB_EVENT_PATH"], "r", encoding="utf-8") as f:
    event = json.load(f)
labels = {l.get("name") for l in (event.get("pull_request") or {}).get("labels", []) if isinstance(l, dict)}

diff = subprocess.check_output(["git", "diff", "--name-only", f"{base_sha}...{head_sha}"], text=True).splitlines()
if not diff:
    print("[check-pii-routing] No files in diff.")
    raise SystemExit(0)

cfg = yaml.safe_load(open("scripts/lam/pii-patterns.yml", "r", encoding="utf-8"))
patterns = [re.compile(p, re.IGNORECASE) for p in cfg.get("patterns", [])]
markers = [m.lower() for m in cfg.get("field_markers", [])]
safe_paths = cfg.get("pii_safe_paths", [])

def safe_file(path):
    return any(fnmatch.fnmatch(path, patt) for patt in safe_paths)

pii_hits = []
for path in diff:
    if path.startswith("scripts/lam/"):
        continue
    if safe_file(path):
        continue
    if not os.path.exists(path):
        continue
    try:
        data = open(path, "r", encoding="utf-8", errors="replace").read()
    except Exception:
        continue

    for line_no, line in enumerate(data.splitlines(), start=1):
        lower = line.lower()
        if any(marker in lower for marker in markers):
            pii_hits.append((path, line_no))
            break
        if any(pattern.search(line) for pattern in patterns):
            pii_hits.append((path, line_no))
            break

has_lam_audit = any(
    p.startswith("raw/lam-audit/") and p.endswith(".manifest.json")
    for p in diff
)
has_pii_safe = "pii-safe" in labels

if pii_hits:
    for path, line_no in pii_hits:
        print(
            f"::error file={path},line={line_no}::[check-pii-routing] PII-like pattern detected; requires pii-safe label and lam audit manifest."
        )

if pii_hits and not has_pii_safe:
    raise SystemExit(1)

if pii_hits and not has_lam_audit:
    print("::error file=raw/lam-audit/*.manifest.json::[check-pii-routing] PII detected but no lam audit manifest in PR.")
    raise SystemExit(1)
