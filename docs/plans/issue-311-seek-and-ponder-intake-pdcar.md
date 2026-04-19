# Issue #311 - seek-and-ponder Governance Intake PDCA/R

Branch: `issue-311-seek-and-ponder-intake-20260419`
Issue: [#311](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/311)
Parent epic: [#298](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/298)

## Plan

#298 requires every active org repo to be represented in governance. `seek-and-ponder` is active, private, and currently missing from the governed repo registry. #311 intakes it into governance without editing the downstream repository.

## Do

- Add `seek-and-ponder` to `docs/governed_repos.json`.
- Add `seek-and-ponder` to `docs/graphify_targets.json`.
- Produce governance-hosted graph/wiki artifacts from the local checkout.
- Validate front-door docs, workflow presence, CODEOWNERS, default branch, branch protection, org rulesets, and recent check history.
- Open downstream issue `NIBARGERB-HLDPRO/seek-and-ponder#23` for repo-local required-check and memory bootstrap follow-up.

## Check

Final acceptance requires:

- `python3 scripts/overlord/validate_governed_repos.py`
- `python3 scripts/overlord/check_org_repo_inventory.py --live --format text`
- `python3 scripts/knowledge_base/graphify_targets.py show --repo-slug seek-and-ponder`
- graph/wiki artifact existence checks,
- structured agent cycle plan validation,
- execution-scope validation,
- backlog/GitHub sync validation,
- Local CI Gate against the changed-file list,
- `python3 -m py_compile` for touched Python validators/helpers,
- `git diff --check`,
- alternate-family review acceptance.

## Act

If validation passes and review accepts the intake, publish #311 as a focused PR and keep #298 open. If live org inventory still reports `seek-and-ponder` as missing after registry intake, do not publish. `EmailAssistant` should remain the only missing active repo until #312 lands.

## Retrospective

To be completed during PR closeout. Expected residual work is #312 EmailAssistant classification, #313 surface reconciliation, #314 final e2e closeout, and downstream seek-and-ponder#23.
