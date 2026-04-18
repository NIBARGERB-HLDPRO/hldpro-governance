#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "hitl-relay-packet.schema.json"
EXAMPLE_ROOT = REPO_ROOT / "docs" / "schemas" / "examples" / "hitl-relay"


def _validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_valid_hitl_relay_examples_pass() -> None:
    validator = _validator()
    valid_files = sorted((EXAMPLE_ROOT / "valid").glob("*.json"))
    assert valid_files, "expected valid HITL relay examples"
    for example in valid_files:
        errors = sorted(validator.iter_errors(_load(example)), key=lambda error: error.path)
        assert not errors, f"{example} failed schema validation: {[error.message for error in errors]}"


def test_invalid_hitl_relay_examples_fail() -> None:
    validator = _validator()
    invalid_files = sorted((EXAMPLE_ROOT / "invalid").glob("*.json"))
    assert invalid_files, "expected invalid HITL relay examples"
    for example in invalid_files:
        errors = sorted(validator.iter_errors(_load(example)), key=lambda error: error.path)
        assert errors, f"{example} unexpectedly passed schema validation"
