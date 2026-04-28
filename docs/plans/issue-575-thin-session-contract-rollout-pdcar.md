# Issue #575 PDCAR: Thin Session-Contract Adapter Rollout

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/575
Branch: `issue-575-thin-session-contract-rollout-20260428`

## Plan

Define the repo-wide rollout plan that propagates the issue-573 governance
session-bootstrap contract into governed consumer repos using thin
`CLAUDE.md` / `CODEX.md` adapter files. The rollout must preserve thick
standards prose in `hldpro-governance` while downstream repos expose only
repo-specific entrypoints, hooks/settings wiring guidance, and pointers back
to the governance SSOT. Before downstream rollout starts, reconcile the
governance repo's own conflicting entrypoints so policy, runbook, and wrapper
paths collapse to one canonical SSOT for review routing, bootstrap, and
thin-consumer ownership.

## Do

Planning-only scope for issue #575:

- audit current governed repo adapter state and classify rollout risk
- sequence rollout waves for thin-adapter adoption
- define acceptance criteria for consumer repos, validation gates, and
  residual follow-up boundaries
- record and resolve governance-source conflicts where multiple docs or
  scripts currently appear to authorize different review or bootstrap paths
- capture alternate-family review before promoting the packet beyond draft
- keep downstream repo edits out of this slice and route execution to child
  issues or follow-up rollout branches

## Check

Before the packet is accepted:

- structured plan validates on the issue branch
- planning execution scope constrains writes to planning/review/validation
  artifacts only
- package handoff validates in a non-implementation lifecycle state
- alternate-family review is captured through the governed Claude path from
  `docs/EXTERNAL_SERVICES_RUNBOOK.md`

After review incorporation and governance-source reconciliation completion:

- the packet records the governance-source SSOT conflicts that must be fixed
  before consumer rollout begins
- the accepted plan defines one canonical alternate-family review path and one
  canonical bootstrap path, with lower-level helpers treated as implementation
  details only
- the packet names issue `#576` as the dedicated governance-source
  reconciliation slice and records that downstream rollout branches stay
  blocked until that slice merges
- once issue `#576` merges, this planning packet remains planning-only and
  becomes the approved rollout map for downstream child execution slices
- PDCAR and structured acceptance criteria reflect the thin-adapter rule
- rollout waves identify the lowest-risk consumer repos first and isolate
  thicker legacy repos into later follow-up slices
- validation and closeout evidence prove that issue #575 remained planning-only

## Adjust

If a candidate repo requires non-trivial normalization of thick local doctrine,
stop and route it to a dedicated child issue instead of widening the first
rollout wave. If a repo is unavailable locally, keep it in the rollout map as
an explicit follow-up rather than guessing at its adapter state. If the
governance repo itself still exposes multiple "correct" review or bootstrap
entrypoints, stop consumer rollout and fix the source contract first; after
that source-contract slice merges, keep issue `#575` planning-only and route
execution into child rollout issues rather than widening this branch.

## Review

Alternate-family review is required before this packet is accepted. The review
must verify that the rollout keeps `hldpro-governance` as the thick source of
truth, keeps consumer `CLAUDE.md` / `CODEX.md` files thin, routes sessions
through the external-services runbook path, eliminates ad hoc alternate
entrypoints from governance SSOT surfaces, and uses issue-backed downstream
slices instead of repo-wide ad hoc edits. Review outcome: `APPROVED_WITH_CHANGES`,
requiring the packet to bind the planning execution scope in the handoff,
clarify that reconciliation executes in dedicated child issue lanes rather than
in the plan artifact itself, and name the dedicated child issue that owns the
source-contract fix (`#576`).
