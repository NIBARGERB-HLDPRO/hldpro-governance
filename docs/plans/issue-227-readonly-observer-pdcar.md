# Issue #227 — Read-Only Always-On Observer PDCA/R

## Plan

Issue #227 introduces observation before autonomy. The observer should classify and report on governance state without enqueuing work, mutating governed repositories, or relying on LLM-only conclusions.

The implementation path is:

- Use `docs/governed_repos.json` as the repo source of truth.
- Read graphify reports, wiki indexes, compendium, closeouts, backlog, and raw issue metadata.
- Compute source commit SHAs and artifact hashes for auditable input state.
- Write reports only under `projects/<repo_slug>/reports/`.
- Provide a launchd plist template and runbook, but do not install it.

## Do

- Added `scripts/orchestrator/read_only_observer.py`.
- Added `scripts/orchestrator/test_read_only_observer.py`.
- Added `launchd/com.hldpro.governance-observer.plist`.
- Added `docs/runbooks/always-on-governance.md`.
- Added the issue-specific structured plan required by the #226 governance-surface gate.
- Extended the governance-surface classifier to cover `launchd/` and `scripts/orchestrator/` now that this slice introduces those surfaces.

## Check

Planned validation:

- `python3 scripts/orchestrator/test_read_only_observer.py`
- `python3 scripts/orchestrator/read_only_observer.py --check-only`
- `python3 scripts/orchestrator/read_only_observer.py`
- `plutil -lint launchd/com.hldpro.governance-observer.plist`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-227-readonly-observer-20260417 --require-if-issue-branch`
- governance-surface changed-file validation with `--enforce-governance-surface`
- model pin checks
- graphify governance contract check
- org governance compendium freshness check

## Adjust

The observer is intentionally file-system-first. Live GitHub API calls and issue-body reads are out of scope for this slice because raw issue feed policy stores metadata only.

The launchd plist is a template for operator installation. This PR validates syntax and documents bootstrap/bootout behavior, but does not load the agent.

## Review

Alternate-family review is recorded in `raw/cross-review/2026-04-17-readonly-observer.md`.
