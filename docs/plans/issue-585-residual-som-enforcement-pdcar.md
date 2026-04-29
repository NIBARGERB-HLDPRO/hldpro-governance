# Issue #585 PDCAR: Residual SoM Enforcement Gaps

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/585
Branch: `issue-585-residual-som-enforcement`

## Plan

Close the residual governance-source enforcement gaps left after issue `#583`
so the source repo fully hard-gates the waterfall before downstream
product-repo rollout resumes.

The post-merge audit confirmed `#583` fixed the originally reproduced bad
Stampede packet and stale consumer-record shapes, but it also surfaced four
remaining gaps:

- `feat/issue-<n>-...` branches can still bypass mandatory packet creation if
  no structured plan file exists
- `alternate_model_review` is not yet machine-checked as genuinely
  alternate-family or alternate-identity
- `handoff_package_ref` and `review_artifact_refs` are checked only for shape,
  not for on-disk existence
- session/runbook enforcement still validates mostly presence and string hints,
  and runbook-only changes can bypass the session-contract local CI gate

## Do

Implementation scope for issue `#585`:

- make issue-lane packet enforcement key off any `issue-<n>` token, not only
  branch prefixes like `issue-` or `riskfix/`, by driving the gate from
  `_branch_issue_number()`
- require machine-checkable alternate-review identity metadata and reject
  same-family or same-identity alternate review claims using
  `reviewer_model_id` and `reviewer_model_family`
- require existence of referenced handoff/review artifacts when evidence gates
  apply
- strengthen `validate_session_contract_surfaces.py` so it proves the canonical
  session-start/runbook contract rather than only file presence
- include `docs/EXTERNAL_SERVICES_RUNBOOK.md` in the local session-contract
  gate scope so runbook-only changes cannot bypass local CI enforcement
- add regression tests for all of the above

## Check

Before implementation:

- the issue-backed planning packet validates locally
- acceptance criteria are phrased as blocking gates rather than advisory
  reminders
- specialist review confirms the bounded fix set is sufficient
- alternate-family review is recorded through the governed
  `scripts/codex-review.sh claude` path before implementation-ready promotion
- clean validation proof is appended before implementation-ready promotion

After implementation:

- `feat/issue-<n>-...` branches with no structured plan fail the mandatory-plan
  gate
- same-family or same-identity alternate review claims fail deterministically
- nonexistent `handoff_package_ref` and nonexistent `review_artifact_refs`
  fail deterministically when the evidence gate applies
- runbook-only changes trigger the session-contract local gate
- `validate_session_contract_surfaces.py` proves the canonical bootstrap note
  and fail-fast hook contract more concretely than file presence alone
- regression tests cover each failure shape

## Adjust

If alternate-review identity needs schema expansion, add the minimum fields
needed and thread them through standards, runbook, validator, and tests in one
slice. Do not add a warning-only path.

If the session-contract validator cannot yet prove every semantic requirement,
raise the floor materially in this issue and record any leftover non-blocking
source gap as a new issue before downstream rollout continues.

## Review

Do not resume downstream issue `#579` child rollout lanes until issue `#585`
is merged and the residual source-level gaps found in the post-merge audit are
closed or explicitly reclassified as non-blocking by issue-backed review.
