# Claude Review Packet: Issue #591 Consumer Research Rollout

Date: 2026-04-29
Repo: `hldpro-governance`
Branch: `issue-591-research-rollout`
Issue: `#591`
Mode: `planning_only`

## Review Request

Review this planning-only governance packet for correctness and scope control.
Focus on:

1. whether issue `#591` stays governance-only and planning-only;
2. whether Stampede issue `#208` is a sufficiently narrow first consumer pilot;
3. whether the verifier replay is being used correctly as stale-baseline proof;
4. whether the acceptance criteria and handoff make downstream consumer
   adoption verifier-led and issue-backed rather than ad hoc.

Return:

- verdict: `accepted`, `accepted_with_followup`, or `rejected`
- findings ordered by severity
- required follow-ups, if any

## Canonical Artifacts

- `docs/plans/issue-591-consumer-research-rollout-pdcar.md`
- `docs/plans/issue-591-consumer-research-rollout-structured-agent-cycle-plan.json`
- `raw/execution-scopes/2026-04-29-issue-591-consumer-research-rollout-planning.json`
- `raw/handoffs/2026-04-29-issue-591-consumer-research-rollout.json`
- `docs/PROGRESS.md`
- `OVERLORD_BACKLOG.md`

## Known Context

- Governance-source research-specialist contract merged in issue `#589`.
- Consumer repos do not auto-upgrade from governance merges.
- Live verifier replay against Stampede currently fails on stale package/version
  and missing managed surfaces; this branch records that state as the first
  downstream proof boundary rather than treating it as consumer completion.

## Scope Constraints

- No direct Stampede repo edits are allowed in this branch.
- No central GitHub settings mutation is allowed in this branch.
- This slice should only open the first consumer pilot issue and capture the
  planning proof needed to start repo-native adoption work later.
