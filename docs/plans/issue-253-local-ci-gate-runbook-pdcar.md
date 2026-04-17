# Issue #253 — Local CI Gate Runbook Planning PDCA/R

Date: 2026-04-17
Repo: hldpro-governance
Issue: [#253](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/253)
Scope: Planning-only org-level toolkit implementation plan

## Plan

Record the supplied Local CI Gate runbook and reviewer-response memo as governance planning artifacts, then update the plan so `hldpro-governance` is the source-of-truth repo for reusable org-level local CI gate tooling that other repos can pull and deploy.

This slice is intentionally limited to the planning surface:

- `docs/plans/HLD_Pro_Local_CI_Gate_Runbook.md`
- `docs/plans/Local_CI_Gate_Runbook_Reviewer_Response_Memo.md`
- `docs/plans/issue-253-local-ci-gate-runbook-pdcar.md`
- `docs/plans/issue-253-structured-agent-cycle-plan.json`
- `raw/cross-review/2026-04-17-issue-253-local-ci-gate-toolkit-plan.md`
- `raw/execution-scopes/2026-04-17-issue-253-local-ci-gate-toolkit-planning.json`
- `raw/execution-scopes/2026-04-17-issue-253-local-ci-gate-toolkit-implementation.json`
- `OVERLORD_BACKLOG.md`

The governing GitHub issue is the system of record for this planning intake and implementation planning. Implementation files remain out of scope for this PR; the next slice should build the governance-owned toolkit and deployer, then roll out thin consumer shims through separate issue-backed adoption slices.

## Do

Add the two supplied files from `/Users/bennibarger/Downloads/files.zip` under `docs/plans/`, then revise the runbook where needed to make the implementation plan coherent for `hldpro-governance` as the reusable toolkit source.

Create this PDCA/R companion so the planning artifact has an issue-backed governance trail and captures the discussion outcome:

- The reviewer-response memo is approved for planning use.
- The runbook is updated to target `hldpro-governance` as the org-level toolkit source, not a one-off consumer repo.
- The runbook records the service-runbook SSOT precedent and graphify hook helper precedent for cross-repo deployment.
- Known pre-implementation corrections are applied in the plan text rather than left ambiguous.
- Alternate-model review returned `APPROVED_WITH_CHANGES` with no blocking findings; the required follow-ups were applied in the runbook as governance-profile implementation micro-slices and an explicit deployer safety contract.

Add an `OVERLORD_BACKLOG.md` Planned row that references issue #253, satisfying the repo rule that Planned governance work is GitHub-issue-backed.

## Check

Acceptance checks for this slice:

- [x] Issue #253 exists before the backlog row is added.
- [x] The supplied runbook exists at `docs/plans/HLD_Pro_Local_CI_Gate_Runbook.md`.
- [x] The supplied reviewer-response memo exists at `docs/plans/Local_CI_Gate_Runbook_Reviewer_Response_Memo.md`.
- [x] This PDCA/R exists at `docs/plans/issue-253-local-ci-gate-runbook-pdcar.md`.
- [x] The canonical structured plan exists at `docs/plans/issue-253-structured-agent-cycle-plan.json`.
- [x] `OVERLORD_BACKLOG.md` Planned references issue #253.
- [x] No implementation files are changed.
- [x] The runbook defines `hldpro-governance` as the org-level toolkit source and defers consumer rollout to follow-up issue-backed slices.
- [x] Subagent planning review findings are incorporated into the runbook and structured plan.
- [x] Alternate-model review is recorded under `raw/cross-review/`.
- [x] The planning-only execution scope is recorded under `raw/execution-scopes/`.
- [x] The follow-up implementation execution scope is recorded under `raw/execution-scopes/` before implementation files are changed.

Recommended validation commands:

```bash
git status --short
python3 scripts/overlord/check_overlord_backlog_github_alignment.py
```

Validation results:

- PASS: `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- PASS: `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name docs/issue-253-local-ci-gate-runbook-20260417 --changed-files-file /tmp/issue-253-changed-files.txt --enforce-governance-surface`
- PASS: `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .`
- PASS: planner-boundary changed files classify as planning-only (`docs/plans/**` and `OVERLORD_BACKLOG.md`)
- PASS: reviewer memo remains imported from `/Users/bennibarger/Downloads/files.zip`; the runbook is intentionally revised in this PR to align issue #253 with the org-level toolkit scope.
- PASS: `git diff --check`
- PASS: changed paths are limited to `docs/plans/`, `raw/cross-review/`, `raw/execution-scopes/`, and `OVERLORD_BACKLOG.md`

## Adjust

The implementation plan now resolves the previously identified runbook corrections:

1. Replace the package-script pipe through `xargs` with a wrapper that handles empty output, `FULL_SUITE`, and spec lists correctly.
2. Describe `test:e2e:full` as the full-suite script override instead of implying a separate `--full` mode exists.
3. Define `scripts/select-playwright-specs.sh [--explain-trigger] [diff-base]` argument semantics explicitly.
4. Specify exact resolver behavior for `@covers *`.
5. Clarify that `hldpro-governance` owns issue #253 and the governance backlog row.
6. Reframe implementation as a reusable org-level toolkit with thin consumer shims, using `docs/EXTERNAL_SERVICES_RUNBOOK.md` and `scripts/knowledge_base/graphify_hook_helper.py` as precedents.

Remaining execution gates before implementation:

- Merge this planning PR so the implementation execution scope is trusted from `main`.
- Carry forward the alternate-model review follow-ups into the future implementation PR: start from the G1-G5 micro-slices and enforce the deployer contract before any consumer rollout.
- Keep consumer-repo rollout as separate issue-backed adoption work after the toolkit is dogfooded in governance.

Subagent review results:

- Fermat recommended the source-of-truth toolkit model: governance-owned runner, repo-family profiles, deployer, thin consumer shims, and reuse of existing `.governance`/reusable-workflow patterns.
- Popper found the prior package split-brained between planning intake and implementation planning; this update makes planning-only org-level toolkit scope the primary story across the runbook, PDCA/R, structured plan, and backlog row.

Service-runbook precedent:

- `docs/EXTERNAL_SERVICES_RUNBOOK.md` is the SSOT for all HLDPRO external services and supersedes independently maintained downstream service runbooks. Local CI Gate should use the same governance-owned SSOT pattern.
- `scripts/knowledge_base/graphify_hook_helper.py` provides the managed-deployer precedent: manifest/profile resolution from governance, safety checks before writing, managed markers, and refusal to overwrite unmanaged artifacts by default.

Alternate-model review result:

- Claude Opus 4.6 reviewed the planning package and returned `APPROVED_WITH_CHANGES` with no blocking findings.
- Required change 1 was resolved by adding governance-profile implementation micro-slices G1-G5 to §1.1 of the runbook.
- Required change 2 was resolved by adding the Local CI Gate deployer contract to §1.1 of the runbook.
- Non-blocking recommendations remain future cleanup candidates: consider separating downstream product-repo profile detail into its own document, refine future sprint names, align backlog wording with v1.4 framing, and test `@covers *` carefully when the downstream Playwright profile is implemented.

## Review

No code or CI behavior changes are included in this slice. The artifacts are planning evidence only.

The Stage 6 closeout for this planning intake should verify the files exist in git, confirm the backlog row remains issue-backed, and state that implementation remains deferred until a pinned execution-scope handoff exists.
