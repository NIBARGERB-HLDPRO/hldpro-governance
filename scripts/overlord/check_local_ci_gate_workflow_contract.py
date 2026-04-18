#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


WORKFLOW = Path(".github/workflows/local-ci-gate.yml")
INDEPENDENT_WORKFLOW = Path(".github/workflows/graphify-governance-contract.yml")
TEST_SCRIPT = "scripts/overlord/test_local_ci_gate_workflow_contract.py"


def _load_workflow(text: str, label: str, failures: list[str]) -> dict:
    try:
        loaded = yaml.load(text, Loader=yaml.BaseLoader)
    except yaml.YAMLError as exc:
        failures.append(f"{label} workflow must parse as YAML: {exc}")
        return {}
    if not isinstance(loaded, dict):
        failures.append(f"{label} workflow must be a YAML mapping")
        return {}
    return loaded


def _contains_main_branch(trigger: object) -> bool:
    if not isinstance(trigger, dict):
        return False
    branches = trigger.get("branches")
    if isinstance(branches, str):
        return branches == "main"
    if isinstance(branches, list):
        return "main" in branches
    return False


def _steps(workflow: dict, job_id: str | None = None) -> list[dict]:
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        return []

    if job_id is not None:
        job = jobs.get(job_id)
        if not isinstance(job, dict):
            return []
        raw_steps = job.get("steps")
        return [step for step in raw_steps if isinstance(step, dict)] if isinstance(raw_steps, list) else []

    steps: list[dict] = []
    for job in jobs.values():
        if not isinstance(job, dict):
            continue
        raw_steps = job.get("steps")
        if isinstance(raw_steps, list):
            steps.extend(step for step in raw_steps if isinstance(step, dict))
    return steps


def _step_named(steps: list[dict], name: str) -> dict:
    for step in steps:
        if step.get("name") == name:
            return step
    return {}


def _executable_lines(run: str) -> list[str]:
    lines: list[str] = []
    for raw_line in run.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def _step_executable_lines(step: dict) -> list[str]:
    run = step.get("run")
    if not isinstance(run, str):
        return []
    return _executable_lines(run)


def _normalized_run(step: dict) -> str:
    joined = " ".join(_step_executable_lines(step))
    return joined.replace("\\ ", " ").replace("\\", " ")


def _all_run_commands(steps: list[dict]) -> list[str]:
    return [_normalized_run(step) for step in steps if _normalized_run(step)]


def _all_executable_lines(steps: list[dict]) -> list[str]:
    lines: list[str] = []
    for step in steps:
        lines.extend(_step_executable_lines(step))
    return lines


def _has_executable_line_starting_with(steps: list[dict], required: str) -> bool:
    return any(line.startswith(required) for line in _all_executable_lines(steps))


def _failures_for_text(workflow_text: str, independent_text: str) -> list[str]:
    failures: list[str] = []
    workflow = _load_workflow(workflow_text, "local-ci-gate", failures)
    independent_workflow = _load_workflow(independent_text, "independent", failures)

    on = workflow.get("on")
    if not isinstance(on, dict):
        failures.append("local-ci-gate workflow must declare triggers")
        on = {}
    env = workflow.get("env")
    if not isinstance(env, dict) or env.get("PYTHONDONTWRITEBYTECODE") != "1":
        failures.append("local-ci-gate workflow must disable Python bytecode writes")

    pull_request = on.get("pull_request")
    push = on.get("push")
    if not _contains_main_branch(pull_request):
        failures.append("local-ci-gate workflow must run on pull_request to main")
    if not _contains_main_branch(push):
        failures.append("local-ci-gate workflow must run on push to main")

    local_steps = _steps(workflow, "local-ci-gate")
    if not local_steps:
        failures.append("local-ci-gate workflow must define a local-ci-gate job with steps")

    checkout_steps = [
        step
        for step in local_steps
        if isinstance(step.get("uses"), str) and step["uses"].startswith("actions/checkout@")
    ]
    if not checkout_steps:
        failures.append("local-ci-gate workflow must use actions/checkout")
    elif not all(isinstance(step.get("with"), dict) and step["with"].get("fetch-depth") == "0" for step in checkout_steps):
        failures.append("every local-ci-gate checkout step must use fetch-depth: 0")

    fetch_step = _step_named(local_steps, "Fetch main for changed-file resolution")
    if not any(line.startswith("git fetch origin main") for line in _step_executable_lines(fetch_step)):
        failures.append("local-ci-gate workflow must fetch origin main for changed-file resolution")

    branch_step = _step_named(local_steps, "Normalize PR branch name for Local CI Gate")
    branch_command = _normalized_run(branch_step)
    if "github.event_name == 'pull_request'" not in str(branch_step.get("if", "")):
        failures.append("local-ci-gate workflow must normalize branch names only for pull requests")
    if not branch_command.startswith("git checkout -B"):
        failures.append("local-ci-gate workflow must normalize the PR branch name before running the gate")

    runner_step = _step_named(local_steps, "Run Local CI Gate")
    runner_command = _normalized_run(runner_step)
    if not runner_command.startswith("python3 tools/local-ci-gate/bin/hldpro-local-ci run"):
        failures.append("local-ci-gate workflow must invoke the Local CI Gate runner")
    elif "--profile hldpro-governance" not in runner_command:
        failures.append("local-ci-gate workflow must run the hldpro-governance profile")
    if "--dry-run" in runner_command:
        failures.append("local-ci-gate workflow must not use --dry-run")

    contract_step = _step_named(local_steps, "Validate Local CI Gate workflow contract")
    if not any(line.startswith(f"python3 {TEST_SCRIPT}") for line in _step_executable_lines(contract_step)):
        failures.append("local-ci-gate workflow must run its contract test")

    independent_steps = _steps(independent_workflow)
    if not _has_executable_line_starting_with(independent_steps, f"python3 {TEST_SCRIPT}"):
        failures.append("an independent CI-visible workflow must run the Local CI Gate workflow contract test")

    return failures


def check_contract(repo_root: Path) -> list[str]:
    workflow_path = repo_root / WORKFLOW
    independent_path = repo_root / INDEPENDENT_WORKFLOW
    failures: list[str] = []

    if not workflow_path.is_file():
        failures.append(f"missing workflow: {WORKFLOW}")
        workflow_text = ""
    else:
        workflow_text = workflow_path.read_text(encoding="utf-8")

    if not independent_path.is_file():
        failures.append(f"missing independent workflow: {INDEPENDENT_WORKFLOW}")
        independent_text = ""
    else:
        independent_text = independent_path.read_text(encoding="utf-8")

    failures.extend(_failures_for_text(workflow_text, independent_text))
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Local CI Gate workflow hardgate contract.")
    parser.add_argument("--root", default=".", help="Repository root to validate")
    args = parser.parse_args(argv)

    failures = check_contract(Path(args.root).resolve())
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("PASS local-ci-gate workflow contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
