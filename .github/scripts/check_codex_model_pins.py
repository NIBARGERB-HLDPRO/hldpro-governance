import ast
import pathlib
import re
import shlex

allowed = {"gpt-5.4", "gpt-5.3-codex-spark"}
allowed_ext = {".py", ".sh", ".yml", ".yaml"}
fail = False
skip_paths = [pathlib.Path(".claude/worktrees"), pathlib.Path("generated"), pathlib.Path("local")]
yaml_ext = {".yml", ".yaml"}
run_key_re = re.compile(r"^(\s*)run:\s*(.*)$")
token_starters = {"if", "&&", "||", ";", "|", "(", "then", "do", "{", "!"}
model_flag_re = re.compile(r"^(?:-m|--model)=(.+)$")
reasoning_re = re.compile(r"model_reasoning_effort=")
dynamic_model_re = re.compile(r"[$({}]")


def in_skipped_path(path: pathlib.Path) -> bool:
    rel = path.as_posix()
    for skip_path in skip_paths:
        prefix = skip_path.as_posix().rstrip("/")
        if rel == prefix or rel.startswith(prefix + "/"):
            return True
    return False


def has_unescaped_backslash(line: str) -> bool:
    count = 0
    idx = len(line.rstrip()) - 1
    while idx >= 0 and line[idx] == "\\":
        count += 1
        idx -= 1
    return count % 2 == 1


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def inspect_invocation(invocation: list[str], path: pathlib.Path, line_no: int) -> None:
    global fail
    has_model = False
    has_reasoning = False
    model = None

    idx = 0
    while idx < len(invocation):
        arg = invocation[idx]
        if arg in {"-m", "--model"}:
            has_model = True
            if idx + 1 < len(invocation):
                model = strip_quotes(invocation[idx + 1])
                idx += 2
                continue
            idx += 1
            continue

        model_match = model_flag_re.match(arg)
        if model_match:
            has_model = True
            model = strip_quotes(model_match.group(1))
            idx += 1
            continue

        if arg == "-c":
            if idx + 1 < len(invocation) and reasoning_re.search(invocation[idx + 1]):
                has_reasoning = True
            idx += 1
            continue

        if arg.startswith("-c") and reasoning_re.search(arg):
            has_reasoning = True
        elif reasoning_re.search(arg):
            has_reasoning = True

        idx += 1

    if not has_model:
        print(
            f"::error file={path},line={line_no}::[codex-model-pins] 'codex exec' missing -m/--model on line"
        )
        fail = True
    elif model is not None and not dynamic_model_re.search(model) and model not in allowed:
        print(
            f"::error file={path},line={line_no}::[codex-model-pins] model '{model}' is not allowed; "
            "must be gpt-5.4 or gpt-5.3-codex-spark"
        )
        fail = True

    if not has_reasoning:
        print(
            f"::error file={path},line={line_no}::[codex-model-pins] 'codex exec' missing model_reasoning_effort on line"
        )
        fail = True


def iter_shell_lines(path: pathlib.Path, text: str):
    lines = text.splitlines()
    if path.suffix.lower() not in yaml_ext:
        for line_no, raw_line in enumerate(lines, start=1):
            yield line_no, raw_line
        return

    i = 0
    run_indent = None
    while i < len(lines):
        raw_line = lines[i]
        raw = raw_line.rstrip()

        if run_indent is not None:
            indent = len(raw_line) - len(raw_line.lstrip(" "))
            if raw.strip() and indent <= run_indent:
                run_indent = None
                continue
            if raw.strip():
                yield i + 1, raw[run_indent + 1 :]
            i += 1
            continue

        match = run_key_re.match(raw_line)
        if not match:
            i += 1
            continue

        prefix = len(match.group(1))
        suffix = match.group(2).strip()

        if not suffix:
            run_indent = prefix
            i += 1
            continue

        if suffix.startswith("|") or suffix.startswith(">"):
            run_indent = prefix
            i += 1
            continue

        yield i + 1, suffix
        i += 1


def inspect_shell(path: pathlib.Path, text: str) -> None:
    lines = list(iter_shell_lines(path, text))
    i = 0
    while i < len(lines):
        start_line, line = lines[i]
        command = ""
        while True:
            command += line.rstrip()
            if has_unescaped_backslash(line):
                command = command[:-1] + " "
                i += 1
                if i >= len(lines):
                    break
                line = lines[i][1]
                continue
            break

        if "codex" in command and "exec" in command:
            try:
                tokens = shlex.split(command)
            except ValueError:
                tokens = []
            for idx, token in enumerate(tokens):
                if token != "codex" or idx + 1 >= len(tokens) or tokens[idx + 1] != "exec":
                    continue
                if idx > 0 and tokens[idx - 1] not in token_starters and tokens[idx - 1] not in {";", "&&", "||"}:
                    continue
                inspect_invocation(tokens[idx + 2 :], path, start_line)

        i += 1


def inspect_python_list(path: pathlib.Path, text: str) -> None:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return
    for node in ast.walk(tree):
        if not isinstance(node, (ast.List, ast.Tuple)):
            continue
        parts: list[str] = []
        for element in node.elts:
            if isinstance(element, ast.Constant) and isinstance(element.value, str):
                parts.append(element.value)
            else:
                parts = []
                break
        if len(parts) < 2 or parts[0] != "codex" or parts[1] != "exec":
            continue
        inspect_invocation(parts[2:], path, getattr(node, "lineno", 1))


for path in sorted(pathlib.Path(".").rglob("*")):
    if not path.is_file():
        continue
    if in_skipped_path(path):
        continue
    if path.suffix.lower() not in allowed_ext:
        continue

    content = path.read_text(errors="replace")
    inspect_shell(path, content)
    inspect_python_list(path, content)

if fail:
    raise SystemExit(1)
