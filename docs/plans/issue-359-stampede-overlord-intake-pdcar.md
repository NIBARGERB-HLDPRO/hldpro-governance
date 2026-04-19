# Issue #359 - Stampede Overlord Governance Intake PDCA/R

Branch: `codex/issue-359-stampede-overlord-intake-runbook`
Issue: [#359](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/359)
Parent epic: [#298](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/298)
Target repo: [NIBARGERB-HLDPRO/Stampede](https://github.com/NIBARGERB-HLDPRO/Stampede)

## Plan

`Stampede` was created as a private org repository for the PHASE0 development cycle. Repo-local HLDPRO product governance is already installed and live GitHub controls are active, but the governance repo does not yet include `Stampede` in Overlord registry sources. That means sweep, metrics, compendium, raw feed sync, memory integrity, Codex ingestion, code governance, and graph/wiki generation cannot select the repo through `docs/governed_repos.json`.

The immediate #359 slice is planning and repeatability: preserve the Stampede audit handoff and create a reusable runbook for creating or adding org-level repos without confusing three separate layers:

- GitHub org/repo controls
- repo-local product governance files
- Overlord governance registry enrollment

## Do

- Use the read-only Stampede audit handoff as the evidence baseline for #359.
- Create a structured issue #359 plan that names scope, exclusions, risks, and validation.
- Create a runbook for creating a new org repo or onboarding an existing repo into HLDPRO governance.
- Explicitly record that `Stampede` Overlord enrollment is not complete until registry and graph target changes land in a follow-up implementation slice.
- Leave unrelated generated `graphify-out/*` changes untouched unless a later validator requires regenerated artifacts.

## Check

Planning/runbook acceptance requires:

- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-359-stampede-overlord-intake-planning.json --changed-files-file <issue-359-changed-files>`
- `python3 -m json.tool docs/plans/issue-359-structured-agent-cycle-plan.json`
- `git diff --check`
- Confirm `docs/governed_repos.json` and `docs/graphify_targets.json` remain unchanged in this planning slice.

Follow-up implementation acceptance for actual Stampede enrollment must include:

- Add `Stampede` to `docs/governed_repos.json` with explicit tier and subsystem flags.
- Add `Stampede` to `docs/graphify_targets.json` if graph/wiki generation is selected.
- Run `python3 scripts/overlord/validate_governed_repos.py`.
- Run `python3 scripts/overlord/check_org_repo_inventory.py --live --format text`.
- Verify `python3 scripts/overlord/validate_governed_repos.py --print-subsystem sweep` includes `Stampede` when sweep is enabled.
- Regenerate compendium/graph artifacts only when the implementation slice scope includes them.

## Act

If this planning slice validates, publish it as a focused PR under #359. Do not claim `Stampede` is Overlord-enrolled from this PR alone. The next implementation PR must decide the intended governance tier, security tier, graphify participation, and subsystem flags before touching registry sources.

If another org repo is created during this work, apply the new runbook and create a separate issue-backed intake unless it is part of the same #298 coverage gap.

## Retrospective

Expected residual work after this planning slice:

- `Stampede` registry enrollment in `docs/governed_repos.json`.
- Optional `Stampede` graph/wiki target setup.
- Solo-owner review policy decision for repos where GitHub blocks self-approval.
- `Stampede` PR #3 evidence refresh merge or closure.
- `Stampede` Dependabot PR #1 review and merge or explicit deferral.
- Code security / CodeQL decision for the `Stampede` tier.
