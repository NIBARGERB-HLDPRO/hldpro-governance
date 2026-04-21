#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import validate_session_error_patterns


VALID_ENTRY = """## Pattern: hook-command-classification-false-positive

| Field | Value |
|---|---|
| Signature | schema-guard blocked a quoted awk comparison. |
| Category | hook classifier |
| Root Cause | Regex matched quoted comparison operators. |
| Correction | Use the shared command classifier. |
| Guardrail | schema-guard consumes check_plan_preflight.py. |
| Validation | python3 scripts/overlord/test_check_plan_preflight.py |
| Related Files | hooks/schema-guard.sh |
| First Observed | 2026-04-21 |
| Prevented By | Issue #538 |
"""


def _write_runbook(root: Path, body: str) -> Path:
    path = root / "docs" / "runbooks" / "session-error-patterns.md"
    path.parent.mkdir(parents=True)
    path.write_text(body, encoding="utf-8")
    return path


class TestValidateSessionErrorPatterns(unittest.TestCase):
    def test_validates_current_repo_runbook(self) -> None:
        failures = validate_session_error_patterns.validate(Path("docs/runbooks/session-error-patterns.md"))

        self.assertEqual(failures, [])

    def test_rejects_missing_required_field(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = _write_runbook(
                root,
                VALID_ENTRY.replace("| Guardrail | schema-guard consumes check_plan_preflight.py. |\n", ""),
            )

            failures = validate_session_error_patterns.validate(path)

            self.assertTrue(any("missing field(s): guardrail" in failure for failure in failures))

    def test_rejects_missing_seed_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = _write_runbook(root, VALID_ENTRY)

            failures = validate_session_error_patterns.validate(path)

            self.assertTrue(any("missing required seed pattern" in failure for failure in failures))

    def test_rejects_invalid_date(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = _write_runbook(root, VALID_ENTRY.replace("2026-04-21", "04/21/2026"))

            failures = validate_session_error_patterns.validate(path)

            self.assertTrue(any("first_observed must be YYYY-MM-DD" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main(verbosity=2)
