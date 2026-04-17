# Issue #253 — Local CI Gate Runbook Planning PDCA/R

Date: 2026-04-17
Repo: hldpro-governance
Issue: [#253](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/253)
Scope: Planning-only artifact intake

## Plan

Record the supplied Local CI Gate runbook and reviewer-response memo as governance planning artifacts before any implementation work begins.

This slice is intentionally limited to the planning surface:

- `docs/plans/HLD_Pro_Local_CI_Gate_Runbook.md`
- `docs/plans/Local_CI_Gate_Runbook_Reviewer_Response_Memo.md`
- `docs/plans/issue-253-local-ci-gate-runbook-pdcar.md`
- `OVERLORD_BACKLOG.md`

The governing GitHub issue is the system of record for this planning intake. Implementation of the local CI gate, lefthook wiring, selective Playwright resolver, package scripts, hooks, workflows, and target-product repo changes is out of scope for this slice.

## Do

Add the two supplied files from `/Users/bennibarger/Downloads/files.zip` under `docs/plans/` without changing their content.

Create this PDCA/R companion so the planning artifact has an issue-backed governance trail and captures the discussion outcome:

- The reviewer-response memo is approved for planning use.
- The runbook is suitable for planning discussion after a small technical correction pass before implementation.
- Known pre-implementation corrections are tracked below rather than applied in this planning-only slice.

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
- PASS: imported runbook and reviewer memo SHA-256 hashes match `/Users/bennibarger/Downloads/files.zip`
- PASS: `git diff --check`
- PASS: changed paths are limited to `docs/plans/` planning artifacts and `OVERLORD_BACKLOG.md`

## Adjust

Before any implementation handoff, resolve these runbook corrections in an issue-backed planning or implementation slice:

1. Replace the package-script pipe through `xargs` with a wrapper that handles empty output, `FULL_SUITE`, and spec lists correctly.
2. Make the full-suite override language consistent: either implement a real `--full` flag or describe `test:e2e:full` as a script override.
3. Define `scripts/select-playwright-specs.sh [--explain-trigger] [diff-base]` argument semantics explicitly.
4. Specify exact resolver behavior for `@covers *`.
5. Clarify which target product repo owns the Local CI Gate issue and `BACKLOG.md` row.

These are planning refinements, not blockers to storing the artifacts in governance.

## Review

No code or CI behavior changes are included in this slice. The artifacts are planning evidence only.

The Stage 6 closeout for this planning intake should verify the files exist in git, confirm the backlog row remains issue-backed, and state that implementation remains deferred until a target-repo issue and execution handoff exist.
