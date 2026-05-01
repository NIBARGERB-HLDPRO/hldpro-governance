import json
import subprocess
import sys
from pathlib import Path

from hldprosim.personas import PersonaLoader


PACKAGE_ROOT = Path(__file__).resolve().parent.parent
PROCESS_AGENTS_DIR = PACKAGE_ROOT / "process-agents"
SCHEMA_PATH = PROCESS_AGENTS_DIR / "governance-process-persona.schema.json"
PERSONA_IDS = [
    "functional-acceptance-auditor",
    "governance-planner",
    "implementation-worker",
    "plan-reviewer",
    "qa-reviewer",
]


def test_process_persona_files_present():
    present = sorted(path.stem for path in PROCESS_AGENTS_DIR.glob("*.json") if path.name != SCHEMA_PATH.name)
    assert present == PERSONA_IDS


def test_process_personas_validate_against_schema():
    for persona_id in PERSONA_IDS:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "jsonschema",
                "--instance",
                str(PROCESS_AGENTS_DIR / f"{persona_id}.json"),
                str(SCHEMA_PATH),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr or result.stdout


def test_persona_loader_prefers_process_agents_from_default_loader():
    persona = PersonaLoader().load("governance-planner")
    assert persona["persona_id"] == "governance-planner"


def test_persona_loader_falls_back_to_legacy_personas():
    persona = PersonaLoader().load("trader-momentum")
    assert persona["name"] == "Momentum Trader"


def test_qa_reviewer_declares_cross_family_constraint():
    persona = json.loads((PROCESS_AGENTS_DIR / "qa-reviewer.json").read_text())
    assert any("cross-family" in constraint for constraint in persona["constraints"])
