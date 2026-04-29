# PDCAR: Issue #591 Governed Research Specialist Consumer Rollout

Date: 2026-04-29
Repo: `hldpro-governance`
Branch: `issue-591-research-rollout`
Issue: [#591](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/591)
Prerequisite: [#589](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/589)
Status: PLANNING_PACKAGE
Canonical plan: `docs/plans/issue-591-consumer-research-rollout-structured-agent-cycle-plan.json`

## Problem

Governance source now defines governed `local-repo researcher` and
`web/external researcher` specialist lanes, but consumer repos do not adopt
those new managed surfaces automatically when governance merges. The live
consumer verifier replay against Stampede still fails on stale package/version
and missing managed surfaces.

Without an issue-backed downstream rollout lane, the new research-specialist
contract remains source-only and operators will keep inferring consumer state
instead of proving it with the governed verifier.

## Plan

Open the governance rollout tracker for consumer adoption and bind the first
pilot lane to Stampede issue `#208`. Keep this governance branch planning-only:
record the rollout contract, open the first child issue, update governance
mirrors, and capture proof that Stampede is still stale until the repo-native
adoption lane lands.

## Scope

In scope:

- Create the governance planning packet for issue `#591`.
- Open the first consumer-pilot issue in Stampede: `#208`.
- Update `OVERLORD_BACKLOG.md` and `docs/PROGRESS.md` to reflect the new open
  rollout epic.
- Record a bounded verifier replay against Stampede as the first stale-state
  proof artifact.
- Route the planning packet through alternate-family review using the governed
  Claude wrapper path.

Out of scope:

- Direct edits to Stampede or any other consumer repo in this branch.
- Central GitHub settings mutation in consumer repos.
- Multi-repo consumer adoption in this first packet.
- Reopening the governance-source design work settled by issue `#589`.

## Do

1. Create the `#591` planning packet with a narrow first-consumer pilot scope.
2. Open Stampede issue `#208` with repo-specific acceptance criteria for the
   research-specialist consumer adoption lane.
3. Update governance mirrors to show `#591` as the active consumer rollout
   epic and to link Stampede `#208` as the first pilot.
4. Replay `verify_governance_consumer.py` against Stampede and record the
   expected fail-closed baseline proof.
5. Route the packet through governed alternate-family review.
6. Validate the packet locally, run Stage 6 closeout in `planning_only` mode,
   and publish the planning PR while keeping `#591` open.

## Check

Planning checks:

- Governance issue `#591` stays planning-only and names Stampede `#208` as the
  first consumer adoption lane.
- Stampede `#208` exists and includes repo-specific acceptance criteria for
  adopting the new managed research-specialist surfaces.
- The structured plan, planning execution scope, and handoff validate.
- The verifier replay against Stampede is recorded and proves the current stale
  baseline without mutating Stampede.
- Alternate-family review is captured through the governed Claude wrapper path.
- `OVERLORD_BACKLOG.md` and `docs/PROGRESS.md` reflect the open rollout epic.
- Local CI Gate passes on the planning-only diff.

Execution checks for the later Stampede child lane:

- Stampede adopts the updated governance package/version and managed surfaces.
- Stampede passes `verify_governance_consumer.py` at an exact pinned governance
  SHA.
- Stampede proof records which surfaces were package-managed versus
  repo-specific.

## Adjust

Stop and revise the rollout plan if:

- the first consumer pilot requires direct governance-source contract changes
  rather than consumer adoption work;
- the Stampede issue proves too broad to keep verifier evidence and managed
  surface adoption in one bounded lane; or
- alternate-family review finds that the rollout packet is trying to mutate
  consumer repos from the governance branch.

## Review

Required review posture:

- Alternate-family review is required because this slice sets the first
  downstream consumer adoption proof boundary for the new research-specialist
  contract.
- The review must confirm that this governance branch remains planning-only and
  that the first consumer pilot stays issue-backed and verifier-led.

## Acceptance Criteria

- Governance issue `#591` has a validated planning packet for consumer rollout.
- Stampede issue `#208` exists with repo-specific consumer adoption acceptance
  criteria.
- The governance mirrors reflect `#591` as the active rollout epic and name the
  Stampede pilot lane.
- A live verifier replay against Stampede is recorded as stale-baseline proof.
- The planning packet validates, records alternate-family review, and closes
  out in `planning_only` mode without mutating consumer repos.
