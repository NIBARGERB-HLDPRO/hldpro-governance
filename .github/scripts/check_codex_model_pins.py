import pathlib
import re

allowed = {"gpt-5.4", "gpt-5.3-codex-spark"}
fail = False
allowed_ext = {".py", ".sh", ".yml", ".yaml"}
exec_re = re.compile(r"\bcodex\s+exec\b")
model_re = re.compile(r"(?:^|\\s)(?:-m|--model)(?:=|\\s+)([\\\"']?)([^\\s\"']+)\\1")

for path in sorted(pathlib.Path(".").rglob("*")):
    if path.as_posix().startswith(".github/workflows/"):
        continue
    if not path.is_file():
        continue
    if path.suffix.lower() not in allowed_ext:
        continue

    for line_no, line in enumerate(path.read_text(errors="replace").splitlines(), start=1):
        if not exec_re.search(line):
            continue

        matches = model_re.findall(line)
        if not matches:
            print(
                f"::error file={path},line={line_no}::[codex-model-pins] 'codex exec' missing -m/--model on line"
            )
            fail = True
            continue

        model = matches[0][1]
        if model not in allowed:
            print(
                f"::error file={path},line={line_no}::[codex-model-pins] model '{model}' is not allowed; "
                "must be gpt-5.4 or gpt-5.3-codex-spark"
            )
            fail = True

if fail:
    raise SystemExit(1)
