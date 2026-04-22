#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT_GLOB = "docs/examples/sql-schema-drift/*.json"
SAFE_ID = re.compile(r"^[A-Za-z0-9._/-]+$")
SQL_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
ALLOWED_PLACEMENTS = {
    "repo-local-local-ci-profile",
    "consumer-profile",
    "documented-deferral",
}
ALLOWED_METADATA_SOURCES = {
    "information_schema.columns": ("information_schema.columns",),
    "pg_catalog": ("pg_catalog",),
    "sqlite_pragma_table_info": ("pragma_table_info",),
}
DESTRUCTIVE_OPERATIONS = {"wipe", "reset", "migration", "drop", "truncate", "delete"}


def _display(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _require(condition: bool, failures: list[str], message: str) -> None:
    if not condition:
        failures.append(message)


def _load_contract(path: Path) -> tuple[Any | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"could not parse JSON: {exc}"]


def _safe_non_empty_string(value: Any, field: str, failures: list[str], *, pattern: re.Pattern[str] | None = None) -> str:
    if not isinstance(value, str) or not value.strip():
        failures.append(f"`{field}` must be a non-empty string")
        return ""
    normalized = value.strip()
    if pattern is not None and not pattern.fullmatch(normalized):
        failures.append(f"`{field}` has invalid format: {normalized}")
    return normalized


def _column_key(raw: Any, field: str, failures: list[str]) -> tuple[str, str, str] | None:
    if not isinstance(raw, dict):
        failures.append(f"`{field}` must be an object")
        return None
    schema = _safe_non_empty_string(raw.get("schema"), f"{field}.schema", failures, pattern=SQL_IDENTIFIER)
    table = _safe_non_empty_string(raw.get("table"), f"{field}.table", failures, pattern=SQL_IDENTIFIER)
    column = _safe_non_empty_string(raw.get("column"), f"{field}.column", failures, pattern=SQL_IDENTIFIER)
    if not schema or not table or not column:
        return None
    return schema, table, column


def _fixture_columns(payload: dict[str, Any], failures: list[str]) -> set[tuple[str, str, str]]:
    fixture = payload.get("schema_fixture")
    if not isinstance(fixture, dict):
        failures.append("`schema_fixture` must be an object for sql_surface=true")
        return set()
    relations = fixture.get("relations")
    if not isinstance(relations, list) or not relations:
        failures.append("`schema_fixture.relations` must be a non-empty array")
        return set()

    columns: set[tuple[str, str, str]] = set()
    for index, relation in enumerate(relations, start=1):
        prefix = f"schema_fixture.relations[{index}]"
        if not isinstance(relation, dict):
            failures.append(f"`{prefix}` must be an object")
            continue
        schema = _safe_non_empty_string(relation.get("schema"), f"{prefix}.schema", failures, pattern=SQL_IDENTIFIER)
        table = _safe_non_empty_string(relation.get("table"), f"{prefix}.table", failures, pattern=SQL_IDENTIFIER)
        raw_columns = relation.get("columns")
        if not isinstance(raw_columns, list) or not raw_columns:
            failures.append(f"`{prefix}.columns` must be a non-empty array")
            continue
        for column_index, raw_column in enumerate(raw_columns, start=1):
            column = _safe_non_empty_string(
                raw_column,
                f"{prefix}.columns[{column_index}]",
                failures,
                pattern=SQL_IDENTIFIER,
            )
            if schema and table and column:
                columns.add((schema, table, column))
    return columns


def _validate_metadata_probe(payload: dict[str, Any], failures: list[str]) -> tuple[str, list[tuple[str, str, str]]]:
    probe = payload.get("metadata_probe")
    if not isinstance(probe, dict):
        failures.append("`metadata_probe` must be an object for sql_surface=true")
        return "", []

    probe_id = _safe_non_empty_string(probe.get("id"), "metadata_probe.id", failures, pattern=SAFE_ID)
    _safe_non_empty_string(probe.get("dialect"), "metadata_probe.dialect", failures, pattern=SAFE_ID)
    metadata_source = _safe_non_empty_string(probe.get("metadata_source"), "metadata_probe.metadata_source", failures)
    metadata_query = _safe_non_empty_string(probe.get("metadata_query"), "metadata_probe.metadata_query", failures)

    if metadata_source and metadata_source not in ALLOWED_METADATA_SOURCES:
        failures.append(
            "`metadata_probe.metadata_source` must be one of "
            + ", ".join(sorted(ALLOWED_METADATA_SOURCES))
        )
    elif metadata_source and metadata_query:
        lowered_query = metadata_query.lower()
        expected_tokens = ALLOWED_METADATA_SOURCES[metadata_source]
        if not any(token in lowered_query for token in expected_tokens):
            failures.append("`metadata_probe.metadata_query` must query the declared schema metadata source")

    raw_required = probe.get("required_columns")
    if not isinstance(raw_required, list) or not raw_required:
        failures.append("`metadata_probe.required_columns` must be a non-empty array")
        return probe_id, []

    required_columns: list[tuple[str, str, str]] = []
    for index, column in enumerate(raw_required, start=1):
        key = _column_key(column, f"metadata_probe.required_columns[{index}]", failures)
        if key is not None:
            required_columns.append(key)
    return probe_id, required_columns


def _validate_destructive_operations(payload: dict[str, Any], probe_id: str, failures: list[str]) -> None:
    operations = payload.get("destructive_operations")
    if not isinstance(operations, list) or not operations:
        failures.append("`destructive_operations` must be a non-empty array for sql_surface=true")
        return

    for index, operation in enumerate(operations, start=1):
        prefix = f"destructive_operations[{index}]"
        if not isinstance(operation, dict):
            failures.append(f"`{prefix}` must be an object")
            continue
        _safe_non_empty_string(operation.get("path"), f"{prefix}.path", failures, pattern=SAFE_ID)
        op_name = _safe_non_empty_string(operation.get("operation"), f"{prefix}.operation", failures, pattern=SAFE_ID)
        if op_name and op_name not in DESTRUCTIVE_OPERATIONS:
            failures.append(f"`{prefix}.operation` must be one of {', '.join(sorted(DESTRUCTIVE_OPERATIONS))}")
        if operation.get("preflight_probe_id") != probe_id:
            failures.append(f"`{prefix}.preflight_probe_id` must match metadata_probe.id")
        if operation.get("preflight_required_before_mutation") is not True:
            failures.append(f"`{prefix}.preflight_required_before_mutation` must be true")


def _validate_negative_controls(
    payload: dict[str, Any],
    fixture_columns: set[tuple[str, str, str]],
    failures: list[str],
) -> None:
    controls = payload.get("negative_controls")
    if not isinstance(controls, list) or not controls:
        failures.append("`negative_controls` must be a non-empty array for sql_surface=true")
        return

    fixture_relations = {(schema, table) for schema, table, _column in fixture_columns}
    for index, control in enumerate(controls, start=1):
        prefix = f"negative_controls[{index}]"
        if not isinstance(control, dict):
            failures.append(f"`{prefix}` must be an object")
            continue
        _safe_non_empty_string(control.get("name"), f"{prefix}.name", failures, pattern=SAFE_ID)
        stale_key = _column_key(control.get("stale_reference"), f"{prefix}.stale_reference", failures)
        _safe_non_empty_string(control.get("expected_failure"), f"{prefix}.expected_failure", failures)
        if stale_key is None:
            continue
        stale_schema, stale_table, _stale_column = stale_key
        if (stale_schema, stale_table) not in fixture_relations:
            failures.append(f"`{prefix}.stale_reference` table must exist in schema_fixture")
        if stale_key in fixture_columns:
            failures.append(f"`{prefix}.stale_reference` must be absent from schema_fixture")


def _validate_local_ci_hook(payload: dict[str, Any], failures: list[str]) -> None:
    hook = payload.get("local_ci_profile_hook")
    if not isinstance(hook, dict):
        failures.append("`local_ci_profile_hook` must be an object for sql_surface=true")
        return
    _safe_non_empty_string(hook.get("profile"), "local_ci_profile_hook.profile", failures, pattern=SAFE_ID)
    _safe_non_empty_string(hook.get("check_id"), "local_ci_profile_hook.check_id", failures, pattern=SAFE_ID)
    paths = hook.get("paths")
    if not isinstance(paths, list) or not paths:
        failures.append("`local_ci_profile_hook.paths` must be a non-empty array")
    elif not all(isinstance(path, str) and path.strip() for path in paths):
        failures.append("`local_ci_profile_hook.paths` entries must be non-empty strings")
    command = hook.get("command")
    if not isinstance(command, list) or not command:
        failures.append("`local_ci_profile_hook.command` must be a non-empty array")
    elif not all(isinstance(part, str) and part.strip() for part in command):
        failures.append("`local_ci_profile_hook.command` entries must be non-empty strings")


def validate_contract(payload: Any) -> list[str]:
    failures: list[str] = []
    if not isinstance(payload, dict):
        return ["top-level JSON must be an object"]

    _require(payload.get("schema_version") == "v1", failures, "`schema_version` must be v1")
    _safe_non_empty_string(payload.get("contract_id"), "contract_id", failures, pattern=SAFE_ID)
    _safe_non_empty_string(payload.get("repo"), "repo", failures, pattern=SAFE_ID)
    placement = _safe_non_empty_string(payload.get("placement"), "placement", failures)
    if placement and placement not in ALLOWED_PLACEMENTS:
        failures.append("`placement` must be one of " + ", ".join(sorted(ALLOWED_PLACEMENTS)))

    sql_surface = payload.get("sql_surface")
    if not isinstance(sql_surface, bool):
        failures.append("`sql_surface` must be a boolean")
        return failures
    if sql_surface is False:
        _safe_non_empty_string(payload.get("residual_risk"), "residual_risk", failures)
        return failures

    if placement != "repo-local-local-ci-profile":
        failures.append("sql_surface=true contracts must use repo-local-local-ci-profile placement")

    probe_id, required_columns = _validate_metadata_probe(payload, failures)
    fixture_columns = _fixture_columns(payload, failures)
    for column in required_columns:
        if column not in fixture_columns:
            failures.append(
                "`metadata_probe.required_columns` must exist in schema_fixture: "
                + ".".join(column)
            )
    _validate_destructive_operations(payload, probe_id, failures)
    _validate_negative_controls(payload, fixture_columns, failures)
    _validate_local_ci_hook(payload, failures)
    _safe_non_empty_string(payload.get("residual_risk"), "residual_risk", failures)
    return failures


def _contract_paths(root: Path, explicit_paths: list[Path]) -> list[Path]:
    if explicit_paths:
        return [path if path.is_absolute() else root / path for path in explicit_paths]
    return sorted(root.glob(DEFAULT_CONTRACT_GLOB))


def run(root: Path, explicit_paths: list[Path]) -> int:
    paths = _contract_paths(root, explicit_paths)
    if not paths:
        print(f"FAIL no SQL schema probe contract files found under {DEFAULT_CONTRACT_GLOB}", file=sys.stderr)
        return 1

    failures: list[str] = []
    for path in paths:
        payload, load_failures = _load_contract(path)
        if load_failures:
            failures.extend(f"{_display(path, root)}: {failure}" for failure in load_failures)
            continue
        failures.extend(f"{_display(path, root)}: {failure}" for failure in validate_contract(payload))

    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print(f"PASS validated {len(paths)} SQL schema probe contract file(s)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate repo-local SQL schema drift probe contracts.")
    parser.add_argument("contracts", nargs="*", type=Path, help="Contract JSON files. Defaults to docs/examples/sql-schema-drift/*.json")
    parser.add_argument("--root", default=".", type=Path, help="Repository root")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return run(args.root.resolve(), args.contracts)


if __name__ == "__main__":
    raise SystemExit(main())
