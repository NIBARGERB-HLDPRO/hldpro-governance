#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = REPO_ROOT / "docs" / "graphify_targets.json"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "overlord-sweep.yml"
HOOK = REPO_ROOT / "hooks" / "closeout-hook.sh"
CLAUDE = REPO_ROOT / "CLAUDE.md"
INDEX = REPO_ROOT / "wiki" / "index.md"
BUILDER = REPO_ROOT / "scripts" / "knowledge_base" / "build_graph.py"
CANONICAL_GRAPH_ARTIFACTS = (
    "GRAPH_REPORT.md",
    "graph.json",
    "community-labels.json",
    ".graphify_summary.json",
    ".graphify_detect.json",
    ".graphify_ast.json",
)
LOCAL_ONLY_IGNORED_PATHS = (
    "graphify-out/cache/sentinel.tmp",
    "graphify-out/.DS_Store",
    "graphify-out/.graphify_tmp.json",
    "graphify-out/graph.html",
)
LOCAL_ONLY_NESTED_IGNORED_ARTIFACTS = (
    "cache/sentinel.tmp",
    ".DS_Store",
)

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        print(f"[PASS] {message}")
    else:
        print(f"[FAIL] {message}")
        failures.append(message)


def is_ignored(path: str) -> tuple[bool, str]:
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "-v", path],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return True, result.stdout.strip()
    if result.returncode == 1:
        return False, ""

    message = f"git check-ignore failed for {path}: {result.stderr.strip() or result.stdout.strip()}"
    print(f"[FAIL] {message}")
    failures.append(message)
    return False, ""


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
    for target in targets:
        output_path = str(target.get("output_path", "")).strip()
        if not output_path:
            check(False, f"manifest target {target.get('repo_slug')} declares output_path")
            continue

        output_ignored, output_rule = is_ignored(output_path)
        check(
            not output_ignored,
            f"manifest output path is not ignored: {output_path}" if not output_ignored else f"manifest output path must be stageable: {output_path} (matched {output_rule})",
        )

        for artifact in CANONICAL_GRAPH_ARTIFACTS:
            artifact_path = f"{output_path}/{artifact}"
            artifact_ignored, artifact_rule = is_ignored(artifact_path)
            check(
                not artifact_ignored,
                f"canonical artifact is not ignored: {artifact_path}" if not artifact_ignored else f"canonical artifact must be stageable: {artifact_path} (matched {artifact_rule})",
            )

        for artifact in LOCAL_ONLY_NESTED_IGNORED_ARTIFACTS:
            artifact_path = f"{output_path}/{artifact}"
            artifact_ignored, artifact_rule = is_ignored(artifact_path)
            check(
                artifact_ignored,
                f"nested local-only path remains ignored: {artifact_path}" if artifact_ignored else f"nested local-only path must stay ignored: {artifact_path}",
            )
            check(
                bool(artifact_rule),
                f"nested local-only ignore rule is discoverable: {artifact_path}",
            )

    for local_only_path in LOCAL_ONLY_IGNORED_PATHS:
        local_only_ignored, local_only_rule = is_ignored(local_only_path)
        check(
            local_only_ignored,
            f"local-only path remains ignored: {local_only_path}" if local_only_ignored else f"local-only path must stay ignored: {local_only_path}",
        )
        check(
            bool(local_only_rule),
            f"local-only ignore rule is discoverable: {local_only_path}",
        )

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
