from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "functional-acceptance-audit.schema.json"
AGENT_PATH = REPO_ROOT / "agents" / "functional-acceptance-auditor.md"
REGISTRY_PATH = REPO_ROOT / "AGENT_REGISTRY.md"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sample_pass_audit() -> dict:
    return {
        "audit_id": "2026-05-01-653-functional-audit",
        "issue_number": 653,
        "slice_branch": "issue-653-slice-h-functional-auditor-20260501",
        "audited_at": "2026-05-01T00:00:00Z",
        "acceptance_criteria": [
            {
                "id": "AC-H1",
                "statement": "Agent definition exists with required frontmatter.",
                "verification_method": "derived",
                "status": "PASS",
                "evidence": ["agents/functional-acceptance-auditor.md"]
            }
        ],
        "hook_results": [
            {
                "hook_name": "governance-check",
                "command": "/opt/homebrew/bin/python3.11 -m pytest tests/test_functional_acceptance_auditor.py",
                "exit_code": 0,
                "status": "PASS",
                "stdout_excerpt": "3 passed",
                "stderr_excerpt": ""
            }
        ],
        "smoke_test_results": [
            {
                "test_suite": "tests/test_functional_acceptance_auditor.py",
                "exit_code": 0,
                "status": "PASS",
                "passed_count": 3,
                "failed_count": 0,
                "coverage_percent": 100
            }
        ],
        "evidence_artifacts": [
            "agents/functional-acceptance-auditor.md",
            "docs/schemas/functional-acceptance-audit.schema.json",
            "tests/test_functional_acceptance_auditor.py"
        ],
        "overall_verdict": "PASS",
        "auditor_model": "claude-haiku-4-5",
        "auditor_signature": "functional-acceptance-auditor"
    }


def test_agent_frontmatter_and_registry_entry_exist() -> None:
    agent_text = AGENT_PATH.read_text(encoding="utf-8")
    assert "name: functional-acceptance-auditor" in agent_text
    assert "model: claude-haiku-4-5" in agent_text
    assert "fallback_model: claude-sonnet-4-6" in agent_text
    assert "authority_scope: slice-validation-read + acceptance-audit-write" in agent_text

    registry_text = REGISTRY_PATH.read_text(encoding="utf-8")
    assert "| functional-acceptance-auditor | hldpro-governance | 4 | auditor |" in registry_text
    assert "slice-validation-read + acceptance-audit-write" in registry_text


def test_schema_accepts_sample_pass_audit() -> None:
    schema = _load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(_sample_pass_audit()), key=lambda err: err.path)
    assert errors == []


def test_schema_rejects_missing_overall_verdict() -> None:
    schema = _load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)

    invalid_audit = _sample_pass_audit()
    invalid_audit.pop("overall_verdict")

    errors = list(validator.iter_errors(invalid_audit))
    assert errors
    assert any("overall_verdict" in error.message for error in errors)
