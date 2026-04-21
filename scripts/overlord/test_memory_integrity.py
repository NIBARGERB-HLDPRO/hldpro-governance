#!/usr/bin/env python3
"""Tests for governed Claude MEMORY.md integrity checks."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.overlord import memory_integrity


class MemoryIntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.memory_root = Path(self.tmpdir.name)

    def write_memory(self, repo_slug: str, memory_text: str, entries: dict[str, str]) -> None:
        memory_dir = self.memory_root / f"-Users-bennibarger-Developer-HLDPRO-{repo_slug}" / "memory"
        memory_dir.mkdir(parents=True)
        (memory_dir / "MEMORY.md").write_text(memory_text, encoding="utf-8")
        for name, text in entries.items():
            (memory_dir / name).write_text(text, encoding="utf-8")

    def test_strict_missing_memory_fails(self) -> None:
        result = memory_integrity.inspect_repo("sample", memory_root=self.memory_root)

        self.assertFalse(result.passed)
        self.assertFalse(result.skipped)
        self.assertIn("MEMORY.md missing", result.issues[0])

    def test_allow_missing_memory_skips_without_failing(self) -> None:
        result = memory_integrity.inspect_repo("sample", memory_root=self.memory_root, allow_missing=True)

        self.assertTrue(result.passed)
        self.assertTrue(result.skipped)
        self.assertIn("skipped in allow-missing mode", result.issues[0])

    def test_valid_memory_pointer_passes(self) -> None:
        self.write_memory(
            "sample",
            "- [Canonical entry](entry.md) - loaded by memory\n",
            {
                "entry.md": "\n".join(
                    [
                        "---",
                        "name: Canonical entry",
                        "description: Fixture memory entry",
                        "type: pattern",
                        "---",
                        "Body",
                    ]
                ),
            },
        )

        result = memory_integrity.inspect_repo("sample", memory_root=self.memory_root)

        self.assertTrue(result.passed)
        self.assertEqual(result.entries, 1)
        self.assertEqual(result.issues, [])

    def test_existing_malformed_memory_still_fails_in_allow_missing_mode(self) -> None:
        self.write_memory("sample", "- [Broken](entry.md) - loaded by memory\n", {"entry.md": "no frontmatter"})

        result = memory_integrity.inspect_repo("sample", memory_root=self.memory_root, allow_missing=True)

        self.assertFalse(result.passed)
        self.assertFalse(result.skipped)
        self.assertIn("missing YAML frontmatter", result.issues[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
