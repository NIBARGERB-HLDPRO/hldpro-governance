# Issue #310 - Governed Repo Classification Schema PDCA/R

Branch: `issue-310-classification-schema-20260418`
Issue: [#310](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/310)
Parent epic: [#298](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/298)

## Plan

#298 made org repository coverage explicit: an active org repository must be represented in governance, and exemptions must be classifications rather than omissions. #309 made drift visible. #310 adds the registry contract that lets later slices distinguish governed, limited, exempt, adoption-blocked, and archived states without reading prose.

This slice updates only the existing registry entries and their validation surface. It does not add `seek-and-ponder` or `EmailAssistant`; those remain #311 and #312.

## Do

- Require `lifecycle_status` on every governed repository row.
- Require `governance_status` on every governed repository row.
- Require `classification.owner`, `classification.rationale`, `classification.review_date`, and `classification.issue_refs`.
- Extend the Python registry loader and validator to enforce the contract.
- Add focused validator tests for valid and invalid classification shapes.
- Keep #309 inventory drift fixtures compatible with the new registry contract.
- Update archived inventory handling so `lifecycle_status: archived` is a real classification rather than a permanent drift blocker.
- Keep live org inventory drift visible in warn-only mode so #311/#312 remain necessary.

## Check

Final acceptance requires:

- `python3 scripts/overlord/test_validate_governed_repos.py`
- `python3 scripts/overlord/test_check_org_repo_inventory.py`
- `python3 scripts/overlord/validate_governed_repos.py`
- `python3 scripts/overlord/check_org_repo_inventory.py --live --warn-only --format markdown`
- structured agent cycle plan validation,
- execution-scope validation,
- backlog/GitHub sync validation,
- Local CI Gate against the changed-file list,
- `python3 -m py_compile` for touched Python files,
- `git diff --check`,
- alternate-family review acceptance with follow-up fixes applied.

## Act

If validation passes and review accepts the contract, publish #310 as a focused PR and keep #298 open. If the live inventory output stops reporting `seek-and-ponder` and `EmailAssistant`, verify #311/#312 already landed before updating the evidence; otherwise do not claim final org-wide closeout.

## Retrospective

To be completed during PR closeout. The expected residual work is #311/#312 registry intake, #313 surface reconciliation, and #314 final e2e closeout.
