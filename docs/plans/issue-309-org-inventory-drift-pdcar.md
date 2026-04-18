# Issue #309 - Org Inventory Drift Detector PDCA/R

## Plan

Parent epic #298 requires every active org repository to be represented in
governance. Current live inventory includes active repos that are not in
`docs/governed_repos.json`, so governance needs a deterministic detector before
intake work starts.

This slice adds only detection and report surfacing:

- fixture mode for local/CI tests,
- live GitHub CLI mode for weekly sweep and operator checks,
- blocking exit codes for direct enforcement,
- warn-only mode for sweep reporting while known gaps remain open,
- focused tests for exact match, missing active repo, stale registry repo, and
  archived repo behavior.

## Do

- Add `scripts/overlord/check_org_repo_inventory.py`.
- Add `scripts/overlord/test_check_org_repo_inventory.py`.
- Add an org inventory drift section to `overlord-sweep.yml`.
- Keep `docs/governed_repos.json` unchanged in this slice.
- Keep registry classification schema changes in #310.
- Keep `seek-and-ponder` and `EmailAssistant` intake in #311/#312.

## Check

Required validation:

- `python3 scripts/overlord/test_check_org_repo_inventory.py`
- `python3 scripts/overlord/check_org_repo_inventory.py --inventory-file <fixture> --registry <fixture-registry>`
- `python3 scripts/overlord/check_org_repo_inventory.py --live --warn-only --format markdown`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .`
- `python3 scripts/overlord/validate_governed_repos.py`
- `tools/local-ci-gate/bin/hldpro-local-ci --profile tools/local-ci-gate/profiles/hldpro-governance.yml --changed-files-file <changed-files>`

Final acceptance requires live mode to report `seek-and-ponder` and
`EmailAssistant` as missing active repos while the registry is unchanged.

## Adjust

If GitHub CLI cannot load live org inventory, keep fixture-backed validation and
record the live-mode blocker on #309.

If archived/exempt classification semantics are needed to avoid false positives,
stop and route those schema changes to #310.

If sweep report formatting is too noisy, keep the machine-readable command output
stable and adjust only the markdown renderer.

## Review

Review should focus on:

- deterministic fixture behavior,
- truthful current drift reporting,
- no registry intake mixed into this slice,
- sweep warn-only behavior,
- clear handoff to #310-#312,
- final #298 e2e compatibility.
