# Issue #313 - Registry-Driven Surface Reconciliation PDCA/R

Branch: `issue-313-registry-surface-reconciliation-20260419`
Issue: [#313](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/313)
Parent epic: [#298](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/298)

## Plan

After #311 and #312, active org repos are represented in `docs/governed_repos.json`. #313 closes remaining static governance surfaces so future repo additions are either generated from the registry/graphify manifest or validator-backed.

## Do

- Add missing `seek-and-ponder` explicit checkout steps where GitHub Actions requires static `actions/checkout` blocks.
- Derive raw-feed repo selection from `raw_feed_sync` subsystem flags.
- Derive local graphify helper symlink targets from scheduled graphify targets.
- Update README and STANDARDS repo registry surfaces.
- Add `scripts/overlord/validate_registry_surfaces.py` and wire it into CI/local gates.

## Check

Final acceptance requires:

- `python3 scripts/overlord/validate_governed_repos.py`
- `python3 scripts/knowledge_base/test_graphify_governance_contract.py`
- `python3 scripts/overlord/validate_registry_surfaces.py`
- structured plan validation
- execution-scope validation
- backlog/GitHub sync validation
- workflow/local contract tests
- `bash -n` for touched shell
- `python3 -m py_compile` for touched Python
- `git diff --check`
- Local CI Gate against the changed-file list
- specialist review acceptance

## Act

If validation and review pass, publish #313 as a focused PR and keep #298 open for #314 final e2e closeout.
