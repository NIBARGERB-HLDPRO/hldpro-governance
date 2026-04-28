# PDCAR: Issue #579 Downstream Thin Session-Contract Adapter Rollout

Date: 2026-04-28
Repo: `hldpro-governance`
Branch: `issue-579-thin-session-adapter-rollout-epic-20260428`
Epic: [#579](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/579)
Prerequisites: [#575](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/575), [#576](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/576)
Status: PLANNING_PACKAGE
Canonical plan: `docs/plans/issue-579-thin-session-adapter-rollout-epic-structured-agent-cycle-plan.json`

## Problem

Governance now has an approved thin-adapter rollout plan (`#575`) and the
governance-source SSOT reconciliation landed on `main` (`#576`), but there is
not yet an issue-backed execution epic and downstream child issue map that
turns that plan into concrete repo rollout lanes.

Without that execution map, downstream repos will continue to drift, and
operators will still have to restate the same session-contract instructions
repo by repo instead of routing implementation through one governed rollout
sequence.

## Plan

Open the governance execution epic and the downstream child issues in the
approved wave order, then mirror that issue map in repo artifacts so the
execution tracker, backlog mirror, review evidence, and validation trail stay
in sync.

This planning slice remains governance-only and planning-only. It does not
modify downstream repos. It establishes the execution contract for the next
repo-specific lanes.

## Scope

In scope:

- Create governance epic `#579`.
- Create downstream child issues in the approved rollout order:
  - local-ai-machine `#515`
  - ai-integration-services `#1405`
  - seek-and-ponder `#190`
  - knocktracker `#187`
  - Stampede `#195`
  - HealthcarePlatform `#1513`
  - ASC-Evaluator `#15`
- Record repo-specific acceptance criteria for each child issue.
- Update `OVERLORD_BACKLOG.md` and `docs/PROGRESS.md` to reflect the open epic.
- Record planning, handoff, review, validation, and closeout artifacts for the
  epic-opening slice itself.

Out of scope:

- Editing any downstream repo in this branch.
- Reopening governance-source SSOT questions settled by `#576`.
- Expanding consumer repos into thick local governance manuals.
- Adding EmailAssistant to the rollout before it is locally available and
  bootstrap-ready.

## Do

1. Create governance epic `#579` with explicit child-story placeholders and
   epic-level acceptance criteria.
2. Create one downstream child issue per repo in the approved wave order with
   repo-specific acceptance criteria.
3. Update the epic body to include the concrete downstream issue links.
4. Mirror the execution epic in `OVERLORD_BACKLOG.md` and `docs/PROGRESS.md`.
5. Create the structured planning packet for this epic-opening slice.
6. Route the packet through alternate-family review using the governed Claude
   wrapper path.
7. Validate the packet, rerun the Stage 6 closeout hook in `planning_only`
   mode, and publish the planning PR while keeping epic `#579` open.

## Check

Planning checks:

- Governance epic `#579` exists and links all seven downstream child issues.
- Every downstream child issue exists in the correct repo and contains
  repo-specific acceptance criteria, not a generic placeholder body.
- The structured plan, handoff package, and planning execution scope validate.
- Alternate-family review is captured through the governed Claude wrapper path.
- `OVERLORD_BACKLOG.md` and `docs/PROGRESS.md` reflect the open rollout epic.
- Local CI Gate passes on the planning-only branch diff.

Execution checks for later child slices:

- Each downstream repo uses a clean issue branch or worktree.
- Each downstream PR links epic `#579` and its repo-native child issue.
- Repo-local validation and GitHub checks pass.
- Closeout evidence proves thin-adapter compliance without thick local doctrine
  regression.

## Adjust

Stop and revise the rollout map if:

- a child repo needs additional prerequisite discovery before a safe execution
  issue can be opened;
- a repo requires a documented thick-doctrine exception instead of thin-adapter
  normalization;
- the repo-specific acceptance criteria prove insufficiently precise for
  validation or closeout; or
- downstream execution begins without repo-native issue lanes and proof
  expectations.

## Review

Required review posture:

- Alternate-family review is required because this slice sets the execution map
  for an org-wide governance rollout.
- The review must confirm that the new epic and child issues faithfully mirror
  the accepted `#575` plan and the merged `#576` SSOT contract.
- The review must verify that downstream execution remains issue-backed and
  that this branch stays planning-only.

## Acceptance Criteria

- Epic `#579` exists with epic-level acceptance criteria and concrete child
  links.
- Downstream child issues exist for local-ai-machine, ai-integration-services,
  seek-and-ponder, knocktracker, Stampede, HealthcarePlatform, and
  ASC-Evaluator.
- Each downstream child issue contains repo-specific acceptance criteria that
  enforce thin adapters, governance SSOT pointers, tracked-versus-local wiring
  separation, and proof expectations.
- `OVERLORD_BACKLOG.md` and `docs/PROGRESS.md` reflect the open rollout epic.
- The planning packet validates and records review, validation, and closeout
  evidence without mutating downstream repos.
