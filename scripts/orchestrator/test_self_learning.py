#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))

import self_learning


def _write_fixture(root: Path) -> None:
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "FAIL_FAST_LOG.md").write_text(
        """# Fail Fast

| Error | Root Cause | Resolution | Date |
|-------|------------|------------|------|
| Graph compendium stale after closeout | Compendium was not regenerated after graph/wiki refresh | Run build_org_governance_compendium.py after closeout hook | 2026-04-17 |
| Graph compendium stale after closeout | Compendium was not regenerated after graph/wiki refresh | Run build_org_governance_compendium.py after closeout hook | 2026-04-17 |
""",
        encoding="utf-8",
    )
    (root / "docs" / "ERROR_PATTERNS.md").write_text(
        """# ERROR_PATTERNS

## Pattern: graph-compendium-stale

Symptom: compendium check fails after graph refresh.
Root Cause: generated docs changed after the freshness check.
Resolution Playbook: rerun compendium build and check.
""",
        encoding="utf-8",
    )
    (root / "docs" / "ORG_GOVERNANCE_COMPENDIUM.md").write_text("graph compendium closeout\n", encoding="utf-8")
    (root / "raw" / "closeouts").mkdir(parents=True)
    (root / "raw" / "closeouts" / "2026-04-17-test.md").write_text(
        """# Stage 6 Closeout

## Decision Made
Compendium refresh follows graph update.

## Pattern Identified
Run generated artifact checks after hooks.

## Residual Risks / Follow-Up
None.
""",
        encoding="utf-8",
    )
    (root / "raw" / "operator-context").mkdir(parents=True)
    (root / "raw" / "operator-context" / "2026-04-17-test.md").write_text(
        "# Operator Context\n\nRemember graph compendium refresh ordering.\n",
        encoding="utf-8",
    )
    (root / "graphify-out" / "hldpro-governance").mkdir(parents=True)
    (root / "graphify-out" / "hldpro-governance" / "GRAPH_REPORT.md").write_text(
        "graph compendium routing attention only\n",
        encoding="utf-8",
    )


class TestSelfLearning(unittest.TestCase):
    def test_lookup_returns_cited_prior_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write_fixture(root)

            matches = self_learning.lookup_patterns("graph compendium stale closeout", root=root, limit=3)

            self.assertTrue(matches)
            self.assertEqual(matches[0].source_path, "docs/FAIL_FAST_LOG.md")
            self.assertIn("docs/FAIL_FAST_LOG.md", matches[0].evidence_paths)
            self.assertGreaterEqual(matches[0].repeat_count, 2)

    def test_enrich_packet_injects_known_failure_context(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write_fixture(root)
            packet = {
                "packet_id": "aaaaaaaa-0000-4000-a000-000000000230",
                "artifacts": ["graph compendium stale closeout"],
                "governance": {},
            }

            enriched = self_learning.enrich_packet(packet, root=root)

            context = enriched["governance"]["known_failure_context"]
            self.assertTrue(context)
            self.assertIn("source_path", context[0])
            self.assertIn("evidence_paths", context[0])
            self.assertNotIn("score", context[0])

    def test_record_failure_is_append_only_and_issue_backed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            first = self_learning.record_failure(
                root=root,
                issue_number=230,
                title="Novel graph stale failure",
                summary="A new generated artifact stale path was found.",
                evidence_path="raw/closeouts/example.md",
                follow_up="#230",
            )
            second = self_learning.record_failure(
                root=root,
                issue_number=230,
                title="Novel graph stale failure",
                summary="A new generated artifact stale path was found.",
                evidence_path="raw/closeouts/example.md",
                follow_up="#230",
            )

            self.assertTrue(first.exists())
            self.assertTrue(second.exists())
            self.assertNotEqual(first, second)
            self.assertIn("Issue: #230", first.read_text(encoding="utf-8"))

    def test_record_failure_rejects_out_of_range_issue_numbers(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with self.assertRaises(ValueError):
                self_learning.record_failure(
                    root=root,
                    issue_number=0,
                    title="Invalid issue",
                    summary="invalid",
                    evidence_path="raw/closeouts/example.md",
                    follow_up="#0",
                )
            with self.assertRaises(ValueError):
                self_learning.record_failure(
                    root=root,
                    issue_number=1000000,
                    title="Invalid issue",
                    summary="invalid",
                    evidence_path="raw/closeouts/example.md",
                    follow_up="#1000000",
                )

    def test_report_flags_duplicates_and_graphify_attention_only(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write_fixture(root)

            report = self_learning.build_report(root)

            self.assertTrue(report["graphify_attention_only"])
            self.assertGreaterEqual(len(report["duplicate_groups"]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
