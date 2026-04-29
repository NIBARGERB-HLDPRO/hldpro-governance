# Claude Review Packet: Issue #609 Consumer Rollout Ref and Gate Repair

Date: 2026-04-29
Repo: `hldpro-governance`
Branch: `issue-609-consumer-rollout-ref-and-gates`
Issue: `#609`
Mode: `implementation_ready`

## Review Request

Review this governance repair packet for correctness and boundedness.
Focus on:

1. whether the root cause is correctly identified as a governance rollout
   procedure defect rather than a repo-local consumer defect;
2. whether the proposed hard gates are the right minimum set:
   - governance refs used for consumer rollout must be reachable from the
     remote governance source of truth;
   - local replay must fail before PR publication when a local-only governance
     SHA is used;
   - consumer rollout procedure must include machine-checked repo-local publish
     gates before PR publication;
3. whether already-merged AIS and knocktracker lanes should be treated as
   follow-up candidates rather than silently complete;
4. whether this issue remains governance-only and does not widen into ad hoc
   consumer repo mutation before the repair is implemented.

Return:

- verdict: `accepted`, `accepted_with_followup`, or `rejected`
- findings ordered by severity
- required follow-ups, if any

## Canonical Artifacts

- `docs/plans/issue-609-consumer-rollout-ref-and-gates-pdcar.md`
- `docs/plans/issue-609-consumer-rollout-ref-and-gates-structured-agent-cycle-plan.json`
- `raw/handoffs/2026-04-29-issue-609-consumer-rollout-ref-and-gates.json`
- `docs/runbooks/org-governance-tooling-distribution.md`
- `docs/runbooks/local-ci-gate-toolkit.md`
- `scripts/overlord/deploy_governance_tooling.py`
- `scripts/overlord/verify_governance_consumer.py`

## Known Context

- Governance tracker `#591` is now paused and records the blocked rollout
  state:
  `https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/591#issuecomment-4347870019`
- Knocktracker consumer lane `#189` / PR `#190` merged, but GitHub reported:
  - `verify-consumer-governance` failure because GitHub could not fetch
    governance ref `da888a5bd09a40105d550658b58489cd96d3ff5e` from the remote
    governance repo
  - `validate` failure from missing file-index refresh
  - `validate-pr` failure from missing required PR-body sections
  - `require-sprint-status-update` failure from workflow changes without
    `docs/sprint/runner-status.md` update
- Local governance checkout that produced those consumer refs was on a local
  branch while remote `origin/main` was different.

## Scope Constraints

- No new consumer adoption lane is allowed before issue `#609` resolves.
- This branch must stay governance-only until the repair is defined and
  validated.
- No ad hoc consumer repo edits are allowed in this branch.
