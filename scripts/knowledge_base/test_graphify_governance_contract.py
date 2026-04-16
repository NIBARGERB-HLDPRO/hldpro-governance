#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = REPO_ROOT / "docs" / "graphify_targets.json"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "overlord-sweep.yml"
HOOK = REPO_ROOT / "hooks" / "closeout-hook.sh"
CLAUDE = REPO_ROOT / "CLAUDE.md"
INDEX = REPO_ROOT / "wiki" / "index.md"
BUILDER = REPO_ROOT / "scripts" / "knowledge_base" / "build_graph.py"

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        print(f"[PASS] {message}")
    else:
        print(f"[FAIL] {message}")
        failures.append(message)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    targets = manifest.get("targets", [])
    target_slugs = [target.get("repo_slug") for target in targets]

    check(MANIFEST.exists(), "graphify target manifest exists")
    check(manifest.get("root_graph_role") in {"compatibility_pointer", "aggregate"}, "manifest declares supported root graph role")
    check(len(targets) >= 6, "manifest includes all scheduled graph targets")
    check(len(set(target_slugs)) == len(target_slugs), "manifest repo slugs are unique")
    check("hldpro-governance" in target_slugs, "manifest includes governance repo target")
    check("ai-integration-services" in target_slugs, "manifest includes ai-integration-services target")
    check(all(str(target.get("output_path", "")).startswith("graphify-out/") for target in targets), "manifest output paths stay under graphify-out/")
    check(all(str(target.get("wiki_path", "")).startswith("wiki/") for target in targets), "manifest wiki paths stay under wiki/")

    workflow = WORKFLOW.read_text(encoding="utf-8")
    check("graphify_targets.py list --scheduled --format tsv" in workflow, "workflow uses manifest-defined scheduled target list")
    check("update_knowledge_index.py" in workflow, "workflow rebuilds knowledge index after graph refresh")
    check("--repo-slug" in workflow, "workflow passes repo slug into builder")
    check("graphify_targets.py stage-paths --scheduled" in workflow, "workflow stages manifest-defined artifact paths")

    hook = HOOK.read_text(encoding="utf-8")
    check('show --repo-slug hldpro-governance --format shell' in hook, "closeout hook resolves graph target from manifest")
    check("resolve_ai_root" not in hook, "closeout hook no longer hardcodes AIS root resolution")
    check("ai-integration-services" not in hook, "closeout hook no longer hardcodes AIS-only refresh path")

    claude = CLAUDE.read_text(encoding="utf-8")
    check("graphify-out/hldpro-governance/GRAPH_REPORT.md" in claude, "dispatcher reads governance-scoped graph report")
    check("Read `graphify-out/GRAPH_REPORT.md`" not in claude, "dispatcher no longer points to legacy root report")

    builder = BUILDER.read_text(encoding="utf-8")
    check('parser.add_argument("--repo-slug", required=True' in builder, "builder requires repo slug")
    check("_sanitize_markdown_artifacts" in builder, "builder sanitizes markdown artifact paths")
    check('"repo_slug": repo_slug' in builder, "builder writes repo slug into summary artifact")

    index = INDEX.read_text(encoding="utf-8")
    check("hldpro-governance:" in index and "../graphify-out/hldpro-governance/GRAPH_REPORT.md" in index, "knowledge index links governance-scoped report")
    check("ai-integration-services:" in index and "../graphify-out/ai-integration-services/GRAPH_REPORT.md" in index, "knowledge index links AIS scoped report")
    check("../graphify-out/healthcareplatform/GRAPH_REPORT.md" in index, "knowledge index links HealthcarePlatform scoped report")
    check("../graphify-out/local-ai-machine/GRAPH_REPORT.md" in index, "knowledge index links local-ai-machine scoped report")
    check("../graphify-out/knocktracker/GRAPH_REPORT.md" in index, "knowledge index links knocktracker scoped report")

    if failures:
        print(f"FAILED: {len(failures)} graphify governance contract checks failed")
        return 1

    print("[PASS] graphify governance contract checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
