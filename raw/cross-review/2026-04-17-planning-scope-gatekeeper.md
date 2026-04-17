# Cross-Review — Issue #226 Planning and Scope Gatekeeper

Date: 2026-04-17
Issue: #226
Reviewer: Claude Opus 4.6
Reviewed worktree: `/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-226-scope-gatekeeper-20260417`
Verdict: APPROVED_WITH_CHANGES
Final disposition: Accepted after required changes

## Scope

Read-only alternate-family review of the #226 governance enforcement diff:

- `scripts/overlord/validate_structured_agent_cycle_plan.py`
- `scripts/overlord/test_validate_structured_agent_cycle_plan.py`
- `.github/workflows/governance-check.yml`
- `hooks/code-write-gate.sh`
- #226 plan, PDCAR, and registry documentation

## Findings

### F1 — `.github/scripts/` missing from governance-surface prefixes

Severity: enforcement gap
Status: resolved

Reviewer finding: governance enforcement scripts such as `check_agent_model_pins.py` and `check_codex_model_pins.py` lived under `.github/scripts/`, but the new classifier only covered `.github/workflows/`.

Resolution: added `.github/scripts/` to `GOVERNANCE_SURFACE_PREFIXES`, replaced `lstrip("./")` path normalization with exact leading `./` removal so `.github/...` keeps its leading dot, and added regression tests for `.github/scripts/check_agent_model_pins.py` and `./.github/workflows/governance-check.yml`.

### F2 — `riskfix/` branches produced a misleading issue-branch error

Severity: diagnostic quality
Status: resolved

Reviewer finding: the validator treated `riskfix/` as a branch family requiring plans, but governance-surface enforcement reported only that an issue branch was required when no issue number was present.

Resolution: updated the diagnostic to require a branch name containing `issue-<number>` and added a regression test for `riskfix/scope-gate`.

### F3 — Non-issue branch matching could validate unrelated plans

Severity: diagnostic noise
Status: resolved

Reviewer finding: when no issue number was extracted, the matching helper could inspect unrelated plans and add confusing implementation-readiness failures.

Resolution: changed matching to return no plans when no issue number is available and added a regression test proving unrelated planning-only plans do not add readiness failures on non-issue branches.

### F4 — Hook relpath fail-open behavior needed documentation

Severity: maintainability
Status: resolved

Reviewer finding: `hooks/code-write-gate.sh` intentionally degrades gracefully if the relpath calculation fails, but that behavior was not documented.

Resolution: added a short comment documenting the hook's historical graceful-degradation behavior.

## Accepted Review Notes

The reviewer verified that:

- CI persists the changed-file list before running the enforcement step.
- The enforcement step runs immediately after changed-file categorization.
- The local hook runs the governance-surface gate before existing-file and `.claude/` exemptions.
- Validator error output is JSON-escaped before the hook emits a block response.
- The branch regex extracts `226` from `issue-226-planning-scope-gatekeeper-20260417`.
- Tests cover non-issue branch, non-governance path, missing plan, approved plan pass, wrong execution mode, and unaccepted review.

## Result

All required review changes were applied before closeout validation.
