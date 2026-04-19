# Issue 176 PDCAR: ASC-Evaluator Exemption Reconciliation

Issue: NIBARGERB-HLDPRO/hldpro-governance#176  
Repo reconciled: NIBARGERB-HLDPRO/ASC-Evaluator  
Date: 2026-04-19

## Plan

Resolve the documented conflict between ASC-Evaluator's knowledge-repo exemption and its existing `.github/workflows/governance.yml`.

Expected disposition:

- Inspect the live ASC-Evaluator workflow and latest default-branch runs.
- If the workflow is compatible with the exemption, close the stale `SOM-ASC-CI-001` blocking exception in governance.
- Preserve `SOM-EXEMPT-ASC-001` as an active knowledge-repo code-governance exemption, but clarify that a minimal docs-only governance gate may remain wired.
- Record validation evidence and Stage 6 closeout before closing #176.

Out of scope:

- Downstream ASC-Evaluator code or workflow edits unless live evidence proves the workflow is still failing.
- Changing ASC-Evaluator's limited registry classification.
- Broad ruleset, branch protection, or org policy changes.

## Do

1. Verify ASC-Evaluator default branch and workflow definition.
2. Verify latest ASC-Evaluator Governance Gate status on `master`.
3. Update governance exception records and progress/backlog mirrors.
4. Run governance local validation and Stage 6 closeout.
5. Merge only after GitHub checks pass, then close #176 with exact evidence.

## Check

Acceptance criteria:

- ASC-Evaluator `.github/workflows/governance.yml` is inspected and cited.
- Either the workflow is updated or the exception register explains why no downstream edit is needed.
- `SOM-ASC-CI-001` no longer remains an active blocker if the current workflow is green.
- `SOM-EXEMPT-ASC-001` remains bounded to code-governance exemption only.

Final e2e gate:

- ASC-Evaluator latest default-branch Governance Gate is `success`.
- `python3 -m json.tool docs/plans/issue-176-structured-agent-cycle-plan.json`
- `python3 -m json.tool raw/execution-scopes/2026-04-19-issue-176-asc-exemption-reconcile-implementation.json`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 scripts/overlord/check_progress_github_issue_staleness.py --repo NIBARGERB-HLDPRO/hldpro-governance`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`
- `hooks/closeout-hook.sh raw/closeouts/2026-04-19-issue-176-asc-exemption-reconcile.md`

## Act

If ASC-Evaluator Governance Gate fails during final verification, stop and either open a downstream ASC-Evaluator PR to update `governance.yml` or leave `SOM-ASC-CI-001` active with fresh failure evidence and a new follow-up.

If governance validation requires additional co-staged artifacts, absorb them into this issue only when they are evidence or generated closeout surfaces for #176.

## Reflect

The conflict was stale documentation, not an active workflow defect. ASC-Evaluator now carries minimal governance docs and its existing reusable governance workflow passes, while the repo remains exempt from code-governance requirements due to its knowledge-repo classification.
