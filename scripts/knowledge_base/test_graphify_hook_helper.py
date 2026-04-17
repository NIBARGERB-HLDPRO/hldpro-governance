#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import graphify_hook_helper as helper


class TestGraphifyHookHelper(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.gov = self.root / "hldpro-governance"
        self.gov.mkdir()
        self.manifest = self.gov / "graphify_targets.json"
        self.product = self.root / "ai-integration-services"
        self.product.mkdir()
        subprocess.run(["git", "init"], cwd=self.product, check=True, capture_output=True, text=True)
        self.write_manifest(
            {
                "version": 1,
                "targets": [
                    {
                        "repo_slug": "ai-integration-services",
                        "display_name": "ai-integration-services",
                        "source_path": "repos/ai-integration-services",
                        "output_path": "graphify-out/ai-integration-services",
                        "wiki_path": "wiki/ai-integration-services",
                    },
                    {
                        "repo_slug": "knocktracker",
                        "display_name": "knocktracker",
                        "source_path": "repos/knocktracker",
                        "output_path": "graphify-out/knocktracker",
                        "wiki_path": "wiki/knocktracker",
                    },
                ],
            }
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_manifest(self, payload: dict[str, object]) -> None:
        self.manifest.write_text(json.dumps(payload), encoding="utf-8")

    def args(self, **overrides: object) -> object:
        values = {
            "governance_root": str(self.gov),
            "manifest": str(self.manifest),
            "target_repo": str(self.product),
            "repo_slug": None,
        }
        values.update(overrides)
        return type("Args", (), values)()

    def test_infers_repo_slug_and_resolves_manifest_paths_from_governance_root(self) -> None:
        plan = helper.build_plan(self.args())

        self.assertEqual(plan.repo_slug, "ai-integration-services")
        self.assertEqual(plan.governance_root, self.gov.resolve())
        self.assertEqual(plan.source_path, (self.gov / "repos/ai-integration-services").resolve())
        self.assertEqual(plan.output_path, (self.gov / "graphify-out/ai-integration-services").resolve())
        self.assertEqual(plan.wiki_path, (self.gov / "wiki/ai-integration-services").resolve())
        self.assertIn("post-commit", plan.hook_paths)
        self.assertIn("post-checkout", plan.hook_paths)

    def test_accepts_explicit_knocktracker_slug(self) -> None:
        knocktracker = self.root / "knocktracker"
        knocktracker.mkdir()
        subprocess.run(["git", "init"], cwd=knocktracker, check=True, capture_output=True, text=True)

        plan = helper.build_plan(self.args(target_repo=str(knocktracker), repo_slug="knocktracker"))

        self.assertEqual(plan.repo_slug, "knocktracker")
        self.assertEqual(plan.output_path, (self.gov / "graphify-out/knocktracker").resolve())

    def test_unsafe_product_repo_output_aborts_before_builder_call(self) -> None:
        plan = helper.HookPlan(
            repo_slug="ai-integration-services",
            target_repo=self.product.resolve(),
            governance_root=self.gov.resolve(),
            source_path=(self.gov / "repos/ai-integration-services").resolve(),
            output_path=(self.product / "graphify-out/ai-integration-services").resolve(),
            wiki_path=(self.gov / "wiki/ai-integration-services").resolve(),
            hook_paths={},
        )

        with mock.patch.object(helper.subprocess, "run") as run:
            with self.assertRaises(helper.HelperError):
                helper.execute_refresh(plan, no_html=True)
            run.assert_not_called()

    def test_install_refuses_unmanaged_existing_hooks(self) -> None:
        plan = helper.build_plan(self.args(repo_slug="ai-integration-services"))
        hook = plan.hook_paths["post-commit"]
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text("#!/usr/bin/env bash\necho unmanaged\n", encoding="utf-8")

        with self.assertRaises(helper.HelperError):
            helper.install_hooks(plan, backup_existing=False, force=False)

        self.assertEqual(hook.read_text(encoding="utf-8"), "#!/usr/bin/env bash\necho unmanaged\n")

    def test_install_backs_up_unmanaged_hook_and_writes_managed_body(self) -> None:
        plan = helper.build_plan(self.args(repo_slug="ai-integration-services"))
        hook = plan.hook_paths["post-commit"]
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text("#!/usr/bin/env bash\necho unmanaged\n", encoding="utf-8")

        helper.install_hooks(plan, backup_existing=True, force=False)

        body = hook.read_text(encoding="utf-8")
        self.assertIn(helper.MANAGED_MARKER, body)
        self.assertIn("graphify_hook_helper.py\" refresh", body)
        self.assertNotIn("graphify.watch._rebuild_code", body)
        self.assertNotIn("graphify hook install", body)
        backup = hook.with_name("post-commit.pre-governance-graphify")
        self.assertTrue(backup.exists())

    def test_dry_run_payload_includes_command_and_hook_targets(self) -> None:
        plan = helper.build_plan(self.args(repo_slug="ai-integration-services"))
        helper.preflight_safe_output(plan)
        payload = plan.to_json()
        payload["refresh_command"] = helper.build_refresh_command(plan, no_html=True)

        self.assertEqual(payload["repo_slug"], "ai-integration-services")
        self.assertIn("hook_paths", payload)
        self.assertIn("--output", payload["refresh_command"])
        self.assertIn("--no-html", payload["refresh_command"])
        self.assertEqual(
            payload["refresh_command"][1],
            str((self.gov / "scripts" / "knowledge_base" / "build_graph.py").resolve()),
        )


if __name__ == "__main__":
    unittest.main()
