# Issue #225 Implementation Handoff

Date: 2026-04-17
Issue: [#225](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/225)
Parent epic: [#224](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/224)
Phase 0 dependency: [#223](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/223) closed by PR #233.
Branch: `issue-225-governed-repo-registry-20260417`
Worktree: `/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-225-registry-20260417`

## Worker Assignment

- Implementation worker: Codex / OpenAI.
- Reviewer/gate: existing #224 cross-review plus CI and local validators for this registry slice.

## Approved Scope

- Add `docs/governed_repos.json` as the executable governed repo registry.
- Add schema and validator for the registry.
- Add a shared Python adapter for registry consumers.
- Migrate production Python consumers that currently carry executable governed repo lists:
  - `scripts/overlord/build_effectiveness_metrics.py`
  - `scripts/overlord/memory_integrity.py`
  - `scripts/overlord/build_org_governance_compendium.py`
- Reconcile graphify target data against the registry.
- Derive weekly sweep runtime repo variables from the registry.
- Document temporary hardcoded-list exemptions.

## Out Of Scope

- Replacing static `actions/checkout` steps in `overlord-sweep.yml`.
- Replacing `docs/graphify_targets.json` as the graphify contract manifest.
- Implementing #226 planning/scope gatekeeper hardening.
- Implementing daemon, launchd, packet queue, or model runtime phases.

## Validation Commands

- `python3 scripts/overlord/validate_governed_repos.py`
- `python3 scripts/overlord/validate_governed_repos.py --print-subsystem sweep`
- `python3 scripts/overlord/validate_governed_repos.py --print-subsystem code_governance`
- `python3 scripts/overlord/validate_governed_repos.py --print-exempt`
- `python3 -m py_compile scripts/overlord/governed_repos.py scripts/overlord/validate_governed_repos.py scripts/overlord/build_effectiveness_metrics.py scripts/overlord/memory_integrity.py scripts/overlord/build_org_governance_compendium.py scripts/overlord/codex_ingestion.py`
- `python3 scripts/overlord/build_org_governance_compendium.py --check`
- `python3 scripts/knowledge_base/test_graphify_governance_contract.py`

## Closeout Expectations

- Add Stage 6 closeout before closing #225.
- Any remaining duplicate executable repo lists must be either migrated or listed in `docs/governed_repos_exemptions.md` with exit criteria.
