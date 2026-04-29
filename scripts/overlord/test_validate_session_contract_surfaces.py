#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.overlord.validate_session_contract_surfaces import validate


def _write(root: Path, relative_path: str, content: str) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _settings(pre_session_command: str, post_tool_command: str) -> str:
    return json.dumps(
        {
            "hooks": {
                "UserPromptSubmit": [
                    {
                        "hooks": [
                            {
                                "type": "command",
                                "command": pre_session_command,
                            }
                        ]
                    }
                ],
                "PostToolUse": [
                    {
                        "matcher": "*",
                        "hooks": [
                            {
                                "type": "command",
                                "command": post_tool_command,
                            }
                        ],
                    }
                ],
            }
        }
    )


class ValidateSessionContractSurfacesTests(unittest.TestCase):
    def _write_required_files(self, root: Path) -> None:
        _write(root, "CODEX.md", "contract\n")
        _write(
            root,
            "docs/EXTERNAL_SERVICES_RUNBOOK.md",
            "Session-start contract note: governance sessions must surface this runbook via\npython3 scripts/session_bootstrap_contract.py --emit-hook-note before implementation-ready work.\n\nbash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh <repo>\n",
        )
        _write(
            root,
            "scripts/session_bootstrap_contract.py",
            'parser.add_argument("--emit-hook-note")\nREQUIRED_DOCS=[\"docs/EXTERNAL_SERVICES_RUNBOOK.md\",\"docs/FAIL_FAST_LOG.md\"]\n',
        )
        _write(
            root,
            "hooks/pre-session-context.sh",
            '#!/bin/bash\npython3 "$REPO_ROOT/scripts/session_bootstrap_contract.py" --emit-hook-note\n',
        )
        _write(
            root,
            ".claude/hooks/pre-session-context.sh",
            '#!/bin/bash\npython3 "$REPO_ROOT/scripts/session_bootstrap_contract.py" --emit-hook-note\n',
        )

    def test_valid_surfaces_pass(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._write_required_files(root)
            _write(
                root,
                ".claude/settings.json",
                _settings(
                    "bash /tmp/repo/hooks/pre-session-context.sh",
                    "bash /tmp/repo/hooks/check-errors.sh",
                ),
            )
            self.assertEqual(validate(root), [])

    def test_missing_wrapper_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._write_required_files(root)
            (root / ".claude/hooks/pre-session-context.sh").unlink()
            _write(
                root,
                ".claude/settings.json",
                _settings(
                    "bash /tmp/repo/hooks/pre-session-context.sh",
                    "bash /tmp/repo/hooks/check-errors.sh",
                ),
            )
            failures = validate(root)
        self.assertTrue(any(".claude/hooks/pre-session-context.sh" in failure for failure in failures))

    def test_missing_user_prompt_submit_command_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._write_required_files(root)
            _write(
                root,
                ".claude/settings.json",
                _settings(
                    "bash /tmp/repo/hooks/something-else.sh",
                    "bash /tmp/repo/hooks/check-errors.sh",
                ),
            )
            failures = validate(root)
        self.assertTrue(any("UserPromptSubmit" in failure for failure in failures))

    def test_missing_runbook_contract_note_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._write_required_files(root)
            _write(root, "docs/EXTERNAL_SERVICES_RUNBOOK.md", "bootstrap only\n")
            _write(
                root,
                ".claude/settings.json",
                _settings(
                    "bash /tmp/repo/hooks/pre-session-context.sh",
                    "bash /tmp/repo/hooks/check-errors.sh",
                ),
            )
            failures = validate(root)
        self.assertTrue(any("canonical session bootstrap hook note path" in failure for failure in failures))

    def test_missing_helper_contract_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._write_required_files(root)
            _write(root, "scripts/session_bootstrap_contract.py", "print('noop')\n")
            _write(
                root,
                ".claude/settings.json",
                _settings(
                    "bash /tmp/repo/hooks/pre-session-context.sh",
                    "bash /tmp/repo/hooks/check-errors.sh",
                ),
            )
            failures = validate(root)
        self.assertTrue(any("scripts/session_bootstrap_contract.py must include" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main(verbosity=2)
