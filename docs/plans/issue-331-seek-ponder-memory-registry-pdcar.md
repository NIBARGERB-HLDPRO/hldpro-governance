# Issue 331 PDCAR: seek-and-ponder Memory Registry Follow-Up

Issue: NIBARGERB-HLDPRO/hldpro-governance#331  
Parent epic: NIBARGERB-HLDPRO/hldpro-governance#298  
Parent intake slice: NIBARGERB-HLDPRO/hldpro-governance#311  
Downstream follow-up: NIBARGERB-HLDPRO/seek-and-ponder#23  
Date: 2026-04-19

## Plan

Close the governance-side follow-up from `seek-and-ponder#23` by enabling or explicitly deferring governance memory-integrity participation in the canonical registry.

Expected implementation:

- Flip `seek-and-ponder.enabled_subsystems.memory_integrity` from `false` to `true` if the downstream memory bootstrap validates.
- Update the registry classification rationale and issue references to point at #331 and the closed downstream follow-up.
- Preserve existing graphify, sweep, metrics, raw-feed, Codex ingestion, compendium, and code-governance settings unless validation proves drift.
- Regenerate/check derived surfaces only when validators require it.
- Record final e2e evidence and Stage 6 closeout before closing #331.

Out of scope:

- Product repo edits.
- Memory file content changes outside the previously bootstrapped `seek-and-ponder` external memory directory.
- Workflow, script, or validator behavior changes unless validation proves a blocker.
- Broad org-ruleset or required-check policy changes.

## Do

1. Land planning/scope artifacts first.
2. In the implementation PR, edit only the scoped registry and generated/evidence surfaces.
3. Run the registry, memory, graphify, compendium, progress, backlog, and closeout gates.
4. Merge only after GitHub checks pass.
5. Close #331 with exact validation evidence.

## Check

Acceptance criteria:

- PDCAR and structured plan cite #331, #298, #311, and `seek-and-ponder#23`.
- `seek-and-ponder` has an explicit memory-integrity disposition in `docs/governed_repos.json`.
- Registry validation and graphify target reconciliation pass.
- `scripts/overlord/memory_integrity.py` includes `seek-and-ponder` and passes, or a linked deferral explains why not.
- Progress/backlog mirrors update from the isolated worktree only.
- Stage 6 closeout artifact exists and `hooks/closeout-hook.sh` passes.

Final e2e gate:

- `python3 scripts/overlord/validate_governed_repos.py`
- `python3 scripts/overlord/validate_registry_surfaces.py`
- `python3 scripts/overlord/memory_integrity.py`
- `python3 scripts/overlord/check_org_repo_inventory.py --live --format text`
- `python3 scripts/knowledge_base/graphify_targets.py show --repo-slug seek-and-ponder --format json`
- `python3 scripts/knowledge_base/test_graphify_governance_contract.py`
- `python3 scripts/overlord/build_org_governance_compendium.py --check`
- `python3 scripts/overlord/check_progress_github_issue_staleness.py --repo NIBARGERB-HLDPRO/hldpro-governance`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `bash hooks/closeout-hook.sh raw/closeouts/2026-04-19-issue-331-seek-ponder-memory-registry.md`

## Act

If memory integrity fails because the external `seek-and-ponder` memory directory is missing or malformed, do not hide the failure by leaving the registry false. Either repair the bootstrap under the existing downstream issue evidence path or create a new downstream follow-up before closing #331.

If derived compendium or graph/wiki surfaces drift after the registry flip, regenerate them in the implementation PR and include the generated output in the execution scope.

## Reflect

`seek-and-ponder#23` completed downstream repo readiness. This governance issue finishes the upstream registry loop so weekly memory integrity and registry-driven consumers no longer silently exclude an active governed repo.
