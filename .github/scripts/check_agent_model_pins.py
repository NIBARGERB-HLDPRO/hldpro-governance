import pathlib
import re
import sys
import yaml

allowed = {
    "opus",
    "sonnet",
    "haiku",
    "claude-opus-4-6",
    "claude-sonnet-4-6",
    "claude-haiku-4-5-20251001",
}

fail = False
excluded_dirs = {"commands", "playbooks", "templates", "schemas"}
base = pathlib.Path("agents")
for path in sorted(base.rglob("*.md")):
    if any(part in excluded_dirs for part in path.parts[1:]):
        continue
    raw = path.read_text(errors="replace")
    if not raw.startswith("---"):
        print(f"::error file={path},line=1::[agent-model-pins] missing YAML frontmatter block")
        fail = True
        continue

    parts = re.split(r"^---\s*$", raw, maxsplit=2, flags=re.M)
    if len(parts) < 3:
        print(f"::error file={path},line=1::[agent-model-pins] malformed YAML frontmatter")
        fail = True
        continue

    try:
        data = yaml.safe_load(parts[1]) or {}
    except Exception as exc:
        print(f"::error file={path},line=1::[agent-model-pins] YAML parse error: {exc}")
        fail = True
        continue

    model = data.get("model")
    if not model:
        print(f"::error file={path},line=1::[agent-model-pins] required key model is missing")
        fail = True
        continue

    if str(model) not in allowed:
        print(
            f"::error file={path},line=1::[agent-model-pins] model '{model}' is not in "
            f"{', '.join(sorted(allowed))}"
        )
        fail = True

if fail:
    raise SystemExit(1)
