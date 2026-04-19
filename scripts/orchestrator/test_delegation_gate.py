#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))

import delegation_gate  # noqa: E402


def test_rules_cover_all_da_delegation_task_types() -> None:
    _, rules = delegation_gate.load_rules()
    task_types = {rule.task_type for rule in rules}

    assert task_types == {
        "Migration validation",
        "Edge function review",
        "Schema consistency",
        "Test writing",
        "Diagram generation",
        "Documentation",
        "Repo health aggregation",
        "Cross-repo health",
    }


def test_high_confidence_agent_owned_work_blocks() -> None:
    result = delegation_gate.decide(
        tool_name="Agent",
        task_description="Audit SQL migrations for schema inconsistencies",
    )

    assert result.decision == "BLOCK"
    assert result.owner == "migration-validator"
    assert result.confidence >= 0.90


def test_high_confidence_bash_owned_work_blocks() -> None:
    result = delegation_gate.decide(
        tool_name="Bash",
        task_description="python scripts/audit_migrations.py --validate sql policy drift",
    )

    assert result.decision == "BLOCK"
    assert result.owner == "migration-validator"


def test_explore_is_warn_only_for_implementation_scoped_owned_work() -> None:
    result = delegation_gate.decide(
        tool_name="Explore",
        task_description="Audit SQL migrations for schema inconsistencies",
    )

    assert result.decision == "WARN"
    assert result.owner == "migration-validator"
    assert result.confidence >= 0.90


def test_explore_allows_non_implementation_routing_context() -> None:
    result = delegation_gate.decide(
        tool_name="Explore",
        task_description="Find files related to session startup context",
    )

    assert result.decision == "ALLOW"


def test_read_is_never_gated() -> None:
    result = delegation_gate.decide(
        tool_name="Read",
        task_description="Audit SQL migrations for schema inconsistencies",
    )

    assert result.decision == "ALLOW"
    assert result.owner == ""


def test_bypass_flag_allows_and_records_source() -> None:
    result = delegation_gate.decide(
        tool_name="Agent",
        task_description="Audit SQL migrations for schema inconsistencies --bypass-delegation-gate",
        bypass=True,
    )

    assert result.decision == "ALLOW"
    assert result.source == "bypass"


def test_classifier_fallback_warns_when_rules_are_inconclusive() -> None:
    result = delegation_gate.decide(
        tool_name="Agent",
        task_description="Review the data model lifecycle",
        classifier_payload={"owner": "schema-reviewer", "confidence": 0.82, "reason": "data model review"},
    )

    assert result.decision == "WARN"
    assert result.owner == "schema-reviewer"
    assert result.source == "classifier"
