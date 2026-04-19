# Issue #312 - EmailAssistant Discovery And Classification PDCA/R

Branch: `issue-312-emailassistant-discovery-20260419`
Issue: [#312](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/312)
Parent epic: [#298](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/298)
Downstream blocker: [EmailAssistant#1](https://github.com/NIBARGERB-HLDPRO/EmailAssistant/issues/1)

## Plan

#298 requires every active org repository to be intentionally represented in governance. `EmailAssistant` is active, private, and missing from the governed repo registry. #312 discovers and classifies it without editing the downstream repository.

## Do

- Inspect `EmailAssistant` with GitHub CLI/API and a temporary read-only checkout.
- Document stack, default branch, workflow/CI state, branch/ruleset state, front-door governance docs, and data sensitivity.
- Open `EmailAssistant#1` for repo-local governance bootstrap before future downstream writes.
- Add `EmailAssistant` to `docs/governed_repos.json` with `governance_status: adoption_blocked`.
- Keep downstream subsystems disabled until repo-local governance, CI, and sensitive-email controls are bootstrapped.

## Check

Final acceptance requires:

- `python3 scripts/overlord/validate_governed_repos.py`
- `python3 scripts/overlord/check_org_repo_inventory.py --live --format text`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py`
- `python3 scripts/overlord/assert_execution_scope.py`
- `python3 scripts/overlord/validate_backlog_gh_sync.py`
- `python3 -m py_compile` for touched Python validators/helpers
- `git diff --check`
- Local CI Gate against the changed-file list
- specialist/subagent review evidence

## Act

If validation passes, publish #312 as a focused PR and keep #298 open. If live org inventory still reports `EmailAssistant` as missing after registry coverage, do not publish. If downstream implementation is needed, route it to `EmailAssistant#1`.

## Retrospective

Expected residual work is #313 registry-driven surface reconciliation, #314 final org e2e closeout, and downstream `EmailAssistant#1`.
