# PDCAR: Issue #609 Consumer Rollout Ref and Gate Repair

Date: 2026-04-29
Repo: `hldpro-governance`
Branch: `issue-609-consumer-rollout-ref-and-gates`
Issue: [#609](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/609)
Parent tracker: [#591](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/591)
Status: IMPLEMENTATION_READY
Canonical plan: `docs/plans/issue-609-consumer-rollout-ref-and-gates-structured-agent-cycle-plan.json`

## Problem

Consumer rollout lanes under governance issue `#591` used governance ref
`da888a5bd09a40105d550658b58489cd96d3ff5e`, which is present in a local
governance branch but not reachable from the remote governance repo. That made
the merged knocktracker lane fail `verify-consumer-governance` in GitHub.

The same merged lane also missed repo-local publish gates that should have been
caught before PR publication: file-index refresh, sprint runner-status update
for workflow changes, and full PR-body contract sections.

Without a governance-source repair, downstream rollout can keep producing
merged-but-incomplete consumer lanes and false confidence about adoption state.

## Plan

Pause additional consumer rollout and repair the rollout procedure at the
governance layer. The governance fix must force remote-reachable governance ref
selection, require repo-local publish gate checks in consumer packets, and
replay already-merged AIS and knocktracker lanes to determine whether they need
corrective follow-up PRs.

The concrete remote-reachability mechanism is:

- `git fetch --quiet --depth=1 origin <governance_sha>`

If that fetch fails, the SHA is not valid rollout proof and consumer deployment
or local verification must fail closed.

## Scope

In scope:

- Create the issue `#609` packet in `hldpro-governance`.
- Audit the already-merged AIS and knocktracker consumer lanes against remote
  governance state.
- Define hard-gated acceptance criteria for remote ref selection and repo-local
  publish gates in future consumer rollout lanes.
- Update governance tracker `#591` with corrected status and follow-up links.

Out of scope:

- Starting a new consumer adoption lane before `#609` is resolved.
- Reopening the governance-source research specialist design work from `#589`.
- Ad hoc product-repo fixes without issue-backed follow-up.

## Do

1. Write the issue `#609` planning packet and record the discovered failures.
2. Replay the merged AIS and knocktracker lanes against remote governance state
   and classify whether they require corrective consumer PRs.
3. Define the rollout hard gates:
   - governance refs must be reachable from the remote source of truth;
   - consumer packets must include repo-local publish gates before PR creation;
   - tracker issue `#591` must reflect blocked rollout when merged lanes are
     incomplete.
   - remote reachability is proved with `git fetch --quiet --depth=1 origin <sha>`
     from the governance checkout.
4. Route the packet through alternate-family review using the governed Claude
   wrapper path.
5. Promote to implementation only after the replay evidence and review agree on
   the repair scope.
6. Implement the hard gates in governance-owned deployer, verifier, and
   rollout runbook/checklist surfaces only.

Replay checklist:

1. Use merged-state evidence from GitHub PR/check logs as the authoritative
   source for already-merged consumer lanes.
2. Replay `verify_governance_consumer.py` only against a consumer checkout that
   is confirmed current with merged remote state; stale local roots are not
   authoritative replay evidence.
3. Include workflow-ref scope in each replay.
4. For repos with repo-local publish gates, run the governance-owned publish
   gate checker with the exact PR title/body inputs to prove whether those
   gates would have failed before PR creation.

## Check

Planning checks:

- Issue `#609` has a validated planning packet with hard ACs for the rollout
  repair.
- Governance tracker `#591` is updated with the actual blocked status and
  links to the repair lane.
- Replay evidence exists for at least AIS and knocktracker merged lanes.
- Alternate-family review is captured through the governed Claude wrapper path.
- Claude follow-up is incorporated before implementation:
  - explicit remote-reachability mechanism
  - concrete replay checklist
  - workflow-ref scope in merged-lane replay

Execution checks for the later implementation lane:

- Governance tooling prevents consumer lanes from pinning refs not reachable
  from the remote governance repo.
- Governance tooling defines the concrete remote-reachability check instead of
  relying on local `HEAD`.
- Consumer rollout packet/checklist enforces repo-local publish gates before PR
  publication.
- Replay commands explicitly include workflow-ref verification for merged lanes.
- AIS and knocktracker have an explicit disposition: verified complete or
  follow-up PR required.

## Adjust

Stop and revise if:

- replay evidence shows the bad governance ref is not systemic beyond one lane;
- the correct fix belongs in a consumer repo only rather than governance
  tooling/checklist logic; or
- alternate-family review finds the packet too broad and requires a smaller
  repair slice.

Current replay disposition:

- `ai-integration-services`: corrective follow-up PR needed to repin managed
  governance surfaces from the unreachable SHA to a remote-published governance
  SHA. No repo-local publish-gate miss was proven on PR `#1411`.
- `knocktracker`: corrective follow-up PR needed for the unreachable governance
  SHA plus repo-local publish-gate misses on PR `#190`:
  - file-index refresh
  - runner-status doc update for workflow changes
  - required PR-body sections

## Review

Required review posture:

- Alternate-family review is required because this slice changes the procedure
  for downstream consumer rollout and determines whether already-merged lanes
  remain acceptable.
- Specialist research/QA must confirm the root cause before the repair is
  treated as complete.

## Acceptance Criteria

- Governance issue `#609` has a validated planning packet for the rollout
  repair.
- The packet hard-requires remote-reachable governance refs for consumer lanes.
- The packet hard-requires repo-local publish gates in consumer rollout proof.
- AIS and knocktracker are replayed against remote governance state with a
  documented disposition.
- Governance tracker `#591` reflects the blocked rollout state until `#609`
  lands.
- Alternate-family review is accepted with follow-up, and that follow-up is
  incorporated before implementation starts.
